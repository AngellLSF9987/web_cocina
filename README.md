# Cocina Nova: Sistema de Gestión de Cocina

## Descripción

**Cocina Nova** 
    
    Es un sistema de gestión diseñado para pequeñas y medianas cocinas, que facilita la organización de clientes, trabajadores, productos y ventas. Este proyecto utiliza Flask para el backend, Jinja2 para plantillas, SQLite como base de datos y Bootstrap/CSS para el frontend.

---

## Estructura del Proyecto

web_cocina/ 
├── main.py# Archivo principal para comprobación desde terminal y testing.
├── app.py # Archivo principal para iniciar la aplicación Flask. 
├── database/ 
|   ├── __init__.py 
│   ├── cocina.db # Base de datos SQLite. 
│   ├── db_setup.py # Script para crear las tablas e insertar datos iniciales. 
|   └── db_connection.py # Script conexión base de datos. 
├── models/
|   ├── __init__.py
|   ├── carrito.py
|   ├── categoria.py
|   ├── cliente.py
|   ├── producto.py
|   ├── proveedor.py
|   ├── rol.py
|   ├── trabajador.py
|   └── venta.py 
├── controllers/
|   ├── __init__.py
|   └── auth_controllerpy # Controlador de acceso en función de rol de usuario, que tomará referencias de respositorio_cliente o repositorio_trabajador.
├── repositories/
|   ├── __init__.py
|   ├── repositorio_carrito.py
|   ├── repositorio_categoria.py
|   ├── repositorio_cliente.py
|   ├── repositorio_producto.py
|   ├── repositorio_proveedor.py
|   ├── repositorio_rol.py
|   ├── repositorio_trabajador.py
|   └── repositorio_venta.py
├── routes/ 
|   ├── __init__.py
|   └── routes.py # Script manejador de rutas. 
├── static/ 
│   |   ├── css/ 
|   |   |   ├── error.css # estilos templates manejadores de errores
│   |   |   └── styles.css # Estilos personalizados. 
│   |   ├── images/ # Recursos gráficos.
│   |   └── uploads/ # Recursos gráficos.  
├── templates/ 
│   ├── base.html # Plantilla base para el frontend. 
│   ├── index.html # Página de inicio. 
│   ├── auth/ # Plantillas relacionadas con autenticación. 
│   |──cliente/ # Plantillas para clientes.
│   |──trabajador/ # Plantillas para trabajadores.
│   |   ├── categoria/ # Plantillas para trabajador de Categoria.
|   |   ├── producto/ # Plantillas para trabajador de Producto.
|   |   ├── pedido/ # Plantillas para trabajador de Pedido.
│   |   └── proveedor/ # plantillas para trabajador de Pedido. 
│   ├── producto/ # Plantillas relacionadas con productos.
│   ├── privacidad/ # Plantillas relacionadas con privacidad y terminos y condiciones generales.
│   ├── proveedor/ # Plantillas relacionadas con productos. 
│   ├── error/ # Plantillas de páginas de error. 
│   └── shared/ # Componentes compartidos como navbar y footer. 
├── utilities/
|   ├── __init__.py
|   └── utilidades.py
├── requirements.txt # Dependencias necesarias. 
└── README.md # Documentación del proyecto.

---

## Instalación

### Requisitos Previos
- Python 3.10 o superior
- Virtualenv (opcional, recomendado)
- SQLite

### Pasos

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/usuario/CocinaNova.git
   cd CocinaNova

Crear un entorno virtual (opcional):


python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
Instalar dependencias:


pip install -r requirements.txt

Configurar la base de datos: Ejecuta el script db_setup.py para crear las tablas necesarias:


### Iniciar la aplicación:

### Descripción de Archivos y Directorios
1. app.py

    Archivo principal de la aplicación Flask. Define las rutas, inicializa la app y gestiona los endpoints principales.

Ejemplo de ruta en app.py:


