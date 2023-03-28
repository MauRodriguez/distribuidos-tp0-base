import logging
import time
from cust_socket import Socket

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
        timeout = time.monotonic() + self._loop_lapse        

        while time.monotonic() < timeout and self._keep_running:
            self._client_socket.connect()

            self._send_msg()
            self._recv_msg()
            
            time.sleep(self._loop_period)
            
            self._current_msg_id += 1
            self._client_socket.close()
    
    def stop(self):
        self._keep_running = False
        self._client_socket.close()
        logging.info(f"[CLIENT {self._client_id}] Gracefully closing client socket")

    def _send_msg(self, msg):
        msg_length = str(len(msg.encode())).encode()

        bytes_sent = self._client_socket.send_msg(msg_length)
        logging.debug(f"action: send_msg | result: success | bytes_sent: {bytes_sent}")
    
    def _recv_msg(self):
        received_msg = self._client_socket.recv_msg()            
        logging.debug(f"action: recv_msg | result: success | bytes_recv: {len(received_msg.encode())}")
        return received_msg
