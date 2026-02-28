class Alimentos:
    """Clase para representar un alimento."""

    def __init__(self, tipo_alimento: str, nombre: str, cantidad: int):
        self.tipo_alimento = tipo_alimento
        self.nombre = nombre
        self.cantidad = cantidad

    def imprimir_datos(self) -> None:
        print(f"Tipo de alimento: {self.tipo_alimento}")
        print(f"Nombre: {self.nombre}")
        print(f"Cantidad: {self.cantidad}")

    def agregar_producto_al_carrito(self, carrito):
        """Agrega el producto al carrito"""
        carrito.append(self)
        print("\nProducto agregado al carrito.\n")
