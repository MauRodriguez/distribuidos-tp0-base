import logging
from .peer_socket import PeerSocket
from .listen_socket import ListenSocket
import time
from .utils import Bet
from .utils import store_bets
from .utils import has_won
from .utils import load_bets
import re
import threading
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
        self._threads = []      
        self._clients = []
        self._client_finished = 0
        self._winners = {"1": "",
                         "2": "",
                         "3": "",
                         "4": "",
                         "5": ""
                         }
        self._winners_already_calculated = False
        self._file_mtx = threading.Lock()
        self._finished_mtx = threading.Lock()

    def run(self):   

        for i in range(0,CLIENTS_AMOUNT):
            client_socket = self._accept_new_connection()
            self._clients.append(client_socket)
            new_thread = threading.Thread(target=self._handle_client_connection,
                                          args=(client_socket,))
            self._threads.append(new_thread)
            new_thread.start()            
        
        for thread in self._threads:
            logging.info("Empiezo a hacer join")
            thread.join()
        self._server_socket.close()

    def stop(self):
        self._keep_running = False
        self._server_socket.close()
        for client in self._clients:
            client.close()
        for thread in self._threads:
            thread.join()
        logging.info("Gracefully closing server sockets")

    def _handle_client_connection(self, client_socket):
        keep_running = True
        while keep_running:
            try:            
                code = client_socket.recv_msg(1).decode('utf-8')
                if code == BET_CODE:
                    msg_lenght = int.from_bytes(client_socket.recv_msg(4), "little",signed=False)            
                    msg_received = client_socket.recv_msg(msg_lenght).decode('utf-8')

                    self._parse_bets(msg_received)
                    with self._file_mtx:    
                        store_bets(self._bets)
                    self._bets = []

                    client_socket.send_msg(OK_CODE.encode('utf-8'))
                    logging.debug(f'action: receive_message | result: success | code: {code}')

                elif code == FINISH_CODE:
                    with self._finished_mtx:
                        self._client_finished += 1
                    client_socket.send_msg(OK_CODE.encode('utf-8'))
                    logging.info(f'action: receive_message | result: success | code: {code}')

                elif code == ASK_WINNERS_CODE:
                    with self._finished_mtx:
                        if self._client_finished < CLIENTS_AMOUNT:
                            client_socket.send_msg(WAIT_CODE.encode('utf-8'))
                            continue
                    
                    client_socket.send_msg(RESULT_CODE.encode('utf-8'))
                    logging.info(f'action: receive_message | result: success | code: {code}')
                    
                    msg_lenght = int.from_bytes(client_socket.recv_msg(4), "little",signed=False)                    
                    client_name = client_socket.recv_msg(msg_lenght).decode('utf-8')
                    
                    encoded_winners = self._calculate_winners(client_name).encode('utf-8')

                    client_socket.send_msg(len(encoded_winners).to_bytes(4, "little", signed=False))
                    client_socket.send_msg(encoded_winners)
                    keep_running = False  
                
            except OSError as e:
                logging.error("action: receive_message | result: fail | error: {e}")
        logging.info("saliendo exitosamente de un hilo")
        client_socket.close()

    def _accept_new_connection(self):
        
        logging.info('action: accept_connections | result: in_progress')
        peer_skt = self._server_socket.accept()                
        return peer_skt
    
    def _parse_bets(self, msg):
        all_bets = re.split(',|\n',msg)
        
        for i in range(0, len(all_bets) - 6, 6):
            
            bet = Bet(all_bets[i], all_bets[i+1], all_bets[i+2], all_bets[i+3], all_bets[i+4], all_bets[i+5])
            self._bets.append(bet)
            
    def _calculate_winners(self, agency):
        with self._file_mtx:
            if not self._winners_already_calculated:
                bets = load_bets()

                for bet in bets:
                    if has_won(bet):
                        self._winners[str(bet.agency)] += (str(bet.document) + ",")
                logging.info('action: calculating winners | result: finish')
                self._winners_already_calculated = True
            return self._winners[agency]

        
        
