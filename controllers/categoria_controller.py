from repositories.repositorio_categoria import RepositorioCategoria

class CategoriaController:

    repo_categoria = RepositorioCategoria()

    @staticmethod
    def obtener_todas_las_categorias(repo_categoria):
        return repo_categoria.obtener_todas_las_categorias()

    @staticmethod
    def crear_categoria(repo_categoria, nombre, descripcion, imagen=None):
        if not nombre or not descripcion:
            raise ValueError("El nombre y la descripción son obligatorios.")
        return repo_categoria.insertar_categoria(nombre, descripcion, imagen)
