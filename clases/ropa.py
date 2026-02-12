class Ropa:
    def __init__(self, color: str, marca: str, cantidad: int):
        self.color = color
        self.marca = marca
        self.cantidad = cantidad

    def imprimir_datos(self) -> None:
        print(f"el color de la ropa es {self.color} y la marca es {self.marca}")


ropa1 = Ropa("azul", "cualquiera")
ropa1.imprimir_datos()
