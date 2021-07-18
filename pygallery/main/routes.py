from flask import Blueprint, request, render_template, redirect, url_for
from pygallery.models import Imagen

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    pagina = request.args.get('pagina', 1, type=int)
    imagenes = Imagen.query.order_by(Imagen.fecha_publicacion.desc()).paginate(page=pagina, per_page=9)
    return render_template('index.html', imagenes=imagenes)


@main.route("/buscar")
def buscar():
    query = request.args.get('query')
    print(query)
    return redirect(url_for('imagenes.imagenes_etiqueta', etiqueta = query))