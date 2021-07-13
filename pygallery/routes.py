from flask import render_template, url_for, flash, redirect, request
from pygallery.forms import RegistrationForm, LoginForm, UpdateUserForm
from pygallery import app, db, bcrypt
from pygallery.models import Usuario, Imagen, Etiqueta
from flask_login import login_user, current_user, logout_user, login_required

imagenes = [{
    "ubicacion_imagen": "https://images.unsplash.com/photo-1626093632846-5c27587a0469?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1834&q=80",
    "propietario": "Juan"
},
{
    "ubicacion_imagen": "https://images.unsplash.com/photo-1625860191460-10a66c7384fb?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=701&q=80",
    "propietario": "Alba"
},
{
    "ubicacion_imagen": "https://images.unsplash.com/photo-1626180583122-c256e0ea54b0?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1834&q=80",
    "propietario": "Alba"
},
{
    "ubicacion_imagen": "https://images.unsplash.com/photo-1626092557341-0263049bb93c?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1834&q=80",
    "propietario": "Alba"
},
{
    "ubicacion_imagen": "https://images.unsplash.com/photo-1625857695225-ddd5f160c064?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "propietario": "Alba"
},
{
    "ubicacion_imagen": "https://images.unsplash.com/photo-1625869388548-11b830e57292?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1827&q=80",
    "propietario": "Alba"
}

]

@app.route("/")
@app.route("/home")
def home():
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

@app.route("/perfil", methods=['GET', 'POST'])
@login_required
def perfil():
    form = UpdateUserForm()
    if form.validate_on_submit():
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