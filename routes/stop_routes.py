from flask import Blueprint, render_template
from models.models import Stop

stop_bp = Blueprint('stop', __name__, url_prefix='/stop')

@stop_bp.route('/editar_stops')
def editar_stops():
    return render_template('editar_stops.html')