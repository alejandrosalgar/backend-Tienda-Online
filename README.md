# backend-Tienda-Online

Sistema backend de tienda online desarrollado en Python con arquitectura modular, manejo de entidades, operaciones CRUD y conexión a base de datos.

## Descripción

Este proyecto es una aplicación de consola para la administración básica de una tienda online.  
Permite el inicio de sesión o creación del primer usuario y, una vez autenticado, acceder a distintos módulos para gestionar:

- Categorías
- Productos
- Pedidos
- Pagos
- Envíos
- Usuarios

El sistema está organizado en módulos CRUD y entidades, siguiendo una estructura más cercana a un backend real.

---

## Características principales

- Inicio de sesión de usuarios
- Creación del primer usuario si la base de datos está vacía
- Menú principal interactivo por consola
- CRUD de categorías
- CRUD de productos
- CRUD de pedidos
- CRUD de pagos
- CRUD de envíos
- Persistencia de datos en base de datos
- Código modular organizado por responsabilidades

---

## Tecnologías utilizadas

- **Python 3**
- **SQLAlchemy**
- **PostgreSQL / Neon** (según tu configuración actual)
- **dotenv** para variables de entorno
- **UUID** como identificadores
- **Git y GitHub** para control de versiones

---

## Video de explicación

En el siguiente enlace se puede ver una explicación general del proyecto, su estructura, funcionamiento por consola y organización del código:

**URL del video:** [Agregar aquí el enlace]

---

## Estructura del proyecto

```bash
backend-Tienda-Online/
│
├── src/
│   ├── crud/
│   │   ├── categoria.py
│   │   ├── envio.py
│   │   ├── pago.py
│   │   ├── pedido.py
│   │   ├── producto.py
│   │   └── usuario.py
│   │
│   ├── database/
│   │   └── config.py
│   │
│   └── entities/
│       ├── categoria.py
│       ├── envio.py
│       ├── pago.py
│       ├── pedido.py
│       ├── producto.py
│       └── usuario.py
│
├── .env
├── .gitignore
├── main.py
├── migrarDb.py
├── README.md
└── requirements.txt

