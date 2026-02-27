class Alimentos:
    def __init__(self, tipo_alimento: str, nombre: str, cantidad: int):
        self.tipo_alimento = tipo_alimento
        self.nombre = nombre
        self.cantidad = cantidad

    def imprimir_datos(self) -> None:
        print(f"Tipo de alimento: {self.tipo_alimento}")
        print(f"Nombre: {self.nombre}")
        print(f"Cantidad: {self.cantidad}")
