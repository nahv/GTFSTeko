from flask import Blueprint, render_template
from models.models import StopTime

stoptimes_bp = Blueprint('stoptimes', __name__, url_prefix='/stoptimes')

@stoptimes_bp.route('/cargar_stoptimes')
def cargar_stoptimes():
    return render_template('cargar_stoptimes.html')


@stoptimes_bp.route('/editar_stoptimes')
def editar_stoptimes():
    return render_template('editar_stoptimes.html')