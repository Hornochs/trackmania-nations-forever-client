import xmlrpc.client as xmlrpclib
import socket
import asyncio

# GbxRemote Protocol specification: https://wiki.trackmania.io/en/dedicated-server/XML-RPC/gbxremote-protocol

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

  async def _receive(self, expected_handler: int) -> tuple:
    header = await self.reader.read(8)
    size = int.from_bytes(header[:4], byteorder='little')
    # print(f'expecting: {size} bytes')
    handler = int.from_bytes(header[4:], byteorder='little')

    if handler != expected_handler:
      raise Exception(f'Handler mismatch! Expected {expected_handler}, got {handler}! Concurrency problem?')

    data = await self.reader.read(size)
    # print(f'received: {len(data)} bytes')
    data = xmlrpclib.loads(data.decode())
    data = data[0][0]

    return data
  
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

    response_data = await self._receive(current_handler)

    return response_data

  async def authenticate(self, username: str, password: str) -> bool:
    response = await self.execute('Authenticate', username, password)

    if not response:
      raise Exception('Authentication failed!')

