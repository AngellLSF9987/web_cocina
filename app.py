import os
import sys
import logging
from flask import Flask, g
from controllers.categoria_controller import categoria_bp
from routes.auth_routes import auth_routes
from routes.routes import routes
from config import Config
from database.db_connection import ConexionDB  # Importación ConexionDB
from database.db_setup import inicializar_base_datos  # Importación de la función de configuración de base de datos
from database.db_connection import cerrar_conexion  # Importación para cerrar la conexión

# Configuración del logger
def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,  # Nivel de log
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Mostrar logs en consola
            logging.FileHandler("web_cocina.log", mode='a', encoding='utf-8')  # Guardar logs en archivo
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger()

# Configuración de la aplicación Flask
def create_app():
    app = Flask(__name__, static_folder='static')

    # Cargar configuración
    app.config.from_object(Config)
    logger.info("Configuración de Flask cargada correctamente.")

    # Registrar blueprints
    app.register_blueprint(categoria_bp, url_prefix='/categoria')
    app.register_blueprint(auth_routes, url_prefix="/auth")    
    app.register_blueprint(routes)
    logger.info("Blueprints registrados correctamente.")

    # Definir un "before_request" para crear la conexión
    @app.before_request
    def cargar_conexion():
        """Se ejecuta antes de cada solicitud para crear la conexión"""
        logger.debug("Estableciendo la conexión con la base de datos...")
        from database.db_connection import crear_conexion  # Importamos la función de conexión
        g.conexion = crear_conexion()  # Usamos g para manejar la conexión

        # Inicializar la base de datos si es necesario
        try:
            inicializar_base_datos(g.conexion)
            logger.info("Base de datos inicializada correctamente.")
        except Exception as e:
            logger.error(f"Error al inicializar la base de datos: {e}")

    # Definir un "teardown_request" para cerrar la conexión después de cada solicitud
    @app.teardown_request
    def cerrar(error=None):
        """Se ejecuta después de cada solicitud para cerrar la conexión."""
        logger.debug("Cerrando la conexión a la base de datos...")
        from database.db_connection import cerrar_conexion  # Llamamos a la función de cierre de conexión
        cerrar_conexion()  # Llamamos a la función que cierra la conexión de la base de datos

    return app

# Ejecutar la aplicación
if __name__ == "__main__":
    try:
        # Agregar el directorio raíz al PYTHONPATH (soluciona posibles problemas de importación)
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        logger.debug("Directorio raíz añadido al PYTHONPATH.")

        # Crear la aplicación Flask
        app = create_app()

        if app is not None:
            # Ejecutar el servidor Flask
            logger.info("Iniciando el servidor Flask en modo debug...")
            app.run(debug=True)
        else:
            logger.error("La aplicación Flask no se pudo crear.")
    except Exception as e:
        logger.exception("Error crítico al iniciar la aplicación Flask:")

