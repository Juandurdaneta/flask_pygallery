from flask import render_template, url_for, flash, redirect
from pygallery.forms import RegistrationForm, LoginForm
from pygallery import app, db, bcrypt
from pygallery.models import Usuario, Imagen, Etiqueta


imagenes = [{
    "ubicacion_imagen": "https://images.unsplash.com/photo-1625860633266-8707a63d6671?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80",
    "propietario": "Juan"
},
{
    "ubicacion_imagen": "https://images.unsplash.com/photo-1625860191460-10a66c7384fb?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=701&q=80",
    "propietario": "Alba"
},
{
    "ubicacion_imagen": "https://images.unsplash.com/photo-1626093632846-5c27587a0469?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1834&q=80",
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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "juan@demo.com" and form.password.data == "password":
            flash("Bienvenido de nuevo!", "success")
            return redirect(url_for('home'))
        else:
            flash("Inicio sesion infructuoso, por favor revisa tus credenciales y vuelva a intentarlo.", "danger")
    return render_template('login.html', title="login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
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
