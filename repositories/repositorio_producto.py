from database.db_connection import ConexionDB
import mysql.connector
class RepositorioProducto:
    def __init__(self, conexion=None):
        """Recibe una conexión ya establecida o la crea."""
        self.conexion = conexion or ConexionDB()

    def obtener_producto_por_id(self, id_producto):
        """Obtiene un producto por su ID."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM Producto WHERE id_producto = ?", (id_producto,))
            producto = cursor.fetchone()
            if not producto:
                print(f"⚠️ No se encontró un producto con ID {id_producto}.")
            return producto
        except Exception as e:
            print(f"❌ Error al obtener el producto por ID: {e}")
        finally:
            cursor.close()

    def obtener_todos_los_productos(self):
        """Obtiene todos los productos."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM Producto")
            productos = cursor.fetchall()
            if not productos:
                print("⚠️ No se encontraron productos en la base de datos.")
            return productos
        except Exception as e:
            print(f"❌ Error al obtener los productos: {e}")
        finally:
            cursor.close()

    def insertar_producto(self, nombre_producto, descripcion, precio, imagen, stock, id_proveedor, id_categoria):
        """Inserta un nuevo producto."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                INSERT INTO Producto (nombre_producto, descripcion, precio, imagen, stock, id_proveedor, id_categoria)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nombre_producto, descripcion, precio, imagen, stock, id_proveedor, id_categoria))
            self.conexion.commit()
            print(f"✔️ Producto '{nombre_producto}' insertado con éxito.")
        except Exception as e:
            print(f"❌ Error al insertar el producto: {e}")
        finally:
            cursor.close()

    def actualizar_producto(self, id_producto, nombre_producto, descripcion, precio, imagen, stock, id_proveedor, id_categoria):
        """Actualiza los detalles de un producto existente."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                UPDATE Producto
                SET nombre_producto = ?, descripcion = ?, precio = ?, imagen = ?, stock = ?, id_proveedor = ?, id_categoria = ?
                WHERE id_producto = ?
            """, (nombre_producto, descripcion, precio, imagen, stock, id_proveedor, id_categoria, id_producto))
            self.conexion.commit()
            print(f"✔️ Producto con ID {id_producto} actualizado con éxito.")
        except Exception as e:
            print(f"❌ Error al actualizar el producto: {e}")
        finally:
            cursor.close()

    def eliminar_producto(self, id_producto):
        """Elimina un producto por su ID."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM Producto WHERE id_producto = ?", (id_producto,))
            self.conexion.commit()
            print(f"✔️ Producto con ID {id_producto} eliminado con éxito.")
        except Exception as e:
            print(f"❌ Error al eliminar el producto: {e}")
        finally:
            cursor.close()
