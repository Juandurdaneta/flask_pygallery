import os
from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app, abort
from flask_login import login_user, current_user, logout_user, login_required
from pygallery import db, bcrypt
from pygallery.models import Usuario, Etiqueta, Imagen
from pygallery.usuarios.forms import (RegistrationForm, LoginForm, UpdateUserForm, 
                                     SolicitarReestablecerContraseĆ±aForm, ReestablecerContraseĆ±aForm)
from pygallery.usuarios.utils import subir_imagen_perfil, enviar_mail

usuarios = Blueprint('usuarios', __name__)

@usuarios.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    form = LoginForm()
    print(current_user)
    if form.validate_on_submit():
        # BUSCANDO USUARIO QUE COINCIDA CON EL CORREO ELECTRONICO INGRESADO
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario, remember = form.remember.data)
            siguiente_pagina = request.args.get('next')

            return redirect(siguiente_pagina) if siguiente_pagina else redirect(url_for('main.home'))
        else:
            flash("Inicio sesion infructuoso, por favor revisa tus credenciales y vuelva a intentarlo.", "danger")

    return render_template('login.html', title="login", form=form)

@usuarios.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  

    form = RegistrationForm()
    if form.validate_on_submit():
        # GENERANDO HASH PARA LA CONTRASEĆA INGRESADA
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # CREANDO USUARIO CON LOS DATOS INGRESADOS EN EL FORM
        user = Usuario(username=form.username.data, email=form.email.data, password=pass_hash)

        # AGREGANDO EL USUARIO A LA BASE DE DATOS
        db.session.add(user)
        db.session.commit()

        flash(f"Cuenta creada para {form.username.data}!", "success")
        return redirect(url_for('main.home'))

    return render_template('register.html', title="register", form=form)

@usuarios.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@usuarios.route("/perfil", methods=['GET', 'POST'])
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
        return redirect(url_for('usuarios.perfil'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    imagen = url_for('static', filename='/imagenes_perfil/'+current_user.imagen_perfil)
    return render_template('perfil.html', title="Perfil", imagen=imagen, form=form)


@usuarios.route("/usuario/<string:usuario>")
def perfil_usuario(usuario):
    pagina = request.args.get('pagina', 1, type=int)
    usuario = Usuario.query.filter_by(username=usuario).first_or_404()
    imagenes = Imagen.query.filter_by(autor=usuario).order_by(Imagen.fecha_publicacion.desc()).paginate(page=pagina, per_page=6)
    return render_template('imagenes_usuario.html', usuario=usuario, imagenes=imagenes)

@usuarios.route("/reestablecer", methods=['GET', 'POST'])
def solicitud_reestablecimiento():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SolicitarReestablecerContraseĆ±aForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        enviar_mail(usuario)
        flash("Se ha enviado un email a tu correo con instrucciones para reestablecer tu contraseĆ±a!", "info")
        return redirect(url_for('main.home'))
    return render_template('solicitud_reestablecimiento.html', title="Solicitar Reestablecimiento de ContraseĆ±a", form=form)

@usuarios.route("/reestablecer_contraseĆ±a/<token>", methods=['GET', 'POST'])
def reestablecer_contraseĆ±a(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ReestablecerContraseĆ±aForm()
    usuario = Usuario.verify_reset_token(token)
    if not usuario:
        flash('El enlace expirĆ³ o es invalido.', 'warning')
        return redirect(url_for('usuarios.solicitud_reestablecimiento'))
    if form.validate_on_submit():
        hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usuario.password = hash
        db.session.commit()
        flash('Tu contraseĆ±a ha sido actualizada exitosamente!', 'success')
        return redirect(url_for('usuarios.login'))

    return render_template('reestablecer_contraseĆ±a.html', title="Reestablecer ContraseĆ±a", form=form)

@usuarios.route("/eliminar_usuario/<int:id_usuario>", methods=['POST'])
@login_required
def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if usuario != current_user:
        abort(403)

    for imagen in usuario.imagenes:
        os.remove(os.path.join(current_app.root_path, 'static/imagenes_subidas', imagen.ubicacion_imagen)) # ELIMINANDO IMAGENES CREADAS POR EL USUARIO
        db.session.delete(imagen)

    os.remove(os.path.join(current_app.root_path, 'static/imagenes_perfil', usuario.imagen_perfil)) # ELIMINANDO LA IMAGEN DEL SERVIDOR


    db.session.delete(usuario)
    db.session.commit()

    logout_user()


    flash('Usuario Eliminado exitosamente, lamentamos verte ir.', 'success')
    return redirect(url_for('main.home'))