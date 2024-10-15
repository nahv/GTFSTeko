from flask import Blueprint, render_template
from models.models import Shape

shapes_bp = Blueprint('shapes', __name__, url_prefix='/shapes')

@shapes_bp.route('/cargar_shapes')
def cargar_shapes():
    return render_template('cargar_shapes.html')

@shapes_bp.route('/editar_shapes')
def editar_shapes():
    return render_template('editar_shapes.html')