# GTFSTekó 🚍🌍

Esto es un proyecto de aprendizaje en el marco del Dathaton 2024 de la Cumbre de Datos <https://www.cumbrededatos.ar/>.

GTFSTekó es una herramienta para producir, mantener y exportar datos sobre el transporte público de la ciudad de Corrientes al formato GTFS (General Transit Feed Specification). <br>
Los datos se integran en una db sqlite para luego exportarlos en el estandar global.

## Objetivo

Generar y mantener actualizados datos de transporte público para que puedan ser utilizados en servicios como Google Maps o Apple Maps.

## Stack 🛠️

- **SQLite**
- **Flask**
- **Bootstrap**

## Estructura del Proyecto 📁

GTFSTeko/ <br>
├── routes/             # rutas <br>
├── templates/          # templates <br>
├── models/             # modelos de AlchemySQL (schema) <br>
├── instance/           # Acá va la base de datos "transporte.db", database.py la crea si no existe <br>
├── app.py              # Corre la app <br>
├── database.py         # lógica para inicializar la db <br>
├── datasets/           # Acá se guardan los csv que se suben para procesar <br>
└── gtfs_exports/       # Acá se guardan los GTFS una vez procesados para descargar <br>


## Probar 🚀

1. **Cloná el repositorio**:
```
   git clone <https://github.com/nahv/GTFSTeko>
```
2. **Navegá a la carpeta del proyecto**:
```
cd GTFSTeko
```
3. **Asegurate de tener Python3 con las siguientes dependencias**:
```
pip install Flask pandas flask-paginate SQLAlchemy Flask-SQLAlchemy
```
4. **Iniciar con:**
```
python3 app.py
```
5. **Abrir en tu servidor local <http://127.0.0.1:5001/><br><br>Por defecto corre en el puerto 5001; de ser necesario ajustar en app.py**

## Contribuciones 🤝

Las contribuciones son bienvenidas.