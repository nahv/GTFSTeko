from flask import Blueprint, render_template
from models import Stop

stop_bp = Blueprint('stop', __name__, url_prefix='/stop')

@stop_bp.route('/')
def list_stops():
    stops = Stop.query.all()
    return render_template('view_data.html', data=stops, data_type="Stops")
