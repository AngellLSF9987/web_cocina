# cocina/main.py
import os
from database.db_connection import ConexionDB
from database.db_setup import inicializar_base_datos, crear_tablas, insertar_datos_ejemplo

def test_db():
    """
    Realiza pruebas de creación de tablas e inserción de datos de ejemplo.
    """
    db_path = os.path.join(os.getcwd(), "database", "cocina.db")

    with ConexionDB(ruta_bd=db_path) as conexion:

        # Crear tablas
        crear_tablas(conexion)
        
        # Insertar datos de ejemplo
        insertar_datos_ejemplo(conexion)

        print("\nPruebas de base de datos completadas con éxito.")

if __name__ == "__main__":
    print("\n=== Bienvenid@ Cocina_Nova ===\n")

    # Ruta relativa a la base de datos
    db_path = os.path.join(
        os.getcwd(),  # Directorio actual
        "database",  # Subdirectorio donde está la base de datos
        "cocina.db"  # Nombre del archivo de la base de datos
    )

    # Inicializar la base de datos (crear tablas e insertar datos de ejemplo)
    inicializar_base_datos(db_path)

    # Realizar pruebas de la base de datos (opcional)
    ejecutar_test = input("\u00bfDeseas ejecutar las pruebas de la base de datos? (s/n): ").strip().lower()
    if ejecutar_test == 's':
        test_db()
    
    print("\nPrograma terminado.")
