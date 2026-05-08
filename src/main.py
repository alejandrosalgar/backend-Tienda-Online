# RUTA: src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import usuario_routes, producto_routes, categoria_routes
from src.routes import pedido_routes

app = FastAPI(title="Tienda Online API")

# CONFIGURACIÓN DE CORS - Vital para conectar con el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permite peticiones desde cualquier origen (luego puedes limitarlo a localhost:4200)
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos los encabezados (headers)
)

# Registro de rutas
app.include_router(usuario_routes.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(producto_routes.router, prefix="/productos", tags=["Productos"])
app.include_router(categoria_routes.router)
app.include_router(pedido_routes.router)


@app.get("/")
def read_root():
    return {"message": "API de Tienda Online funcionando correctamente"}
