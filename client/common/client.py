import socket
import logging
import time

class Client:
    def __init__(self, config_params):

        self._client_socket = None

        split_info = config_params["server_address"].split(":")
        self._server_address = (split_info[0],int(split_info[1]))

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
            self._connect()
            self._send_msg(f"[CLIENT {self._client_id}] MESSAGE N°: {self._current_msg_id}")
            received_msg = self._recv_msg()            
            time.sleep(self._loop_period)
            self._current_msg_id += 1
            self._end_connection()
    
    def stop(self):
        self._keep_running = False
        self._end_connection()
        logging.info(f"[CLIENT {self._client_id}] Gracefully closing client socket")

    def _recv_msg(self):
        received_msg = self._client_socket.recv(1024).decode()
        logging.info(f"action: recv_msg | result: success | client_id: {self._client_id} | msg {received_msg} ")
        return received_msg
        
    def _send_msg(self, msg):
        self._client_socket.send(msg.encode())
    
    def _connect(self):
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.connect(self._server_address)
    
    def _end_connection(self):
        self._client_socket.close()

