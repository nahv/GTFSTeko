import os
import zipfile
from flask import Blueprint, render_template, send_file, flash, redirect, url_for, request
from models.models import Agency, Route, Stop, Calendar, Trip, StopTime

export_gtfs_bp = Blueprint('export_gtfs_bp', __name__)

GTFS_FOLDER = os.path.join(os.getcwd(), 'gtfs_exports')

@export_gtfs_bp.route('/export_gtfs', methods=['GET', 'POST'])
def export_gtfs():
    if request.method == 'POST':
        # Ensure the GTFS folder exists
        if not os.path.exists(GTFS_FOLDER):
            os.makedirs(GTFS_FOLDER)

        try:
            # Generate each GTFS file from the database
            generate_agency_txt()
            generate_routes_txt()
            generate_stops_txt()
            generate_calendar_txt()
            generate_trips_txt()
            generate_stop_times_txt()

            # Zip the GTFS files
            zip_file_path = zip_gtfs_files()

            # Provide the zip file for download
            return send_file(zip_file_path, as_attachment=True)

        except Exception as e:
            flash(f"Error exporting GTFS: {e}", 'danger')
            return redirect(url_for('export_gtfs_bp.export_gtfs'))

    # On GET request, calculate statistics
    agencies_count = Agency.query.count()
    routes_count = Route.query.count()
    stops_count = Stop.query.count()
    calendars_count = Calendar.query.count()
    trips_count = Trip.query.count()
    stop_times_count = StopTime.query.count()

    return render_template('export_gtfs.html', 
                           agencies_count=agencies_count,
                           routes_count=routes_count,
                           stops_count=stops_count,
                           calendars_count=calendars_count,
                           trips_count=trips_count,
                           stop_times_count=stop_times_count,
                           agencies=Agency.query.all())


# Helper function to zip all the GTFS files
def zip_gtfs_files():
    zip_path = os.path.join(GTFS_FOLDER, 'gtfs.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_name in os.listdir(GTFS_FOLDER):
            if file_name.endswith('.txt'):
                zipf.write(os.path.join(GTFS_FOLDER, file_name), file_name)
    return zip_path


# Functions to generate each TXT file
def generate_agency_txt():
    agency_file = os.path.join(GTFS_FOLDER, 'agency.txt')
    agencies = Agency.query.all()

    with open(agency_file, 'w') as f:
        f.write('agency_id,agency_name,agency_url,agency_timezone\n')
        for agency in agencies:
            f.write(f'{agency.agency_id},{agency.agency_name},{agency.agency_url},{agency.agency_timezone}\n')


def generate_routes_txt():
    routes_file = os.path.join(GTFS_FOLDER, 'routes.txt')
    routes = Route.query.all()

    with open(routes_file, 'w') as f:
        f.write('route_id,agency_id,route_short_name,route_long_name,route_type,route_color\n')
        for route in routes:
            f.write(f'{route.route_id},{route.agency_id},{route.route_short_name},{route.route_long_name},{route.route_type},{route.route_color}\n')


def generate_stops_txt():
    stops_file = os.path.join(GTFS_FOLDER, 'stops.txt')
    stops = Stop.query.all()

    with open(stops_file, 'w') as f:
        f.write('stop_id,stop_name,stop_lat,stop_lon,stop_desc\n')
        for stop in stops:
            f.write(f'{stop.stop_id},{stop.stop_name},{stop.stop_lat},{stop.stop_lon},{stop.stop_desc}\n')


def generate_calendar_txt():
    calendar_file = os.path.join(GTFS_FOLDER, 'calendar.txt')
    calendars = Calendar.query.all()

    with open(calendar_file, 'w') as f:
        f.write('service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n')
        for cal in calendars:
            f.write(f'{cal.service_id},{cal.monday},{cal.tuesday},{cal.wednesday},{cal.thursday},{cal.friday},{cal.saturday},{cal.sunday},{cal.start_date},{cal.end_date}\n')


def generate_trips_txt():
    trips_file = os.path.join(GTFS_FOLDER, 'trips.txt')
    trips = Trip.query.all()

    with open(trips_file, 'w') as f:
        f.write('trip_id,route_id,service_id,trip_headsign,direction_id\n')
        for trip in trips:
            f.write(f'{trip.trip_id},{trip.route_id},{trip.service_id},{trip.trip_headsign},{trip.direction_id}\n')


def generate_stop_times_txt():
    stop_times_file = os.path.join(GTFS_FOLDER, 'stop_times.txt')
    stop_times = StopTime.query.all()

    with open(stop_times_file, 'w') as f:
        f.write('trip_id,stop_id,arrival_time,departure_time,stop_sequence,stop_lat,stop_lon\n')
        for stop_time in stop_times:
            f.write(f'{stop_time.trip_id},{stop_time.stop_id},{stop_time.arrival_time},{stop_time.departure_time},{stop_time.stop_sequence},{stop_time.stop_lat},{stop_time.stop_lon}\n')


