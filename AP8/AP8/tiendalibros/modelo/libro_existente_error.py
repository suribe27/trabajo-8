from tiendalibros.modelo.libro_error import LibroError

class LibroExistenteError(LibroError):
    def __init__(self, libro):
        super().__init__(libro)

    def __str__(self):
        return f"El libro con título '{self.libro.titulo}' y isbn: '{self.libro.isbn}' ya existe en el catálogo"
