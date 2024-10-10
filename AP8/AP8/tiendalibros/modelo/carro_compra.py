from .item_compra import ItemCompra


class CarroCompras:
    def __init__(self):
        self.items = []

    def agregar_item(self, libro, cantidad: int):
        item = ItemCompra(libro, cantidad)
        self.items.append(item)
        return item

    def calcular_total(self):
        total = sum(item.calcular_subtotal() for item in self.items)
        return total

    def quitar_item(self, isbn: str):
        self.items = [item for item in self.items if item.libro.isbn == isbn]
