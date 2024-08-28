from typing import Callable
import xmlrpc.client as xmlrpclib
import asyncio

# GbxRemote Protocol specification: https://wiki.trackmania.io/en/dedicated-server/XML-RPC/gbxremote-protocol

class GbxRemoteFault(xmlrpclib.Fault):
  def __init__(self, fault, handler):
    super().__init__(fault.faultCode, fault.faultString)
    self.handler = handler


class GbxRemotePacket:
  def __init__(self, handler: int, data: tuple):
    self.handler = handler
    self.data = data

  def __str__(self):
    return f'Handler: {self.handler}, Data: {self.data}'


class GbxRemoteCallbackPacket(GbxRemotePacket):
  def __init__(self, handler: int, data: tuple, callback: str):
    super().__init__(handler, data)
    self.callback = callback
  
  def __str__(self):
    return f'Handler: {self.handler}, Callback: {self.callback}, Data: {self.data}'


class GbxRemoteClient:
  INITIAL_HANDLER = 0x80000000
  MAXIMUM_HANDLER = 0xFFFFFFFF
  
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
    
    self.handler = self.MAXIMUM_HANDLER
    self.waiting_messages: map[int, asyncio.Future] = {}
    self.callback_handlers: map[int, Callable[[str, tuple], None]] = []
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
        packet = await self._receive()
        handler = packet.handler
        data = packet.data
      except GbxRemoteFault as fault:
        handler = fault.handler
        data = fault
      
      if isinstance(packet, GbxRemoteCallbackPacket):
        # received a callback
        # print(f"Received callback: {handler}, {data}")
        self._handle_callback(packet.callback, data)
      else:
        try:
          future = self.waiting_messages.pop(handler)

          if isinstance(data, GbxRemoteFault):
            future.set_exception(data)
          else:
            future.set_result(data)
        except KeyError:
          print(f"Unexpected message received: {handler}!")
          raise Exception(f'Unexpected handler: {handler}!')
  
  async def _receive(self, expected_handler: int = None) -> GbxRemotePacket:
    header = await self.reader.read(8)
    size = int.from_bytes(header[:4], byteorder='little')
    handler = int.from_bytes(header[4:], byteorder='little')

    if expected_handler is not None and  handler != expected_handler:
      raise Exception(f'Handler mismatch! Expected {expected_handler}, got {handler}! Concurrency problem?')

    data = await self.reader.read(size)
    try:
      data = xmlrpclib.loads(data.decode())
    except xmlrpclib.Fault as e:
      raise GbxRemoteFault(e, handler)

    if len(data) >= 2 and data[1] is not None:
      return GbxRemoteCallbackPacket(handler, data[0][0], data[1])
    else:
      return GbxRemotePacket(handler, data[0][0])
  
  async def execute(self, method: str, *args) -> tuple:
    if self.handler == self.MAXIMUM_HANDLER:
      self.handler = self.INITIAL_HANDLER      
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
  
  def _handle_callback(self, callback: str, data: tuple) -> None:
    for callback_handler in self.callback_handlers:
      callback_handler(callback, data)
  
  def register_callback_handler(self, handler: Callable[[str, tuple], None]) -> None:
    self.callback_handlers.append(handler)
  
  async def unregister_callback_handler(self, handler: Callable[[str, tuple], None]) -> None:
    self.callback_handlers.remove(handler)

  async def authenticate(self, username: str, password: str) -> bool:
    response = await self.execute('Authenticate', username, password)

    if not response:
      raise Exception('Authentication failed!')

