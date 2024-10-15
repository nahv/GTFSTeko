from flask import Flask, render_template
from routes.agency_routes import agency_bp
from routes.calendar_routes import calendar_bp
from routes.route_routes import route_bp
from routes.shapes_routes import shapes_bp
from routes.stop_routes import stop_bp
from routes.stoptime_routes import stoptimes_bp
from routes.trip_routes import trips_bp
from database import init_db
import os

app = Flask(__name__)

app.secret_key = os.urandom(24) 

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "transporte.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: to suppress warnings

init_db(app)

app.register_blueprint(agency_bp)
app.register_blueprint(calendar_bp)
app.register_blueprint(route_bp)
app.register_blueprint(shapes_bp)
app.register_blueprint(stop_bp)
app.register_blueprint(stoptimes_bp)
app.register_blueprint(trips_bp)

# index.html
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)