class Venta:
    def __init__(self, id_venta, fecha, id_cliente, total):
        self.id_venta = id_venta
        self.fecha = fecha
        self.id_cliente = id_cliente
        self.total = total

    def __str__(self):
        return f"Venta [ID: {self.id_venta}, Fecha: {self.fecha}, Cliente ID: {self.id_cliente}, Total: {self.total}]"
