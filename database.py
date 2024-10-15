from flask_sqlalchemy import SQLAlchemy

# Instancia global de la base de datos
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crea todas las tablas