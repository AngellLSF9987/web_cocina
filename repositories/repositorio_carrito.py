from models.carrito import Carrito
import mysql.connector
from database.db_connection import ConexionDB

class RepositorioCarrito:
    def __init__(self, conexion=None):
        """Recibe una conexión ya establecida o la crea."""
        self.conexion = conexion or ConexionDB()

    def obtener_conexion(self):
        """Obtiene la conexión a la base de datos."""
        return self.conexion

    def crear_carrito(self, id_venta, id_cliente, id_producto, cantidad=1, precio_total=1.00):
        """Crea un nuevo carrito en la base de datos."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""INSERT INTO Carrito (id_venta, id_cliente, id_producto, cantidad, precio_total)
                              VALUES (%s, %s, %s, %s, %s)""", 
                           (id_venta, id_cliente, id_producto, cantidad, precio_total))
            self.conexion.commit()
            print(f"✔️ Carrito creado para Cliente {id_cliente} y Producto {id_producto}.")
        except mysql.connector.Error as err:
            print(f"⚠️ Error al crear el carrito: {err}")
        finally:
            cursor.close()

    def obtener_carrito_por_id(self, id_carrito):
        """Obtiene un carrito específico por id_carrito."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM Carrito WHERE id_carrito = %s", (id_carrito,))
            carrito = cursor.fetchone()
            if carrito:
                print(f"✔️ Carrito encontrado: {carrito}")
                return Carrito(*carrito)  # Devolver un objeto Carrito
            else:
                print(f"⚠️ No se encontró el carrito con id {id_carrito}.")
                return None
        except mysql.connector.Error as err:
            print(f"⚠️ Error al obtener el carrito: {err}")
        finally:
            cursor.close()

    def actualizar_carrito(self, id_carrito, cantidad=None, precio_total=None):
        """Actualiza el carrito con nuevos valores (cantidad y precio_total)."""
        try:
            cursor = self.conexion.cursor()
            if cantidad:
                cursor.execute("UPDATE Carrito SET cantidad = %s WHERE id_carrito = %s", (cantidad, id_carrito))
            if precio_total:
                cursor.execute("UPDATE Carrito SET precio_total = %s WHERE id_carrito = %s", (precio_total, id_carrito))
            self.conexion.commit()
            print(f"✔️ Carrito con ID {id_carrito} actualizado.")
        except mysql.connector.Error as err:
            print(f"⚠️ Error al actualizar el carrito: {err}")
        finally:
            cursor.close()

    def eliminar_carrito(self, id_carrito):
        """Elimina el carrito con el id especificado."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM Carrito WHERE id_carrito = %s", (id_carrito,))
            self.conexion.commit()
            print(f"✔️ Carrito con ID {id_carrito} eliminado.")
        except mysql.connector.Error as err:
            print(f"⚠️ Error al eliminar el carrito: {err}")
        finally:
            cursor.close()

    def obtener_carritos_cliente(self, id_cliente):
        """Obtiene todos los carritos de un cliente específico."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM Carrito WHERE id_cliente = %s", (id_cliente,))
            carritos = cursor.fetchall()
            if carritos:
                print(f"✔️ Carritos encontrados para Cliente {id_cliente}:")
                return [Carrito(*carrito) for carrito in carritos]  # Devolver lista de objetos Carrito
            else:
                print(f"⚠️ No se encontraron carritos para Cliente {id_cliente}.")
                return []
        except mysql.connector.Error as err:
            print(f"⚠️ Error al obtener los carritos: {err}")
        finally:
            cursor.close()
