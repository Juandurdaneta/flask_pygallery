from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pygallery import db, login_manager
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    imagen_perfil = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    imagenes = db.relationship('Imagen', backref="autor", lazy=True)
    repositorios = db.relationship('Repositorio', backref="propietario", lazy=True)

    def __repr__(self):
        return f"Usuario('{self.username}','{self.email}','{self.imagen_perfil}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try: 
            user_id = s.loads(token)['user_id']
        except:
            return none
        return Usuario.query.get(user_id)

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

    def __repr__(self):
        return f"Imagen('{self.ubicacion_imagen}','{self.fecha_publicacion}')"


class Etiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Etiqueta('{self.nombre}')"


repositorios = db.Table('repositorios',
                db.Column('repositorio_id', db.Integer, db.ForeignKey('repositorio.id'), primary_key=True),
                db.Column('imagen_id', db.Integer, db.ForeignKey('imagen.id'), primary_key=True)
                )

class Repositorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_repositorio = db.Column(db.String(20), nullable=False)
    id_propietario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    descripcion = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f"Repositorio('{self.nombre_repositorio}')"