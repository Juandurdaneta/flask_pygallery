from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class CrearRepositorioForm(FlaskForm):
    nombre_repositorio = StringField('Nombre del repositorio', validators=[DataRequired(),  Length(min=2, max=20)])
    submit = SubmitField('Crear Repositorio')
