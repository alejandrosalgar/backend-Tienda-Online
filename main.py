from clases.alimentos import Alimentos
from clases.electronicos import Electronicos
from clases.ropa import Ropa

carrito = []


def menu():
    print("\n------------------------------")
    print("        TIENDA ONLINE")
    print("------------------------------")
    print("1. Agregar producto")
    print("2. Ver carrito")
    print("3. Salir")
    print("------------------------------")


def calcular_total():
    total = 0
    for producto in carrito:
        total += producto.cantidad * producto.precio
    return total


def aplicar_descuento(total):
    """
    Aplica 10% de descuento si el total es mayor o igual a 200000
    """
    if total >= 200000:
        return total * 0.9
    return total


def ver_carrito():
    if len(carrito) == 0:
        print("\nEl carrito está vacío.\n")
    else:
        print("\nProductos en el carrito:\n")

        for i, producto in enumerate(carrito, start=1):
            print(f"\nProducto #{i}")
            producto.imprimir_datos()
            print("----------------------")

        subtotal = calcular_total()
        total_final = aplicar_descuento(subtotal)

        print(f"\nSubtotal: ${subtotal}")
        print(f"Total con descuento: ${total_final}\n")


def main():
    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nCategorías:")
            print("1. Electrónicos")
            print("2. Ropa")
            print("3. Alimentos")

            categoria = input("Seleccione categoría: ")

            if categoria == "1":
                tipo = input("Tipo de artículo: ")
                marca = input("Marca: ")
                modelo = input("Modelo: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio unitario: "))

                producto = Electronicos(tipo, marca, modelo, cantidad, precio)
                producto.agregar_producto_al_carrito(carrito)

            elif categoria == "2":
                tipo = input("Tipo de prenda: ")
                genero = input("Género: ")
                color = input("Color: ")
                marca = input("Marca: ")
                talla = input("Talla: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio unitario: "))

                producto = Ropa(tipo, genero, color, marca, talla, cantidad, precio)
                producto.agregar_producto_al_carrito(carrito)

            elif categoria == "3":
                tipo = input("Tipo de alimento: ")
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio unitario: "))

                producto = Alimentos(tipo, nombre, cantidad, precio)
                producto.agregar_producto_al_carrito(carrito)

            else:
                print("Categoría no válida")

        elif opcion == "2":
            ver_carrito()

        elif opcion == "3":
            print("\nGracias por usar la tienda.")
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    main()
