# Script para el tratamiento de los csv
# Este archivo es únicamente de referencia
# Ya no se usa en la app, la funciones de acá se implementan en routes/export_gtfs_routes.py

import pandas as pd
import sqlite3
import json

# Paths
paradas_csv = 'paradas.csv'
recorridos_csv = 'recorridos.csv'
db_path = '../instance/transporte.db'

# Helper para redondear coordenadas a 2 decimales
def round_coords(coords):
    return [[round(coord[0], 2), round(coord[1], 2)] for coord in coords]

# Función para insertar data en 'stops' table
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

# Función para insertar data en 'routes' and 'trips' y update 'stop_time'
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

            # Determina direction_id
            if direction.lower() == "outbound":
                direction_id = 0
            elif direction.lower() == "inbound":
                direction_id = 1
            else:
                direction_id = None 

            # Insertar en 'routes' table
            agency_id = 1  # Agencia 1 por defecto
            route_type = 3  # Buses

            query_route = '''
            INSERT INTO route (agency_id, route_short_name, route_long_name, route_type)
            VALUES (?, ?, ?, ?)
            '''
            cursor.execute(query_route, (agency_id, route_short_name, route_long_name, route_type))
            route_id = cursor.lastrowid

            # trip_headsign from 'nombre' and direction_id
            service_id = 1  
            trip_headsign = nombre  # Usar columna 'nombre' para el trip headsign

            query_trip = '''
            INSERT INTO trip (route_id, service_id, trip_headsign, direction_id)
            VALUES (?, ?, ?, ?)
            '''
            cursor.execute(query_trip, (route_id, service_id, trip_headsign, direction_id))
            trip_id = cursor.lastrowid 

            # Parse GeoJSON data y redondear coordenadas
            geojson_str = row['st_asgeojson']

            if not geojson_str:
                print(f"GeoJSON vacío para el ramal {ramal}...")
                continue  # Skip columna sin GeoJSON

            try:
                geojson_data = json.loads(geojson_str)
                rounded_coords = round_coords(geojson_data['coordinates'])
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error en el GeoJSON para ramal {ramal}: {e}...")
                continue  # Skip GeoJSON data inválido

            # arrival_time and departure_time por defecto a '06:00:00'
            for stop_sequence, coord in enumerate(rounded_coords, start=1):
                stop_lat, stop_lon = coord  # Extraer lat/lon from GeoJSON coordinates
                query_stop_time = '''
                INSERT INTO stop_time (trip_id, stop_id, arrival_time, departure_time, stop_sequence, stop_lat, stop_lon)
                VALUES (?, NULL, ?, ?, ?, ?, ?)
                '''
                cursor.execute(query_stop_time, (trip_id, '06:00:00', '06:00:00', stop_sequence, stop_lat, stop_lon))


# Cargar archivos CSV
paradas_df = pd.read_csv(paradas_csv)
recorridos_df = pd.read_csv(recorridos_csv)

# Conexión SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Cargar datos a la DB
load_paradas_to_stops(paradas_df, cursor)
load_recorridos_to_routes_trips(recorridos_df, cursor)

# Commit y cerrar connexión
conn.commit()
conn.close()

print("Se cargaron datos exitosamente.")