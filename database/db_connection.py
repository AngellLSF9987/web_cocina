# import mysql.connector
# import logging

# class ConexionDB:
#     def __init__(self, host="localhost", user="angelpaco", password="angelpaco", database="cocina_db"):
#         self.host = host
#         self.user = user
#         self.password = password
#         self.database = database
#         self.conexion = None
#         self.logger = logging.getLogger(__name__)  # Usar logger en lugar de print()

#     def __enter__(self):
#         try:
#             self.logger.info(f"Conectando a MySQL en {self.host}...")
#             # Conectar sin especificar la base de datos inicialmente
#             self.conexion = mysql.connector.connect(
#                 host=self.host,
#                 user=self.user,
#                 password=self.password,
#                 autocommit=True  # Aseguramos que las operaciones como CREATE DATABASE se ejecuten inmediatamente
#             )
#             cursor = self.conexion.cursor()

#             # Intentar usar la base de datos especificada
#             cursor.execute(f"USE {self.database}")
#             self.logger.info(f"Conexión establecida con la base de datos '{self.database}'.")
#             return self.conexion  # Devolver la conexión para su uso
#         except mysql.connector.Error as e:
#             if e.errno == 1049:  # Error: Base de datos desconocida
#                 self.logger.warning(f"La base de datos '{self.database}' no existe. Creándola...")
#                 cursor.execute(f"CREATE DATABASE {self.database}")
#                 self.conexion.database = self.database
#                 self.logger.info(f"Base de datos '{self.database}' creada y seleccionada.")
#                 return self.conexion
#             else:
#                 self.logger.error(f"Error al conectar con MySQL: {e}")
#                 raise
#         finally:
#             cursor.close()  # Aseguramos de cerrar el cursor al final

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.conexion and self.conexion.is_connected():
#             try:
#                 self.conexion.close()
#                 self.logger.info("Conexión cerrada correctamente.")
#             except mysql.connector.Error as e:
#                 self.logger.error(f"Error al cerrar la conexión: {e}")
#         else:
#             self.logger.warning("La conexión no está abierta o ya se ha cerrado.")


import mysql.connector
import logging
from config import Config  # Importamos la configuración

class ConexionDB:
    def __init__(self, config=Config.MYSQL_CONFIG):
        self.config = config
        self.conexion = None
        self.logger = logging.getLogger(__name__)  # Usar logger en lugar de print()

    def __enter__(self):
        try:
            self.logger.info(f"Conectando a MySQL en {self.config['host']}...")
            # Conectar sin especificar la base de datos inicialmente
            self.conexion = mysql.connector.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"],
                autocommit=True  # Aseguramos que las operaciones como CREATE DATABASE se ejecuten inmediatamente
            )
            cursor = self.conexion.cursor()

            # Intentar usar la base de datos especificada
            cursor.execute(f"USE {self.config['database']}")
            self.logger.info(f"Conexión establecida con la base de datos '{self.config['database']}'.")
            return self.conexion  # Devolver la conexión para su uso
        except mysql.connector.Error as e:
            if e.errno == 1049:  # Error: Base de datos desconocida
                self.logger.warning(f"La base de datos '{self.config['database']}' no existe. Creándola...")
                cursor.execute(f"CREATE DATABASE {self.config['database']}")
                self.conexion.database = self.config['database']
                self.logger.info(f"Base de datos '{self.config['database']}' creada y seleccionada.")
                return self.conexion
            else:
                self.logger.error(f"Error al conectar con MySQL: {e}")
                raise
        finally:
            cursor.close()  # Aseguramos de cerrar el cursor al final

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conexion and self.conexion.is_connected():
            try:
                self.conexion.close()
                self.logger.info("Conexión cerrada correctamente.")
            except mysql.connector.Error as e:
                self.logger.error(f"Error al cerrar la conexión: {e}")
        else:
            self.logger.warning("La conexión no está abierta o ya se ha cerrado.")
