from database.db_connection import ConexionDB
import mysql.connector

class RepositorioCliente:
    def __init__(self, conexion=None):
        """Recibe una conexión ya establecida o la crea."""
        self.conexion = conexion or ConexionDB()

    def obtener_todos_los_clientes(self):
        """Obtiene todos los clientes de la base de datos, incluyendo su rol."""
        try:
            cursor = self.conexion.cursor(dictionary=True)  # Usamos cursor de diccionario para facilitar el acceso
            cursor.execute("""
                SELECT Cliente.id_cliente, Cliente.nombre_cliente, Cliente.apellido1, 
                    Cliente.apellido2, Cliente.dni_cliente, Cliente.telefono, 
                    Cliente.direccion, Usuario.email, Usuario.fecha_registro, Rol.nombre_rol
                FROM Cliente
                JOIN Usuario ON Cliente.id_usuario = Usuario.id_usuario
                JOIN Rol ON Usuario.rol = Rol.nombre_rol
            """)
            clientes = cursor.fetchall()
            if not clientes:
                print("⚠️ No se encontraron clientes en la base de datos.")
            return clientes
        except Exception as e:
            print(f"❌ Error al obtener todos los clientes: {e}")
            return None
        finally:
            cursor.close()

    def obtener_cliente_por_id(self, id_cliente):
        """Obtiene un cliente por su ID, incluyendo su rol."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT Cliente.id_cliente, Cliente.nombre_cliente, Cliente.apellido1, 
                    Cliente.apellido2, Cliente.dni_cliente, Cliente.telefono, 
                    Cliente.direccion, Usuario.email, Usuario.fecha_registro, Rol.nombre_rol
                FROM Cliente
                JOIN Usuario ON Cliente.id_usuario = Usuario.id_usuario
                JOIN Rol ON Usuario.rol = Rol.nombre_rol
                WHERE Cliente.id_cliente = %s
            """, (id_cliente,))  # El parámetro 'id_cliente' se pasa como una tupla
            
            cliente = cursor.fetchone()
            
            if not cliente:
                print(f"⚠️ No se encontró ningún cliente con ID {id_cliente}.")
                return None
            
            return cliente
        
        except Exception as e:
            print(f"❌ Error al obtener el cliente por ID: {e}")
            return None
        finally:
            cursor.close()

    def obtener_datos_cliente(id_cliente):
        """
        Consulta los datos de un cliente en la base de datos.

        :param cliente_id: ID del cliente.
        :return: Diccionario con los datos del cliente.
        """
        # Simula una consulta a la base de datos
        cliente = {
            "id_cliente": id_cliente,
            "nombre_cliente": "Ángel Luis",
            "email": "angel@cliente.com",
        }
        return cliente


    def insertar_cliente(self, nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion, email, contraseña):
        """Inserta un nuevo cliente en la base de datos."""
        try:
            cursor = self.conexion.cursor()

            # Verificar si el email ya está registrado en la tabla Usuario
            cursor.execute("SELECT 1 FROM Usuario WHERE email = %s", (email,))
            if cursor.fetchone():
                print("⚠️ El email ya está registrado.")
                return

            # Verificar si el DNI ya está registrado en la tabla Cliente
            cursor.execute("SELECT 1 FROM Cliente WHERE dni_cliente = %s", (dni_cliente,))
            if cursor.fetchone():
                print("⚠️ El DNI ya está registrado.")
                return

            # Insertar un nuevo usuario en la tabla Usuario
            cursor.execute("""
                INSERT INTO Usuario (email, contraseña, id_rol)
                VALUES (%s, %s, 1)  -- 1 es el ID del rol 'Cliente'
            """, (email, contraseña))
            self.conexion.commit()

            # Obtener el id_usuario del nuevo usuario insertado
            id_usuario = cursor.lastrowid  # Devuelve el ID del último registro insertado

            # Insertar en la tabla Cliente usando el id_usuario generado
            cursor.execute("""
                INSERT INTO Cliente (id_usuario, nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (id_usuario, nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion))
            self.conexion.commit()

            print(f"✔️ Cliente '{nombre_cliente} {apellido1}' insertado con éxito.")
        except Exception as e:
            print(f"❌ Error al insertar el cliente: {e}")
        finally:
            cursor.close()

    def actualizar_cliente(self, id_cliente, nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion, email):
        """Actualiza la información de un cliente existente."""
        try:
            cursor = self.conexion.cursor()

            # Verificar si el email o el DNI ya están registrados en la tabla Usuario (excluyendo al cliente actual)
            cursor.execute("""
                SELECT 1 FROM Usuario 
                WHERE (email = %s) AND id_usuario != 
                (SELECT id_usuario FROM Cliente WHERE id_cliente = %s)
            """, (email, id_cliente))
            if cursor.fetchone():
                print("⚠️ El email ya está registrado para otro usuario.")
                return

            cursor.execute("""
                SELECT 1 FROM Cliente 
                WHERE (dni_cliente = %s) AND id_cliente != %s
            """, (dni_cliente, id_cliente))
            if cursor.fetchone():
                print("⚠️ El DNI ya está registrado para otro cliente.")
                return

            # Actualizar los datos del Usuario asociado al Cliente
            cursor.execute("""
                UPDATE Usuario 
                SET email = %s 
                WHERE id_usuario = (SELECT id_usuario FROM Cliente WHERE id_cliente = %s)
            """, (email, id_cliente))

            # Actualizar los datos en la tabla Cliente
            cursor.execute("""
                UPDATE Cliente 
                SET nombre_cliente = %s, apellido1 = %s, apellido2 = %s, dni_cliente = %s, 
                    telefono = %s, direccion = %s
                WHERE id_cliente = %s
            """, (nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion, id_cliente))

            if cursor.rowcount == 0:
                print(f"⚠️ No se encontró ningún cliente con ID {id_cliente} para actualizar.")
            else:
                self.conexion.commit()
                print(f"✔️ Cliente con ID {id_cliente} actualizado con éxito.")
        except Exception as e:
            print(f"❌ Error al actualizar el cliente: {e}")
        finally:
            cursor.close()

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente de la base de datos."""
        try:
            cursor = self.conexion.cursor()

            # Obtener el id_usuario asociado al cliente
            cursor.execute("SELECT id_usuario FROM Cliente WHERE id_cliente = %s", (id_cliente,))
            resultado = cursor.fetchone()
            if not resultado:
                print(f"⚠️ No se encontró ningún cliente con ID {id_cliente}.")
                return
            id_usuario = resultado[0]

            # Eliminar el cliente de la tabla Cliente
            cursor.execute("DELETE FROM Cliente WHERE id_cliente = %s", (id_cliente,))
            self.conexion.commit()

            # Eliminar el usuario asociado en la tabla Usuario
            cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id_usuario,))
            self.conexion.commit()

            print(f"✔️ Cliente con ID {id_cliente} y su usuario asociado eliminado con éxito.")
        except Exception as e:
            print(f"❌ Error al eliminar el cliente: {e}")
        finally:
            cursor.close()
