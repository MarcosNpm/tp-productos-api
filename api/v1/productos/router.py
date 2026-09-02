from typing import Optional
from fastapi import APIRouter, HTTPException, status
from app.api.v1.productos import repository
from app.api.v1.productos.schemas import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("", response_model=list[ProductoResponse])
def listar_productos(query: Optional[str] = None, categoria_id: Optional[int] = None):
    return repository.list_productos(query=query, categoria_id=categoria_id)


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int):
    producto = repository.get_by_id(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail=f"El producto {producto_id} no existe")
    return repository._to_dict(producto)


@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(data: ProductoCreate):
    es_valida, error = repository.ensure_categoria(data.categoria_id)
    if not es_valida:
        raise HTTPException(status_code=400, detail=error)
    nuevo = repository.create(data)
    return repository._to_dict(nuevo)


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, data: ProductoUpdate):
    if data.categoria_id is not None:
        es_valida, error = repository.ensure_categoria(data.categoria_id)
        if not es_valida:
            raise HTTPException(status_code=400, detail=error)
    actualizado = repository.update(producto_id, data)
    if actualizado is None:
        raise HTTPException(status_code=404, detail=f"El producto {producto_id} no existe")
    return repository._to_dict(actualizado)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int):
    eliminado = repository.delete(producto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail=f"El producto {producto_id} no existe")
    return None