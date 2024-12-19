import os
from werkzeug.utils import secure_filename
from functools import wraps
from flask import (Blueprint, render_template, redirect, url_for, request, flash, session, 
                   current_app, g)
from controllers.auth_controller import autenticar_usuario
from controllers.categoria_controller import CategoriaController
from database.db_connection import ConexionDB
from models.categoria import Categoria
from repositories.repositorio_producto import RepositorioProducto
from repositories.repositorio_categoria import RepositorioCategoria
from repositories.repositorio_rol import RepositorioRol
from repositories.repositorio_cliente import RepositorioCliente
from repositories.repositorio_proveedor import RepositorioProveedor
from repositories.repositorio_usuario import RepositorioUsuario
# from repositories.repositorio_trabajador import RepositorioTrabajador
from config import Config
import logging

# Instanciar logger
logger = logging.getLogger(__name__)

# Blueprint
routes = Blueprint("routes", __name__)

# Instancia de ConexionDB
db = ConexionDB()

# Repositorios
repo_producto = RepositorioProducto(db)
repo_categoria = RepositorioCategoria(db)
repo_cliente = RepositorioCliente(db)
repo_proveedor = RepositorioProveedor(db)
repo_usuario = RepositorioUsuario(db)
# repo_trabajador = RepositorioTrabajador(db)
repo_rol = RepositorioRol(db)

# Decoradores de autenticación y roles combinados
def access_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_role" not in session:
                flash("Por favor, inicia sesión.", "warning")
                return redirect(url_for("routes.login"))
            if role and session.get("user_role") != role:
                logger.warning(f"Acceso denegado. Rol requerido: {role}")
                flash("No tienes permisos para acceder a esta página.", "danger")
                return redirect(url_for("routes.index"))
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Seguridad para archivos subidos
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rutas
def role_redirect(role):
    role_map = {
        "autenticado": "routes.index",
        "trabajador": "routes.index"
    }
    return role_map.get(role, "routes.index")

@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Ingresa tu correo y contraseña.", "warning")
            return render_template("auth/login.html")

        # Usa la función autenticar_usuario del controlador
        usuario = autenticar_usuario(email, password)
        if usuario:
            try:
                # Intentamos obtener el nombre del rol de forma segura
                nombre_rol = usuario.get("rol")  # Usamos .get() para evitar KeyError

                if not nombre_rol:  # Si no encontramos nombre_rol
                    flash("Error al obtener el rol del usuario.", "danger")
                    logger.error(f"Error al obtener 'nombre_rol' para el usuario: {email}")
                    return redirect(url_for("routes.index"))  # Redirigir a la página de error

                # Si encontramos el nombre_rol, lo usamos en la sesión
                session["user_role"] = nombre_rol.lower()
                session["user_email"] = email
                logger.info(f"Rol del usuario en sesión: {session['user_role']}")
                logger.debug(f"Sesión actual: {session}")  # Agregado para inspeccionar la sesión
                return redirect(url_for(role_redirect(nombre_rol.lower())))  # Redirigir según el rol
            except Exception as e:
                # Capturamos cualquier otro error inesperado
                flash("Hubo un error al procesar tu solicitud.", "danger")
                logger.error(f"Error inesperado al procesar el login para {email}: {e}")
                return redirect(url_for("routes.index"))  # Redirigir a la página de error
        else:
            flash("Credenciales incorrectas.", "danger")
            logger.warning(f"Inicio fallido: {email}")
    return render_template("auth/login.html")


@routes.route("/logout")
@access_required()
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("routes.index"))

@routes.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    # Lógica para el restablecimiento de la contraseña
    return render_template('auth/reset_password.html')


@routes.route("/")
def index():
    return render_template("index.html")

# Rutas para cliente

@routes.route('/cliente/pedidos')
@access_required(role="autenticado")
def cliente_pedidos():
    return render_template('cliente/cliente_pedidos.html')

# Rutas para trabajador

@routes.route('/cliente/gestion_clientes')
@access_required(role="autenticado")
def gestion_clientes():
    return render_template('cliente/gestion_clientes.html')

@routes.route('/cliente/producto/gestion_productos')
@access_required(role="autenticado")
def gestion_productos():
    return render_template('cliente/gestion_productos.html')

