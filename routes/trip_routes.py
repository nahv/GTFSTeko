from flask import Blueprint, render_template
from models.models import Trip

trips_bp = Blueprint('trips', __name__, url_prefix='/trips')

@trips_bp.route('/cargar_trips')
def cargar_trips():
    return render_template('cargar_trips.html')


@trips_bp.route('/editar_trips')
def editar_trips():
    return render_template('editar_trips.html')