from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import Route, Agency
from database import db
from flask_paginate import Pagination, get_page_parameter

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

    agencies = Agency.query.all()

    # Pagination setup
    page = request.args.get(get_page_parameter(), type=int, default=1)  # Get the current page
    per_page = 10  # Set the number of items per page
    routes = Route.query.paginate(page=page, per_page=per_page)  # Paginate routes

    # Prepare the pagination object for template rendering
    pagination = Pagination(page=page, total=routes.total, search=False, record_name='routes', per_page=per_page)

    return render_template('cargar_routes.html', agencies=agencies, routes=routes.items, pagination=pagination, current_page=page, total_pages=routes.pages)

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

    db.session.commit()  # Commit the changes to the database
    flash('Línea actualizada con éxito.', 'success')
    return redirect(url_for('route.cargar_routes'))
