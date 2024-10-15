from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import Calendar, Trip, StopTime
from database import db

# Define the blueprint for the calendar routes
calendar_bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@calendar_bp.route('/cargar_calendario', methods=['GET', 'POST'])
def cargar_calendario():
    if request.method == 'POST':
        # Get calendar data from form
        monday = request.form.get('monday')
        tuesday = request.form.get('tuesday')
        wednesday = request.form.get('wednesday')
        thursday = request.form.get('thursday')
        friday = request.form.get('friday')
        saturday = request.form.get('saturday')
        sunday = request.form.get('sunday')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Create and save a new Calendar instance
        calendar = Calendar(
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(calendar)
        db.session.commit()
        flash('Servicio cargado exitosamente', 'success')

        # Handle Trip data from the form
        route_id = request.form.get('route_id')
        service_id = request.form.get('service_id')
        trip_id = request.form.get('trip_id')
        trip_headsign = request.form.get('trip_headsign')
        direction_id = request.form.get('direction_id')

        # Create and save a new Trip instance
        trip = Trip(
            route_id=route_id,
            service_id=service_id,
            trip_id=trip_id,
            trip_headsign=trip_headsign,
            direction_id=direction_id
        )
        db.session.add(trip)
        db.session.commit()

        # Handle Stop Times data from the form
        trip_id_stop_times = request.form.get('trip_id_stop_times')
        arrival_time = request.form.get('arrival_time')
        departure_time = request.form.get('departure_time')
        stop_id = request.form.get('stop_id')
        stop_sequence = request.form.get('stop_sequence')
        pickup_type = request.form.get('pickup_type')
        drop_off_type = request.form.get('drop_off_type')

        # Create and save StopTime instances
        stop_time = StopTime(
            trip_id=trip_id_stop_times,
            arrival_time=arrival_time,
            departure_time=departure_time,
            stop_id=stop_id,
            stop_sequence=stop_sequence,
            pickup_type=pickup_type,
            drop_off_type=drop_off_type
        )
        db.session.add(stop_time)
        db.session.commit()

        flash('Datos de viaje y tiempos de parada cargados exitosamente', 'success')

        return redirect(url_for('calendar.cargar_Servicio'))

    # Retrieve all calendar entries to display in the template
    servicios = Calendar.query.all()  # Now called 'servicios'
    return render_template('cargar_servicio.html', servicios=servicios)

@calendar_bp.route('/cargar_servicio/<int:service_id>', methods=['POST'])
def cargar_servicio(service_id):
    servicio = Calendar.query.get(service_id)
    if not servicio:
        flash('Servicio no encontrado', 'danger')
        return redirect(url_for('calendar.cargar_Servicio'))

    # Update the servicio details from the form data
    servicio.monday = request.form.get('monday')
    servicio.tuesday = request.form.get('tuesday')
    servicio.wednesday = request.form.get('wednesday')
    servicio.thursday = request.form.get('thursday')
    servicio.friday = request.form.get('friday')
    servicio.saturday = request.form.get('saturday')
    servicio.sunday = request.form.get('sunday')
    servicio.start_date = request.form.get('start_date')
    servicio.end_date = request.form.get('end_date')

    db.session.commit()
    flash('Servicio actualizado exitosamente', 'success')

    return redirect(url_for('calendar.cargar_Servicio'))

@calendar_bp.route('/eliminar_servicio/<int:service_id>', methods=['POST'])
def delete_data(service_id):
    servicio = Calendar.query.get(service_id)
    if servicio:
        db.session.delete(servicio)
        db.session.commit()
        flash('Servicio eliminado exitosamente', 'success')
    else:
        flash('Servicio no encontrado', 'danger')

    return redirect(url_for('calendar.cargar_Servicio'))
