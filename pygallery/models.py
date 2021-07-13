from datetime import datetime
from pygallery import db

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
