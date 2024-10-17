from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import StopTime, Route, Stop, Trip
from database import db

gtfs_bp = Blueprint('gtfs', __name__, url_prefix='/gtfs')

@gtfs_bp.route('/cargar_recorrido', methods=['GET', 'POST'])
def cargar_recorrido():
    if request.method == 'POST':
        stop_ids = request.form.getlist('stop_ids')  # get selected stop_id
        arrival_times = request.form.getlist('arrival_times[]')  # list of arrival times
        departure_times = request.form.getlist('departure_times[]')  # list of departure times
        route_id = request.form['route_id']  # get selected route_id
        trip_headsign = request.form['trip_headsign']  # trip headsign

        # Validate that at least one stop was selected
        if not stop_ids or not arrival_times or not departure_times:
            flash('Seleccione al menos una parada', 'danger')
            return redirect(url_for('gtfs.cargar_recorrido'))

        # New trip
        new_trip = Trip(
            route_id=route_id,
            service_id=1,  
            trip_headsign=trip_headsign  
        )
        db.session.add(new_trip)
        db.session.flush()  # Ensure the trip is added and trip_id is available before adding stop_times

        # Loop through the stop IDs and create StopTime entries
        for i, stop_id in enumerate(stop_ids):
            # Check if the stop_time entry already exists
            existing_stop_time = StopTime.query.filter_by(trip_id=new_trip.trip_id, stop_id=stop_id).first()
            if existing_stop_time:
                flash(f'La combinación de trip_id {new_trip.trip_id} y stop_id {stop_id} ya existe. Saltando parada.', 'warning')
                continue  # Skip and continue with the next

            # Add new StopTime entry for each stop with corresponding times
            stop_time = StopTime(
                trip_id=new_trip.trip_id,  # New trip_id for recorrido
                stop_id=stop_id,
                arrival_time=arrival_times[i],
                departure_time=departure_times[i],
                stop_sequence=i + 1  
            )
            db.session.add(stop_time)

        db.session.commit()
        flash('Recorrido cargado con éxito.', 'success')
        return redirect(url_for('gtfs.cargar_recorrido'))

    # Fetch existing routes, stops, and stop times for display
    routes = Route.query.all()
    stops = Stop.query.all()
    stop_times = StopTime.query.all()

    return render_template('cargar_recorrido.html', routes=routes, stops=stops, stop_times=stop_times)