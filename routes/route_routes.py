from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import Route, Agency
from database import db 

route_bp = Blueprint('route', __name__, url_prefix='/route')

@route_bp.route('/cargar_routes', methods=['GET', 'POST'])
def cargar_routes():
    if request.method == 'POST':
        agency_id = request.form['agency_id']
        route_short_name = request.form['route_short_name']
        route_long_name = request.form['route_long_name']
        route_type = request.form['route_type']
        route_color = request.form.get('route_color')  # Optional

        new_route = Route(
            agency_id=agency_id,
            route_short_name=route_short_name,
            route_long_name=route_long_name,
            route_type=route_type,
            route_color=route_color
        )
        db.session.add(new_route)
        db.session.commit()
        flash('Ruta cargada con éxito.', 'success')
        return redirect(url_for('route.cargar_routes'))

    agencies = Agency.query.all()  # Fetch all agencies for dropdown
    routes = Route.query.all()  # Fetch all routes to display in the table
    return render_template('cargar_routes.html', agencies=agencies, routes=routes)

@route_bp.route('/delete_route/<int:route_id>', methods=['POST'])
def delete_route(route_id):
    route = Route.query.get(route_id)
    if route:
        db.session.delete(route)
        db.session.commit()
        flash('Ruta eliminada con éxito.', 'success')
    else:
        flash('Ruta no encontrada.', 'danger')
    return redirect(url_for('route.cargar_routes'))  # Adjust the route as necessary

@route_bp.route('/editar_routes')
def editar_routes():
    return render_template('editar_routes.html')
