import socket
import logging

class PeerSocket:
    def __init__(self, socket, addr):
        self._socket = socket    
        self._addr = addr

    def close(self):
        self._socket.close()

    def recv_msg(self, lenght):
        try:
            received_msg = self._socket.recv(lenght)
            while len(received_msg) < lenght:
                received_msg = received_msg + (self._socket.recv(lenght - len(received_msg)))                

            logging.debug(f"action: recv | result: success")

            return received_msg
        except socket.error as e:
            logging.error(f"action: recv | result: error | error: {repr(e)}") 
        
    def send_msg(self, msg):
        try:
            self._socket.sendall(msg)
            logging.debug(f"action: sendall | result: success")
        except socket.error as e:
            logging.error(f"action: sendall | result: error | error: {repr(e)}")
    
    def get_name(self):
        return self._addr[0]
