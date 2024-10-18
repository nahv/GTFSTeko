from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import StopTime, Route, Stop, Trip
from database import db

gtfs_bp = Blueprint('gtfs', __name__, url_prefix='/gtfs')

@gtfs_bp.route('/cargar_recorrido', methods=['GET', 'POST'])
def cargar_recorrido():
    if request.method == 'POST':
        # Handle form submission logic here
        stop_ids = request.form.getlist('stop_ids[]')  # Get selected stop_id
        arrival_times = request.form.getlist('arrival_times[]')  # List of arrival times
        departure_times = request.form.getlist('departure_times[]')  # List of departure times
        route_id = request.form['route_id']  # Get selected route_id
        trip_headsign = request.form['trip_headsign']  # Trip headsign

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
            existing_stop_time = StopTime.query.filter_by(trip_id=new_trip.trip_id, stop_id=stop_id).first()
            if existing_stop_time:
                flash(f'La combinación de trip_id {new_trip.trip_id} y stop_id {stop_id} ya existe. Saltando parada.', 'warning')
                continue

            # Fetch the Stop instance to get latitude and longitude
            stop = Stop.query.get(stop_id)
            if not stop:
                flash(f'La parada con ID {stop_id} no existe. Saltando parada.', 'warning')
                continue

            stop_time = StopTime(
                trip_id=new_trip.trip_id,
                stop_id=stop_id,
                arrival_time=arrival_times[i],
                departure_time=departure_times[i],
                stop_sequence=i + 1,
                stop_lat=stop.stop_lat,  # Get latitude from Stop
                stop_lon=stop.stop_lon   # Get longitude from Stop
            )
            db.session.add(stop_time)

        db.session.commit()
        flash('Recorrido cargado con éxito.', 'success')
        return redirect(url_for('gtfs.cargar_recorrido'))

    # Pagination logic for stops
    page = request.args.get('page', 1, type=int)
    stops_pagination = Stop.query.paginate(page=page, per_page=10)

    stop_times_page = request.args.get('stop_times_page', 1, type=int)
    stop_times_pagination = StopTime.query.paginate(page=stop_times_page, per_page=10)

    routes = Route.query.all()

    # Stops dictionary
    stops = {stop.stop_id: stop.stop_name for stop in Stop.query.all()}

    return render_template('cargar_recorrido.html', 
                           routes=routes, 
                           stops=stops_pagination,  
                           stop_times=stop_times_pagination,
                           stop_names=stops)