@app.route('/')
def index():
    return render_template('index.html')

2. database/db_setup.py

    Script encargado de configurar la base de datos. Incluye la creación de tablas y restricciones para mantener la integridad de los datos.

Tablas creadas:

- Rol: Define los roles de usuario.
- Usuario: Almacena las credenciales y roles de los usuarios.
- Cliente: Registra información de los clientes.
- Trabajador: Información de los trabajadores.
- Proveedor: Registra datos de los proveedores.
- Categoria: Categorización de productos.
- Producto: Información de los productos.
- Venta: Gestión de ventas.
- Carrito: Relación entre ventas y productos.

3. templates/

    Directorio con las plantillas HTML. Usa Jinja2 para incrustar datos dinámicos y permite extender componentes comunes.

    ### Plantillas destacadas:
        - base.html: Plantilla base con navbar y footer.
        - index.html: Página principal.
        - auth/login.html: Formulario de inicio de sesión.

4. static/css/styles.css

    Archivo de estilos personalizados. Define los colores, fuentes y diseño general del sitio.

            Ejemplo de reglas CSS:

            css
            Copiar código
            body {
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }

            .navbar {
                background-color: #343a40;
                color: #fff;
            }

## Funcionalidades

### Clientes
### Registro, inicio de sesión y gestión de perfil.
### Historial de pedidos.
### Trabajadores
### Gestión de productos, pedidos y clientes.
### Administradores
### Configuración avanzada de roles y acceso.
### Tecnologías Usadas
### Backend: Flask, SQLite
### Frontend: Jinja2, Bootstrap, CSS
### Herramientas: Git, Virtualenv
### Próximos Pasos
### Mejorar la UI con más interactividad (JavaScript).
### Implementar autenticación avanzada (JWT o Flask-Login).
### Ampliar el sistema de reportes con gráficos y estadísticas.
### Contribuciones

## ¡Contribuciones son bienvenidas! Si deseas colaborar:

### Haz un fork del proyecto.
Crea una rama para tus cambios: git checkout -b feature/nueva-funcionalidad.

### Haz un pull request describiendo tus cambios.
Contacto
Para más información, contáctanos en:

Email: contacto@cocinanova.com
GitHub: https://github.com/usuario/CocinaNova
yaml
Copiar código

---

### **Siguientes pasos**

templates/
│
├── base.html  # Plantilla base común a todas las páginas
├── index.html  # Página principal del sitio
│
├── shared/  # Subdirectorio para componentes y plantillas compartidas
│   ├── header.html
│   ├── footer.html
│   ├── navbar.html
│   └── modal.html  # Otros componentes reutilizables
│
├── auth/  # Plantillas relacionadas con autenticación
│   ├── login.html
│   ├── reset_password.html
│   └── register.html  # Página de registro
│
├── cliente/  # Plantillas para el cliente
│   ├── cliente_dashboard.html
│   ├── cliente_perfil.html
│   └── cliente_pedidos.html
│   └── producto/  # Subdirectorio para templates de productos
│       ├── producto_lista.html
│       ├── producto_nuevo.html
│       ├── producto_editar.html
│       └── producto_detalle.html
│   └── categoria/  # Subdirectorio para templates de categorías
│       ├── categoria_lista.html
│       └── categoria_editar.html
│
├── error/  # Plantillas para errores de carga o innaccesibilidad
│   ├── 403.html
│   ├── 404.html
│   └── 500.html
│
├── privacidad/  # Plantillas para privacidad y términos y condiciones generales
│   ├── privacidad.html
│   └── terminos.html│    
│
├── servicios/  # Plantillas para servicios ofrecidos
│   └── servicios.html
│
├── trabajador/  # Plantillas para el trabajador
│   ├── trabajador_dashboard.html
│   ├── trabajador_gestion_clientes.html
│   ├── trabajador_gestion_productos.html
│   ├── trabajador_reportes.html
│   ├── trabajador_perfil.html
│   └── producto/  # Subdirectorio para templates de productos
│       ├── producto_lista.html
│       ├── producto_nuevo.html
│       ├── producto_editar.html
│       └── producto_detalle.html
│   └── categoria/  # Subdirectorio para templates de categorías
│       ├── categoria_lista.html
│       └── categoria_editar.html
│   └── proveedor/  # Subdirectorio para templates de proveedores
│       ├── proveedor_lista.html
│       ├── proveedor_nuevo.html
│       ├── proveedor_detalle.html
│       └── proveedor_editar.html
│
└── contacto/  # Plantillas para el formulario de contacto
    └── contacto.html


