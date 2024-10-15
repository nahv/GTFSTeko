from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import Agency
from database import db 

agency_bp = Blueprint('agency', __name__, url_prefix='/agency')

@agency_bp.route('/cargar_agencia', methods=['GET', 'POST'])
def cargar_agencia():
    if request.method == 'POST':
        agency_name = request.form['agency_name']
        agency_url = request.form.get('agency_url')
        agency_timezone = request.form['agency_timezone']

        new_agency = Agency(
            agency_name=agency_name,
            agency_url=agency_url,
            agency_timezone=agency_timezone
        )
        db.session.add(new_agency)
        db.session.commit()
        flash('Agencia cargada con éxito.', 'success')
        return redirect(url_for('agency.cargar_agencia'))  # Correctly reference the endpoint

    agencies = Agency.query.all()
    return render_template('cargar_agencia.html', agencies=agencies)

@agency_bp.route('/delete_agency/<int:agency_id>', methods=['POST'])
def delete_agency(agency_id):
    agency = Agency.query.get(agency_id)
    if agency:
        db.session.delete(agency)
        db.session.commit()
        flash('Agencia eliminada con éxito.', 'success')
    else:
        flash('Agencia no encontrada.', 'danger')
    return redirect(url_for('agency.cargar_agencia'))

@agency_bp.route('/editar_agencia/', methods=['GET', 'POST'])
def editar_agencia(agency_id):
    # Fetch the agency by ID
    agency = Agency.query.get_or_404(agency_id)
    
    if request.method == 'POST':
        # Update agency details with form data
        agency.agency_name = request.form['agency_name']
        agency.agency_url = request.form.get('agency_url')
        agency.agency_timezone = request.form['agency_timezone']
        
        db.session.commit()
        flash('Agencia actualizada con éxito.', 'success')
        return redirect(url_for('agency.cargar_agencia'))  # Redirect after successful update

    return render_template('editar_agencia.html', agency=agency)
