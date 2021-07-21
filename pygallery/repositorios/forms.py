from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class CrearRepositorioForm(FlaskForm):
    nombre_repositorio = StringField('Nombre del repositorio', validators=[DataRequired(),  Length(min=2, max=20)])
    descripcion_repositorio = TextAreaField('Descripcion (opcional)')
    submit = SubmitField('Crear Repositorio')

class EditarRepositorioForm(FlaskForm):
    nombre_repositorio = StringField('Nombre del repositorio', validators=[DataRequired(),  Length(min=2, max=20)])
    descripcion_repositorio = TextAreaField('Descripcion (opcional)')
    submit = SubmitField('Editar Repositorio')
