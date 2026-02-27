class Electronicos:
    def __init__(self, tipo_articulo: str, marca: str, modelo: str, cantidad: int):
        self.tipo_articulo = tipo_articulo
        self.marca = marca
        self.modelo = modelo
        self.cantidad = cantidad

    def imprimir_datos(self) -> None:
        print(f"Tipo de artículo: {self.tipo_articulo}")
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")
        print(f"Cantidad: {self.cantidad}")
