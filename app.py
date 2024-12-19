import os
import sys
import logging
import mysql.connector
from flask import Flask
from controllers.categoria_controller import categoria_bp
from routes.auth_routes import auth_routes
from routes.routes import routes
from config import Config
from database.db_connection import ConexionDB  # Importación ConexionDB
from database.db_setup import inicializar_base_datos  # Importación la función de configuración de base de datos

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

    # Registrar el blueprint de autenticación
    app.register_blueprint(categoria_bp, url_prefix='/categoria')
    app.register_blueprint(auth_routes, url_prefix="/auth")

    # Cargar configuración
    app.config.from_object(Config)
    logger.info("Configuración de Flask cargada correctamente.")

    # Si tienes otro blueprint para las rutas generales, regístralo también
    app.register_blueprint(routes)
    logger.info("Blueprints registrados correctamente.")
    # Intentar conectar a la base de datos
    try:
        # db_config = Config.MYSQL_CONFIG
        db_config = {
            "host": "localhost",
            "user": "angelpaco",
            "password": "angelpaco",
            "database": "cocina_db"
        }

        logger.info(f"Configuración de conexión: {db_config}")
        logger.debug(f"db_config: {db_config}")  # Esto te permitirá ver si los valores son correctos

        # Establecer la conexión con la base de datos
        # with ConexionDB(db_config['host'], db_config['user'], db_config['password'], db_config['database']) as conexion:
        with ConexionDB() as conexion:
            logger.info("Conexión establecida con la base de datos.")
            # Inicializar la base de datos si es necesario
            inicializar_base_datos(conexion)

    except mysql.connector.Error as db_error:
        logger.error(f"Error de MySQL: {db_error}")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")

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
