from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import Stop
from database import db
from flask_paginate import Pagination, get_page_parameter

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

    # Pagination setup
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10  # Set the number of items per page
    stops = Stop.query.paginate(page=page, per_page=per_page)

    pagination = Pagination(page=page, total=stops.total, search=False, record_name='stops', per_page=per_page)

    # Calculate the page range on the server side
    start_page = max(1, pagination.page - 2)
    end_page = min(pagination.page + 3, stops.pages + 1)

    return render_template(
        'cargar_stops.html',
        stops=stops.items,
        pagination=pagination,
        total_pages=stops.pages,
        start_page=start_page,
        end_page=end_page
    )


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
