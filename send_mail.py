import os
import smtplib
from email.mime.text import MIMEText
from bottle import route, run, request, redirect, static_file

SMTP_SERVER = "smtp.timeweb.ru"
SMTP_PORT = 465
EMAIL = os.environ.get('EMAIL_USER', 'your-email@sluzhba86.ru')
PASSWORD = os.environ.get('EMAIL_PASS', 'your_password')
TO_EMAIL = "Novikov.K.S@mail.ru"

@route('/')
def serve_homepage():
    return static_file('index.html', root='.')

@route('/assets/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='assets')

@route('/send-form', method='POST')
def send_form():
    last_name = request.forms.get('last_name', 'Не указана')
    first_name = request.forms.get('first_name', 'Не указано')
    patronymic = request.forms.get('patronymic', 'Не указано')
    phone = request.forms.get('phone', 'Не указан')
    city = request.forms.get('city', 'Не указан')

    subject = f"Новая заявка: {last_name} {first_name}"
    body = f"""
    Новая заявка с сайта sluzhba86.ru!
    
    Фамилия: {last_name}
    Имя: {first_name}
    Отчество: {patronymic}
    Телефон: {phone}
    Город: {city}
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        redirect('/?success#application-form')
    except Exception as e:
        print(f"Ошибка при отправке: {e}")
        redirect('/?error#application-form')

app = application = bottle.app()

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))