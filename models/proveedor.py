class Proveedor:
    def __init__(self, id_proveedor, nombre_proveedor, nombre_empresa, telefono, email):
        self.id_proveedor = id_proveedor
        self.nombre_proveedor = nombre_proveedor
        self.nombre_empresa = nombre_empresa
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"Proveedor [ID: {self.id_proveedor}, Nombre: {self.nombre_proveedor}, Empresa: {self.nombre_empresa}, Email: {self.email}]"
