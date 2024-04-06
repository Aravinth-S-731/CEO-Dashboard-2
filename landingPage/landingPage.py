from flask import Flask, render_template, Blueprint, request
from flask_mail import Mail, Message

landing_page = Blueprint('landing_page', __name__, template_folder='templates', static_folder='static', static_url_path='/landingPage/static')

mail = Mail()

def init_mysql_auth(app):
    app.config['MAIL_SERVER'] = "smtp.googlemail.com"
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "aravinth7871867225@gmail.com"
    app.config['MAIL_PASSWORD'] = "hoijwhxxspatlmys"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)

@landing_page.route('/')
def landingPage():
    return render_template('index.html')

@landing_page.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    mail_message = Message('Contact Form Submission', sender='email', recipients=[email])
    mail_message.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        mail.send(mail_message)
        return 'Message sent successfully!'
    except Exception as e:
        print(e)
        return 'Failed to send message.'