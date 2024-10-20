from flask import Flask, render_template
from routes.agency_routes import agency_bp
from routes.route_routes import route_bp
from routes.stop_routes import stop_bp
from routes.recorrido_routes import gtfs_bp
from routes.importar_csv_routes import csv_bp
from routes.export_gtfs_routes import export_gtfs_bp
from database import init_db
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "transporte.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

app.register_blueprint(agency_bp)
app.register_blueprint(route_bp)
app.register_blueprint(stop_bp)
app.register_blueprint(gtfs_bp)
app.register_blueprint(csv_bp)
app.register_blueprint(export_gtfs_bp)

# index.html
@app.route('/')
def index():
    return render_template('index.html')

# App
if __name__ == '__main__':
    app.run(debug=True, port=5001)