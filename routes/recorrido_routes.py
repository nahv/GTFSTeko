from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import StopTime, Route, Stop, Trip
from database import db

gtfs_bp = Blueprint('gtfs', __name__, url_prefix='/gtfs')

@gtfs_bp.route('/cargar_recorrido', methods=['GET', 'POST'])
def cargar_recorrido():
    if request.method == 'POST':
        # Recibe datos del formulario
        stop_ids = request.form.getlist('stop_ids[]')
        arrival_times = request.form.getlist('arrival_times[]') 
        departure_times = request.form.getlist('departure_times[]')
        route_id = request.form['route_id']
        trip_headsign = request.form['trip_headsign']

        # Verifica si hay paradas seleccionadas
        if not stop_ids or not arrival_times or not departure_times:
            flash('Seleccione al menos una parada', 'danger')
            return redirect(url_for('gtfs.cargar_recorrido'))

        # Crea un nuevo viaje (Trip)
        new_trip = Trip(
            route_id=route_id,
            service_id=1,  
            trip_headsign=trip_headsign  
        )
        db.session.add(new_trip)
        db.session.flush()  # Para obtener el trip_id antes de commitear

        # Añade las StopTime correspondientes
        for i, stop_id in enumerate(stop_ids):
            # Verifica si ya existe la combinación
            existing_stop_time = StopTime.query.filter_by(trip_id=new_trip.trip_id, stop_id=stop_id).first()
            if existing_stop_time:
                flash(f'La combinación de trip_id {new_trip.trip_id} y stop_id {stop_id} ya existe. Salteando parada...', 'warning')
                continue

            # Verifica la existencia de la parada (Stop)
            stop = Stop.query.get(stop_id)
            if not stop:
                flash(f'La parada con ID {stop_id} no existe. Saltando parada.', 'warning')
                continue

            # Crea la entrada StopTime
            stop_time = StopTime(
                trip_id=new_trip.trip_id,
                stop_id=stop_id,
                arrival_time=arrival_times[i],
                departure_time=departure_times[i],
                stop_sequence=i + 1,
                stop_lat=stop.stop_lat,
                stop_lon=stop.stop_lon
            )
            db.session.add(stop_time)

        db.session.commit()  # Confirma los cambios
        flash('Recorrido cargado con éxito.', 'success')
        return redirect(url_for('gtfs.cargar_recorrido'))

    # Paginación para mostrar las paradas
    page = request.args.get('page', 1, type=int)
    stops_pagination = Stop.query.paginate(page=page, per_page=10)

    # Paginación para mostrar StopTimes
    stop_times_page = request.args.get('stop_times_page', 1, type=int)
    stop_times_pagination = StopTime.query.paginate(page=stop_times_page, per_page=10)

    # Rutas disponibles
    routes = Route.query.all()

    # Diccionario de paradas (para asociar stop_id a stop_name)
    stops = {stop.stop_id: stop.stop_name for stop in Stop.query.all()}

    return render_template('cargar_recorrido.html', 
                           routes=routes, 
                           stops=stops_pagination,  # Lista paginada de paradas
                           stop_times=stop_times_pagination,  # Lista paginada de StopTimes
                           stop_names=stops,
                           stop_dict=stops)  # Diccionario de nombres de paradas
