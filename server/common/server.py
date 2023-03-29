import socket
import logging
from peer_socket import PeerSocket
from listen_socket import ListenSocket
from utils import Bet
from utils import store_bets
BET_CODE = "B"
RESULT_CODE = "R"
WAIT_CODE = "W"
OK_CODE = "O"
CLIENT_NUMBER = 5

class Server:
    def __init__(self, port, listen_backlog):        
        self._server_socket = ListenSocket(('', port), listen_backlog)
        self._server_socket.bind_and_listen()
        self._bets = []        
        self._client_socket = None
        self._keep_running = True
        self._client_finished = 0

    def run(self):    
        while self._keep_running:
            self._client_socket = self._accept_new_connection()
            self._handle_client_connection(BET_CODE)

    def stop(self):
        self._keep_running = False
        self._client_socket.close()
        self._server_socket.close()
        logging.info("Gracefully closing server sockets")

    def _handle_client_connection(self, spected_code):
        try:            
            code = self._client_sock.recv(len(spected_code.encode())).decode('utf-8')
            msg_lenght = int.from_bytes(self._client_sock.recv(6), "little",signed=False)            
            
            if code == BET_CODE:
                msg_received = self._client_sock.recv(msg_lenght).decode('utf-8').split(';')
                self._bets.append(Bet(self._client_socket.get_name(), msg_received[0], msg_received[1], msg_received[2]
                                , msg_received[3], msg_received[4]))
                store_bets(self._bets.pop())
                self._client_sock.send(OK_CODE.encode('utf-8'))

            logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {msg}')
            
            
        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
            logging.debug("action: client_close | result: success")
            self._client_sock.close()

    def _accept_new_connection(self):
        
        logging.info('action: accept_connections | result: in_progress')
        peer_skt = self._server_socket.accept()                
        return peer_skt
