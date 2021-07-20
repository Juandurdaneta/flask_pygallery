from pygallery.models import Usuario, Imagen, Etiqueta, Repositorio
from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app, abort
from pygallery.repositorios.forms import CrearRepositorioForm

repositorios = Blueprint('repositorios', __name__)

@repositorios.route('/usuario/<string:usuario>/repositorios')
def repositorios_usuario(usuario):
    usuario = Usuario.query.filter_by(username=usuario).first_or_404()
    repositorios_user = Repositorio.query.filter_by(propietario=usuario).first()
    form = CrearRepositorioForm()
    return render_template('repositorios_user.html', usuario=usuario, repositorios = repositorios_user, form=form)