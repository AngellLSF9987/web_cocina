# Decoradores de autenticación y roles combinados
# def access_required(role=None):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             if "user_role" not in session:
#                 flash("Por favor, inicia sesión.", "warning")
#                 return redirect(url_for("routes.login"))
#             if role and session.get("user_role") != role:
#                 logger.warning(f"Acceso denegado. Rol requerido: {role}")
#                 flash("No tienes permisos para acceder a esta página.", "danger")
#                 return redirect(url_for("routes.index"))
#             return f(*args, **kwargs)
#         return wrapper
#     return decorator

# # Seguridad para archivos subidos
# ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # Rutas
# def role_redirect(role):
#     role_map = {
#         "autenticado": "routes.index",
#         "trabajador": "routes.index"
#     }
#     return role_map.get(role, "routes.index")

# @routes.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")

#         if not email or not password:
#             flash("Ingresa tu correo y contraseña.", "warning")
#             return render_template("auth/login.html")

#         # Usa la función autenticar_usuario del controlador
#         usuario = autenticar_usuario(email, password)
#         if usuario:
#             try:
#                 # Intentamos obtener el nombre del rol de forma segura
#                 nombre_rol = usuario.get("rol")  # Usamos .get() para evitar KeyError

#                 if not nombre_rol:  # Si no encontramos nombre_rol
#                     flash("Error al obtener el rol del usuario.", "danger")
#                     logger.error(f"Error al obtener 'nombre_rol' para el usuario: {email}")
#                     return redirect(url_for("routes.index"))  # Redirigir a la página de error

#                 # Si encontramos el nombre_rol, lo usamos en la sesión
#                 session["user_role"] = nombre_rol.lower()
#                 session["user_email"] = email
#                 logger.info(f"Rol del usuario en sesión: {session['user_role']}")
#                 logger.debug(f"Sesión actual: {session}")  # Agregado para inspeccionar la sesión
#                 return redirect(url_for(role_redirect(nombre_rol.lower())))  # Redirigir según el rol
#             except Exception as e:
#                 # Capturamos cualquier otro error inesperado
#                 flash("Hubo un error al procesar tu solicitud.", "danger")
#                 logger.error(f"Error inesperado al procesar el login para {email}: {e}")
#                 return redirect(url_for("routes.index"))  # Redirigir a la página de error
#         else:
#             flash("Credenciales incorrectas.", "danger")
#             logger.warning(f"Inicio fallido: {email}")
#     return render_template("auth/login.html")


# @routes.route("/logout")
# @access_required()
# def logout():
#     session.clear()
#     flash("Has cerrado sesión.", "info")
#     return redirect(url_for("routes.index"))

# @routes.route('/reset_password', methods=['GET', 'POST'])
# def reset_password():
#     # Lógica para el restablecimiento de la contraseña
#     return render_template('auth/reset_password.html')