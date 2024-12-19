class Carrito:
    def __init__(self, id_carrito, id_venta, id_cliente, id_producto, cantidad=1, precio_total=1.00):
        self.id_carrito = id_carrito  # ID del carrito
        self.id_venta = id_venta  # ID de la venta
        self.id_cliente = id_cliente  # ID del cliente
        self.id_producto = id_producto  # ID del producto
        self.cantidad = cantidad  # Cantidad del producto
        self.precio_total = precio_total  # Precio total del carrito

    def __str__(self):
        # Representación en formato cadena de la instancia del carrito
        return f"Carrito [ID: {self.id_carrito}, Producto ID: {self.id_producto}, Cliente ID: {self.id_cliente}, Cantidad: {self.cantidad}, Total: {self.precio_total}]"