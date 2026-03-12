# ============================================================
#  cola_interactiva.py  –  Cola con menú interactivo
# ============================================================


class Node:
    """Nodo de la lista enlazada."""

    def __init__(self, info):
        self.info = info
        self.next = None

    def get_info(self):
        return self.info

    def get_next(self):
        return self.next

    def set_next(self, next_node):
        self.next = next_node


class Order:
    """Representa un pedido con cliente y cantidad."""

    def __init__(self, qtty: int, customer: str):
        self.customer = customer
        self.qtty = qtty

    def print_info(self):
        print(f"     Customer: {self.customer}")
        print(f"     Quantity: {self.qtty}")
        print( "     ------------")

    def get_qtty(self):
        return self.qtty

    def get_customer(self):
        return self.customer


class Queue:
    """Cola FIFO implementada con lista enlazada."""

    def __init__(self):
        self._top = None
        self._tail = None
        self._size = 0

    def size(self):
        return self._size

    def is_empty(self):
        return self._top is None

    def front(self):
        if self.is_empty():
            return None
        return self._top.get_info()

    def enqueue(self, info):
        """Añade un elemento al final de la cola."""
        new_node = Node(info)
        if self.is_empty():
            self._top = new_node
            self._tail = new_node
        else:
            self._tail.set_next(new_node)
            self._tail = new_node
        self._size += 1

    def dequeue(self):
        """Extrae y devuelve el primer elemento. None si está vacía."""
        if self.is_empty():
            return None
        info = self._top.get_info()
        self._top = self._top.get_next()
        if self._top is None:
            self._tail = None
        self._size -= 1
        return info

    def get_nth(self, pos: int):
        """Devuelve el n-ésimo elemento sin borrarlo. None si posición inválida."""
        if pos < 1 or pos > self._size:
            return None
        node = self._top
        for _ in range(pos - 1):
            node = node.get_next()
        return node.get_info()

    def print_info(self):
        """Muestra el contenido completo de la cola."""
        if self.is_empty():
            print("\n  [ La cola está vacía ]")
            return
        print("\n********* QUEUE DUMP *********")
        print(f"   Size: {self._size}")
        node = self._top
        count = 1
        while node is not None:
            print(f"   ** Element {count}")
            node.get_info().print_info()
            node = node.get_next()
            count += 1
        print("******************************\n")


# ============================================================
#  Funciones del menú
# ============================================================

def pedir_entero(mensaje: str) -> int:
    """Pide un número entero al usuario, repitiendo si el input no es válido."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("  ⚠ Por favor, introduce un número entero.")


def insertar_n_pedidos(cola: Queue):
    """Pregunta cuántos pedidos insertar y los añade uno a uno."""
    n = pedir_entero("¿Cuántos pedidos quieres insertar? ")
    for i in range(1, n + 1):
        print(f"\n  -- Pedido {i} --")
        customer = input("  Nombre del cliente: ").strip()
        qtty = pedir_entero("  Cantidad: ")
        cola.enqueue(Order(qtty, customer))
        print(f"  ✔ Pedido de '{customer}' añadido a la cola.")
    cola.print_info()


def eliminar_n_pedidos(cola: Queue):
    """Pregunta cuántos pedidos eliminar y los extrae del frente."""
    if cola.is_empty():
        print("\n  ⚠ La cola está vacía, no hay nada que eliminar.")
        return
    n = pedir_entero(f"¿Cuántos pedidos quieres eliminar? (hay {cola.size()}): ")
    if n <= 0:
        print("  ⚠ Debes indicar al menos 1.")
        return
    eliminados = 0
    for _ in range(n):
        order = cola.dequeue()
        if order is None:
            print("  ⚠ La cola se vació antes de completar las eliminaciones.")
            break
        print(f"  ✔ Eliminado → Customer: {order.get_customer()}, Quantity: {order.get_qtty()}")
        eliminados += 1
    print(f"\n  Se eliminaron {eliminados} pedido(s).")
    cola.print_info()


def ver_nesimo(cola: Queue):
    """Muestra el n-ésimo elemento sin eliminarlo."""
    if cola.is_empty():
        print("\n  ⚠ La cola está vacía.")
        return
    pos = pedir_entero(f"¿Qué posición quieres consultar? (1 a {cola.size()}): ")
    order = cola.get_nth(pos)
    if order is None:
        print(f"  ⚠ Posición {pos} no válida.")
    else:
        print(f"\n  Elemento en posición {pos}:")
        order.print_info()


def ver_primero(cola: Queue):
    """Muestra el primer elemento sin extraerlo."""
    order = cola.front()
    if order is None:
        print("\n  ⚠ La cola está vacía.")
    else:
        print(f"\n  Primer elemento (front):")
        order.print_info()


# ============================================================
#  Menú principal
# ============================================================

def menu():
    cola = Queue()

    opciones = {
        "1": ("Insertar N pedidos",    lambda: insertar_n_pedidos(cola)),
        "2": ("Eliminar N pedidos",    lambda: eliminar_n_pedidos(cola)),
        "3": ("Ver primer elemento",   lambda: ver_primero(cola)),
        "4": ("Ver n-ésimo elemento",  lambda: ver_nesimo(cola)),
        "5": ("Ver cola completa",     lambda: cola.print_info()),
        "6": ("Salir",                 None),
    }

    while True:
        print("\n========== MENÚ COLA ==========")
        for clave, (desc, _) in opciones.items():
            print(f"  {clave}. {desc}")
        print("================================")

        opcion = input("Elige una opción: ").strip()

        if opcion == "6":
            print("Saliendo... ¡hasta luego!")
            break
        elif opcion in opciones:
            _, accion = opciones[opcion]
            accion()
        else:
            print("  ⚠ Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
