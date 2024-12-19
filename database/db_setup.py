from config import Config  # Importación la configuración desde config.py
from database.db_connection import ConexionDB  # Importación la clase de conexión a la base de datosctor
from mysql.connector import Error

def crear_tablas(conexion):
    """
    Crea las tablas necesarias para la base de datos de Cocina.
    """
    cursor = conexion.cursor()
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

# ,
#                 FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)

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

        # Tabla Pedido
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pedido (
                id_pedido INT AUTO_INCREMENT PRIMARY KEY,
                fecha_pedido DATE DEFAULT CURRENT_DATE,
                estado ENUM('enviado', 'pendiente', 'recibido') NOT NULL,
                total DECIMAL(10, 2) NOT NULL,
                id_cliente INT,
                FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
            );
        """)

        # Tabla Pedido_Producto
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pedido_Producto (
                id_pedido_producto INT AUTO_INCREMENT PRIMARY KEY,
                id_pedido INT,
                id_producto INT,
                FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido),
                FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
            );
        """)

        # Tabla Venta
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Venta (
                id_venta INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE DEFAULT CURRENT_DATE,
                id_cliente INT NOT NULL,
                total DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
            );
        """)

        # Tabla intermedia Carrito con FOREIGN KEY
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Carrito (
                id_carrito INT AUTO_INCREMENT PRIMARY KEY,
                id_venta INT NOT NULL,
                id_producto INT NOT NULL,
                id_cliente INT NOT NULL,
                cantidad INT NOT NULL,
                precio_total DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (id_venta) REFERENCES Venta(id_venta),
                FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
                FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
                CONSTRAINT UCAR_Carrito UNIQUE (id_carrito, id_venta, id_producto, id_cliente)
            );
        """)

        # Datos iniciales para Roles
        cursor.execute("INSERT IGNORE INTO Rol (nombre_rol) VALUES ('autenticado');")
        cursor.execute("INSERT IGNORE INTO Rol (nombre_rol) VALUES ('trabajador');")
        print("Roles 'cliente' y 'trabajador' insertados correctamente.")
        conexion.commit()
        print("Tablas creadas exitosamente y datos iniciales añadidos.")
    except Error as e:
        print(f"Error al crear las tablas: {e}")
        conexion.rollback()

def insertar_datos_ejemplo(conexion):
    """
    Inserta datos de ejemplo en las tablas para pruebas iniciales,
    verificando que no haya duplicados.
    """
    cursor = conexion.cursor()

    try:
        # Insertar usuarios en la tabla Usuario
        datos_usuario = [
            ("paco@nava.com", "paco123", "autenticado"),  # (email, contraseña, id_rol)
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

        # Insertar clientes en la tabla Cliente
        datos_clientes = [
            ("paco@nava.com", "Paco", "Nava", "Gomez", "12345678A", "600123456", "Calle Luna, 6"),
            ("angel@saorin.com", "Angel Luis", "Saorin", "Martinez", "12345678C", "610654321", "Calle Sol, 8"),
        ]
        for email, nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion in datos_clientes:
            cursor.execute("SELECT id_usuario FROM Usuario WHERE email = %s", (email,))
            resultado = cursor.fetchone()
            if resultado:
                id_usuario = resultado[0]
                # Verificar si el id_usuario ya existe en la tabla Cliente
                cursor.execute("SELECT 1 FROM Cliente WHERE id_usuario = %s", (id_usuario,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO Cliente (id_usuario, nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (id_usuario, nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion))
                    print(f"✔️ Cliente {nombre_cliente} ({email}) insertado.")
                else:
                    print(f"⚠️ Cliente con email {email} ya existe en Cliente.")
            else:
                print(f"⚠️ Usuario con email {email} no encontrado.")

        # Insertar trabajadores en la tabla Trabajador
        datos_trabajadores = [
            ("paco@trabajador.com", "Paco", "Lopez", "Garcia", "12345678D", "620987654", "Calle Estrella, 10"),
            ("angel@trabajador.com", "Angel", "Martinez", "Perez", "12345678F", "630456789", "Calle Cometa, 12"),
        ]
        for email, nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion in datos_trabajadores:
            cursor.execute("SELECT id_usuario FROM Usuario WHERE email = %s", (email,))
            resultado = cursor.fetchone()
            if resultado:
                id_usuario = resultado[0]
                # Verificar si el id_usuario ya existe en la tabla Trabajador
                cursor.execute("SELECT 1 FROM Trabajador WHERE id_usuario = %s", (id_usuario,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO Trabajador (id_usuario, nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (id_usuario, nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion))
                    print(f"✔️ Trabajador {nombre_trabajador} ({email}) insertado.")
                else:
                    print(f"⚠️ Trabajador con email {email} ya existe en Trabajador.")
            else:
                print(f"⚠️ Usuario con email {email} no encontrado.")

        # Confirmar cambios en la base de datos
        conexion.commit()
        print("✅ Datos insertados exitosamente.")
    
    except Error as e:
        print(f"❌ Error al insertar datos: {e}")
        conexion.rollback()


def inicializar_base_datos(conexion):
    try:
        # Asegúrate de pasar los parámetros correctos de configuración
        # with ConexionDB(
        #     host=Config.MYSQL_CONFIG['host'],
        #     user=Config.MYSQL_CONFIG['user'],
        #     password=Config.MYSQL_CONFIG['password'],
        #     database=Config.MYSQL_CONFIG['database']
        # ) as conexion:
        with ConexionDB() as conexion:
            # Crear las tablas necesarias
            crear_tablas(conexion)
        
            # Insertar datos de ejemplo
            insertar_datos_ejemplo(conexion)

    except Error as e:
        print(f"Error al inicializar la base de datos: {e}")