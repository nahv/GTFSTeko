from flask import Blueprint, render_template
from models import Route

route_bp = Blueprint('route', __name__, url_prefix='/route')

@route_bp.route('/')
def list_routes():
    routes = Route.query.all()
    return render_template('view_data.html', data=routes, data_type="Routes")