## 1. Templates compartidos
base.html:

 - Template base con el diseño principal del sitio.
 - Incluye el navbar y el footer mediante include.
 - Extendido por todos los demás templates.
 - Uso de Bootstrap para estructura y estilos básicos.
 - navbar.html:

    Barra de navegación responsiva con enlaces para clientes y trabajadores.
    Cambia dinámicamente dependiendo del tipo de usuario autenticado.

- footer.html:

    Información básica y enlaces a redes sociales.

- sidebar.html (opcional):

    Menú lateral para trabajadores o administradores con opciones de gestión.

## 2. Página de inicio

- index.html:

    Página principal del sitio.
    Botones para iniciar sesión, ver productos destacados y contacto.

## 3. Autenticación

- auth/login.html: Formulario para iniciar sesión.
- auth/register.html: Formulario de registro de clientes.
- auth/reset_password.html: Formulario para recuperar contraseña.

## 4. Panel de Cliente

- cliente/cliente_dashboard.html: Resumen de pedidos recientes y perfil.
- cliente/cliente_pedidos.html: Lista de pedidos realizados.
- cliente/cliente_perfil.html: Información y edición del perfil.

## 5. Panel de Trabajador

- trabajador/trabajador_dashboard.html: Vista general de órdenes pendientes y estadísticas.
- trabajador/trabajador_ordenes.html: Gestión de órdenes.
- trabajador/trabajador_perfil.html: Información y edición del perfil.

## 6. Productos

- producto/producto_lista.html: Lista de productos con paginación.
- producto/producto_detalle.html: Información detallada de un producto.
- producto/producto_busqueda.html: Resultados de búsqueda.

## 7. Páginas de error

- error/404.html: Página no encontrada.
- error/403.html: Acceso denegado.
- error/500.html: Error interno del servidor.

### **Siguientes pasos**

- Definir rutas en Flask: Configurar app.py para manejar cada template.
- Estilo con CSS: Crear un archivo styles.css en static/css/ para personalización.
- Bootstrap: Usar componentes como cards, forms, y modals para mejorar la UI.

Pasos para crear un requirements.txt

1. Instala las dependencias necesarias:

Asegúrate de que tienes instaladas todas las dependencias que necesitas. En este caso, al menos necesitas Flask y Flask-SQLAlchemy.

Ejecuta estos comandos en la terminal:


            pip install flask
            pip install flask_sqlalchemy

2. Genera el archivo requirements.txt:

Una vez que las dependencias estén instaladas en tu entorno virtual (o global, si no usas un entorno virtual), puedes generar el archivo requirements.txt con el siguiente comando:

            pip freeze > requirements.txt

Esto creará un archivo requirements.txt en tu directorio actual con todas las dependencias de tu proyecto.

El contenido de requirements.txt debería verse algo así:

        Flask==2.2.2
        Flask-SQLAlchemy==3.0.1

Puedes agregar más dependencias si es necesario.

3. Usar el archivo requirements.txt:

Para asegurarte de que las dependencias estén instaladas en otros entornos o si otras personas están trabajando en el proyecto, simplemente pueden ejecutar:

        pip install -r requirements.txt

Esto instalará todas las dependencias que aparecen en el archivo requirements.txt.