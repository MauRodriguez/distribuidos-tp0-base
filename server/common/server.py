import logging
from .peer_socket import PeerSocket
from .listen_socket import ListenSocket
from .utils import Bet
from .utils import store_bets
import re
BET_CODE = "B"
RESULT_CODE = "R"
WAIT_CODE = "W"
OK_CODE = "O"
CLIENT_NUMBER = 5

class Server:
    def __init__(self, port, listen_backlog):        
        self._server_socket = ListenSocket('', port, listen_backlog)
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
            code = self._client_socket.recv_msg(len(spected_code.encode())).decode('utf-8')
            msg_lenght = int.from_bytes(self._client_socket.recv_msg(6), "little",signed=False)            
            addr = self._client_socket.get_name()
            if code == BET_CODE:
                msg_received = self._client_socket.recv_msg(msg_lenght).decode('utf-8')
                self._parse_bets(msg_received)
                store_bets(self._bets)
                self._bets = []
                self._client_socket.send_msg(OK_CODE.encode('utf-8'))
                logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {msg_received}')            
            
        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
            logging.debug("action: client_close | result: success")
            self._client_socket.close()

    def _accept_new_connection(self):
        
        logging.info('action: accept_connections | result: in_progress')
        peer_skt = self._server_socket.accept()                
        return peer_skt
    
    def _parse_bets(self, msg):
        all_bets = re.split(';|\n',msg)
        
        for i in range(0, len(all_bets) - 6, 6):
            bet = Bet(msg[i], msg[i+1], msg[i+2], msg[i+3], msg[i+4], msg[i+5])
            self._bets.append(bet)
