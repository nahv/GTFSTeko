
CREATE TABLE agency (
    agency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agency_name TEXT NOT NULL,
    agency_url TEXT,
    agency_timezone TEXT NOT NULL,
    agency_phone TEXT
);
	
CREATE TABLE route (
    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agency_id INTEGER NOT NULL,
    route_short_name TEXT NOT NULL,
    route_long_name TEXT NOT NULL,
    route_type INTEGER NOT NULL,  -- 3 para buses (según GTFS)
    route_color TEXT,  -- Código de color opcional
    FOREIGN KEY (agency_id) REFERENCES agency(agency_id)
);

CREATE TABLE stop (
    stop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stop_name TEXT NOT NULL,
    stop_lat REAL NOT NULL,  -- Latitud
    stop_lon REAL NOT NULL,  -- Longitud
    stop_desc TEXT  -- Dirección o descripción de la parada
);

CREATE TABLE calendar (  -- 1 para operativo, 0 para no
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    monday INTEGER, 
    tuesday INTEGER,
    wednesday INTEGER,
    thursday INTEGER,
    friday INTEGER,
    saturday INTEGER,
    sunday INTEGER,
    start_date TEXT,  -- Fecha de inicio del servicio (AAAAMMDD)
    end_date TEXT  -- Fecha de fin del servicio (AAAAMMDD)	
);

CREATE TABLE trip (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,  -- Servicio (días de operación)
    trip_headsign TEXT,  -- Dirección del viaje
    FOREIGN KEY (route_id) REFERENCES route(route_id),
    FOREIGN KEY (service_id) REFERENCES calendar(service_id)
);

CREATE TABLE stop_time (
    trip_id INTEGER NOT NULL,
    stop_id INTEGER NOT NULL,
    arrival_time TEXT NOT NULL,  -- Hora de llegada (HH:MM:SS)
    departure_time TEXT NOT NULL,  -- Hora de salida (HH:MM:SS)
    stop_sequence INTEGER NOT NULL,  -- Orden de las paradas en el viaje
    PRIMARY KEY (trip_id, stop_sequence),
    FOREIGN KEY (trip_id) REFERENCES trip(trip_id),
    FOREIGN KEY (stop_id) REFERENCES stop(stop_id)
);