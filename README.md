QR Code App
Esta es una aplicacion para la creacion y el escaneo de código QR, donde tenes autenticacion JWT.

Requirements
============

- Python (3.10)
- fastapi
- uvicorn
- sqlalchemy
- httpx
- pytest
- pytest-mock
- pillow
- qrcode
- passlib[bcrypt]
- requests
- pyjwt
- psycopg2

Run with docker
===================
Se encuentra un archivo Dockerfile para crear la imagen del proyecto y un docker-compose para gestionar el contenedor.

Así mismo esta creado un archivo Makefile con las acciones automatizadas.

Podes crear la imagen y levantar el proyecto ejecutando los siguientes comandos:

Run commands with make

- Create image

    ```bash
    make build
    ```

- Run container

    ```bash
    make up
    ```

Esto levantará el proyecto localmente en la dirección 127.0.0.1:8000

## Running the tests

```sh
make test
```

Docs
===================
Para ingresar a la documentacion de los endpoints luego de levantar el servidor
debes de acceder a la direccion 127.0.0.1:8000/docs