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
