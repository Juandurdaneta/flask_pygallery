from pygallery import db
from pygallery.models import Usuario, Repositorio
from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app, abort
from pygallery.repositorios.forms import CrearRepositorioForm
from flask_login import current_user

repositorios = Blueprint('repositorios', __name__)

@repositorios.route('/usuario/<string:usuario>/repositorios', methods=['GET', 'POST'])
def repositorios_usuario(usuario):
    usuario = Usuario.query.filter_by(username=usuario).first_or_404()
    repositorios_user = Repositorio.query.filter(Repositorio.id_propietario == usuario.id).all()
    form = CrearRepositorioForm()
    if form.validate_on_submit() and request.method == "POST":
        if current_user != usuario:
            abort(403)
        nuevo_repositorio = Repositorio(nombre_repositorio = form.nombre_repositorio.data, id_propietario = current_user.id, descripcion=form.descripcion_repositorio.data)
        db.session.add(nuevo_repositorio)
        db.session.commit()
        flash("Repositorio creado exitosamente!", "success")
        return redirect(url_for('repositorios_usuario', usuario=current_user.username))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("Error al crear el repositorio, Intenalo de nuevo", "danger")
    return render_template('repositorios_user.html', usuario=usuario, repositorios = repositorios_user, form=form)

