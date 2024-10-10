from tiendalibros.modelo.libro_error import LibroError

class ExistenciasInsuficientesError(LibroError):
    def __init__(self, libro, cantidad_a_comprar: int):
        super().__init__(libro)  # Llama al inicializador de la clase padre
        self.cantidad_a_comprar = cantidad_a_comprar  # Asigna la cantidad a comprar

    def __str__(self):
        return (f"El libro con título '{self.libro.titulo}' y ISBN '{self.libro.isbn}' "
                f"no tiene suficientes existencias para realizar la compra: "
                f"cantidad a comprar: {self.cantidad_a_comprar}, "
                f"existencias: {self.libro.existencias}.")



    # Defina metodo inicializador

    # Defina metodo espcial
