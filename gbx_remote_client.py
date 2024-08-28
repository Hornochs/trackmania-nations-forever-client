import xmlrpc.client as xmlrpclib
import socket

# GbxRemote Protocol specification: https://wiki.trackmania.io/en/dedicated-server/XML-RPC/gbxremote-protocol

class GbxRemoteClient:
  def __init__(self, host: str, port: int = 5000) -> None:
    self.host = host
    self.port = port

  def connect(self) -> None:
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((socket.gethostbyname(self.host), self.port))

    data = self.socket.recv(4)
    headerLength = int.from_bytes(data, byteorder='little')
    
    data = self.socket.recv(headerLength)
    header = data.decode()

    if header != "GBXRemote 2":
      raise Exception('No "GBXRemote 2" header found! Server may not be a GBXRemote server!')
    
    self.handler = None

  def _receive(self, expected_handler: int) -> tuple:
    header = self.socket.recv(8)
    size = int.from_bytes(header[:4], byteorder='little')
    # print(f'expecting: {size} bytes')
    handler = int.from_bytes(header[4:], byteorder='little')

    if handler != expected_handler:
      raise Exception(f'Handler mismatch! Expected {expected_handler}, got {handler}! Concurrency problem?')

    data = self.socket.recv(size)
    # print(f'received: {len(data)} bytes')
    data = xmlrpclib.loads(data.decode())
    data = data[0][0]

    return data
  
  def execute(self, method: str, *args) -> tuple:
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

    self.socket.send(packet)

    response_data = self._receive(current_handler)

    return response_data

  def authenticate(self, username: str, password: str) -> bool:
    response = self.execute('Authenticate', username, password)

    if not response:
      raise Exception('Authentication failed!')

