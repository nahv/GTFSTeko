import os
import subprocess
import pandas as pd
import sqlite3
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Define the blueprint
csv_bp = Blueprint('csv_bp', __name__)

# Directory where the files will be saved
DATASET_FOLDER = os.path.join(os.getcwd(), 'datasets')

# Paths to the CSV files and database
PARADAS_CSV = os.path.join(DATASET_FOLDER, 'paradas.csv')
RECORRIDOS_CSV = os.path.join(DATASET_FOLDER, 'recorridos.csv')
DB_PATH = os.path.join(os.getcwd(), 'instance', 'transporte.db')

# Helper function to round coordinates to 2 decimals
def round_coords(coords):
    return [[round(coord[0], 2), round(coord[1], 2)] for coord in coords]

# Function to load data from paradas.csv into the 'stop' table
def load_paradas_to_stops(paradas_df, cursor):
    for _, row in paradas_df.iterrows():
        stop_name = row['linea_ramal']
        stop_lat = row['lat']
        stop_lon = row['lng']
        stop_desc = row['linea_ramal']

        query = '''
        INSERT INTO stop (stop_name, stop_lat, stop_lon, stop_desc)
        VALUES (?, ?, ?, ?)
        '''
        cursor.execute(query, (stop_name, stop_lat, stop_lon, stop_desc))

# Function to load data from recorridos.csv into the 'routes' and 'trips' tables
def load_recorridos_to_routes_trips(recorridos_df, cursor):
    unique_ramal = recorridos_df['ramal'].unique()

    for ramal in unique_ramal:
        recorridos_ramal = recorridos_df[recorridos_df['ramal'] == ramal]
        for _, row in recorridos_ramal.iterrows():
            nombre = row['nombre']  # trip_headsign
            descripcion = row['descripcion']

            if '-' in descripcion:
                parts = descripcion.split(' - ')
                route_short_name = ''.join(filter(str.isdigit, parts[0]))
                route_long_name = parts[0].replace(route_short_name, '').strip()
                direction = parts[1]
            else:
                route_short_name = ''
                route_long_name = descripcion.strip()
                direction = ''

            # Determine direction_id
            if direction.lower() == "outbound":
                direction_id = 0
            elif direction.lower() == "inbound":
                direction_id = 1
            else:
                direction_id = None

            # Insert into 'route' table
            agency_id = 1  # Default agency
            route_type = 3  # Buses

            query_route = '''
            INSERT INTO route (agency_id, route_short_name, route_long_name, route_type)
            VALUES (?, ?, ?, ?)
            '''
            cursor.execute(query_route, (agency_id, route_short_name, route_long_name, route_type))
            route_id = cursor.lastrowid

            # Insert into 'trip' table
            service_id = 1  
            trip_headsign = nombre

            query_trip = '''
            INSERT INTO trip (route_id, service_id, trip_headsign, direction_id)
            VALUES (?, ?, ?, ?)
            '''
            cursor.execute(query_trip, (route_id, service_id, trip_headsign, direction_id))
            trip_id = cursor.lastrowid

            # Parse GeoJSON data
            geojson_str = row['st_asgeojson']

            if not geojson_str:
                continue  # Skip rows with empty GeoJSON

            try:
                geojson_data = json.loads(geojson_str)
                rounded_coords = round_coords(geojson_data['coordinates'])
            except (json.JSONDecodeError, KeyError):
                continue  # Skip invalid GeoJSON data

            # Insert into 'stop_time' table
            for stop_sequence, coord in enumerate(rounded_coords, start=1):
                stop_lat, stop_lon = coord
                query_stop_time = '''
                INSERT INTO stop_time (trip_id, stop_id, arrival_time, departure_time, stop_sequence, stop_lat, stop_lon)
                VALUES (?, NULL, ?, ?, ?, ?, ?)
                '''
                cursor.execute(query_stop_time, (trip_id, '06:00:00', '06:00:00', stop_sequence, stop_lat, stop_lon))

# Route to handle the CSV upload and database loading
@csv_bp.route('/importar_csv', methods=['GET', 'POST'])
def importar_csv():
    if request.method == 'POST':
        # Handle file upload for Paradas and Recorridos
        paradas_file = request.files.get('paradas')
        recorridos_file = request.files.get('recorridos')

        # Ensure the datasets folder exists
        if not os.path.exists(DATASET_FOLDER):
            os.makedirs(DATASET_FOLDER)

        # Process Paradas file
        if paradas_file and paradas_file.filename.endswith('.csv'):
            paradas_file.save(PARADAS_CSV)
        elif paradas_file:
            flash('El archivo de Paradas debe ser un CSV', 'danger')
            return redirect(url_for('csv_bp.importar_csv'))

        # Process Recorridos file
        if recorridos_file and recorridos_file.filename.endswith('.csv'):
            recorridos_file.save(RECORRIDOS_CSV)
        elif recorridos_file:
            flash('El archivo de Recorridos debe ser un CSV', 'danger')
            return redirect(url_for('csv_bp.importar_csv'))

        # If files were successfully uploaded, load them into the database
        if paradas_file or recorridos_file:
            try:
                # Load Paradas and Recorridos into the SQLite database
                paradas_df = pd.read_csv(PARADAS_CSV)
                recorridos_df = pd.read_csv(RECORRIDOS_CSV)

                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()

                load_paradas_to_stops(paradas_df, cursor)
                load_recorridos_to_routes_trips(recorridos_df, cursor)

                conn.commit()
                conn.close()

                flash('Datos importados y cargados correctamente a la base de datos', 'success')
            except Exception as e:
                flash(f'Error al cargar los datos: {str(e)}', 'danger')
        else:
            flash('Cargar al menos un archivo CSV', 'warning')

        return redirect(url_for('csv_bp.importar_csv'))

    return render_template('importar_csv.html')
