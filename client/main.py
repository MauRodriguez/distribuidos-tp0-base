#!/usr/bin/env python3

from configparser import ConfigParser
from common.client import Client
import logging
import os
import sys
import signal
from functools import partial

def initialize_config():

    config = ConfigParser(os.environ)
    config.read("config.ini")

    config_params = {}
    try:
        config_params["id"] = int(os.getenv("CLI_ID", config["DEFAULT"]["CLI_ID"]))
        config_params["server_address"] = os.getenv("CLI_SERVER_ADDRESS", config["DEFAULT"]["CLI_SERVER_ADDRESS"])
        config_params["logging_level"] = os.getenv("CLI_LOGGING_LEVEL", config["DEFAULT"]["CLI_LOGGING_LEVEL"])
        config_params["loop_lapse"] = int(os.getenv("CLI_LOOP_LAPSE", config["DEFAULT"]["CLI_LOOP_LAPSE"]))
        config_params["loop_period"] = int(os.getenv("CLI_LOOP_PERIOD", config["DEFAULT"]["CLI_LOOP_PERIOD"]))
        config_params["apuesta_nombre"] = os.getenv("NOMBRE")
        config_params["apuesta_apellido"] = os.getenv("APELLIDO")
        config_params["apuesta_documento"] = os.getenv("DOCUMENTO")
        config_params["apuesta_nacimiento"] = os.getenv("NACIMIENTO")
        config_params["apuesta_numero"] = os.getenv("NUMERO")
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting client".format(e))

    return config_params


def main():
    config_params = initialize_config()
    logging_level = config_params["logging_level"]
    server_address = config_params["server_address"]
    id = config_params["id"]    

    initialize_log(logging_level)

    logging.debug(f"action: config | result: success | client_id: {id} | "
                  f"server_address: {server_address} | logging_level: {logging_level}")

    # Initialize server and start server loop    
    client = Client(config_params)
    signal.signal(signal.SIGTERM, partial(handle_sigterm, client))
    client.run()

def handle_sigterm(client, signum, frame):
    client.stop()
    logging.info(f"Sigterm received with signum {signum} frame {frame}") 
    sys.exit() 

def initialize_log(logging_level):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

if __name__ == "__main__":
    main()
