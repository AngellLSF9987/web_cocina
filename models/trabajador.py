class Trabajador:
    def __init__(self, id_trabajador, id_usuario, nombre, apellido1, apellido2, dni_trabajador, telefono, direccion):
        self.id_trabajador = id_trabajador
        self.id_usuario = id_usuario  # Relación con Usuario
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.dni_trabajador = dni_trabajador
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return f"Trabajador [ID: {self.id_trabajador}, Nombre: {self.nombre}, Apellidos: {self.apellido1} {self.apellido2}]"
