from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import Stop  # Make sure to import your Stop model
from database import db

stop_bp = Blueprint('stop', __name__, url_prefix='/stop')

@stop_bp.route('/cargar_stops', methods=['GET', 'POST'])
def cargar_stops():
    if request.method == 'POST':
        stop_name = request.form['stop_name']
        stop_lat = request.form['stop_lat']
        stop_lon = request.form['stop_lon']
        stop_desc = request.form['stop_desc']

        new_stop = Stop(
            stop_name=stop_name,
            stop_lat=stop_lat,
            stop_lon=stop_lon,
            stop_desc=stop_desc
        )
        db.session.add(new_stop)
        db.session.commit()
        flash('Parada cargada con éxito.', 'success')
        return redirect(url_for('stop.cargar_stops'))

    stops = Stop.query.all()  # Fetch stops for the table
    return render_template('cargar_stops.html', stops=stops)

@stop_bp.route('/delete_stop/<int:stop_id>', methods=['POST'])
def delete_stop(stop_id):
    stop = Stop.query.get(stop_id)
    if stop:
        db.session.delete(stop)
        db.session.commit()
        flash('Parada eliminada con éxito.', 'success')
    else:
        flash('Parada no encontrada.', 'danger')
    return redirect(url_for('stop.cargar_stops'))

@stop_bp.route('/editar_stop', methods=['POST'])
def editar_stop():
    stop_id = request.form['stop_id']
    stop = Stop.query.get_or_404(stop_id)
    return render_template('editar_stop.html', stop=stop)

@stop_bp.route('/guardar_stop/<int:stop_id>', methods=['POST'])
def guardar_stop(stop_id):
    stop = Stop.query.get_or_404(stop_id)
    
    stop.stop_name = request.form['stop_name']
    stop.stop_lat = request.form['stop_lat']
    stop.stop_lon = request.form['stop_lon']
    stop.stop_desc = request.form['stop_desc']

    db.session.commit()
    flash('Parada actualizada con éxito.', 'success')
    return redirect(url_for('stop.cargar_stops'))
