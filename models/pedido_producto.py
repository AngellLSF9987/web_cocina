class PedidoProducto:
    def __init__(self, id_pedido_producto, id_pedido, id_producto):
        self.id_pedido_producto = id_pedido_producto
        self.id_pedido = id_pedido
        self.id_producto = id_producto

    def __str__(self):
        return f"Pedido_Producto [ID: {self.id_pedido_producto}, Pedido ID: {self.id_pedido}, Producto ID: {self.id_producto}]"
