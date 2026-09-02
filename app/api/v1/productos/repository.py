from typing import Optional
from app.core import db
from app.models.producto import Producto
from app.api.v1.productos.schemas import ProductoCreate, ProductoUpdate


def _find_categoria(categoria_id: int):
    for cat in db.categorias:
        if cat.id == categoria_id:
            return cat
    return None


def _to_dict(producto: Producto) -> dict:
    categoria = _find_categoria(producto.categoria_id)
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "stock": producto.stock,
        "activo": producto.activo,
        "categoria": {"id": categoria.id, "nombre": categoria.nombre},
    }


def list_productos(query: Optional[str] = None, categoria_id: Optional[int] = None):
    resultado = db.productos
    if query:
        resultado = search_by_nombre(query, base=resultado)
    if categoria_id is not None:
        resultado = [p for p in resultado if p.categoria_id == categoria_id]
    return [_to_dict(p) for p in resultado]


def get_by_id(producto_id: int):
    for p in db.productos:
        if p.id == producto_id:
            return p
    return None


def search_by_nombre(query: str, base=None):
    fuente = base if base is not None else db.productos
    q = query.lower()
    return [p for p in fuente if q in p.nombre.lower()]


def ensure_categoria(categoria_id: int):
    if _find_categoria(categoria_id) is None:
        return False, f"La categoria {categoria_id} no existe"
    return True, None


def create(data: ProductoCreate) -> Producto:
    nuevo = Producto(
        id=db.bump_producto_id(),
        nombre=data.nombre,
        precio=data.precio,
        stock=data.stock,
        categoria_id=data.categoria_id,
        activo=True,
    )
    db.productos.append(nuevo)
    return nuevo


def update(producto_id: int, data: ProductoUpdate):
    producto = get_by_id(producto_id)
    if producto is None:
        return None
    cambios = data.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(producto, campo, valor)
    return producto


def delete(producto_id: int) -> bool:
    producto = get_by_id(producto_id)
    if producto is None:
        return False
    db.productos.remove(producto)
    return True