from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db  # Replace with your actual database import
from models.models import Calendar, Trip  # Adjust the import based on your models

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/cargar_trips', methods=['GET', 'POST'])
def cargar_trips():
    if request.method == 'POST':
        route_id = request.form.get('route_id')
        service_id = request.form.get('service_id')
        trip_headsign = request.form.get('trip_headsign')
        
        # Add validation for inputs here if necessary
        
        new_trip = Trip(route_id=route_id, service_id=service_id, trip_headsign=trip_headsign)
        db.session.add(new_trip)
        db.session.commit()
        flash('Viaje cargado exitosamente.', 'success')
        return redirect(url_for('trips.cargar_trips'))
    
    calendars = Calendar.query.all()  # Fetch all calendars for selection
    trips = Trip.query.all()  # Fetch all trips for display
    return render_template('cargar_trips.html', calendars=calendars, trips=trips)
