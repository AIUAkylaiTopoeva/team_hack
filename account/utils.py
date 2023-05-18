from django.core.mail import send_mail

def send_activation_code(email, activation_code):
    message = f'Вы зарегестровались на нашем сайте. Пройдите активацию аккаента\n Код активациии: {activation_code}'
    send_mail('Активация аккаунта',
               message, 
               'test@gmail.com',
                [email]
                 )
    