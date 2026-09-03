from app.models.categoria import Categoria
from app.models.producto import Producto

categorias: list[Categoria] = [
   Categoria(id=1, nombre="Electronica"),
   Categoria(id=2, nombre="Hogar"),
   Categoria(id=3, nombre="Libreria"),
]
productos: list[Producto] = [
    Producto(id=1, nombre="Audiculares Bluetooth", precio= 15999.0, stock= 20, categoria_id=1),
    Producto(id=2, nombre="Mouse inalambrico", precio= 7000.0, stock= 35, categorias_id=1),
    Producto(id=3, nombre="Cafetera Electrica", precio=  24798.0, stock= 17, categoria_id=2),
    Producto(id=4, nombre="Set de sartenes", precio= 23890.0, stock=9, categoria=2),
    Producto(id=5, nombre="Cuaderno A4 Tapa dura", precio= 4000.0, stock=32, categoria=3),
    Producto(id=6, nombre="Lapicera", precio= 2000.0, stock= 17, categoria= 3 ),
]
_next_id = len(productos) + 1

def bump_producto_id() -> int:
    global _next_id
    nuevo_id = _next_id
    _next_id += 1
    return nuevo_id