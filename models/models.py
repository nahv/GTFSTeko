from database import db

class Agency(db.Model):
    agency_id = db.Column(db.Integer, primary_key=True)
    agency_name = db.Column(db.String(80), nullable=False)
    agency_url = db.Column(db.String(200))
    agency_timezone = db.Column(db.String(80), nullable=False)

class Route(db.Model):
    route_id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.agency_id'), nullable=False)
    route_short_name = db.Column(db.String(10), nullable=False)
    route_long_name = db.Column(db.String(100), nullable=False)
    route_type = db.Column(db.Integer, nullable=False)
    route_color = db.Column(db.String(6))

class Stop(db.Model):
    stop_id = db.Column(db.Integer, primary_key=True)
    stop_name = db.Column(db.String(100), nullable=False)
    stop_lat = db.Column(db.Float, nullable=False)
    stop_lon = db.Column(db.Float, nullable=False)
    stop_location = db.Column(db.String(100))

class Calendar(db.Model):
    service_id = db.Column(db.Integer, primary_key=True)
    monday = db.Column(db.Integer)
    tuesday = db.Column(db.Integer)
    wednesday = db.Column(db.Integer)
    thursday = db.Column(db.Integer)
    friday = db.Column(db.Integer)
    saturday = db.Column(db.Integer)
    sunday = db.Column(db.Integer)
    start_date = db.Column(db.String(8))
    end_date = db.Column(db.String(8))

class Trip(db.Model):
    trip_id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.route_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('calendar.service_id'), nullable=False)
    trip_headsign = db.Column(db.String(100))

class StopTime(db.Model):
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'), primary_key=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stop.stop_id'), primary_key=True)
    arrival_time = db.Column(db.String(8), nullable=False)
    departure_time = db.Column(db.String(8), nullable=False)
    stop_sequence = db.Column(db.Integer, nullable=False)

class Shape(db.Model):
    shape_id = db.Column(db.Integer, primary_key=True)
    shape_pt_lat = db.Column(db.Float, nullable=False)
    shape_pt_lon = db.Column(db.Float, nullable=False)
    shape_pt_sequence = db.Column(db.Integer, nullable=False)