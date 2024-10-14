from flask import Blueprint, render_template
from models import Agency

agency_bp = Blueprint('agency', __name__, url_prefix='/agency')

@agency_bp.route('/')
def list_agencies():
    agencies = Agency.query.all()
    return render_template('view_data.html', data=agencies, data_type="Agencies")
