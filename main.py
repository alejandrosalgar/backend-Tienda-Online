"""
Punto de entrada: inicio de sesión (o creación del primer usuario)
y menú CRUD para Categoría, Producto y Pedido.
"""

import sys
from typing import Optional
from uuid import UUID

sys.path.insert(0, ".")

from src.crud import categoria as crud_categoria
from src.crud import envio as crud_envio
from src.crud import pago as crud_pago
from src.crud import pedido as crud_pedido
from src.crud import producto as crud_producto
from src.crud import usuario as crud_usuario
from src.entities.usuario import Usuario


def leer_texto(mensaje: str, default: str = "") -> str:
    s = input(mensaje).strip()
    return s if s else default


def leer_float(mensaje: str, default: float = 0.0) -> float:
    try:
        return float(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_int(mensaje: str, default: int = 0) -> int:
    try:
        return int(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_uuid(mensaje: str) -> Optional[UUID]:
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return UUID(s)
    except ValueError:
        return None


def ingresar_o_crear_usuario() -> Optional[Usuario]:
    """
    Si no hay usuarios, ofrece crear el primero.
    Si hay usuarios, muestra menú para crear, ingresar o salir.
    Devuelve el Usuario logueado o None si elige salir.
    """

    if not crud_usuario.hay_usuarios():
        print("\n--- No hay usuarios en el sistema ---")
        print("Crea el primer usuario para poder entrar.\n")
        nombre = leer_texto("Nombre de usuario: ")
        if not nombre:
            print("Nombre obligatorio.")
            return None
        email = leer_texto("Email: ")
        if not email:
            print("Email obligatorio.")
            return None
        contra = leer_texto("Contraseña: ")
        if not contra:
            print("Contraseña obligatoria.")
            return None
        rol = leer_texto("Rol (por defecto 'admin'): ") or "admin"
        try:
            usuario_creado = crud_usuario.crear(
                nombre_usuario=nombre, email=email, contrasena=contra, rol=rol
            )
            print(
                f"\nUsuario '{usuario_creado.nombre_usuario}' creado. Inicia sesión.\n"
            )
            return usuario_creado
        except Exception as e:
            print("Error al crear usuario:", e)
            return None

    while True:
        print("\n--- Menú de Inicio ---")
        print("1. Ingresar  2. Crear usuario  3. Salir")
        op = leer_texto("Opción: ")

        if op == "1":
            # Ingresar
            while True:
                print("\n--- Inicio de sesión ---")
                nombre = leer_texto("Usuario: ")
                email = leer_texto("Email: ")
                contra = leer_texto("Contraseña: ")
                if not nombre or not email or not contra:
                    print("Todos los campos son obligatorios.\n")
                    continue
                usuario = crud_usuario.login(nombre, email, contra)
                if usuario:
                    print(f"\nBienvenido, {usuario.nombre_usuario} ({usuario.rol}).\n")
                    return usuario
                print("Usuario o contraseña incorrectos.\n")
                retry = leer_texto("¿Intentar de nuevo? (S/N): ").upper()
                if retry != "S":
                    break

        elif op == "2":
            # Crear usuario
            nombre = leer_texto("Nombre de usuario: ")
            if not nombre:
                print("Nombre obligatorio.")
                continue
            email = leer_texto("Email: ")
            if not email:
                print("Email obligatorio.")
                continue
            contra = leer_texto("Contraseña: ")
            if not contra:
                print("Contraseña obligatoria.")
                continue
            rol = leer_texto("Rol (por defecto 'user'): ") or "user"
            try:
                usuario_creado = crud_usuario.crear(
                    nombre_usuario=nombre, email=email, contrasena=contra, rol=rol
                )
                print(
                    f"\nUsuario '{usuario_creado.nombre_usuario}' creado exitosamente.\n"
                )
            except Exception as e:
                print(f"Error al crear usuario: {e}\n")

        elif op == "3":
            # Salir
            print("Saliendo del sistema.")
            return None

        else:
            print("Opción inválida. Por favor, intenta de nuevo.\n")


def menu_categorias(usuario_id: UUID) -> None:
    while True:
        print("\n--- Categorías ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            categorias = crud_categoria.obtener_todos()
            print(
                "  ID                                  | Nombre categoría           | Descripción"
            )
            print("  " + "-" * 36 + "+" + "-" * 26 + "+" + "-" * 30)
            if not categorias:
                print("  (sin categorías)")
            for c in categorias:
                id_str = str(c.id_categoria)
                nombre_str = c.nombre_categoria or ""
                desc_str = c.descripcion or "-"
                print(f"  {id_str:<36} | {nombre_str:<26} | {desc_str:<30}")
        elif op == "2":
            nombre = leer_texto("Nombre categoría: ")
            desc = leer_texto("Descripción (opcional): ")
            if nombre:
                try:
                    crud_categoria.crear(nombre, usuario_id, desc or None)
                    print("Categoría creada.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Nombre obligatorio.")
        elif op == "3":
            categorias = crud_categoria.obtener_todos()
            if not categorias:
                print("No hay categorías para actualizar.")
                continue
            print("Categorías disponibles:")
            for i, c in enumerate(categorias, 1):
                print(
                    f"{i}. ID: {c.id_categoria}, Nombre: {c.nombre_categoria}, Descripción: {c.descripcion or 'N/A'}"
                )
            try:
                num = int(leer_texto("Elige el número de la categoría: "))
                if num < 1 or num > len(categorias):
                    print("Número inválido.")
                    continue
                c = categorias[num - 1]
            except ValueError:
                print("Entrada inválida.")
                continue
            nombre = (
                leer_texto(f"Nuevo nombre (actual: {c.nombre_categoria}): ")
                or c.nombre_categoria
            )
            desc = leer_texto(f"Nueva descripción (actual: {c.descripcion or ''}): ")
            crud_categoria.actualizar(
                c.id_categoria,
                usuario_id,
                nombre_categoria=nombre,
                descripcion=desc if desc else c.descripcion,
            )
            print("Actualizado.")
        elif op == "4":
            categorias = crud_categoria.obtener_todos()
            if not categorias:
                print("No hay categorías para eliminar.")
                continue
            print("Categorías disponibles:")
            for i, c in enumerate(categorias, 1):
                print(f"{i}. ID: {c.id_categoria}, Nombre: {c.nombre_categoria}")
            try:
                num = int(leer_texto("Elige el número de la categoría a eliminar: "))
                if num < 1 or num > len(categorias):
                    print("Número inválido.")
                    continue
                c = categorias[num - 1]
                if crud_categoria.eliminar(c.id_categoria):
                    print("Eliminada.")
                else:
                    print("No se pudo eliminar (ID inválido o no existe).")
            except ValueError:
                print("Entrada inválida.")


def menu_productos(usuario_id: UUID) -> None:
    while True:
        print("\n--- Productos ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            productos = crud_producto.obtener_todos()
            print(
                "  ID                                   | Nombre producto           | Precio    | Stock | Categoria"
            )
            print(
                "  "
                + "-" * 36
                + "+"
                + "-" * 26
                + "+"
                + "-" * 10
                + "+"
                + "-" * 7
                + "+"
                + "-" * 11
            )
            if not productos:
                print("  (sin productos)")
            for p in productos:
                categoria_nombre = (
                    p.categoria.nombre_categoria
                    if getattr(p, "categoria", None)
                    else "N/A"
                )
                print(
                    f"  {str(p.id_producto):<36} | {p.nombre_producto:<26} | {p.precio:<9} | {p.stock:<5} | {categoria_nombre:<11}"
                )
        elif op == "2":
            nombre_producto = leer_texto("Nombre producto: ")
            nombre_categoria = leer_texto("Nombre categoría: ")
            precio = leer_float("Precio: ")
            stock = leer_int("Stock: ")
            descripcion_producto = leer_texto("Descripción (opcional): ")
            if not nombre_producto or not nombre_categoria:
                print("Nombre de producto y nombre de categoría son obligatorios.")
            else:
                categoria = None
                for c in crud_categoria.obtener_todos():
                    if c.nombre_categoria.lower() == nombre_categoria.strip().lower():
                        categoria = c
                        break
                if not categoria:
                    print(
                        f"Categoría '{nombre_categoria}' no existe. Crea primero la categoría."
                    )
                else:
                    try:
                        crud_producto.crear(
                            nombre_producto,
                            categoria.id_categoria,
                            usuario_id,
                            precio,
                            stock,
                            descripcion_producto or None,
                        )
                        print("Producto creado.")
                    except Exception as e:
                        print("Error:", e)

        elif op == "3":
            productos = crud_producto.obtener_todos()
            if not productos:
                print("No hay productos para actualizar.")
                continue
            print("Productos disponibles:")
            for i, p in enumerate(productos, 1):
                categoria_nombre = (
                    p.categoria.nombre_categoria
                    if getattr(p, "categoria", None)
                    else "N/A"
                )
                print(
                    f"{i}. ID: {p.id_producto}, Nombre: {p.nombre_producto}, Precio: {p.precio}, Stock: {p.stock}, Categoria: {categoria_nombre}"
                )
            try:
                num = int(leer_texto("Elige el número del producto: "))
                if num < 1 or num > len(productos):
                    print("Número inválido.")
                    continue
                p = productos[num - 1]
            except ValueError:
                print("Entrada inválida.")
                continue
            nombre_producto = (
                leer_texto(f"Nuevo nombre (actual: {p.nombre_producto}): ")
                or p.nombre_producto
            )
            precio = leer_float(f"Nuevo precio (actual: {p.precio}): ")
            if precio <= 0:
                precio = p.precio
            stock = leer_int(f"Nuevo stock (actual: {p.stock}): ")
            if stock < 0:
                stock = p.stock
            crud_producto.actualizar(
                p.id_producto,
                usuario_id,
                nombre_producto=nombre_producto,
                precio=precio,
                stock=stock,
            )
            print("Actualizado.")
        elif op == "4":
            productos = crud_producto.obtener_todos()
            if not productos:
                print("No hay productos para eliminar.")
                continue
            print("Productos disponibles:")
            for i, p in enumerate(productos, 1):
                print(f"{i}. ID: {p.id_producto}, Nombre: {p.nombre_producto}")
            try:
                num = int(leer_texto("Elige el número del producto a eliminar: "))
                if num < 1 or num > len(productos):
                    print("Número inválido.")
                    continue
                p = productos[num - 1]
                if crud_producto.eliminar(p.id_producto):
                    print("Eliminado.")
                else:
                    print("No se pudo eliminar.")
            except ValueError:
                print("Entrada inválida.")


def menu_pedidos(usuario_id: UUID) -> None:
    while True:
        print("\n--- Pedidos ---")
        print("1. Listar todos  2. Actualizar pedido  3. Crear  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            pedidos = crud_pedido.obtener_todos()
            print(
                "  ID                                   | Usuario                       | Total"
            )
            print("  " + "-" * 36 + "+" + "-" * 30 + "+" + "-" * 10)
            if not pedidos:
                print("  (sin pedidos)")
            for p in pedidos:
                print(
                    f"  {str(p.id_pedido):<36} | {str(p.id_usuario):<30} | {p.total_pagado:<10}"
                )
        elif op == "2":
            pedidos = crud_pedido.obtener_por_usuario(usuario_id)
            if not pedidos:
                print("No tienes pedidos para actualizar.")
                continue
            print("Pedidos disponibles:")
            for i, p in enumerate(pedidos, 1):
                print(
                    f"{i}. ID: {p.id_pedido}, Total: {p.total_pagado}, Fecha: {p.fecha_creacion}"
                )
            try:
                num = int(leer_texto("Elige el número del pedido: "))
                if num < 1 or num > len(pedidos):
                    print("Número inválido.")
                    continue
                pedido = pedidos[num - 1]
            except ValueError:
                print("Entrada inválida.")
                continue
            nuevo_total = leer_float(f"Nuevo total (actual: {pedido.total_pagado}): ")
            if nuevo_total < 0:
                print("Total inválido.")
                continue
            crud_pedido.actualizar(
                pedido.id_pedido,
                usuario_id,
                total_pagado=nuevo_total,
            )
            print("Pedido actualizado.")
        elif op == "3":
            total = leer_float("Total pagado: ")
            if total >= 0:
                try:
                    crud_pedido.crear(total, usuario_id, usuario_id)
                    print("Pedido creado.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Total debe ser >= 0.")
        elif op == "4":
            pedidos = crud_pedido.obtener_por_usuario(usuario_id)
            if not pedidos:
                print("No tienes pedidos para eliminar.")
                continue
            print("Pedidos disponibles:")
            for i, p in enumerate(pedidos, 1):
                print(
                    f"{i}. ID: {p.id_pedido}, Total: {p.total_pagado}, Fecha: {p.fecha_creacion}"
                )
            try:
                num = int(leer_texto("Elige el número del pedido a eliminar: "))
                if num < 1 or num > len(pedidos):
                    print("Número inválido.")
                    continue
                pedido = pedidos[num - 1]
                if crud_pedido.eliminar(pedido.id_pedido):
                    print("Eliminado.")
                else:
                    print("No se pudo eliminar.")
            except ValueError:
                print("Entrada inválida.")


def menu_pagos(usuario_id: UUID) -> None:
    while True:
        print("\n--- Pagos ---")
        print("1. Listar pagos  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            pagos = crud_pago.obtener_todos()
            print(
                "  ID                                   | Pedido                         | Metodo      | Monto      | Estado"
            )
            print(
                "  "
                + "-" * 36
                + "+"
                + "-" * 30
                + "+"
                + "-" * 12
                + "+"
                + "-" * 12
                + "+"
                + "-" * 10
            )
            if not pagos:
                print("  (sin pagos)")
            for p in pagos:
                print(
                    f"  {str(p.id_pago):<36} | {str(p.id_pedido):<30} | {p.metodo_pago:<10} | {p.monto_pagado:<10} | {p.estado_pago:<10}"
                )
        elif op == "2":
            pedidos = crud_pedido.obtener_por_usuario(usuario_id)
            if not pedidos:
                print("No tienes pedidos para asociar un pago.")
                continue
            print("Pedidos disponibles:")
            for i, p in enumerate(pedidos, 1):
                print(
                    f"{i}. ID: {p.id_pedido}, Total: {p.total_pagado}, Fecha: {p.fecha_creacion}"
                )
            try:
                num = int(leer_texto("Elige el número del pedido: "))
                if num < 1 or num > len(pedidos):
                    print("Número inválido.")
                    continue
                id_pedido = pedidos[num - 1].id_pedido
            except ValueError:
                print("Entrada inválida.")
                continue
            metodo = leer_texto("Método de pago: ")
            monto = leer_texto("Monto pagado: ")
            estado = leer_texto("Estado del pago: ")
            if not metodo or not monto or not estado:
                print("Método, monto y estado son obligatorios.")
                continue
            try:
                pago = crud_pago.crear(
                    id_pedido=id_pedido,
                    metodo_pago=metodo,
                    monto_pagado=monto,
                    estado_pago=estado,
                    id_usuario_creacion=usuario_id,
                )
                print(f"Pago creado: {pago.id_pago}")
            except Exception as e:
                print("Error creando pago:", e)
        elif op == "3":
            pagos = crud_pago.obtener_todos()
            if not pagos:
                print("No hay pagos para actualizar.")
                continue
            print("Pagos disponibles:")
            for i, p in enumerate(pagos, 1):
                print(
                    f"{i}. ID: {p.id_pago}, Pedido: {p.id_pedido}, Monto: {p.monto_pagado}, Estado: {p.estado_pago}"
                )
            try:
                num = int(leer_texto("Elige el número del pago: "))
                if num < 1 or num > len(pagos):
                    print("Número inválido.")
                    continue
                pago = pagos[num - 1]
            except ValueError:
                print("Entrada inválida.")
                continue
            metodo = (
                leer_texto(f"Nuevo método (actual: {pago.metodo_pago}): ")
                or pago.metodo_pago
            )
            monto = (
                leer_texto(f"Nuevo monto (actual: {pago.monto_pagado}): ")
                or pago.monto_pagado
            )
            estado = (
                leer_texto(f"Nuevo estado (actual: {pago.estado_pago}): ")
                or pago.estado_pago
            )
            crud_pago.actualizar(
                pago.id_pago,
                usuario_id,
                metodo_pago=metodo,
                monto_pagado=monto,
                estado_pago=estado,
            )
            print("Pago actualizado.")
        elif op == "4":
            pagos = crud_pago.obtener_todos()
            if not pagos:
                print("No hay pagos para eliminar.")
                continue
            print("Pagos disponibles:")
            for i, p in enumerate(pagos, 1):
                print(
                    f"{i}. ID: {p.id_pago}, Pedido: {p.id_pedido}, Método: {p.metodo_pago}, Monto: {p.monto_pagado}, Estado: {p.estado_pago}"
                )
            try:
                num = int(leer_texto("Elige el número del pago a eliminar: "))
                if num < 1 or num > len(pagos):
                    print("Número inválido.")
                    continue
                pago = pagos[num - 1]
                if crud_pago.eliminar(pago.id_pago):
                    print("Pago eliminado.")
                else:
                    print("No se pudo eliminar.")
            except ValueError:
                print("Entrada inválida.")
        else:
            print("Opción inválida.")


def menu_envios(usuario_id: UUID) -> None:
    while True:
        print("\n--- Envíos ---")
        print("1. Listar envíos  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            envios = crud_envio.obtener_todos()
            print(
                "  ID                                   | Pedido                         | Dirección                      | Estado      | Transportista"
            )
            print(
                "  "
                + "-" * 36
                + "+"
                + "-" * 30
                + "+"
                + "-" * 30
                + "+"
                + "-" * 12
                + "+"
                + "-" * 15
            )
            if not envios:
                print("  (sin envíos)")
            for e in envios:
                print(
                    f"  {str(e.id_envio):<36} | {str(e.id_pedido):<30} | {e.direccion_envio[:28]:<30} | {e.estado_envio:<10} | {(e.transportista or '-'):<15}"
                )
        elif op == "2":
            pedidos = crud_pedido.obtener_por_usuario(usuario_id)
            if not pedidos:
                print("No tienes pedidos para asociar un envío.")
                continue
            print("Pedidos disponibles:")
            for i, p in enumerate(pedidos, 1):
                print(
                    f"{i}. ID: {p.id_pedido}, Total: {p.total_pagado}, Fecha: {p.fecha_creacion}"
                )
            try:
                num = int(leer_texto("Elige el número del pedido: "))
                if num < 1 or num > len(pedidos):
                    print("Número inválido.")
                    continue
                id_pedido = pedidos[num - 1].id_pedido
            except ValueError:
                print("Entrada inválida.")
                continue
            direccion = leer_texto("Dirección de envío: ")
            estado = leer_texto("Estado del envío: ")
            transportista = leer_texto("Transportista (opcional): ")
            if not direccion or not estado:
                print("Dirección y estado son obligatorios.")
                continue
            try:
                envio = crud_envio.crear(
                    id_pedido=id_pedido,
                    direccion_envio=direccion,
                    estado_envio=estado,
                    transportista=transportista or None,
                    id_usuario_creacion=usuario_id,
                )
                print(f"Envío creado: {envio.id_envio}")
            except Exception as e:
                print("Error creando envío:", e)
        elif op == "3":
            envios = crud_envio.obtener_todos()
            if not envios:
                print("No hay envíos para actualizar.")
                continue
            print("Envíos disponibles:")
            for i, e in enumerate(envios, 1):
                print(
                    f"{i}. ID: {e.id_envio}, Pedido: {e.id_pedido}, Dirección: {e.direccion_envio}, Estado: {e.estado_envio}, Transportista: {e.transportista or 'N/A'}"
                )
            try:
                num = int(leer_texto("Elige el número del envío: "))
                if num < 1 or num > len(envios):
                    print("Número inválido.")
                    continue
                envio = envios[num - 1]
            except ValueError:
                print("Entrada inválida.")
                continue
            direccion = (
                leer_texto(f"Nueva dirección (actual: {envio.direccion_envio}): ")
                or envio.direccion_envio
            )
            estado = (
                leer_texto(f"Nuevo estado (actual: {envio.estado_envio}): ")
                or envio.estado_envio
            )
            transportista = (
                leer_texto(
                    f"Nuevo transportista (actual: {envio.transportista or ''}): "
                )
                or envio.transportista
            )
            crud_envio.actualizar(
                envio.id_envio,
                usuario_id,
                direccion_envio=direccion,
                estado_envio=estado,
                transportista=transportista,
            )
            print("Envío actualizado.")
        elif op == "4":
            envios = crud_envio.obtener_todos()
            if not envios:
                print("No hay envíos para eliminar.")
                continue
            print("Envíos disponibles:")
            for i, e in enumerate(envios, 1):
                print(
                    f"{i}. ID: {e.id_envio}, Pedido: {e.id_pedido}, Dirección: {e.direccion_envio}, Estado: {e.estado_envio}, Transportista: {e.transportista or 'N/A'}"
                )
            try:
                num = int(leer_texto("Elige el número del envío a eliminar: "))
                if num < 1 or num > len(envios):
                    print("Número inválido.")
                    continue
                envio = envios[num - 1]
                if crud_envio.eliminar(envio.id_envio):
                    print("Envío eliminado.")
                else:
                    print("No se pudo eliminar.")
            except ValueError:
                print("Entrada inválida.")
        else:
            print("Opción inválida.")


def main() -> None:
    usuario = ingresar_o_crear_usuario()
    if not usuario:
        print("No se pudo iniciar sesión. Saliendo.")
        return

    while True:
        print("\n========== Menú principal ==========")
        print("1. Categorías  2. Productos  3. Pedidos  4. Pagos  5. Envíos  0. Salir")
        op = leer_texto("Opción: ")
        if op == "0":
            print(f"Hasta luego {usuario.nombre_usuario}.")
            break
        if op == "1":
            menu_categorias(usuario.id_usuario)
        elif op == "2":
            menu_productos(usuario.id_usuario)
        elif op == "3":
            menu_pedidos(usuario.id_usuario)
        elif op == "4":
            menu_pagos(usuario.id_usuario)
        elif op == "5":
            menu_envios(usuario.id_usuario)
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
