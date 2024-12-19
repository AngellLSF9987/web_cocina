class Cliente:
    def __init__(self, id_cliente, id_usuario, nombre, apellido1, apellido2, dni_cliente, telefono, direccion):
        self.id_cliente = id_cliente
        self.id_usuario = id_usuario  # Relación con Usuario
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.dni_cliente = dni_cliente
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return f"Cliente [ID: {self.id_cliente}, Nombre: {self.nombre}, Apellidos: {self.apellido1} {self.apellido2}]"
