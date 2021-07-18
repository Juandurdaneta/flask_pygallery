import os
import secrets
from pygallery import db
from pygallery.models import Etiqueta, Imagen
from flask_login import current_user
from flask import current_app

def agregar_etiquetas(form_etiquetas):
    etiquetas = form_etiquetas.split(",")
    etiquetas_agregadas = []

    for etiqueta in etiquetas:
        etiqueta = etiqueta.capitalize()
        etiqueta_existente = Etiqueta.query.filter_by(nombre=etiqueta).first() 

        if not etiqueta_existente:
            etiqueta_nueva = Etiqueta(nombre=etiqueta)
            db.session.add(etiqueta_nueva)
            db.session.commit()
            etiquetas_agregadas.append(etiqueta_nueva)
        
        else:
            etiquetas_agregadas.append(etiqueta_existente)

    return etiquetas_agregadas

def subir_imagen(form_imagen, tags):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_imagen.filename)
    imagen_fn = random_hex + f_ext
    ubicacion_imagen = os.path.join(current_app.root_path, 'static/imagenes_subidas', imagen_fn)

    form_imagen.save(ubicacion_imagen)

    nueva_imagen = Imagen(ubicacion_imagen = imagen_fn, id_usuario=current_user.id)

    for etiqueta in tags:
        nueva_imagen.etiquetas.append(etiqueta)
    
    db.session.add(nueva_imagen)
    db.session.commit()

    return True

def cambiar_imagen(form_imagen):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_imagen.filename)
    imagen_fn = random_hex + f_ext
    ubicacion_imagen = os.path.join(current_app.root_path, 'static/imagenes_subidas', imagen_fn)
    form_imagen.save(ubicacion_imagen)

    return imagen_fn
