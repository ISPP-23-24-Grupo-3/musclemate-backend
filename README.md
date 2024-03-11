# MuscleMate-Backend
[![Bluejay Dashboard](https://img.shields.io/badge/Bluejay-Dashboard_03-blue.svg)](http://dashboard.bluejay.governify.io/dashboard/script/dashboardLoader.js?dashboardURL=https://reporter.bluejay.governify.io/api/v4/dashboards/tpa-ISPP-2024-GH-ISPP-23-24-Grupo-3_musclemate-backend/main)
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
    
    python ./manage.py loaddata user owner gym client routine equipment event assessment reservation ticket workout serie

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
