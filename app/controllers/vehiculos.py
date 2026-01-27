# app/controllers/vehiculos.py
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from typing import Optional
import logging

from app.database import (
    fetch_all_vehiculos,
    insert_vehiculo,
    delete_vehiculo,
    fetch_vehiculo_by_id,
    update_vehiculo,
    fetch_all_modelos,
    fetch_all_categorias,
    DatabaseConnectionError,
)
from app.schemas import VehiculoCreate, VehiculoUpdate, VehiculoDB

logger = logging.getLogger("autorent")

# ✅ IMPORTANTE: Exportar como vehiculos_router para que main.py lo encuentre
vehiculos_router = APIRouter()


def _is_ajax(request: Request) -> bool:
    """Detecta peticiones AJAX/fetch"""
    xrw = (request.headers.get("x-requested-with") or "").lower()
    accept = (request.headers.get("accept") or "").lower()
    if xrw == "xmlhttprequest":
        return True
    if "application/json" in accept:
        return True
    return False


@vehiculos_router.get("/vehiculos", response_class=HTMLResponse)
def get_vehiculos(request: Request):
    try:
        vehiculos_rows = fetch_all_vehiculos() or []
        vehiculos = [VehiculoDB(**r) for r in vehiculos_rows] if vehiculos_rows else []
        modelos = fetch_all_modelos() or []
        categorias = fetch_all_categorias() or []
        return request.app.state.templates.TemplateResponse(
            "pages/vehiculos.html",
            {"request": request, "vehiculos": vehiculos, "modelos": modelos, "categorias": categorias},
        )
    except DatabaseConnectionError:
        raise
    except Exception:
        logger.exception("Error al obtener vehículos")
        raise HTTPException(status_code=500, detail="Error interno al obtener vehículos")


@vehiculos_router.get("/vehiculos/nuevo", response_class=HTMLResponse)
def get_nuevo_vehiculo(request: Request):
    try:
        modelos = fetch_all_modelos() or []
        categorias = fetch_all_categorias() or []
        return request.app.state.templates.TemplateResponse(
            "pages/nuevo_vehiculo.html", {"request": request, "modelos": modelos, "categorias": categorias}
        )
    except DatabaseConnectionError:
        raise
    except Exception:
        logger.exception("Error al preparar formulario nuevo vehículo")
        raise HTTPException(status_code=500, detail="Error interno al preparar formulario")


@vehiculos_router.post("/vehiculos/nuevo")
def post_nuevo_vehiculo(
    request: Request,
    matricula: str = Form(...),
    vin: Optional[str] = Form(None),
    modelo_id: int = Form(...),
    color: Optional[str] = Form(None),
    kilometraje: Optional[int] = Form(0),
    estado: Optional[str] = Form("disponible"),
    precio_dia: float = Form(...),
    ubicacion: Optional[str] = Form(None),
):
    try:
        vehiculo_data = VehiculoCreate(
            matricula=matricula,
            vin=vin if vin else None,
            modelo_id=int(modelo_id),
            color=color if color else None,
            kilometraje=int(kilometraje) if kilometraje is not None else 0,
            estado=estado,
            precio_dia=float(precio_dia),
            ubicacion=ubicacion if ubicacion else None,
        )
        insert_vehiculo(
            vehiculo_data.matricula,
            vehiculo_data.vin,
            vehiculo_data.modelo_id,
            vehiculo_data.color,
            vehiculo_data.kilometraje,
            vehiculo_data.estado,
            vehiculo_data.precio_dia,
            vehiculo_data.ubicacion,
        )
        return RedirectResponse(url="/", status_code=303)
    except DatabaseConnectionError:
        raise
    except Exception:
        logger.exception("Error al insertar vehículo")
        raise HTTPException(status_code=500, detail="Error interno al insertar vehículo")


@vehiculos_router.delete("/vehiculos/{vehiculo_id}")
def delete_vehiculo_endpoint(request: Request, vehiculo_id: int):
    """
    Elimina un vehículo. Maneja tanto peticiones AJAX como normales.
    """
    try:
        eliminado = delete_vehiculo(vehiculo_id)
        if not eliminado:
            if _is_ajax(request):
                return JSONResponse(content={"redirect": "/error404"}, status_code=200)
            return RedirectResponse(url="/error404", status_code=303)

        return JSONResponse(content={"mensaje": "Vehículo eliminado exitosamente"}, status_code=200)

    except DatabaseConnectionError:
        logger.exception("DatabaseConnectionError al eliminar vehículo")
        if _is_ajax(request):
            return JSONResponse(content={"redirect": "/error404"}, status_code=200)
        return RedirectResponse(url="/error404", status_code=303)
    except Exception:
        logger.exception("Error inesperado al eliminar vehículo")
        if _is_ajax(request):
            return JSONResponse(content={"redirect": "/error404"}, status_code=200)
        return RedirectResponse(url="/error404", status_code=303)


@vehiculos_router.get("/vehiculos/editar/{vehiculo_id}", response_class=HTMLResponse)
def get_editar_vehiculo(request: Request, vehiculo_id: int):
    try:
        vehiculo_data = fetch_vehiculo_by_id(vehiculo_id)
        if not vehiculo_data:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        vehiculo = VehiculoDB(**vehiculo_data)
        modelos = fetch_all_modelos() or []
        categorias = fetch_all_categorias() or []
        return request.app.state.templates.TemplateResponse(
            "pages/editar_vehiculo.html",
            {"request": request, "vehiculo": vehiculo, "modelos": modelos, "categorias": categorias},
        )
    except DatabaseConnectionError:
        raise
    except Exception:
        logger.exception("Error al obtener vehículo para editar")
        raise HTTPException(status_code=500, detail="Error interno al obtener vehículo")


@vehiculos_router.post("/vehiculos/editar/{vehiculo_id}")
def post_editar_vehiculo(
    request: Request,
    vehiculo_id: int,
    matricula: str = Form(...),
    vin: Optional[str] = Form(None),
    modelo_id: int = Form(...),
    color: Optional[str] = Form(None),
    kilometraje: Optional[int] = Form(0),
    estado: Optional[str] = Form("disponible"),
    precio_dia: float = Form(...),
    ubicacion: Optional[str] = Form(None),
):
    try:
        vehiculo_data = VehiculoUpdate(
            matricula=matricula,
            vin=vin if vin else None,
            modelo_id=int(modelo_id),
            color=color if color else None,
            kilometraje=int(kilometraje) if kilometraje is not None else 0,
            estado=estado,
            precio_dia=float(precio_dia),
            ubicacion=ubicacion if ubicacion else None,
        )
        actualizado = update_vehiculo(
            vehiculo_id,
            vehiculo_data.matricula,
            vehiculo_data.vin,
            vehiculo_data.modelo_id,
            vehiculo_data.color,
            vehiculo_data.kilometraje,
            vehiculo_data.estado,
            vehiculo_data.precio_dia,
            vehiculo_data.ubicacion,
        )
        if not actualizado:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return RedirectResponse(url="/vehiculos", status_code=303)
    except DatabaseConnectionError:
        raise
    except Exception:
        logger.exception("Error al actualizar vehículo")
        raise HTTPException(status_code=500, detail="Error interno al actualizar vehículo")