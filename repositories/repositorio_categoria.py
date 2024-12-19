from database.db_connection import ConexionDB
import mysql.connector
class RepositorioCategoria:
    def __init__(self, conexion=None):
        """Recibe una conexión ya establecida o la crea."""
        self.conexion = conexion or ConexionDB()

    def obtener_categoria_por_id(self, id_categoria):
        """Obtiene una categoría por su ID."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM Categoria WHERE id_categoria = ?", (id_categoria,))
            categoria = cursor.fetchone()
            if not categoria:
                print(f"⚠️ No se encontró ninguna categoría con ID {id_categoria}.")
            return categoria
        except Exception as e:
            print(f"❌ Error al obtener la categoría por ID: {e}")
        finally:
            cursor.close()

    def obtener_todas_las_categorias(self):
        """Obtiene todas las categorías."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM Categoria")
            categorias = cursor.fetchall()
            if not categorias:
                print("⚠️ No hay categorías registradas.")
            return categorias
        except Exception as e:
            print(f"❌ Error al obtener las categorías: {e}")
        finally:
            cursor.close()

    def insertar_categoria(self, nombre_categoria, descripcion, imagen):
        """Inserta una nueva categoría."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                INSERT INTO Categoria (nombre_categoria, descripcion, imagen)
                VALUES (?, ?, ?)
            """, (nombre_categoria, descripcion, imagen))
            self.conexion.commit()
            print(f"✔️ Categoría '{nombre_categoria}' insertada con éxito.")
        except Exception as e:
            print(f"❌ Error al insertar la categoría: {e}")
        finally:
            cursor.close()

    def actualizar_categoria(self, id_categoria, nombre_categoria, descripcion, imagen):
        """Actualiza los detalles de una categoría existente."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                UPDATE Categoria
                SET nombre_categoria = ?, descripcion = ?, imagen = ?
                WHERE id_categoria = ?
            """, (nombre_categoria, descripcion, imagen, id_categoria))
            if cursor.rowcount == 0:
                print(f"⚠️ No se encontró ninguna categoría con ID {id_categoria} para actualizar.")
            else:
                self.conexion.commit()
                print(f"✔️ Categoría con ID {id_categoria} actualizada con éxito.")
        except Exception as e:
            print(f"❌ Error al actualizar la categoría: {e}")
        finally:
            cursor.close()

    def eliminar_categoria(self, id_categoria):
        """Elimina una categoría por su ID."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM Categoria WHERE id_categoria = ?", (id_categoria,))
            if cursor.rowcount == 0:
                print(f"⚠️ No se encontró ninguna categoría con ID {id_categoria} para eliminar.")
            else:
                self.conexion.commit()
                print(f"✔️ Categoría con ID {id_categoria} eliminada con éxito.")
        except Exception as e:
            print(f"❌ Error al eliminar la categoría: {e}")
        finally:
            cursor.close()