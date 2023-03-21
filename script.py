import sys

def main():
    clients_amount = int(sys.argv[1])

    compose = open("docker-compose-dev.yaml","w")
    
    initial_lines = [
    "version: '3.9'\n",
    "name: tp0\n",
    "services:\n",
    "    server:\n",
    "        volumes:\n",
    "            - ./server/config.ini:/config.ini\n",
    "        container_name: server\n",
    "        image: server:latest\n",
    "        entrypoint: python3 /main.py\n",
    "        environment:\n",
    "            - PYTHONUNBUFFERED=1\n",
    "            - LOGGING_LEVEL=DEBUG\n",
    "        networks:\n",
    "            - testing_net\n\n"
    ]

    compose.writelines(initial_lines)

    for i in range(1, clients_amount + 1):
        client_lines = [
        "    client" + str(i) + ":\n",
        "        container_name: client" + str(i) + "\n",
        "        volumes:\n",
        "            - ./client/config.yaml:/config.yaml\n",
        "        image: client:latest\n",
        "        entrypoint: /client\n",
        "        environment:\n",
        "            - CLI_ID=" + str(i) + "\n",
        "            - CLI_LOG_LEVEL=DEBUG\n",
        "        networks:\n",
        "            - testing_net\n",
        "        depends_on:\n",
        "            - server\n\n"
        ]

        compose.writelines(client_lines)

    final_lines = [
    "networks:\n",
    "    testing_net:\n",
    "        ipam:\n",
    "            driver: default\n",
    "            config:\n",
    "                - subnet: 172.25.125.0/24\n"
    ]

    compose.writelines(final_lines)
    compose.close()

main()