class Rol:
    def __init__(self, id_rol, nombre_rol):
        self.id_rol = id_rol
        self.nombre_rol = nombre_rol

    def __str__(self):
        return f"Rol [ID: {self.id_rol}, Nombre: {self.nombre_rol}]"
