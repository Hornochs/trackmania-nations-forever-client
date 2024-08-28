import xmlrpc.client as xmlrpclib
import asyncio

# GbxRemote Protocol specification: https://wiki.trackmania.io/en/dedicated-server/XML-RPC/gbxremote-protocol

class GbxRemoteFault(xmlrpclib.Fault):
  def __init__(self, fault, handler):
    super().__init__(fault.faultCode, fault.faultString)
    self.handler = handler


class GbxRemoteClient:
  def __init__(self, host: str, port: int = 5000) -> None:
    self.host = host
    self.port = port

  async def connect(self) -> None:
    self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    data = await self.reader.read(4)
    headerLength = int.from_bytes(data, byteorder='little')
    
    data = await self.reader.read(headerLength)
    header = data.decode()

    if header != "GBXRemote 2":
      raise Exception('No "GBXRemote 2" header found! Server may not be a GBXRemote server!')
    
    self.handler = None
    self.waiting_messages: map[int, asyncio.Future] = {}
    self.receive_loop = asyncio.create_task(self._start_receive_loop())
  
  async def close(self) -> None:
    self.receive_loop.cancel()
    self.writer.close()
    await self.writer.wait_closed()

  async def __aenter__(self):
    await self.connect()

    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.close()

  async def _start_receive_loop(self) -> None:
    while True:
      try:
        handler, data = await self._receive()
      except GbxRemoteFault as fault:
        handler = fault.handler
        data = fault

      try:
        future = self.waiting_messages.pop(handler)

        if isinstance(data, GbxRemoteFault):
          future.set_exception(data)
        else:
          future.set_result(data)
      except KeyError:
        raise Exception(f'Unexpected handler: {handler}!')
  
  async def _receive(self, expected_handler: int = None) -> tuple[int, tuple]:
    header = await self.reader.read(8)
    size = int.from_bytes(header[:4], byteorder='little')
    handler = int.from_bytes(header[4:], byteorder='little')

    if expected_handler is not None and  handler != expected_handler:
      raise Exception(f'Handler mismatch! Expected {expected_handler}, got {handler}! Concurrency problem?')

    data = await self.reader.read(size)
    try:
      data = xmlrpclib.loads(data.decode())
      data = data[0][0]
    except xmlrpclib.Fault as e:
      raise GbxRemoteFault(e, handler)

    return handler, data
  
  async def execute(self, method: str, *args) -> tuple:
    if self.handler is None:
      self.handler = 0x80000000
    else:
      self.handler += 1
    current_handler = self.handler
    
    handler_bytes = self.handler.to_bytes(4, byteorder='little')
    data = xmlrpclib.dumps(args, method).encode()
    packet_len = len(data)

    packet = bytes()
    packet += packet_len.to_bytes(4, byteorder='little')
    packet += handler_bytes
    packet += data

    self.writer.write(packet)
    await self.writer.drain()

    response_future = asyncio.Future()
    self.waiting_messages[current_handler] = response_future
    response_data = await response_future

    return response_data

  async def authenticate(self, username: str, password: str) -> bool:
    response = await self.execute('Authenticate', username, password)

    if not response:
      raise Exception('Authentication failed!')

