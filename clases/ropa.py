class Ropa:
    def __init__(self, color: str, marca: str):
        self.color = color
        self.marca = marca

    def imprimir_datos(self) -> None:
        print(f"el color de la ropa es {self.color} y la marca es {self.marca}")


ropa1 = Ropa("azul", "cualquiera")
ropa1.imprimir_datos()
