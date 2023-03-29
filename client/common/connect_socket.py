import socket
import logging

class ConnectSocket:
    def __init__(self, address):
        self._socket = None
        self._address = address
    
    def connect(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect(self._address)
            logging.debug(f"action: connect | result: success | error: {repr(e)}")
        except socket.timeout as e:
            logging.error(f"action: connect | result: error | error: {repr(e)}")
        except socket.error as e:
            logging.error(f"action: connect | result: error | error: {repr(e)}")

    def close(self):
        self._socket.close()

    def recv_msg(self, lenght):
        try:
            received_msg = self._socket.recv(lenght)
            while len(received_msg) < lenght:
                received_msg.append(self._socket.recv(lenght - len(received_msg)))

            logging.debug(f"action: recv | result: success | msg: {received_msg}")

            return received_msg
        except socket.error as e:
            logging.error(f"action: recv | result: error | error: {repr(e)}") 
        
    def send_msg(self, msg):
        try:
            self._socket.sendall(msg)
            logging.debug(f"action: sendall | result: success | msg: {msg}")
        except socket.error as e:
            logging.error(f"action: sendall | result: error | error: {repr(e)}")
