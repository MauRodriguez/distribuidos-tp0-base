import logging
import time
from .connect_socket import ConnectSocket
import csv
import os
MAX_MSG_LENGHT = 8192
BET_CODE = "B"
RESULT_CODE = "R"
WAIT_CODE = "W"
OK_CODE = "O"

BETS_PER_BATCH = 40

class Client:
    def __init__(self, config_params):
        split_info = config_params["server_address"].split(":")

        self._client_socket = ConnectSocket((split_info[0],int(split_info[1])))
        self._loop_period = config_params["loop_period"]
        self._loop_lapse = config_params["loop_lapse"]
        self._keep_running = True
        self._client_id = config_params["id"]
        self._current_msg_id = 1        

    def run(self):
        #timeout = time.monotonic() + self._loop_lapse    

        #while time.monotonic() < timeout and self._keep_running:
        all_bets = self._read_csv()
        batch = "".encode('utf-8')

        for bet in all_bets:     
            bet_encoded = bet.encode('utf-8')

            if(len(batch) + len(bet_encoded)) >= MAX_MSG_LENGHT:
                self._handle_connection(batch)
                batch = "".encode('utf-8')
            
            batch = batch + bet_encoded
        if len(batch) != 0:
            self._handle_connection(batch)
        logging.info(f"[CLIENT {self._client_id}] finished")
        
    
    def stop(self):
        self._keep_running = False
        self._client_socket.close()
        logging.info(f"[CLIENT {self._client_id}] Gracefully closing client socket")

    def _send_msg(self, msg_encoded):
        try:
            msg_encoded_lenght = len(msg_encoded).to_bytes(6, "little", signed=False)

            if len(msg_encoded) > MAX_MSG_LENGHT:
                raise Exception("Message lenght to long")

            self._client_socket.send_msg(BET_CODE.encode('utf-8'))
            self._client_socket.send_msg(msg_encoded_lenght)
            self._client_socket.send_msg(msg_encoded)
            logging.debug(f"action: send_msg | result: success")
        except Exception as e:
            logging.error(f"action: send_msg | result: error | error: {e.args}")

    def _read_csv(self):
        all_bets = []

        filename = os.path.join(os.path.dirname(__file__),f"./dataset/agency-{self._client_id}.csv")

        with open(filename,"r") as file:
            reader = csv.reader(file, delimiter='\n')
            for i , line in enumerate(reader):
                aux = ','.join(line)
                aux = str(self._client_id) + "," + aux + '\n'
                all_bets.append(aux)

        return all_bets
        
    
    def _recv_msg(self, spected_code):
        try:
            received_msg = self._client_socket.recv_msg(len(spected_code.encode('utf-8'))).decode('utf-8')
            if received_msg != spected_code:
                raise Exception("Message received not match with spected")
            logging.debug(f"action: recv_msg | result: success | msg: {received_msg}")
            return received_msg
        except Exception as e:
            logging.error(f"action: recv_msg | result: error | error: {e.args}")   

    def _handle_connection(self, batch):
        self._client_socket.connect()

        self._send_msg(batch)
        self._recv_msg(OK_CODE)
        
        self._current_msg_id += 1
        self._client_socket.close()         
