import socket
import logging

class Socket:
    def __init__(self, address):
        self._socket = None
        self._address = address
    
    def connect(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect(self._address)
            logging.debug(f"action: connect | result: success | error: {e}")
        except socket.timeout as e:
            logging.error(f"action: connect | result: error | error: {e}")
        except socket.error as e:
            logging.error(f"action: connect | result: error | error: {e}")

    def close(self):
        self._socket.close()

    def recv_msg(self):
        try:
            received_msg = self._socket.recv(1024).decode()
            logging.debug(f"action: recv | result: success | msg: {received_msg}")
            return received_msg
        except socket.error as e:
            logging.error(f"action: recv | result: error | error: {e}") 
        
    def send_msg(self, msg):
        try:
            self._socket.sendall(msg.encode())
            logging.debug(f"action: sendall | result: success | msg: {msg}")
        except socket.error as e:
            logging.error(f"action: sendall | result: error | error: {e}")
