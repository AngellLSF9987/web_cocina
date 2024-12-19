import logging
from database.db_connection import ConexionDB
from mysql.connector import Error as MySQL_Error

class RepositorioCategoria:
    def __init__(self, conexion=None):
        """Recibe una conexión ya establecida o la crea."""
        self.conexion = conexion or ConexionDB()
        self.logger = logging.getLogger(__name__)  # Usar logger para los mensajes

    def obtener_categoria_por_id(self, id_categoria):
        """Obtiene una categoría por su ID."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM Categoria WHERE id_categoria = %s", (id_categoria,))
            categoria = cursor.fetchone()
            if not categoria:
                self.logger.warning(f"No se encontró ninguna categoría con ID {id_categoria}.")
            return categoria
        except MySQL_Error as e:
            self.logger.error(f"Error en la consulta MySQL: {e}")
        except Exception as e:
            self.logger.error(f"Error general: {e}")
        finally:
            cursor.close()

    def obtener_todas_las_categorias(self):
        """Obtiene todas las categorías."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM Categoria")
            categorias = cursor.fetchall()
            if not categorias:
                self.logger.warning("No hay categorías registradas.")
            return categorias
        except MySQL_Error as e:
            self.logger.error(f"Error en la consulta MySQL: {e}")
        except Exception as e:
            self.logger.error(f"Error general: {e}")
        finally:
            cursor.close()

    def insertar_categoria(self, nombre_categoria, descripcion, imagen):
        """Inserta una nueva categoría."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                INSERT INTO Categoria (nombre_categoria, descripcion, imagen)
                VALUES (%s, %s, %s)
            """, (nombre_categoria, descripcion, imagen))
            self.conexion.commit()
            self.logger.info(f"Categoría '{nombre_categoria}' insertada con éxito.")
        except MySQL_Error as e:
            self.logger.error(f"Error en la consulta MySQL: {e}")
        except Exception as e:
            self.logger.error(f"Error general: {e}")
        finally:
            cursor.close()

    def actualizar_categoria(self, id_categoria, nombre_categoria, descripcion, imagen):
        """Actualiza los detalles de una categoría existente."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                UPDATE Categoria
                SET nombre_categoria = %s, descripcion = %s, imagen = %s
                WHERE id_categoria = %s
            """, (nombre_categoria, descripcion, imagen, id_categoria))
            if cursor.rowcount == 0:
                self.logger.warning(f"No se encontró ninguna categoría con ID {id_categoria} para actualizar.")
            else:
                self.conexion.commit()
                self.logger.info(f"Categoría con ID {id_categoria} actualizada con éxito.")
        except MySQL_Error as e:
            self.logger.error(f"Error en la consulta MySQL: {e}")
        except Exception as e:
            self.logger.error(f"Error general: {e}")
        finally:
            cursor.close()

    def eliminar_categoria(self, id_categoria):
        """Elimina una categoría por su ID."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM Categoria WHERE id_categoria = %s", (id_categoria,))
            if cursor.rowcount == 0:
                self.logger.warning(f"No se encontró ninguna categoría con ID {id_categoria} para eliminar.")
            else:
                self.conexion.commit()
                self.logger.info(f"Categoría con ID {id_categoria} eliminada con éxito.")
        except MySQL_Error as e:
            self.logger.error(f"Error en la consulta MySQL: {e}")
        except Exception as e:
            self.logger.error(f"Error general: {e}")
        finally:
            cursor.close()
