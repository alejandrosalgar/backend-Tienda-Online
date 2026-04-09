from fastapi import FastAPI

from src.routes import usuario_routes, producto_routes, categoria_routes

app = FastAPI(title="Tienda Online API")

app.include_router(usuario_routes.router)
app.include_router(producto_routes.router)
app.include_router(categoria_routes.router)
