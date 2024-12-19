from flask import g
from mysql.connector import Error
from database.db_connection import ConexionDB  # Asegúrate de que la clase ConexionDB se ajuste a esta implementación
from config import Config

def crear_tablas():
    """
    Crea las tablas necesarias para la base de datos de Cocina.
    """
    cursor = g.conexion.cursor()
    try:
        # Tabla Roles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rol (
                nombre_rol VARCHAR(255) UNIQUE NOT NULL
            );
        """)

        # Tabla Usuario (solo información de login)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                contraseña VARCHAR(255) NOT NULL,
                fecha_registro DATE DEFAULT CURRENT_DATE,
                rol VARCHAR(255)
            );
        """)

        # Tabla Cliente (información adicional)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cliente (
                id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL UNIQUE,
                nombre_cliente VARCHAR(255) NOT NULL,
                apellido1 VARCHAR(255) NOT NULL,
                apellido2 VARCHAR(255) NOT NULL,
                dni_cliente VARCHAR(255) UNIQUE NOT NULL,
                telefono VARCHAR(255),
                direccion VARCHAR(255),
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
            );
        """)

        # Tabla Trabajador (información adicional)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Trabajador (
                id_trabajador INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL UNIQUE,
                nombre_trabajador VARCHAR(255) NOT NULL,
                apellido1 VARCHAR(255) NOT NULL,
                apellido2 VARCHAR(255) NOT NULL,
                dni_trabajador VARCHAR(255) UNIQUE NOT NULL,
                telefono VARCHAR(255),
                direccion VARCHAR(255),
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
            );
        """)

        # Tabla Proveedor con restricción UNIQUE en correo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Proveedor (
                id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
                nombre_proveedor VARCHAR(255) NOT NULL,
                nombre_empresa VARCHAR(255) NOT NULL,
                telefono VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                CONSTRAINT UP_Proveedor UNIQUE (nombre_proveedor, nombre_empresa, email, telefono)
            );
        """)

        # Tabla Categorías
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Categoria (
                id_categoria INT AUTO_INCREMENT PRIMARY KEY,
                nombre_categoria VARCHAR(255) NOT NULL UNIQUE,
                descripcion TEXT,
                imagen TEXT,
                CONSTRAINT UCAT_Categoria UNIQUE (id_categoria, nombre_categoria)
            );
        """)

        # Tabla Producto con FOREIGN KEY
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Producto (
                id_producto INT AUTO_INCREMENT PRIMARY KEY,
                nombre_producto VARCHAR(255) NOT NULL UNIQUE,
                descripcion TEXT,
                precio DECIMAL(10, 2) NOT NULL,
                imagen TEXT,
                stock INT NOT NULL,
                id_proveedor INT,
                id_categoria INT,
                FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor),
                FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria),
                CONSTRAINT UPROD_Producto UNIQUE (id_producto, id_proveedor, id_categoria)
            );
        """)

        # Resto de las tablas...

        # Datos iniciales para Roles
        cursor.execute("INSERT IGNORE INTO Rol (nombre_rol) VALUES ('autenticado');")
        cursor.execute("INSERT IGNORE INTO Rol (nombre_rol) VALUES ('trabajador');")
        g.conexion.commit()
        print("Tablas creadas exitosamente y datos iniciales añadidos.")
    except Error as e:
        g.conexion.rollback()
        print(f"Error al crear las tablas: {e}")

def insertar_datos_ejemplo():
    """
    Inserta datos de ejemplo en las tablas para pruebas iniciales,
    verificando que no haya duplicados.
    """
    cursor = g.conexion.cursor()

    try:
        # Insertar usuarios en la tabla Usuario
        datos_usuario = [
            ("paco@nava.com", "paco123", "autenticado"),  # (email, contraseña, rol)
            ("angel@saorin.com", "angel123", "autenticado"),
            ("paco@trabajador.com", "paco456", "trabajador"),
            ("angel@trabajador.com", "angel456", "trabajador"),
        ]

        for email, contraseña, rol in datos_usuario:
            cursor.execute("SELECT 1 FROM Usuario WHERE email = %s", (email,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO Usuario (email, contraseña, rol)
                    VALUES (%s, %s, %s);
                """, (email, contraseña, rol))
                print(f"✔️ Usuario {email} insertado.")
            else:
                print(f"⚠️ Usuario con email {email} ya existe, no se insertó.")

        # Insertar datos de clientes, trabajadores, etc.

        # Confirmar cambios en la base de datos
        g.conexion.commit()
        print("Datos insertados exitosamente.")
    
    except Error as e:
        g.conexion.rollback()
        print(f"Error al insertar datos: {e}")

def inicializar_base_datos():
    try:
        # Conexión desde g
        with ConexionDB() as conexion:
            g.conexion = conexion  # Guardamos la conexión en g
            crear_tablas()
            insertar_datos_ejemplo()

    except Error as e:
        print(f"Error al inicializar la base de datos: {e}")
