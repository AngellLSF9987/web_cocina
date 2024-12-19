class Producto:
    def __init__(self, id_producto, nombre_producto, descripcion, precio, imagen, stock, id_proveedor, id_categoria):
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.descripcion = descripcion
        self.precio = precio
        self.imagen = imagen
        self.stock = stock
        self.id_proveedor = id_proveedor
        self.id_categoria = id_categoria

    def __str__(self):
        return f"Producto [ID: {self.id_producto}, Nombre: {self.nombre_producto}, Precio: {self.precio}, Stock: {self.stock}]"
