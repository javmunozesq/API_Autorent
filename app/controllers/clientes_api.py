# app/controllers/clientes_api.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from app import schemas
from app.database import (
    fetch_all_clientes,
    insert_cliente,
    fetch_cliente_by_id,
    update_cliente,
    delete_cliente,
    DatabaseConnectionError,
)

clientes_router = APIRouter()

@clientes_router.get("/clientes", response_model=List[schemas.ClienteDB])
def list_clientes():
    try:
        rows = fetch_all_clientes() or []
        return rows
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al listar clientes")

@clientes_router.post("/clientes", status_code=status.HTTP_201_CREATED, response_model=schemas.ClienteDB)
def create_cliente(payload: schemas.ClienteCreate):
    try:
        new_id = insert_cliente(
            payload.nombre, payload.apellido, payload.email, payload.telefono, payload.direccion
        )
        cliente = fetch_cliente_by_id(new_id)
        if not cliente:
            raise HTTPException(status_code=500, detail="No se pudo recuperar el cliente creado")
        return cliente
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al crear cliente")

@clientes_router.get("/clientes/{cliente_id}", response_model=schemas.ClienteDB)
def get_cliente(cliente_id: int):
    try:
        cliente = fetch_cliente_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al obtener cliente")

@clientes_router.put("/clientes/{cliente_id}", response_model=schemas.ClienteDB)
def put_cliente(cliente_id: int, payload: schemas.ClienteUpdate):
    try:
        updated = update_cliente(
            cliente_id, payload.nombre, payload.apellido, payload.email, payload.telefono, payload.direccion
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        cliente = fetch_cliente_by_id(cliente_id)
        return cliente
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al actualizar cliente")

@clientes_router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente_endpoint(cliente_id: int):
    try:
        deleted = delete_cliente(cliente_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return {}
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al eliminar cliente")