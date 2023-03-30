import logging
from .peer_socket import PeerSocket
from .listen_socket import ListenSocket
import time
from .utils import Bet
from .utils import store_bets
from .utils import has_won
from .utils import load_bets
import re
BET_CODE = "B"
RESULT_CODE = "R"
WAIT_CODE = "W"
OK_CODE = "O"
ASK_WINNERS_CODE = "A"
FINISH_CODE = "F"
CLIENTS_AMOUNT = 5

class Server:
    def __init__(self, port, listen_backlog):        
        self._server_socket = ListenSocket('', port, listen_backlog)
        self._server_socket.bind_and_listen()
        self._bets = []        
        self._client_socket = None
        self._keep_running = True
        self._client_finished = 0
        self._client_notified = 0
        self._winners = {"1": "",
                         "2": "",
                         "3": "",
                         "4": "",
                         "5": ""
                         }

    def run(self):    
        while self._keep_running and self._client_finished < CLIENTS_AMOUNT:
            self._client_socket = self._accept_new_connection()
            self._handle_client_connection()
        
        self._calculate_winners()

        while self._keep_running and self._client_notified < CLIENTS_AMOUNT:
            self._client_socket = self._accept_new_connection()
            self._handle_client_connection()

    def stop(self):
        self._keep_running = False
        self._client_socket.close()
        self._server_socket.close()
        logging.info("Gracefully closing server sockets")

    def _handle_client_connection(self):
        try:            
            code = self._client_socket.recv_msg(1).decode('utf-8')
            addr = self._client_socket.get_name()
            if code == BET_CODE:
                msg_lenght = int.from_bytes(self._client_socket.recv_msg(2), "little",signed=False)            
                msg_received = self._client_socket.recv_msg(msg_lenght).decode('utf-8')

                self._parse_bets(msg_received)
                store_bets(self._bets)
                self._bets = []

                self._client_socket.send_msg(OK_CODE.encode('utf-8'))
                logging.debug(f'action: receive_message | result: success | code: {code}')

            elif code == FINISH_CODE:
                self._client_finished += 1
                self._client_socket.send_msg(OK_CODE.encode('utf-8'))
                logging.info(f'action: receive_message | result: success | code: {code}')

            elif code == ASK_WINNERS_CODE:
                if self._client_finished < CLIENTS_AMOUNT:
                    self._client_socket.send_msg(WAIT_CODE.encode('utf-8'))
                else:
                    self._client_socket.send_msg(RESULT_CODE.encode('utf-8'))
                    logging.info(f'action: receive_message | result: success | code: {code}')
                    self._client_socket = self._accept_new_connection()

                    msg_lenght = int.from_bytes(self._client_socket.recv_msg(2), "little",signed=False)                    
                    client_name = self._client_socket.recv_msg(msg_lenght).decode('utf-8')
                    
                    encoded_winners = self._winners[client_name].encode('utf-8')

                    self._client_socket.send_msg(len(encoded_winners).to_bytes(2, "little", signed=False))
                    self._client_socket.send_msg(encoded_winners)   
                    self._client_notified += 1    
            
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
        all_bets = re.split(',|\n',msg)
        
        for i in range(0, len(all_bets) - 6, 6):
            
            bet = Bet(all_bets[i], all_bets[i+1], all_bets[i+2], all_bets[i+3], all_bets[i+4], all_bets[i+5])
            self._bets.append(bet)
            
    def _calculate_winners(self):
        bets = load_bets()

        for bet in bets:
            if has_won(bet):
                self._winners[str(bet.agency)] += (str(bet.document) + ",")
        logging.info('action: calculating winners | result: finish')

        
        
