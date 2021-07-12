from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '59eb5820bce3227f5308d8e82fa62e97'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    imagen_perfil = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    imagenes = db.relationship('Imagen', backref="autor", lazy=True)

    def __repr__(self):
        return f"Usuario('{self.username}','{self.email}','{self.imagen_perfil}')"

etiquetas = db.Table('etiquetas',
            db.Column('etiqueta_id', db.Integer, db.ForeignKey('etiqueta.id'), primary_key=True),
            db.Column('imagen_id', db.Integer, db.ForeignKey('imagen.id'), primary_key=True)
            )


class Imagen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ubicacion_imagen = db.Column(db.String(20), nullable=False, unique=True)
    fecha_publicacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    etiquetas = db.relationship('Etiqueta', secondary=etiquetas, lazy='subquery', backref=db.backref('imagenes', lazy=True))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr_(self):
        return f"Imagen('{self.ubicacion_imagen}','{self.fecha_publicacion}')"


class Etiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Etiqueta('{self.nombre}')"


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

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title="login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Cuenta creada para {form.username.data}!", "success")
        return redirect(url_for('home'))

    return render_template('register.html', title="register", form=form)


if __name__ == '__main__':
    app.run(debug=True)