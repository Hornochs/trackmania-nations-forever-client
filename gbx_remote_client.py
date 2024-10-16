from enum import Enum
from typing import Callable
import xmlrpc.client as xmlrpclib
import asyncio
import traceback

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
    self.general_callback_handlers: list[Callable[[str, tuple], None]] = []
    self.callback_handlers: map[str, list[Callable[[str, tuple], None]]] = {}
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
      except asyncio.IncompleteReadError as e:
        print(f'Caught IncompleteReadError: {e}')
        continue
      except ConnectionError as e:
        return
      except Exception as e:
        print(f'Error receiving packet: {e}')
        # await asyncio.sleep(1)
        continue
      
      if isinstance(packet, GbxRemoteCallbackPacket):
        try:
          self._handle_callback(packet.callback, data)
        except Exception as e:
          print(f'Error handling {packet.callback} callback:')
          traceback.print_exc()
          continue
      else:
        try:
          future = self.waiting_messages.pop(handler)

          if isinstance(data, GbxRemoteFault):
            future.set_exception(data)
          else:
            future.set_result(data)
        except KeyError:
          # message was not expected -> ignore
          continue
  
  async def _receive(self, expected_handler: int = None) -> GbxRemotePacket:
    header = await self.reader.read(8)
    size = int.from_bytes(header[:4], byteorder='little')
    
    if size == 0:
      raise ConnectionResetError('Receiving 0 bytes from server!')

    handler = int.from_bytes(header[4:], byteorder='little')

    if expected_handler is not None and  handler != expected_handler:
      raise Exception(f'Handler mismatch! Expected {expected_handler}, got {handler}! Concurrency problem?')

    data = await self.reader.readexactly(size)

    try:
      #print(f'Received: {data} instead of {size} bytes')
      data = xmlrpclib.loads(data.decode())
    except xmlrpclib.Fault as e:
      raise GbxRemoteFault(e, handler)

    if len(data) >= 2 and data[1] is not None:
      return GbxRemoteCallbackPacket(handler, data[0], data[1])
    else:
      return GbxRemotePacket(handler, data[0][0])
  
  async def execute(self, method: str, *args, response_timeout: float = 10) -> tuple:
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
    response_data = await asyncio.wait_for(response_future, timeout=response_timeout)

    return response_data
  
  def _handle_callback(self, callback: str, data: tuple) -> None:
    for callback_handler in self.general_callback_handlers:
      result = callback_handler(callback, data)
      if asyncio.iscoroutine(result):
        asyncio.create_task(result)
    
    if self.callback_handlers.get(callback) is not None:
      for callback_handler in self.callback_handlers[callback]:
        result = callback_handler(callback, data)
        if asyncio.iscoroutine(result):
          asyncio.create_task(result)
  
  def register_general_callback_handler(self, handler: Callable[[str, tuple], None]) -> None:
    self.general_callback_handlers.append(handler)
  
  def register_callback_handler(self, callback: Enum | str, handler: Callable[[str, tuple], None]) -> None:
    if isinstance(callback, Enum) and isinstance(callback.value, str):
      callback = callback.value

    if self.callback_handlers.get(callback) is None:
      self.callback_handlers[callback] = []
    
    self.callback_handlers[callback].append(handler)
  
  def unregister_general_callback_handler(self, handler: Callable[[str, tuple], None]) -> None:
    self.general_callback_handlers.remove(handler)
  
  def unregister_callback_handler(self, callback: str, handler: Callable[[str, tuple], None]) -> None:
    if isinstance(callback, Enum) and isinstance(callback.value, str):
      callback = callback.value

    if self.callback_handlers.get(callback) is not None:
      self.callback_handlers[callback].remove(handler)

  async def authenticate(self, username: str, password: str) -> bool:
    response = await self.execute('Authenticate', username, password)

    if not response:
      raise Exception('Authentication failed!')
  
  async def list_methods(self) -> list:
    """Return an array of all available XML-RPC methods on this server."""
    return await self.execute('system.listMethods')
  
  async def method_signature(self, method_name: str) -> list:
    """Given the name of a method, return an array of legal signatures."""
    return await self.execute('system.methodSignature', method_name)
  
  async def method_help(self, method_name: str) -> str:
    """Given the name of a method, return a help string."""
    return await self.execute('system.methodHelp', method_name)
  
  # async def multicall(self, calls: list) -> list:
  #   """Process an array of calls, and return an array of results."""
  #   return await self.execute('system.multicall', calls)
