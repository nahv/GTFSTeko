# GTFSTekó 🚍🌍

Esto es un proyecto de aprendizaje en el marco del Dathaton 2024 de la Cumbre de Datos <https://www.cumbrededatos.ar/>.

GTFSTekó es una herramienta para producir, mantener y exportar datos sobre el transporte público de la ciudad de Corrientes al formato GTFS (General Transit Feed Specification). Se integran en una base de datos sqlite para luego exportarlos en el estandar global.

## Objetivo 🎯

Generar y mantener actualizados datos de transporte público que puedan ser utilizados en servicios como Google Maps o Apple Maps.

## Stack 🛠️

- **SQLite**
- **Flask**
- **Bootstrap**

## Estructura del Proyecto 📁

GTFSTeko/
├── routes/             # rutas
├── templates/          # templates
├── models/             # modelos de AlchemySQL (schema)
├── instance/           # Acá va la base de datos "transporte.db", database.py la crea si no existe
├── app.py              # Corre la app
├── database.py         # lógica para inicializar la db
├── datasets/           # Acá se guardan los csv que se suben para procesar
└── gtfs_exports/       # Acá se guardan los GTFS una vez procesados para descargar

## Probar 🚀

1. **Cloná el repositorio**:
```
   git clone <https://github.com/nahv/GTFSTeko>
```
2. **Navega a la carpeta del proyecto**:
```
cd GTFSTeko
```
3. **Asegurate de tener Python3 con las siguientes dependencias**:
```
pip install Flask pandas flask-paginate
```
4. **Iniciala con:**
```
python3 app.py
```
Y luego abrir en el servidor local <http://127.0.0.1:5001/>
Por defecto corre en el puerto 5001; de ser necesario ajustar en app.py

## Contribuciones 🤝

Las contribuciones son bienvenidas.