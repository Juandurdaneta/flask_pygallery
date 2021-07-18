from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from pygallery.models import Usuario

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Correo Electronico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Crear Cuenta')

    def validate_username(self, username):
        user = Usuario.query.filter_by(username = username.data).first()

        if user:
            raise ValidationError('Ya existe un usuario con ese nombre. Porfavor ingresa un nombre de usuario diferente')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError('Ya existe una cuenta asosciada a ese correo electronico. Porfavor ingresa un correo electronico diferente.')

class LoginForm(FlaskForm):
    email = StringField('Correo Electronico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesion')

class UpdateUserForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Correo Electronico', validators=[DataRequired(), Email()])
    imagen = FileField('Actualizar Imagen De Perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Actualizar Cuenta')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Usuario.query.filter_by(username = username.data).first()

            if user:
                raise ValidationError('Ya existe un usuario con ese nombre. Porfavor ingresa un nombre de usuario diferente')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Usuario.query.filter_by(email = email.data).first()

            if user:
                raise ValidationError('Ya existe una cuenta asosciada a ese correo electronico. Porfavor ingresa un correo electronico diferente.')

class SolicitarReestablecerContraseñaForm(FlaskForm):
    email = StringField('Correo Electronico', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar restablecimiento de la Contraseña')

    
    def validate_email(self, email):
        user = Usuario.query.filter_by(email = email.data).first()

        if not user:
            raise ValidationError('No existe una cuenta con ese correo electronico. Tienes que crear una cuenta.')

class ReestablecerContraseñaForm(FlaskForm):
     password = PasswordField('Contraseña', validators=[DataRequired()])
     confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
     submit = SubmitField('Reestablecer Contraseña')