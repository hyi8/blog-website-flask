import os
import secrets
from PIL import Image
from flask import url_for, current_app
import smtplib
from email.message import EmailMessage


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profilepic', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    
    body= f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    msg = EmailMessage()
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = os.environ.get('EMAIL_USER')
    msg['To'] = os.environ.get('EMAIL_USER')
    msg.set_content(body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS'))
    server.sendmail(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_USER'), msg.as_string())
   
     