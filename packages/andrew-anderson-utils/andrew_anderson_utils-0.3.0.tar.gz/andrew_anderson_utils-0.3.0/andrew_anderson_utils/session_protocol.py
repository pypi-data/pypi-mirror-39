import socket as sock
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Signature import PKCS1_PSS
import json

def make_packet(cmd, *args, **kwargs): # low-level function for making packets (without encrypting)
  return json.dumps([ cmd, args, kwargs ], sort_keys = True, separators = (',', ':')).encode('utf-8')

def split_packet(packet): # -> (cmd, args, kwargs)
  return json.loads(packet.decode())

class SessionProtocol(sock.socket):
  def __init__(self, rsa_key, socket_obj = None):
    if socket_obj == None:
      super().__init__(family = sock.AF_INET, type = sock.SOCK_STREAM)
    else:
      assert(socket_obj.family == sock.AF_INET and socket_obj.type == sock.SOCK_STREAM)
      super().__init__(family = sock.AF_INET, type = sock.SOCK_STREAM, fileno = socket_obj.detach())
    self.rsa_key = rsa_key
    self.rsa_obj = RSA.importKey(rsa_key)

    self.aes_key = None

  def accept(self):
    conn, addr = super().accept()
    return (SessionProtocol(rsa_key = self.rsa_key, socket_obj = conn), addr)

  def send(self, bts, initial = False): # low-level function for sending unencrypted bytes as encrypted packets
    if initial:
      # check if len(data) < len(rsa_key)
      return super().send(self.rsa_obj.encrypt(bts, 0)[0])
    else:
      # check if len(data) % AES.aes_obj.block_size == 0
      return super().send(self.aes_obj.encrypt(bts))

  def recv(self, buffersize, initial = False):
    return self.recvfrom(buffersize, initial)[0]

  def recvfrom(self, buffersize, initial = False):
    if initial:
      data, addr = super().recvfrom(buffersize)
      # check if len(data) < len(rsa_key)
      return (self.rsa_obj.decrypt(data), addr)
    else:
      data, addr = super().recvfrom(buffersize)
      # check if len(data) % AES.aes_obj.block_size == 0
      return (self.aes_obj.decrypt(data), addr)

  def setup_aes(self, aes_key):
    pass

  def send_initial(self):
    pass

  def recv_initial(self):
    pass
