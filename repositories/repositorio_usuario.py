# repositorio_usuario.py

from repositories.repositorio_rol import RepositorioRol
from database.db_connection import ConexionDB
import mysql.connector

class RepositorioUsuario:
    def __init__(self, conexion=None):
        """Recibe una conexión ya establecida o la crea."""
        self.conexion = conexion or ConexionDB()
        self.repositorio_rol = RepositorioRol(self.conexion)  # Inicializamos el repositorio de roles

    def autenticar_usuario(self, email, password):
        """Autentica a un usuario y devuelve sus datos, incluido su rol, si las credenciales son correctas."""
        try:
            cursor = self.conexion.cursor(dictionary=True)  # Cursor que devuelve resultados como diccionarios
            print(f"🔍 Buscando usuario con email: {email}")

            # Consulta para obtener usuario y su id_rol
            query = """
                SELECT id_usuario, email, contraseña, rol
                FROM Usuario
                WHERE email = %s
            """
            cursor.execute(query, (email,))
            usuario = cursor.fetchone()

            if usuario:
                print(f"🔑 Usuario encontrado: {usuario}")
                if usuario.get("contraseña") == password:  # Usamos get() para evitar KeyError si la clave no existe
                    print(f"✅ Contraseña correcta para el usuario: {email}")
                    # Obtenemos el nombre del rol usando el repositorio de roles
                    nombre_rol = self.repositorio_rol.obtener_rol_por_nombre_rol(usuario["rol"])
                    if nombre_rol:
                        return {
                            "id_usuario": usuario["id_usuario"],
                            "email": usuario["email"],
                            "rol": usuario["rol"],
                            # "nombre_rol": nombre_rol
                        }
                    else:
                        print(f"❌ No se pudo obtener el nombre del rol para el usuario: {email}")
                        return None
                else:
                    print(f"❌ Contraseña incorrecta para el usuario: {email}")
            else:
                print(f"❌ Usuario no encontrado con email: {email}")

            return None
        except Exception as e:
            print(f"❌ Error al autenticar al usuario: {e}")
            return None
        finally:
            cursor.close()  # Solo se cierra el cursor, no la conexión
