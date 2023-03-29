import logging
import time
from cust_socket import Socket
MAX_MSG_LENGHT = 8000
BET_CODE = "B"
RESULT_CODE = "R"
WAIT_CODE = "W"
OK_CODE = "O"

class Client:
    def __init__(self, config_params):
        split_info = config_params["server_address"].split(":")

        self._client_socket = Socket((split_info[0],int(split_info[1])))
        self._loop_period = config_params["loop_period"]
        self._loop_lapse = config_params["loop_lapse"]
        self._keep_running = True
        self._client_id = config_params["id"]
        self._current_msg_id = 1

        self._bet = ';'.join([config_params["apuesta_nombre"],
                    config_params["apuesta_apellido"],
                    config_params["apuesta_documento"],
                    config_params["apuesta_nacimiento"],
                    config_params["apuesta_numero"]])

    def run(self):
        #timeout = time.monotonic() + self._loop_lapse        

        #while time.monotonic() < timeout and self._keep_running:
        self._client_socket.connect()

        self._send_msg(self._bet)
        self._recv_msg(OK_CODE)
        
        # time.sleep(self._loop_period)
        
        self._current_msg_id += 1
        self._client_socket.close()
    
    def stop(self):
        self._keep_running = False
        self._client_socket.close()
        logging.info(f"[CLIENT {self._client_id}] Gracefully closing client socket")

    def _send_msg(self, msg):
        try:
            msg_encoded = msg.encode()
            msg_encoded_lenght = len(msg_encoded).to_bytes(6, "little", signed=False)

            if(len(msg_encoded) > MAX_MSG_LENGHT):
                raise Exception("Message lenght to long")

            self._client_socket.send_msg(BET_CODE.encode())
            self._client_socket.send_msg(msg_encoded_lenght)
            self._client_socket.send_msg(msg_encoded)
            logging.debug(f"action: send_msg | result: success")
        except Exception as e:
            logging.error(f"action: send_msg | result: error | error: {e.args}")
        
    
    def _recv_msg(self, SPECTED_CODE):
        try:
            received_msg = self._client_socket.recv_msg(len(SPECTED_CODE.encode()))
            if(received_msg != SPECTED_CODE):
                raise Exception("Message received not match with spected")
        except Exception as e:
            logging.error(f"action: recv_msg | result: error | error: {e.args}")            
        logging.debug(f"action: recv_msg | result: success | bytes_recv: {len(received_msg.encode())}")
        return received_msg
