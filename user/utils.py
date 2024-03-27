from django.core.mail import send_mail

def send_verification_email(user):
    token = user.gen_verification_token()
    subject = 'Verify your email'
    message = f'Buenas, {user}! \nTras iniciar sesión como su nuevo usuario, por favor haga click en el siguiente enlace para verificar su e-mail:
\nhttp://localhost:5173/verify \nInicie sesión como su nuevo usuario y haga uso de el siguiente token: {token}'
    send_mail(subject, message, 'musclemateverification@outlook.com', [user.email])