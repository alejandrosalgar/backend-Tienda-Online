import os
from dotenv import load_dotenv

from src.database.config import create_tables

# IMPORTAR TODOS LOS MODELOS
import src.entities.usuario
import src.entities.categoria
import src.entities.producto
import src.entities.pedido

# Cargar .env correctamente
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

if __name__ == "__main__":
    create_tables()
    print("Tablas creadas correctamente en Neon.")
