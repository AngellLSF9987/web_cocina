from database.db_connection import ConexionDB
import mysql.connector

class RepositorioTrabajador:
    def __init__(self, conexion=None):
        """Recibe una conexión ya establecida o la crea."""
        self.conexion = conexion or ConexionDB()

    def obtener_todos_los_trabajadores(self):
        """Obtiene todos los trabajadores de la base de datos."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT Trabajador.id_trabajador, Trabajador.nombre_trabajador, Trabajador.apellido1, 
                    Trabajador.apellido2, Trabajador.dni_trabajador, Trabajador.telefono, 
                    Trabajador.direccion, Usuario.email, Usuario.fecha_registro, Rol.nombre_rol
                FROM Trabajador
                JOIN Usuario ON Trabajador.id_usuario = Usuario.id_usuario
                JOIN Rol ON Usuario.rol = Rol.nombre_rol
            """)
            trabajadores = cursor.fetchall()
            if not trabajadores:
                print("⚠️ No se encontraron trabajadores.")
            return trabajadores
        except Exception as e:
            print(f"❌ Error al obtener los trabajadores: {e}")
            return None
        finally:
            cursor.close()

    def obtener_trabajador_por_id(self, id_trabajador):
        """Obtiene un trabajador por su ID."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT Trabajador.id_trabajador, Trabajador.nombre_trabajador, Trabajador.apellido1, 
                    Trabajador.apellido2, Trabajador.dni_trabajador, Trabajador.telefono, 
                    Trabajador.direccion, Usuario.email, Usuario.fecha_registro, Rol.nombre_rol
                FROM Trabajador
                JOIN Usuario ON Trabajador.id_usuario = Usuario.id_usuario
                JOIN Rol ON Usuario.rol = Rol.nombre_rol
                WHERE Trabajador.id_trabajador = %s
            """, (id_trabajador,))
            trabajador = cursor.fetchone()
            if not trabajador:
                print(f"⚠️ No se encontró el trabajador con ID {id_trabajador}.")
            return trabajador
        except Exception as e:
            print(f"❌ Error al obtener el trabajador por ID: {e}")
            return None
        finally:
            cursor.close()

    def obtener_datos_trabajador(id_trabajador):
        """
        Consulta los datos de un trabajador en la base de datos.

        :param trabajador_id: ID del trabajador.
        :return: Diccionario con los datos del trabajador.
        """
        # Simula una consulta a la base de datos
        trabajador = {
            "id_trabajador": id_trabajador,
            "nombre_trabajador": "Luis Miguel",
            "email": "luis@trabajador.com",
        }
        return trabajador

def insertar_trabajador(self, nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion, email, contraseña, rol = "trabajador"):
    """Inserta un nuevo trabajador en la base de datos."""
    try:
        cursor = self.conexion.cursor()

        # Verificar si el email o el DNI ya existen
        cursor.execute("SELECT 1 FROM Usuario WHERE email = %s", (email,))
        if cursor.fetchone():
            print("⚠️ El email ya está registrado.")
            return

        cursor.execute("SELECT 1 FROM Trabajador WHERE dni_trabajador = %s", (dni_trabajador,))
        if cursor.fetchone():
            print("⚠️ El DNI ya está registrado.")
            return

        # Insertar en la tabla Usuario
        cursor.execute("""
            INSERT INTO Usuario (email, contraseña, rol)
            VALUES (%s, %s, %s)
        """, (email, contraseña, rol))  # Rol = 2 (suponiendo que este es el rol de trabajador)
        self.conexion.commit()

        # Obtener el id_usuario recién insertado
        id_usuario = cursor.lastrowid

        # Insertar en la tabla Trabajador
        cursor.execute("""
            INSERT INTO Trabajador (id_usuario, nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_usuario, nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion))
        self.conexion.commit()

        print(f"✔️ Trabajador '{nombre_trabajador} {apellido1}' insertado con éxito.")
    except Exception as e:
        print(f"❌ Error al insertar el trabajador: {e}")
        self.conexion.rollback()
    finally:
        cursor.close()

def actualizar_trabajador(self, id_trabajador, nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion, email, contraseña):
    """Actualiza la información de un trabajador existente."""
    try:
        cursor = self.conexion.cursor()

        # Verificar si el email o DNI ya existen para otro trabajador
        cursor.execute("""
            SELECT 1 
            FROM Usuario 
            WHERE email = %s AND id_usuario != (SELECT id_usuario FROM Trabajador WHERE id_trabajador = %s)
        """, (email, id_trabajador))
        if cursor.fetchone():
            print("⚠️ El email ya está registrado.")
            return

        cursor.execute("""
            SELECT 1 
            FROM Trabajador 
            WHERE dni_trabajador = %s AND id_trabajador != %s
        """, (dni_trabajador, id_trabajador))
        if cursor.fetchone():
            print("⚠️ El DNI ya está registrado.")
            return

        # Actualizar la tabla Usuario
        cursor.execute("""
            UPDATE Usuario 
            SET email = %s, contraseña = %s
            WHERE id_usuario = (SELECT id_usuario FROM Trabajador WHERE id_trabajador = %s)
        """, (email, contraseña, id_trabajador))

        # Actualizar la tabla Trabajador
        cursor.execute("""
            UPDATE Trabajador 
            SET nombre_trabajador = %s, apellido1 = %s, apellido2 = %s, dni_trabajador = %s, telefono = %s, direccion = %s
            WHERE id_trabajador = %s
        """, (nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion, id_trabajador))
        self.conexion.commit()

        print(f"✔️ Trabajador con ID {id_trabajador} actualizado con éxito.")
    except Exception as e:
        print(f"❌ Error al actualizar el trabajador: {e}")
        self.conexion.rollback()
    finally:
        cursor.close()

def eliminar_trabajador(self, id_trabajador):
    """Elimina un trabajador de la base de datos."""
    try:
        cursor = self.conexion.cursor()

        # Obtener el id_usuario asociado al trabajador
        cursor.execute("SELECT id_usuario FROM Trabajador WHERE id_trabajador = %s", (id_trabajador,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"⚠️ No se encontró ningún trabajador con ID {id_trabajador}.")
            return
        id_usuario = resultado[0]

        # Eliminar el registro en Trabajador
        cursor.execute("DELETE FROM Trabajador WHERE id_trabajador = %s", (id_trabajador,))
        # Eliminar el registro en Usuario
        cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id_usuario,))
        self.conexion.commit()

        print(f"✔️ Trabajador con ID {id_trabajador} eliminado con éxito.")
    except Exception as e:
        print(f"❌ Error al eliminar el trabajador: {e}")
        self.conexion.rollback()
    finally:
        cursor.close()

