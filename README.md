# MuscleMate-Backend

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a73f85f8fc504c888bef694a4ac6c69f)](https://app.codacy.com/gh/ISPP-23-24-Grupo-3/musclemate-backend?utm_source=github.com&utm_medium=referral&utm_content=ISPP-23-24-Grupo-3/musclemate-backend&utm_campaign=Badge_Grade)

## Como lanzar el proyecto (local):

Clona el repositorio en la carpeta que desees:

    git clone https://github.com/ISPP-23-24-Grupo-3/musclemate-backend.git

Entra en la carpeta musclemate-backend:

    cd musclemate-backend/

Crea un entorno virtual (opcional):

    python -m venv venv

Activa el entorno virtual (opcional):

    · source venv/bin/activate (Linux)
    · venv\Scripts\activate.bat (Windows)

Instala las dependencias:

    pip install -r requirements.txt

Realiza el setup de la base de datos (PostgresSQL):

    sudo su - postgres
    psql -c "create user muscleuser with password 'musclepass123'"
    psql -c "create database muscledb owner muscleuser"

Modifica el archivo local_settings.example.py para introducir la nueva base de datos y renómbralo como "local_settings.py".

Realiza las migraciones:

    python ./manage.py migrate

Crea un usuario administrador:

    python ./manage.py createsuperuser

Puebla la base de datos:
    
    python ./manage.py loaddata user owner gym

Lanza el proyecto:

    python ./manage.py runserver

El proyecto debería lanzarse correctamente. Por defecto, se lanza en la dirección "http://localhost:8000/".

# Despliegue en Docker

Dentro de la carpeta del proyecto, crea la imagen:

```bash
    docker build -t ispp-backend .
```

Ejecuta la imagen y mapea el puerto para poder acceder a la aplicación:

```bash
    docker run -dp 8000:8000 ispp-backend
```

## Con Docker Compose

Intencionado para su uso con el Front End.
Deberás configurar un directorio de la siguiente manera:

```
    .
    ├── docker-compose.yaml
    ├── musclemate-backend
    └── musclemate-frontend
```

El fichero docker-compose.yaml se encuentra inicialmente dentro de musclemate-frontend.

A continuación, desde el directorio con el fichero `docker-compose.yaml`, ejecuta:

```bash
    docker compose up -d
```

Tras hacer esto, se desplegarán:

- Una base de datos
- El proyecto de backend conectado a la base de datos
- El proyecto de frontend conectado al backend

La carpeta del proyecto de backend se montarán como un volumen dentro de su contenedor, por lo que se pueden realizar cambios libremente, de manera que se actualizarán en tiempo real.
