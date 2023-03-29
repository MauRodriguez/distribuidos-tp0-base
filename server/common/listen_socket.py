import socket
import logging
from peer_socket import PeerSocket

class ListenSocket:
    def __init__(self, dir, port, listen_backlog):
        self._socket = None
        self._port = port
        self._dir = dir
        self._listen_backlog = listen_backlog
    
    def bind_and_listen(self):
        try:
            self._socket.bind((self._dir, self._port))
            self._socket.listen(self._listen_backlog)
            logging.debug(f"action: bind_and_listen | result: success | error: {repr(e)}")
        except socket.timeout as e:
            logging.error(f"action: bind_and_listen | result: error | error: {repr(e)}")
        except socket.error as e:
            logging.error(f"action: bind_and_listen | result: error | error: {repr(e)}")
    
    def accept(self):
        skt, addr = self._socket.accept()
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')

        return PeerSocket(skt), addr

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
