import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from pygallery.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'usuarios.login'
login_manager.login_message = 'Debes iniciar sesion para acceder a esta pagina.'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from pygallery.usuarios.routes import usuarios
    from pygallery.imagenes.routes import imagenes
    from pygallery.main.routes import main
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    app.register_blueprint(usuarios)
    app.register_blueprint(imagenes)
    app.register_blueprint(main)

    return app
