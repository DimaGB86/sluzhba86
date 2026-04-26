import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, redirect, send_from_directory

app = Flask(__name__)

# --- Настройки почты ---
SMTP_SERVER = "smtp.timeweb.ru"
SMTP_PORT = 465
EMAIL = os.environ.get('EMAIL_USER', 'your-email@sluzhba86.ru')
PASSWORD = os.environ.get('EMAIL_PASS', 'your_password')
TO_EMAIL = "Novikov.K.S@mail.ru"

# --- Главная страница ---
@app.route('/')
def serve_homepage():
    return send_from_directory('.', 'index.html')

# --- Статические файлы ---
@app.route('/assets/<path:filepath>')
def serve_static(filepath):
    return send_from_directory('assets', filepath)

# --- Обработка формы ---
@app.route('/send-form', methods=['POST'])
def send_form():
    last_name = request.form.get('last_name', 'Не указана')
    first_name = request.form.get('first_name', 'Не указано')
    patronymic = request.form.get('patronymic', 'Не указано')
    phone = request.form.get('phone', 'Не указан')
    city = request.form.get('city', 'Не указан')

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
        return redirect('/?success#application-form')
    except Exception as e:
        print(f"Ошибка при отправке: {e}")
        return redirect('/?error#application-form')

# --- Точка входа для Gunicorn ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))