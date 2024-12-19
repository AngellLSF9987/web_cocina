# auth_controller.py

from repositories.repositorio_cliente import RepositorioCliente
from repositories.repositorio_trabajador import RepositorioTrabajador
from repositories.repositorio_usuario import RepositorioUsuario
from database.db_connection import ConexionDB

def autenticar_usuario(email, password):
    """Autentica a un usuario como cliente, trabajador o usuario general."""
    try:
        # Establecer conexión con la base de datos
        with ConexionDB() as conexion:  # Usamos un 'with' para asegurar la conexión
            repositorio_usuario = RepositorioUsuario(conexion)
            print(f"🔍 Intentando autenticar al usuario con email: {email}")

            # Llamada al repositorio para obtener el usuario y su rol
            usuario = repositorio_usuario.autenticar_usuario(email, password)

            if usuario:
                print(f"✅ Usuario autenticado: {usuario}")
                # Aseguramos que estamos extrayendo 'nombre_rol' de forma correcta
                nombre_rol = usuario.get("rol")  # Devuelve None si no existe
                if nombre_rol:
                    print(f"🔑 Rol del usuario: {nombre_rol}")  # Añadimos depuración aquí

                    # Verificar el rol y retornar los datos correspondientes
                    if nombre_rol.lower() == "autenticado":
                        repositorio_cliente = RepositorioCliente(conexion)
                        print(f"🔍 Obteniendo cliente con ID: {usuario['id_usuario']}")
                        cliente = repositorio_cliente.obtener_cliente_por_id(usuario["id_usuario"])
                        if cliente:
                            print(f"🧑‍🍳 Cliente encontrado: {cliente['nombre_cliente']}")
                            return {"usuario": cliente["nombre_cliente"], "rol": "cliente"}

                    elif nombre_rol.lower() == "trabajador":
                        repositorio_trabajador = RepositorioTrabajador(conexion)
                        trabajador = repositorio_trabajador.obtener_trabajador_por_id(usuario["id_usuario"])
                        if trabajador:
                            print(f"👨‍🍳 Trabajador encontrado: {trabajador['nombre_trabajador']}")
                            return {"usuario": trabajador["nombre_trabajador"], "rol": "trabajador"}

                else:
                    print(f"❌ Error: 'nombre_rol' no encontrado para el usuario con email: {email}")
            else:
                print("⚠️ Usuario no encontrado o credenciales incorrectas.")

            return None
    except Exception as e:
        print(f"❌ Error al autenticar usuario: {e}")
        return None
