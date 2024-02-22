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

Realiza las migraciones:

    python manage.py migrate

Crea un usuario administrador (opcional, existe uno creado por defecto):

    python manage.py createsuperuser

Lanza el proyecto:

    python manage.py runserver

El proyecto debería lanzarse correctamente. Por defecto, se lanza en la dirección "http://localhost:8000/".

Por defecto, para iniciar sesión en "http://localhost:8000/admin", usar:
- Username: admin
- Password: gymadmin123
