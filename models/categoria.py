class Categoria:
    def __init__(self, id_categoria, nombre_categoria, descripcion=None, imagen=None):
        self.id_categoria = id_categoria  # ID de la categoría
        self.nombre_categoria = nombre_categoria  # Nombre de la categoría
        self.descripcion = descripcion  # Descripción de la categoría
        self.imagen = imagen  # Imagen asociada a la categoría

    def __str__(self):
        # Representación en formato cadena de la instancia de la categoría
        return f"Categoria [ID: {self.id_categoria}, Nombre: {self.nombre_categoria}, Descripción: {self.descripcion}, Imagen: {self.imagen}]"
