# MuscleMate-Backend

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
