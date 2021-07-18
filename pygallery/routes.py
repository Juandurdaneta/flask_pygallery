import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from pygallery.forms import RegistrationForm, LoginForm, UpdateUserForm, PublicarImagenForm, SolicitarReestablecerContraseñaForm, ReestablecerContraseñaForm
from pygallery import app, db, bcrypt, mail
from pygallery.models import Usuario, Imagen, Etiqueta
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    pagina = request.args.get('pagina', 1, type=int)
    imagenes = Imagen.query.order_by(Imagen.fecha_publicacion.desc()).paginate(page=pagina, per_page=9)
    return render_template('index.html', imagenes=imagenes)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = LoginForm()
    print(current_user)
    if form.validate_on_submit():
        # BUSCANDO USUARIO QUE COINCIDA CON EL CORREO ELECTRONICO INGRESADO
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario, remember = form.remember.data)
            siguiente_pagina = request.args.get('next')

            return redirect(siguiente_pagina) if siguiente_pagina else redirect(url_for('home'))
        else:
            flash("Inicio sesion infructuoso, por favor revisa tus credenciales y vuelva a intentarlo.", "danger")

    return render_template('login.html', title="login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  

    form = RegistrationForm()
    if form.validate_on_submit():
        # GENERANDO HASH PARA LA CONTRASEÑA INGRESADA
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # CREANDO USUARIO CON LOS DATOS INGRESADOS EN EL FORM
        user = Usuario(username=form.username.data, email=form.email.data, password=pass_hash)

        # AGREGANDO EL USUARIO A LA BASE DE DATOS
        db.session.add(user)
        db.session.commit()

        flash(f"Cuenta creada para {form.username.data}!", "success")
        return redirect(url_for('home'))

    return render_template('register.html', title="register", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def subir_imagen_perfil(form_imagen):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_imagen.filename)
    imagen_fn = random_hex + f_ext
    ubicacion_imagen = os.path.join(app.root_path, 'static/imagenes_perfil', imagen_fn)

    output_size = (300, 300)
    i = Image.open(form_imagen)
    i.thumbnail(output_size)
    i.save(ubicacion_imagen)

    return imagen_fn

@app.route("/perfil", methods=['GET', 'POST'])
@login_required
def perfil():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.imagen.data:
            archivo_imagen = subir_imagen_perfil(form.imagen.data)
            current_user.imagen_perfil = archivo_imagen
        # ACTUALIZANDO DATOS DEL USUARIO
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        db.session.commit()
        print(current_user)
        flash("Tu usuario ha sido actualizado exitosamente!", "success")
        return redirect(url_for('perfil'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    imagen = url_for('static', filename='/imagenes_perfil/'+current_user.imagen_perfil)
    return render_template('perfil.html', title="Perfil", imagen=imagen, form=form)

def agregar_etiquetas(form_etiquetas):
    etiquetas = form_etiquetas.split(",")
    etiquetas_agregadas = []

    for etiqueta in etiquetas:
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
    ubicacion_imagen = os.path.join(app.root_path, 'static/imagenes_subidas', imagen_fn)

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
    ubicacion_imagen = os.path.join(app.root_path, 'static/imagenes_subidas', imagen_fn)
    form_imagen.save(ubicacion_imagen)

    return imagen_fn

@app.route("/publicar_imagen", methods=['GET', 'POST'])
@login_required
def publicar_imagen():
    form = PublicarImagenForm()
    if form.validate_on_submit():
        etiquetas = agregar_etiquetas(form.etiquetas.data)
        if subir_imagen(form.imagen.data, etiquetas):
            flash("Tu imagen ha sido publicada exitosamente!", "success")
            return redirect(url_for('home'))
        else:
            flash("Ha ocurrido un error al subir la imagen, intentalo de nuevo", "danger")
    
    return render_template('publicar_imagen.html', title="Publicar Imagen", leyenda="Publicar Imagen", form=form)

@app.route("/imagen/<int:id_imagen>")
def imagen(id_imagen):
    imagen = Imagen.query.get_or_404(id_imagen)
    return render_template('imagen.html', title = "Imagen", imagen=imagen)


@app.route("/imagen/<int:id_imagen>/editar", methods=['GET', 'POST'])
@login_required
def editar_imagen(id_imagen):
    imagen = Imagen.query.get_or_404(id_imagen)
    form = PublicarImagenForm()
    if imagen.autor != current_user: # EN CASO DE QUE ALGUIEN DIFERENTE DEL AUTOR DE LA IMAGEN TRATE DE EDITARLA
        abort(403)

    if form.validate_on_submit():
        if form.imagen.data:
            os.remove(os.path.join(app.root_path, 'static/imagenes_subidas', imagen.ubicacion_imagen)) # ELIMINANDO LA IMAGEN ACTUAL PARA AGREGAR LA NUEVA
            nueva_imagen = cambiar_imagen(form.imagen.data)
            imagen.ubicacion_imagen = nueva_imagen
        etiquetas = agregar_etiquetas(form.etiquetas.data)
        
        imagen.etiquetas = []

        for etiqueta in etiquetas:
            imagen.etiquetas.append(etiqueta)
        
        db.session.commit()

        flash("Tu imagen ha sido publicada exitosamente!", "success")
        return redirect(url_for('home'))

    elif request.method == 'GET':
        form.imagen.data = imagen.ubicacion_imagen
        etiquetas = ""
        for etiqueta in imagen.etiquetas:
            if etiqueta == imagen.etiquetas[-1]:  # EN CASO DE QUE LA ETIQUETA SEA LA ULTIMA EN LA LISTA DE ETIQUETAS
                etiquetas += etiqueta.nombre
            else:
                etiquetas += etiqueta.nombre + ","
        form.etiquetas.data = etiquetas

    return render_template('publicar_imagen.html', title = "Editar imagen", leyenda="Editar imagen", form=form)

@app.route("/imagen/<int:id_imagen>/eliminar", methods=['POST'])
@login_required
def eliminar_imagen(id_imagen):
    imagen = Imagen.query.get_or_404(id_imagen)
    if imagen.autor != current_user: # EN CASO DE QUE ALGUIEN DIFERENTE DEL AUTOR DE LA IMAGEN TRATE DE ELIMINARLA
        abort(403)
    os.remove(os.path.join(app.root_path, 'static/imagenes_subidas', imagen.ubicacion_imagen)) # ELIMINANDO LA IMAGEN DEL SERVIDOR
   
    db.session.delete(imagen)
    db.session.commit()
   
    flash("Tu imagen ha sido eliminada!", "success")
    return redirect(url_for('home')) 

@app.route("/etiqueta/<string:etiqueta>")
def imagenes_etiqueta(etiqueta):
    etiqueta_requerida = Etiqueta.query.filter_by(nombre=etiqueta).first_or_404()
    imagenes = Imagen.query.filter(Imagen.etiquetas.contains(etiqueta_requerida)).order_by(Imagen.fecha_publicacion.desc())
    return render_template('imagen_etiqueta.html', imagenes=imagenes, title=etiqueta_requerida.nombre)

@app.route("/usuario/<string:usuario>")
def perfil_usuario(usuario):
    pagina = request.args.get('pagina', 1, type=int)
    usuario = Usuario.query.filter_by(username=usuario).first_or_404()
    imagenes = Imagen.query.filter_by(autor=usuario).order_by(Imagen.fecha_publicacion.desc()).paginate(page=pagina, per_page=6)
    return render_template('imagenes_usuario.html', usuario=usuario, imagenes=imagenes)


def enviar_mail(usuario):
    token = usuario.get_reset_token()
    msg = Message('Solicitud de reestablecimiento de Contraseña', sender='noreply@pygallery.com', recipients=[usuario.email])
    msg.body= f''' Para reestablecer tu contraseña visita el siguiente enlace:
{url_for('reestablecer_contraseña', token = token, _external=True)}
Si no hiciste esta solicitud simplemente ignora este mensaje y no se hara ningún cambio.
'''
    mail.send(msg)

@app.route("/reestablecer", methods=['GET', 'POST'])
def solicitud_reestablecimiento():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SolicitarReestablecerContraseñaForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        enviar_mail(usuario)
        flash("Se ha enviado un email a tu correo con instrucciones para reestablecer tu contraseña!", "info")
        return redirect(url_for('home'))
    return render_template('solicitud_reestablecimiento.html', title="Solicitar Reestablecimiento de Contraseña", form=form)

@app.route("/reestablecer_contraseña/<token>", methods=['GET', 'POST'])
def reestablecer_contraseña(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ReestablecerContraseñaForm()
    usuario = Usuario.verify_reset_token(token)
    if not usuario:
        flash('El enlace expiró o es invalido.', 'warning')
        return redirect(url_for('solicitud_reestablecimiento'))
    if form.validate_on_submit():
        hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usuario.password = hash
        db.session.commit()
        flash('Tu contraseña ha sido actualizada exitosamente!', 'success')
        return redirect(url_for('login'))

    return render_template('reestablecer_contraseña.html', title="Reestablecer Contraseña", form=form)