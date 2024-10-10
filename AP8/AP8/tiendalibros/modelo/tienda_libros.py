from tiendalibros.modelo.carro_compra import CarroCompras
from libro import Libro
from libro_existente_error import LibroExistenteError
from libro_agotado_error import LibroAgotadoError
from existencias_insuficientes_error import ExistenciasInsuficientesError

class TiendaLibros:
    def __init__(self):
        self.catalogo = {}
        self.carrito = CarroCompras()

    def adicionar_libro_a_catalogo(self, isbn: str, titulo: str, precio: float, existencias: int) -> Libro:
        if isbn in self.catalogo:
            raise LibroExistenteError(self.catalogo[isbn])
        
        libro = Libro(isbn, titulo, precio, existencias)
        self.catalogo[isbn] = libro
        return libro

    def agregar_libro_a_carrito(self, libro: Libro, cantidad: int):
        if libro.existencias <= 0:
            raise LibroAgotadoError(libro)  # Lanza excepción si no hay existencias

        if cantidad > libro.existencias:
            raise ExistenciasInsuficientesError(libro, cantidad)  # Lanza excepción si no hay suficientes existencias

        # Agrega el libro al carrito
        self.carrito.agregar_item(libro, cantidad)

    def retirar_item_de_carrito(self, isbn: str):
        self.carrito.quitar_item(isbn)




    
    # Defina metodo retirar_item_de_carrito
