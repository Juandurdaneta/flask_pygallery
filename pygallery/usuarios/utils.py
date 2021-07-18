import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from pygallery import mail

def subir_imagen_perfil(form_imagen):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_imagen.filename)
    imagen_fn = random_hex + f_ext
    ubicacion_imagen = os.path.join(current_app.root_path, 'static/imagenes_perfil', imagen_fn)

    output_size = (300, 300)
    i = Image.open(form_imagen)
    i.thumbnail(output_size)
    i.save(ubicacion_imagen)

    return imagen_fn


def enviar_mail(usuario):
    token = usuario.get_reset_token()
    msg = Message('Solicitud de reestablecimiento de Contraseña', sender='noreply@pygallery.com', recipients=[usuario.email])
    msg.body= f''' Para reestablecer tu contraseña visita el siguiente enlace:
{url_for('usuarios.reestablecer_contraseña', token = token, _external=True)}
Si no hiciste esta solicitud simplemente ignora este mensaje y no se hara ningún cambio.
'''
    mail.send(msg)
