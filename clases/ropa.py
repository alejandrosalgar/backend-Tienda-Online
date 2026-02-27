class Ropa:
    def __init__(
        self,
        tipo_prenda: str,
        genero: str,
        color: str,
        marca: str,
        talla: str,
        cantidad: int,
    ):
        self.tipo_prenda = tipo_prenda
        self.genero = genero
        self.color = color
        self.marca = marca
        self.talla = talla
        self.cantidad = cantidad

    def imprimir_datos(self) -> None:
        print(f"Tipo de prenda: {self.tipo_prenda}")
        print(f"Género: {self.genero}")
        print(f"Color: {self.color}")
        print(f"Marca: {self.marca}")
        print(f"Talla: {self.talla}")
        print(f"Cantidad: {self.cantidad}")

    def agregar_producto_al_carrito(self, carrito):
        """Agrega el producto al carrito."""
        carrito.append(self)
        print("\nProducto agregado al carrito.\n")
