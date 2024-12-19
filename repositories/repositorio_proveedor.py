from database.db_connection import ConexionDB
import mysql.connector
class RepositorioProveedor:
    def __init__(self, conexion=None):
        """Recibe una conexión ya establecida o la crea."""
        self.conexion = conexion or ConexionDB()

    def obtener_todos_los_proveedores(self):
        """Obtiene todos los proveedores."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM proveedores")
            proveedores = cursor.fetchall()
            if not proveedores:
                print("⚠️ No se encontraron proveedores.")
            return proveedores
        except Exception as e:
            print(f"❌ Error al obtener los proveedores: {e}")
        finally:
            cursor.close()

    def obtener_proveedor_por_id(self, id_proveedor):
        """Obtiene un proveedor por su ID."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM proveedores WHERE id_proveedor = ?", (id_proveedor,))
            proveedor = cursor.fetchone()
            if not proveedor:
                print(f"⚠️ No se encontró el proveedor con ID {id_proveedor}.")
            return proveedor
        except Exception as e:
            print(f"❌ Error al obtener el proveedor por ID: {e}")
        finally:
            cursor.close()

    def insertar_proveedor(self, nombre, direccion, telefono, email):
        """Inserta un nuevo proveedor."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("INSERT INTO proveedores (nombre, direccion, telefono, email) VALUES (?, ?, ?, ?)",
                           (nombre, direccion, telefono, email))
            self.conexion.commit()
            print(f"✔️ Proveedor '{nombre}' insertado con éxito.")
        except Exception as e:
            print(f"❌ Error al insertar el proveedor: {e}")
        finally:
            cursor.close()

    def actualizar_proveedor(self, id_proveedor, nombre, direccion, telefono, email):
        """Actualiza los detalles de un proveedor existente."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("UPDATE proveedores SET nombre = ?, direccion = ?, telefono = ?, email = ? WHERE id_proveedor = ?",
                           (nombre, direccion, telefono, email, id_proveedor))
            if cursor.rowcount == 0:
                print(f"⚠️ No se encontró ningún proveedor con ID {id_proveedor} para actualizar.")
            else:
                self.conexion.commit()
                print(f"✔️ Proveedor con ID {id_proveedor} actualizado con éxito.")
        except Exception as e:
            print(f"❌ Error al actualizar el proveedor: {e}")
        finally:
            cursor.close()

    def eliminar_proveedor(self, id_proveedor):
        """Elimina un proveedor por su ID."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM proveedores WHERE id_proveedor = ?", (id_proveedor,))
            if cursor.rowcount == 0:
                print(f"⚠️ No se encontró ningún proveedor con ID {id_proveedor} para eliminar.")
            else:
                self.conexion.commit()
                print(f"✔️ Proveedor con ID {id_proveedor} eliminado con éxito.")
        except Exception as e:
            print(f"❌ Error al eliminar el proveedor: {e}")
        finally:
            cursor.close()
