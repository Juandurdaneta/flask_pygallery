import os
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, abort
from flask_login import current_user, login_required
from pygallery import db
from pygallery.models import Usuario, Etiqueta, Imagen, Repositorio
from pygallery.imagenes.forms import PublicarImagenForm, EditarImagenForm
from pygallery.imagenes.utils import agregar_etiquetas, subir_imagen, cambiar_imagen


imagenes = Blueprint('imagenes', __name__)

@imagenes.route("/publicar_imagen", methods=['GET', 'POST'])
@login_required
def publicar_imagen():
    form = PublicarImagenForm()
    if form.validate_on_submit():
        etiquetas = agregar_etiquetas(form.etiquetas.data)
        if subir_imagen(form.imagen.data, etiquetas):
            flash("Tu imagen ha sido publicada exitosamente!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Ha ocurrido un error al subir la imagen, intentalo de nuevo", "danger")
    etiquetas = Etiqueta.query.limit(5).all()
    return render_template('publicar_imagen.html', title="Publicar Imagen", leyenda="Publicar Imagen", form=form, etiquetas=etiquetas)

@imagenes.route("/imagen/<int:id_imagen>")
def imagen(id_imagen):
    imagen = Imagen.query.get_or_404(id_imagen)
    if current_user.is_authenticated:
        repositorios_user = Repositorio.query.filter(Repositorio.id_propietario == current_user.id).all()   
        return render_template('imagen.html', title = "Imagen", imagen=imagen, repositorios=repositorios_user)
    else:
         return render_template('imagen.html', title = "Imagen", imagen=imagen)


@imagenes.route("/imagen/<int:id_imagen>/editar", methods=['GET', 'POST'])
@login_required
def editar_imagen(id_imagen):
    imagen = Imagen.query.get_or_404(id_imagen)
    form = EditarImagenForm()
    if imagen.autor != current_user: # EN CASO DE QUE ALGUIEN DIFERENTE DEL AUTOR DE LA IMAGEN TRATE DE EDITARLA
        abort(403)

    if form.validate_on_submit():
        if form.imagen.data:
            os.remove(os.path.join(current_app.root_path, 'static/imagenes_subidas', imagen.ubicacion_imagen)) # ELIMINANDO LA IMAGEN ACTUAL PARA AGREGAR LA NUEVA
            nueva_imagen = cambiar_imagen(form.imagen.data)
            imagen.ubicacion_imagen = nueva_imagen
        etiquetas = agregar_etiquetas(form.etiquetas.data)
        
        imagen.etiquetas = []

        for etiqueta in etiquetas:
            imagen.etiquetas.append(etiqueta)
        
        db.session.commit()

        flash("Tu imagen ha sido publicada exitosamente!", "success")
        return redirect(url_for('main.home'))

    elif request.method == 'GET':
        form.imagen.data = imagen.ubicacion_imagen
        etiquetas = ""
        for etiqueta in imagen.etiquetas:
            if etiqueta == imagen.etiquetas[-1]:  # EN CASO DE QUE LA ETIQUETA SEA LA ULTIMA EN LA LISTA DE ETIQUETAS
                etiquetas += etiqueta.nombre
            else:
                etiquetas += etiqueta.nombre + ","
        form.etiquetas.data = etiquetas

    etiquetas = Etiqueta.query.limit(5).all()
    return render_template('publicar_imagen.html', title = "Editar imagen", leyenda="Editar imagen", form=form, etiquetas=etiquetas)

@imagenes.route("/imagen/<int:id_imagen>/eliminar", methods=['POST'])
@login_required
def eliminar_imagen(id_imagen):
    imagen = Imagen.query.get_or_404(id_imagen)
    if imagen.autor != current_user: # EN CASO DE QUE ALGUIEN DIFERENTE DEL AUTOR DE LA IMAGEN TRATE DE ELIMINARLA
        abort(403)
    os.remove(os.path.join(current_app.root_path, 'static/imagenes_subidas', imagen.ubicacion_imagen)) # ELIMINANDO LA IMAGEN DEL SERVIDOR
   
    db.session.delete(imagen)
    db.session.commit()
   
    flash("Tu imagen ha sido eliminada!", "success")
    return redirect(url_for('main.home')) 

@imagenes.route("/etiqueta/<string:etiqueta>")
def imagenes_etiqueta(etiqueta):
    etiqueta_requerida = Etiqueta.query.filter_by(nombre=etiqueta).first()
    if etiqueta_requerida:
        imagenes = Imagen.query.filter(Imagen.etiquetas.contains(etiqueta_requerida)).order_by(Imagen.fecha_publicacion.desc())
        return render_template('imagen_etiqueta.html', imagenes=imagenes, title=etiqueta)
    else:
        return render_template('imagen_etiqueta.html', title=etiqueta)

