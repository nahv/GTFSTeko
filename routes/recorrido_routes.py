from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import StopTime, Route, Stop
from database import db

gtfs_bp = Blueprint('gtfs', __name__, url_prefix='/gtfs')

# Route to handle stop times form submission and display
@gtfs_bp.route('/cargar_recorrido', methods=['GET', 'POST'])
def cargar_recorrido():
    if request.method == 'POST':
        stop_ids = request.form.getlist('stop_ids')  # Get selected stop ids from the form
        arrival_time = request.form['arrival_time']  # Single arrival time input
        departure_time = request.form['departure_time']  # Single departure time input
        route_id = request.form['route_id']  # The selected route

        # Validate that at least one stop was selected
        if not stop_ids:
            flash('Por favor seleccione al menos una parada.', 'danger')
            return redirect(url_for('gtfs.cargar_recorrido'))

        # Loop through the stop IDs and create StopTime entries
        for i, stop_id in enumerate(stop_ids):
            # Check if the entry already exists
            existing_stop_time = StopTime.query.filter_by(trip_id=route_id, stop_id=stop_id).first()
            if existing_stop_time:
                flash(f'La combinación de trip_id {route_id} y stop_id {stop_id} ya existe.')
                continue  # Skip and continue with the next

            stop_time = StopTime(
                trip_id=route_id,  # Assuming trip_id is the same as route_id, adjust as needed
                stop_id=stop_id,
                arrival_time=arrival_time,  # Same time for all stops, can be adjusted for each stop
                departure_time=departure_time,
                stop_sequence=i + 1  # Sequence number based on the order of the selected stops
            )
            db.session.add(stop_time)

        db.session.commit()
        flash('Recorrido con éxito.', 'success')
        return redirect(url_for('gtfs.cargar_recorrido'))

    # Fetch existing routes, stops, and stop times for display
    routes = Route.query.all()
    stops = Stop.query.all()
    stop_times = StopTime.query.all()

    return render_template('cargar_recorrido.html', routes=routes, stops=stops, stop_times=stop_times)

    # Fetch existing routes, stops, and stop times for display
    routes = Route.query.all()
    stops = Stop.query.all()
    stop_times = StopTime.query.all()

    return render_template('cargar_recorrido.html', routes=routes, stops=stops, stop_times=stop_times)
