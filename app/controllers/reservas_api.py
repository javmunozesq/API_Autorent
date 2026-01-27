# app/controllers/pagos_api.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database import insert_pago, fetch_pagos_by_reserva, DatabaseConnectionError

pagos_router = APIRouter()

@pagos_router.post("/pagos", status_code=status.HTTP_201_CREATED)
def create_pago(reserva_id: int, monto: float, metodo_pago: str, referencia: str | None = None):
    try:
        if monto <= 0:
            raise HTTPException(status_code=422, detail="El monto debe ser mayor que 0")
        pago_id = insert_pago(reserva_id, monto, metodo_pago, referencia)
        if not pago_id:
            raise HTTPException(status_code=400, detail="No se pudo registrar el pago")
        return {"mensaje": "Pago registrado exitosamente", "pago_id": pago_id}
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al registrar pago")

@pagos_router.get("/pagos/{reserva_id}")
def list_pagos(reserva_id: int):
    try:
        pagos = fetch_pagos_by_reserva(reserva_id)
        return {"pagos": pagos}
    except DatabaseConnectionError:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al obtener pagos")