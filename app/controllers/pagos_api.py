# app/controllers/pagos.py
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from app.database import insert_pago, fetch_pagos_by_reserva, DatabaseConnectionError

logger = logging.getLogger("autorent")

pagos_router = APIRouter()


@pagos_router.post("/pagos/nuevo")
def post_nuevo_pago(
    reserva_id: int = Form(...),
    monto: float = Form(...),
    metodo_pago: str = Form(...),
    referencia: Optional[str] = Form(None),
):
    """
    Endpoint para crear un nuevo pago asociado a una reserva.
    
    Args:
        reserva_id: ID de la reserva a la que se asocia el pago
        monto: Cantidad del pago (debe ser mayor que 0)
        metodo_pago: Método de pago (tarjeta, efectivo, transferencia, paypal)
        referencia: Referencia opcional del pago
        
    Returns:
        JSON con el mensaje de éxito y el ID del pago creado
    """
    try:
        if monto <= 0:
            raise HTTPException(status_code=422, detail="El monto debe ser mayor que 0")

        pago_id = insert_pago(reserva_id, monto, metodo_pago, referencia)
        if not pago_id:
            raise HTTPException(status_code=400, detail="No se pudo registrar el pago")

        return JSONResponse(
            content={"mensaje": "Pago registrado exitosamente", "pago_id": pago_id}, status_code=201
        )
    except DatabaseConnectionError:
        logger.exception("Error de conexión a la base de datos al registrar pago")
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error inesperado al registrar pago")
        raise HTTPException(status_code=500, detail="Error interno al registrar el pago")


@pagos_router.get("/pagos/{reserva_id}")
def get_pagos_reserva(reserva_id: int):
    """
    Obtiene todos los pagos asociados a una reserva específica.
    
    Args:
        reserva_id: ID de la reserva
        
    Returns:
        JSON con la lista de pagos de la reserva
    """
    try:
        pagos = fetch_pagos_by_reserva(reserva_id)
        return JSONResponse(content={"pagos": pagos}, status_code=200)
    except DatabaseConnectionError:
        logger.exception("Error de conexión a la base de datos al obtener pagos")
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    except Exception:
        logger.exception("Error inesperado al obtener pagos")
        raise HTTPException(status_code=500, detail="Error interno al obtener pagos")