from flask import g, Flask
import mysql.connector
import logging
from config import Config

app = Flask(__name__)

def crear_conexion(config=Config.MYSQL_CONFIG):
    if 'conexion' not in g:  # Si no existe una conexión en g, la creamos
        logger = logging.getLogger(__name__)  # Usar logger en lugar de print()
        try:
            g.conexion = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                autocommit=True  # Aseguramos que las operaciones como CREATE DATABASE se ejecuten inmediatamente
            )
            logger.info(f"Conectado a MySQL en {config['host']} con la base de datos {config['database']}.")
        except mysql.connector.Error as e:
            logger.error(f"Error al conectar con MySQL: {e}")
            raise
    return g.conexion

# Usamos context manager para cerrar la conexión al final de la solicitud
@app.teardown_appcontext
def cerrar_conexion(error=None):
    if hasattr(g, 'conexion') and g.conexion.is_connected():
        g.conexion.close()
        logger = logging.getLogger(__name__)
        logger.info("Conexión cerrada correctamente.")
