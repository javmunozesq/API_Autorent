# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import importlib

from app.database import DatabaseConnectionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("autorent")

app = FastAPI(title="Autorent API")

# Include routers explicitly (detect attributes ending with "_router")
controller_modules = [
    "app.controllers.clientes_api",
    "app.controllers.vehiculos_api",
    "app.controllers.reservas_api",
    "app.controllers.pagos_api",
]

for mod_name in controller_modules:
    try:
        mod = importlib.import_module(mod_name)
    except ModuleNotFoundError:
        logger.info("Controller module not found (skipping): %s", mod_name)
        continue
    for attr in dir(mod):
        if attr.endswith("_router"):
            router = getattr(mod, attr)
            app.include_router(router, prefix="", tags=[attr.replace("_router", "")])

# Global handlers
@app.exception_handler(DatabaseConnectionError)
async def db_exception_handler(request: Request, exc: DatabaseConnectionError):
    logger.exception("DatabaseConnectionError: %s", exc)
    return JSONResponse(status_code=503, content={"detail": "Database connection error"})

@app.get("/health")
def health():
    return {"status": "ok", "service": "autorent"}