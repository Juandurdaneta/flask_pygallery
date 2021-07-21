from pygallery import db
from pygallery.models import Usuario, Repositorio, Imagen
from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app, abort
from pygallery.repositorios.forms import CrearRepositorioForm, EditarRepositorioForm
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
        return redirect(url_for('repositorios.repositorios_usuario', usuario=current_user.username))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("Error al crear el repositorio, Intenalo de nuevo", "danger")
    return render_template('repositorios_user.html', title="Repositorios", usuario=usuario, repositorios = repositorios_user, form=form)

@repositorios.route('/usuario/<string:usuario>/<int:repositorio>', methods=['GET', 'POST'])
def repositorio(usuario, repositorio):
    usuario = Usuario.query.filter_by(username=usuario).first_or_404()
    repositorio_usuario = Repositorio.query.filter(Repositorio.id_propietario == usuario.id, Repositorio.id == repositorio).first_or_404()
    
    form = EditarRepositorioForm()


    if request.method == 'POST':
        if repositorio_usuario.propietario != current_user:
            abort(403)

        repositorio_usuario.nombre_repositorio = form.nombre_repositorio.data
        repositorio_usuario.descripcion = form.descripcion_repositorio.data

        db.session.commit()

        flash('Repositorio editado exitosamente', 'success')

    form.nombre_repositorio.data = repositorio_usuario.nombre_repositorio
    form.descripcion_repositorio.data = repositorio_usuario.descripcion

    return render_template("repositorio.html", title=repositorio_usuario.nombre_repositorio, repositorio=repositorio_usuario, form=form)

@repositorios.route('/repositorio/<int:id_repositorio>/agregar/<int:id_imagen>', methods=['POST'])
def agregar_imagen_repositorio(id_repositorio, id_imagen):
    repositorio = Repositorio.query.get_or_404(id_repositorio)
    imagen = Imagen.query.get_or_404(id_imagen)

    if repositorio.propietario != current_user:
        abort(403)
    
    if imagen in repositorio.imagenes:
        flash("Esta imagen ya existe en el repositorio seleccionado.", "danger")
    else:
        repositorio.imagenes.append(imagen)
        db.session.commit()

        flash("Imagen agregada exitosamente!", "success")
        
    return redirect(url_for("imagenes.imagen", id_imagen = id_imagen))


@repositorios.route('/repositorio/<int:id_repositorio>/quitar/<int:id_imagen>')
def quitar_imagen(id_imagen, id_repositorio):
    repositorio = Repositorio.query.get_or_404(id_repositorio)
    imagen = Imagen.query.get_or_404(id_imagen)

    if repositorio.propietario != current_user:
        abort(403)

    if imagen in repositorio.imagenes:
        repositorio.imagenes.remove(imagen)
        db.session.commit()
        flash("Imagen eliminada del repositorio", "success")
        return redirect(url_for('repositorios.repositorio', usuario=repositorio.propietario.username, repositorio=repositorio.id))
    else:
        abort(404)

@repositorios.route('/repositorio/<int:id_repositorio>/eliminar', methods=['POST'])
def eliminar_repositorio(id_repositorio):
    repositorio = Repositorio.query.get_or_404(id_repositorio)

    if repositorio.propietario != current_user:
        abort(403)

    db.session.delete(repositorio)
    db.session.commit()
    flash('Repositorio eliminado exitosamente!', "success")
    return redirect(url_for('repositorios.repositorios_usuario', usuario=current_user.username))