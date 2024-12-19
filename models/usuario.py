class Usuario:
    def __init__(self, id_usuario, email, contraseña, fecha_registro, id_rol):
        self.id_usuario = id_usuario
        self.email = email
        self.contraseña = contraseña
        self.fecha_registro = fecha_registro
        self.id_rol = id_rol  # Relación con Rol

    def __str__(self):
        return f"Usuario [ID: {self.id_usuario}, Email: {self.email}, Fecha de Registro: {self.fecha_registro}]"
