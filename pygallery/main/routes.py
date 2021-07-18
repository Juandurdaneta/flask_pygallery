from flask import Blueprint, request, render_template
from pygallery.models import Imagen

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    pagina = request.args.get('pagina', 1, type=int)
    imagenes = Imagen.query.order_by(Imagen.fecha_publicacion.desc()).paginate(page=pagina, per_page=9)
    return render_template('index.html', imagenes=imagenes)


