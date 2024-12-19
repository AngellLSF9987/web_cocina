# repositorio_rol.py

from database.db_connection import ConexionDB
import mysql.connector

class RepositorioRol:
    def __init__(self, conexion=None):
        """Recibe una conexión ya establecida o la crea."""
        self.conexion = conexion or ConexionDB()

    def obtener_rol_por_nombre_rol(self, nombre_rol):
        """Obtiene el nombre del rol a partir de su ID."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = "SELECT nombre_rol FROM Rol WHERE nombre_rol = %s"
            cursor.execute(query, (nombre_rol,))
            rol = cursor.fetchone()
            if rol:
                return rol["nombre_rol"]
            else:
                return None
        except Exception as e:
            print(f"❌ Error al obtener rol: {e}")
            return None
