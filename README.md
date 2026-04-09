# backend-Tienda-Online

Sistema backend de tienda online desarrollado en Python con arquitectura modular, ahora evolucionado a una *API REST con FastAPI*.

---

## 📌 Descripción

Este proyecto inició como una aplicación de consola para la administración de una tienda online y fue evolucionado a un *backend moderno basado en API REST*.

Actualmente permite gestionar:

* Usuarios
* Categorías
* Productos
* Pedidos
* Pagos
* Envíos

A través de endpoints HTTP utilizando *FastAPI*, manteniendo una estructura modular basada en entidades y CRUD.

---

## 🚀 Características principales

### 🔹 Versión actual (API REST)

* API REST con *FastAPI*
* Documentación automática con *Swagger (OpenAPI)*
* Endpoints para:

  * Usuarios
  * Categorías (incluye descripción)
  * Productos
  * Pedidos
  * Pagos
  * Envíos
* CRUD completo por cada módulo
* Validación de datos
* Uso de UUID como identificadores
* Arquitectura modular (entities + crud + routes)

### 🔹 Versión anterior (consola)

* Inicio de sesión de usuarios
* Menú interactivo por consola
* Creación automática del primer usuario
* Gestión completa desde terminal

---

## 🧱 Tecnologías utilizadas

* *Python 3*
* *FastAPI*
* *Uvicorn*
* *SQLAlchemy*
* *PostgreSQL / Neon*
* *dotenv*
* *UUID*
* *Git y GitHub*

---

## 📂 Estructura del proyecto

bash
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
│   ├── entities/
│   │   ├── categoria.py
│   │   ├── envio.py
│   │   ├── pago.py
│   │   ├── pedido.py
│   │   ├── producto.py
│   │   └── usuario.py
│   │
│   ├── routes/
│   │   ├── categoria_routes.py
│   │   ├── producto_routes.py
│   │   └── usuario_routes.py
│   │
│   └── main.py
│
├── .env
├── .gitignore
├── app_consola.py
├── migrarDb.py
├── README.md
└── requirements.txt


---

## ▶️ Cómo ejecutar el proyecto

### 1. Instalar dependencias

bash
py -m pip install -r requirements.txt


---

### 2. Ejecutar la API

bash
py -m uvicorn src.main:app --reload


---

### 3. Acceder a la documentación

Swagger UI:

👉 http://127.0.0.1:8000/docs

---

## 🧪 Ejemplo de uso

### Crear usuario

http
POST /usuarios/


Parámetros:

* nombre_usuario
* email
* contrasena

---

### Crear categoría

http
POST /categorias/


Parámetros:

* nombre_categoria
* descripcion

---

## 🎥 Video de explicación

Se puede ver una explicación general del proyecto, estructura y funcionamiento:

👉 https://drive.google.com/file/d/1zfUJb6TOeSHZ8JLoz04jnvm0B6dEsTKl/view?usp=sharing
---

## 📌 Notas finales

* El proyecto evolucionó de una aplicación de consola a una API REST profesional.
* Se mantiene separación de responsabilidades (CRUD, entidades, rutas).
* Preparado para escalar a frontend o microservicios.

---