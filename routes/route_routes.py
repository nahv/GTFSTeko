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
        route_color = request.form.get('route_color')

        new_route = Route(
            agency_id=agency_id,
            route_short_name=route_short_name,
            route_long_name=route_long_name,
            route_type=route_type,
            route_color=route_color
        )
        db.session.add(new_route)
        db.session.commit()
        flash('Línea cargada con éxito.', 'success')
        return redirect(url_for('route.cargar_routes'))

    agencies = Agency.query.all()  # Fetch agencies for dropdown
    routes = Route.query.all()  # Fetch routes for table
    return render_template('cargar_routes.html', agencies=agencies, routes=routes)

@route_bp.route('/delete_route/<int:route_id>', methods=['POST'])
def delete_route(route_id):
    route = Route.query.get(route_id)
    if route:
        db.session.delete(route)
        db.session.commit()
        flash('Línea eliminada con éxito.', 'success')
    else:
        flash('Línea no encontrada.', 'danger')
    return redirect(url_for('route.cargar_routes'))  # Adjust the route as necessary

@route_bp.route('/editar_route', methods=['POST'])
def editar_route():
    # Get the route ID from the form
    route_id = request.form['route_id']
    # Fetch the route por ID
    route = Route.query.get_or_404(route_id)
    # Fetch agencies for dropdown
    agencies = Agency.query.all()
    # Render the edit form
    return render_template('editar_route.html', route=route, agencies=agencies)

@route_bp.route('/guardar_route/<int:route_id>', methods=['POST'])
def guardar_route(route_id):
    route = Route.query.get_or_404(route_id)  # Fetch the route by ID

    # Update route details with form data
    route.agency_id = request.form['agency_id']
    route.route_short_name = request.form['route_short_name']
    route.route_long_name = request.form['route_long_name']
    route.route_type = request.form['route_type']
    route.route_color = request.form.get('route_color')  # Optional

    db.session.commit()
    flash('Línea actualizada con éxito.', 'success')
    return redirect(url_for('route.cargar_routes'))  # Redirect after successful update
