from flask import Blueprint, render_template
from models.models import Calendar

calendar_bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@calendar_bp.route('/cargar_calendar', endpoint='cargar_calendar')  
def cargar_calendar():
    return render_template('cargar_calendar.html')

@calendar_bp.route('/editar_calendar', endpoint='editar_calendar_calendar') 
def editar_calendar():
    return render_template('editar_calendar.html')
