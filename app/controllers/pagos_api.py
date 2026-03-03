# app/controllers/reservas_api.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database import DatabaseConnectionError

reservas_router = APIRouter()

# Ejemplo mínimo: lista de reservas (reemplaza por llamadas reales a la BD)
@reservas_router.get("/reservas", response_model=List[dict])
async def list_reservas():
    # Aquí deberías llamar a tu función de DB, p.ej. fetch_reservas()
    return [
        {
            "id": 1,
            "cliente_id": 1,
            "vehiculo_id": 2,
            "fecha_inicio": "2026-03-01",
            "fecha_fin": "2026-03-03",
            "estado": "confirmada"
        }
    ]

@reservas_router.get("/reservas/{reserva_id}")
async def get_reserva(reserva_id: int):
    # Reemplaza por fetch_reserva(reserva_id) real
    if reserva_id != 1:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {
        "id": 1,
        "cliente_id": 1,
        "vehiculo_id": 2,
        "fecha_inicio": "2026-03-01",
        "fecha_fin": "2026-03-03",
        "estado": "confirmada"
    }

@reservas_router.post("/reservas", status_code=status.HTTP_201_CREATED)
async def create_reserva(payload: dict):
    # Validar y guardar en BD; aquí devolvemos el payload con id simulado
    payload["id"] = 2
    return payload

@reservas_router.put("/reservas/{reserva_id}")
async def update_reserva(reserva_id: int, payload: dict):
    # Lógica real: actualizar en BD
    if reserva_id != 1:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    payload["id"] = reserva_id
    return payload

@reservas_router.delete("/reservas/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reserva(reserva_id: int):
    # Lógica real: eliminar en BD
    if reserva_id != 1:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return None