from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class PublicarImagenForm(FlaskForm):
        imagen = FileField('Imagen', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
        etiquetas = StringField('Etiquetas de la Imagen', validators=[DataRequired()])
        submit = SubmitField('Publicar')

        def validate_etiquetas(self, etiquetas):
                etiquetasIngresadas = etiquetas.data.split(",")

                contiene_duplicados = any(etiquetasIngresadas.count(etiqueta) > 1 for etiqueta in etiquetasIngresadas)
                if contiene_duplicados :
                    raise ValidationError('Ha ingresado una misma etiqueta varias veces, por favor revisa las etiquetas ingresadas.')


class EditarImagenForm(FlaskForm):
        imagen = FileField('Imagen', validators=[FileAllowed(['jpg', 'png'])])
        etiquetas = StringField('Etiquetas de la Imagen', validators=[DataRequired()])
        submit = SubmitField('Publicar')

        def validate_etiquetas(self, etiquetas):
                etiquetasIngresadas = etiquetas.data.split(",")

                contiene_duplicados = any(etiquetasIngresadas.count(etiqueta) > 1 for etiqueta in etiquetasIngresadas)
                if contiene_duplicados :
                    raise ValidationError('Ha ingresado una misma etiqueta varias veces, por favor revisa las etiquetas ingresadas.')




