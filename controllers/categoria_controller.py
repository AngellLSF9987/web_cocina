from flask import Blueprint, request, render_template, redirect, url_for, flash
from repositories.repositorio_categoria import RepositorioCategoria
from routes.auth_routes import access_required

# Crear el Blueprint para manejar las rutas de categorías
categoria_bp = Blueprint('categoria_bp', __name__)

# Instanciamos el repositorio
repo_categoria = RepositorioCategoria()

# Ruta para obtener todas las categorías
@categoria_bp.route('/')
def obtener_todas_las_categorias():
    try:
        categorias = repo_categoria.obtener_todas_las_categorias()
        return render_template('cliente_categoria_lista.html', categorias=categorias)
    except Exception as e:
        flash(f'Error al obtener las categorías: {str(e)}', 'error')
        return redirect(url_for('categoria_bp.obtener_todas_las_categorias'))

@categoria_bp.route('/lista_categorias')
def cliente_lista_categorias():
    try:
        categorias = repo_categoria.obtener_todas_las_categorias()
        return render_template('cliente_categoria_lista.html', categorias=categorias)
    except Exception as e:
        flash(f'Error al obtener las categorías: {str(e)}', 'error')
        return redirect(url_for('categoria_bp.cliente_lista_categorias'))

# Ruta para obtener los detalles de una categoría
@categoria_bp.route('/<int:id_categoria>', methods=['GET'])
def obtener_detalle_categoria(id_categoria):
    try:
        categoria = repo_categoria.obtener_categoria_por_id(id_categoria)
        if categoria:
            return render_template('categoria_detalle.html', categoria=categoria)
        else:
            flash('Categoría no encontrada.', 'error')
            return redirect(url_for('categoria_bp.obtener_todas_las_categorias'))
    except Exception as e:
        flash(f'Error al obtener los detalles de la categoría: {str(e)}', 'error')
        return redirect(url_for('categoria_bp.obtener_todas_las_categorias'))

# Ruta para crear una categoría
@categoria_bp.route('/nueva', methods=['GET', 'POST'])
@access_required(role="autenticado")
def crear_categoria():
    if request.method == 'POST':
        nombre = request.form.get('nombre_categoria')
        descripcion = request.form.get('descripcion')
        imagen = request.files.get('imagen')

        try:
            repo_categoria.insertar_categoria(nombre, descripcion, imagen)
            flash('Categoría creada con éxito.', 'success')
            return redirect(url_for('categoria_bp.obtener_todas_las_categorias'))
        except Exception as e:
            flash(f'Error al crear la categoría: {str(e)}', 'error')
            return redirect(url_for('categoria_bp.crear_categoria'))

    return render_template('cliente_categoria_nueva.html')

# Ruta para editar una categoría
@categoria_bp.route('/<int:id_categoria>/editar', methods=['GET', 'POST'])
@access_required(role="autenticado")
def editar_categoria(id_categoria):
    categoria = repo_categoria.obtener_categoria_por_id(id_categoria)

    if request.method == 'POST':
        nombre = request.form.get('nombre_categoria')
        descripcion = request.form.get('descripcion')
        imagen = request.files.get('imagen')

        try:
            repo_categoria.actualizar_categoria(id_categoria, nombre, descripcion, imagen)
            flash('Categoría actualizada con éxito.', 'success')
            return redirect(url_for('categoria_bp.obtener_detalle_categoria', id_categoria=id_categoria))
        except Exception as e:
            flash(f'Error al actualizar la categoría: {str(e)}', 'error')
            return redirect(url_for('categoria_bp.editar_categoria', id_categoria=id_categoria))

    return render_template('cliente_categoria_editar.html', categoria=categoria)

# Ruta para eliminar una categoría
@categoria_bp.route('/<int:id_categoria>/eliminar', methods=['POST'])
@access_required(role="autenticado")
def eliminar_categoria(id_categoria):
    try:
        repo_categoria.eliminar_categoria(id_categoria)
        flash('Categoría eliminada con éxito.', 'success')
        return redirect(url_for('categoria_bp.obtener_todas_las_categorias'))
    except Exception as e:
        flash(f'Error al eliminar la categoría: {str(e)}', 'error')
        return redirect(url_for('categoria_bp.obtener_todas_las_categorias'))
