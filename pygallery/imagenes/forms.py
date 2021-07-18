from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PublicarImagenForm(FlaskForm):
        imagen = FileField('Imagen', validators=[FileAllowed(['jpg', 'png'])])
        etiquetas = StringField('Etiquetas de la Imagen', validators=[DataRequired()])
        submit = SubmitField('Publicar')
