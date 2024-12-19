class Pedido:
    def __init__(self, id_pedido, fecha_pedido, estado, total, id_cliente):
        self.id_pedido = id_pedido
        self.fecha_pedido = fecha_pedido
        self.estado = estado
        self.total = total
        self.id_cliente = id_cliente

    def __str__(self):
        return f"Pedido [ID: {self.id_pedido}, Fecha: {self.fecha_pedido}, Estado: {self.estado}, Total: {self.total}]"
