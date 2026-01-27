# app/controllers/__init__.py
"""
Módulo de controllers para la API REST Autorent.

Este módulo expone todos los routers de los diferentes recursos
para que puedan ser importados fácilmente desde otros módulos.

Ejemplo de uso:
    from app.controllers import clientes_router, vehiculos_router

Los routers disponibles son:
    - clientes_router: Operaciones CRUD sobre clientes
    - vehiculos_router: Operaciones CRUD sobre vehículos
    - reservas_router: Operaciones CRUD sobre reservas
    - pagos_router: Operaciones sobre pagos
"""

from .clientes import clientes_router
from .vehiculos import vehiculos_router
from .reservas import reservas_router
from .pagos import pagos_router

__all__ = [
    "clientes_router",
    "vehiculos_router",
    "reservas_router",
    "pagos_router",
]