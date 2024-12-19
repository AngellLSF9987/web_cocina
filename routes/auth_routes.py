import os
from werkzeug.utils import secure_filename
from functools import wraps
from flask import (Blueprint, render_template, redirect, url_for, request, flash, session, 
                   current_app, g)
from controllers.auth_controller import autenticar_usuario
from database.db_connection import ConexionDB
from repositories.repositorio_rol import RepositorioRol
from repositories.repositorio_cliente import RepositorioCliente
from repositories.repositorio_usuario import RepositorioUsuario
from config import Config
import logging

# Instanciar logger
logger = logging.getLogger(__name__)

# Blueprint
auth_routes = Blueprint("auth_routes", __name__)

# Instancia de ConexionDB
db = ConexionDB()

# Repositorios

repo_cliente = RepositorioCliente(db)
repo_usuario = RepositorioUsuario(db)
repo_rol = RepositorioRol(db)

# Decoradores de autenticación y roles combinados
def access_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_role" not in session:
                flash("Por favor, inicia sesión.", "warning")
                return redirect(url_for("auth_routes.login"))
            if role and session.get("user_role") != role:
                logger.warning(f"Acceso denegado. Rol requerido: {role}")
                flash("No tienes permisos para acceder a esta página.", "danger")
                return redirect(url_for("auth_routes.login"))
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Mapeo de roles para redirecciones
def role_redirect(role):
    role_map = {
        "autenticado": "auth_routes.login",  # Aquí puedes ajustar según la lógica real
        "trabajador": "auth_routes.login"   # Esto también
    }
    return role_map.get(role, "auth_routes.login")

# Ruta de login
@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Ingresa tu correo y contraseña.", "warning")
            return render_template("auth/login.html")

        usuario = autenticar_usuario(email, password)
        if usuario:
            try:
                nombre_rol = usuario.get("rol")
                if not nombre_rol:
                    flash("Error al obtener el rol del usuario.", "danger")
                    logger.error(f"Error al obtener 'nombre_rol' para el usuario: {email}")
                    return redirect(url_for("auth_routes.login"))

                session["user_role"] = nombre_rol.lower()
                session["user_email"] = email
                logger.info(f"Rol del usuario en sesión: {session['user_role']}")
                return redirect(url_for(role_redirect(nombre_rol.lower())))
            except Exception as e:
                flash("Hubo un error al procesar tu solicitud.", "danger")
                logger.error(f"Error inesperado al procesar el login para {email}: {e}")
                return redirect(url_for("auth_routes.login"))
        else:
            flash("Credenciales incorrectas.", "danger")
            logger.warning(f"Inicio fallido: {email}")
    return render_template("auth/login.html")

# Ruta de logout
@auth_routes.route("/logout")
@access_required()
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("auth_routes.login"))

# Ruta de reset password
@auth_routes.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    # Lógica para el restablecimiento de la contraseña
    return render_template('auth/reset_password.html')
