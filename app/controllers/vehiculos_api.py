# app/controllers/vehiculos_api.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from app import schemas
from app.database import (
    fetch_all_vehiculos,
    insert_vehiculo,
    fetch_vehiculo_by_id,
    update_vehiculo,
    delete_vehiculo,
    DatabaseConnectionError,
)

vehiculos_router = APIRouter()

@vehiculos_router.get("/vehiculos", response_model=List[schemas.VehiculoDB])
def list_vehiculos():
    try:
        return fetch_all_vehiculos() or []
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al listar vehículos")

@vehiculos_router.post("/vehiculos", status_code=status.HTTP_201_CREATED, response_model=schemas.VehiculoDB)
def create_vehiculo(payload: schemas.VehiculoCreate):
    try:
        new_id = insert_vehiculo(
            payload.matricula, payload.vin, payload.modelo_id, payload.color,
            payload.kilometraje, payload.estado, payload.precio_dia, payload.ubicacion
        )
        veh = fetch_vehiculo_by_id(new_id)
        if not veh:
            raise HTTPException(status_code=500, detail="No se pudo recuperar el vehículo creado")
        return veh
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al crear vehículo")

@vehiculos_router.get("/vehiculos/{vehiculo_id}", response_model=schemas.VehiculoDB)
def get_vehiculo(vehiculo_id: int):
    try:
        v = fetch_vehiculo_by_id(vehiculo_id)
        if not v:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return v
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al obtener vehículo")

@vehiculos_router.put("/vehiculos/{vehiculo_id}", response_model=schemas.VehiculoDB)
def put_vehiculo(vehiculo_id: int, payload: schemas.VehiculoUpdate):
    try:
        updated = update_vehiculo(
            vehiculo_id, payload.matricula, payload.vin, payload.modelo_id, payload.color,
            payload.kilometraje, payload.estado, payload.precio_dia, payload.ubicacion
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return fetch_vehiculo_by_id(vehiculo_id)
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al actualizar vehículo")

@vehiculos_router.delete("/vehiculos/{vehiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehiculo_endpoint(vehiculo_id: int):
    try:
        deleted = delete_vehiculo(vehiculo_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return {}
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al eliminar vehículo")