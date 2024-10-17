import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
import pandas as pd

# Define the blueprint
csv_bp = Blueprint('csv_bp', __name__)

# Directory where the files will be saved
DATASET_FOLDER = os.path.join(os.getcwd(), 'datasets')

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
            paradas_path = os.path.join(DATASET_FOLDER, 'paradas.csv')
            paradas_file.save(paradas_path)
        elif paradas_file:
            flash('El archivo de Paradas debe ser un CSV', 'danger')
            return redirect(url_for('csv_bp.importar_csv'))

        # Process Recorridos file
        if recorridos_file and recorridos_file.filename.endswith('.csv'):
            recorridos_path = os.path.join(DATASET_FOLDER, 'recorridos.csv')
            recorridos_file.save(recorridos_path)
        elif recorridos_file:
            flash('El archivo de Recorridos debe ser un CSV', 'danger')
            return redirect(url_for('csv_bp.importar_csv'))

        # If at least one file is uploaded successfully
        if paradas_file or recorridos_file:
            flash('Archivos importados correctamente', 'success')
        else:
            flash('Cargar al menos un archivo CSV', 'warning')

        return redirect(url_for('csv_bp.importar_csv'))

    return render_template('importar_csv.html')