@routes.route('/cliente/reportes')
@access_required(role="autenticado")
def reportes():
    return render_template('cliente/cliente_reportes.html')

# Rutas CRUD Producto - Cliente

@routes.route("/cliente/producto/lista")
@access_required(role="autenticado")
def cliente_lista_productos():
    try:
        productos = repo_producto.obtener_todos_los_productos()
        return render_template('cliente/producto/producto_lista.html', productos=productos)
    except Exception as e:
        logger.exception("Error al obtener la lista de productos.")
        flash("Error al cargar productos.", "error")
        return redirect(url_for("routes.index"))

@routes.route("/cliente/producto/nuevo", methods=["GET", "POST"])
@access_required(role="autenticado")
def cliente_nuevo_producto():
    categorias = repo_categoria.obtener_todas_las_categorias()
    if request.method == "POST":
        try:
            nombre = request.form["nombre_producto"]
            descripcion = request.form["descripcion"]
            precio = request.form["precio"]
            imagen = request.files["imagen"] if "imagen" in request.files else None

            if imagen and allowed_file(imagen.filename):
                filename = secure_filename(imagen.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                imagen.save(filepath)
            else:
                flash("Formato de imagen no permitido.", "error")
                return redirect(request.url)

            repo_producto.insertar_producto(nombre, descripcion, precio, filename)
            flash("Producto creado exitosamente.", "success")
            return redirect(url_for("routes.cliente_lista_productos"))
        except Exception as e:
            logger.exception("Error al crear un producto.")
            flash("Error al crear producto.", "error")
    return render_template('cliente/producto/producto_nuevo.html', categorias=categorias)

@routes.route("/cliente/producto/eliminar/<int:id_producto>", methods=["POST"])
@access_required(role="autenticado")
def cliente_eliminar_producto(id_producto):
    try:
        repo_producto.eliminar_producto(id_producto)
        flash("Producto eliminado exitosamente.", "success")
    except Exception as e:
        logger.exception("Error al eliminar el producto.")
        flash("No se pudo eliminar el producto.", "error")
    return redirect(url_for("routes.cliente_lista_productos"))


# Rutas CRUD Categoria - Cliente

@routes.route("/cliente/categoria/lista")
@access_required(role="autenticado")
def cliente_lista_categorias():
    try:
        categorias = repo_categoria.obtener_todas_las_categorias()
        return render_template('cliente/categoria/cliente_categoria_lista.html', categorias=categorias)
    except Exception as e:
        logger.exception("Error al obtener la lista de categorías.")
        flash("Error al cargar categorías.", "error")
        return redirect(url_for("routes.index"))

@routes.route("/cliente/categoria/nueva", methods=["POST"])
@access_required(role="autenticado")
def nueva_categoria():
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        imagen = request.files.get('imagen')
        CategoriaController.crear_categoria(nombre, descripcion, imagen)
        flash('Categoría creada exitosamente.', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    except Exception as e:
        logger.exception("Error al crear categoría.")
        flash("Error al crear categoría.", 'error')
    return redirect(url_for('routes.cliente_lista_categorias'))

# Ruta de contacto
@routes.route('/contacto/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre_cliente = request.form['nombre_cliente']
        dni_cliente = request.form['dni_cliente']
        email = request.form['email']
        asunto = request.form['asunto']
        mensaje = request.form['mensaje']
        
        # Procesar los datos (enviar un correo, guardar en base de datos, etc.)
        
        flash("Gracias por ponerte en contacto. Te responderemos pronto.", "success")
        return redirect(url_for('routes.contacto'))  # Redirigir al mismo formulario o a otra página de agradecimiento
    return render_template('contacto/contacto.html')

# Ruta de privacidad, términos y servicios
@routes.route('/privacidad')
def privacidad():
    return render_template('/privacidad/privacidad.html')

@routes.route('/terminos')
def terminos():
    return render_template('/privacidad/terminos.html')

@routes.route("/servicios")
def servicio():
    return render_template("servicios/servicios.html")

# Manejo de errores
@routes.app_errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404

@routes.app_errorhandler(403)
def forbidden(e):
    return render_template("error/403.html"), 403

@routes.errorhandler(500)
def internal_error(error):
    logger.error(f"Error interno: {error}")
    return "Ocurrió un error en el servidor", 500
