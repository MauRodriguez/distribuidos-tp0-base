# SISTEMAS DISTRIBUIDOS - TRABAJO PRÁCTICO 0

## PARTE 1

### Ejercicio 1
Para este ejercicio simplemente se agregó un servicio nuevo en el docker-compose llamado cliente 2 con caracteristicas identicas al cliente 1.

### Ejercicio 1.1
**Correr con:** `python3 docker_compose_n_clients.py`

Para este ejercicio se creo un script en python que escriba un docker-compose nuevo con las prestaciones requeridas.

### Ejercicio 2

Se agrega en todos los servicios un volumen que contenga la carpeta de configuración `config.ini`

### Ejercicio 3
**Para verificar el script:**
En una terminal `sudo make docker-compose-up` y en otra en pararelo `bash test_server_with_netcat.sh`. A continuacion escribir algo de prueba y presionar ENTER. Ver como se recibe de nuevo el mensaje enviado.

Para lograr esto se levantar un servicio a parte, alpine, que solo contiene netcat, y se lo conecta a la misma network del docker-compose. Luego se ejecuta un comando que se conecta como cliente al servidor en modo interactivo.

### Ejercicio 4
**Para testear este ejercicio:**
`sudo make docker-compose-up`, 
`sudo make docker-compose-logs`, 
mientras los logs corren, en paralelo
`sudo make docker-compose-down` y 
verificar que todos los servicios terminan con exit status 0.

Luego de pasar el cliente a python, en ambos programas se agrega un signal handler, que al recibir la señal SIGTERM enviaba por el docker-compose stop, detiene su ejecución por completo para ejecutar el handler. En el handler se ejecuta los cierres de sockets gracefully y se ejecuta un `sys.exit()`, de lo contrario el programa continuaria con su ejecución normal.
El parametro -t del docker-compose stop al pasar un determinado tiempo manda un SIGKILL que evita el cierre gracefully, pero de todas formas lo dejé, subiendolo a 3, para evitar bloqueos si el programa falla en cerrar gracefully.

### Ejercicio 5

**Protocolo de comunicación:**
Como protocolo de comunicación se utilizo TLV. Los distintos Types por ahora son "B" de Bet, que representa que el mensaje será el que mande el cliente al servidor con la apuesta, y el tipo "O" Ok que responde el servidor al cliente para detonar que su mensaje fue recibido.
El Lenght de cada mensaje se codifican los ints en 6 bytes no signados, con little endian.
El Value es codificado como chars en utf-8, y su longitud máxima no puede superar la constante MSG_MAX_LENGHT que es de 8kB. Esta verificación solo se realiza en el cliente dado que es suficiente. Si nadie le manda al servidor mensajes largos por demás, nunca debería recibir un Lenght de longitud mayor.


Se crean los sockets de tipo connect, listen, y peer. El primero es el que usa el cliente, tiene las funciones connect y las necesarias para el socket. El segundo es el socket listener que usa el servidor para despachar conexiones, posee las funciones especiales bind and listen. Y el útlimo es el tipo de socket peer para cada cliente que maneja el server, que no posee la función connect.


### Ejercicio 6

Se agrega un reader en el cliente, y un parser tanto en client como en el server. El parser lo que hace es convertir un montón de bets en formato csv a formato batch, y en el servidor viceversa.
El formato del batch es bet separando cada campo por ',' y luego separando cada bet entre si por '\n'. Se sigue utilizando TLV.


### Ejercicio 7

**Protocolo de comunicación**:
Se agrega la parte del protocolo de comunicación para cuando el cliente pide los winners. Una vez que termina de mandar todos los mensajes, manda finish 'F' y el servidor lo recibe como un cliente terminado. Desde entonces el cliente comienza a hacer ping al servidor con mensajes de tipo 'A' asking_for_winners, y el servidor le puede responder con 'W' wait_code o con un 'R' result_code. Si le responde con un result_code el cliente le envia su nombre y seguido de esto el servidor le envia sus respectivos winners.


### Ejercicio 8
**Concurrencia**: se lanza un hilo por cliente, en cada uno de estos se realiza la comunicación con los mismos de principio a fin (desde las bets hasta obtener los winners). Hay un lock que se comparte tanto para escritura o lectura del archivo donde se guardan las bets, y otro lock que encapsula la variable _clients_finished que indica si todos los clientes ya terminaron o no. Al finalizar cada hilo se joinea.