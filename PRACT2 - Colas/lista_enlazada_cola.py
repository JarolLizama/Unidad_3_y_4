# ============================================================
#  cola.py  –  Implementación de una Cola con lista enlazada
# ============================================================


# --------------------------------------------------------------
#  Clase Node
# --------------------------------------------------------------

class Node:
    """Nodo de la lista enlazada. Guarda el objeto y un puntero al siguiente nodo."""

    def __init__(self, info):
        self.info = info      # Objeto almacenado en el nodo
        self.next = None      # Referencia al siguiente nodo (None si es el último)

    def get_info(self):
        return self.info

    def get_next(self):
        return self.next

    def set_next(self, next_node):
        self.next = next_node


# --------------------------------------------------------------
#  Clase Order (traducción directa del Java del enunciado)
# --------------------------------------------------------------

class Order:
    """Representa un pedido con cliente y cantidad de producto."""

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


# --------------------------------------------------------------
#  Clase Queue  (implementa la interfaz QueueInterface del enunciado)
# --------------------------------------------------------------

class Queue:
    """
    Cola (FIFO) implementada sobre una lista enlazada.

    Atributos internos:
        _top   – Puntero a la cabeza (primer elemento en salir).
        _tail  – Puntero al último nodo (donde se insertan nuevos elementos).
        _size  – Número de elementos en la cola.

    Métodos públicos:
        size()           – Número de elementos.
        is_empty()       – True si la cola está vacía.
        front()          – Primer elemento sin extraerlo (None si vacía).
        enqueue(info)    – Añade un elemento al final.
        dequeue()        – Extrae y devuelve el primer elemento (None si vacía).
        get_nth(pos)     – Devuelve el n-ésimo elemento sin borrarlo (None si inválido).
        print_info()     – Muestra el contenido completo de la cola.
    """

    def __init__(self):
        self._top = None    # Cabeza de la cola (extracción)
        self._tail = None   # Cola de la cola (inserción)
        self._size = 0

    # ----------------------------------------------------------
    def size(self) -> int:
        """Devuelve el número de elementos en la cola."""
        return self._size

    # ----------------------------------------------------------
    def is_empty(self) -> bool:
        """True si la cola no contiene ningún elemento."""
        return self._top is None

    # ----------------------------------------------------------
    def front(self):
        """
        Devuelve el primer elemento SIN extraerlo.
        Devuelve None si la cola está vacía.
        """
        if self.is_empty():
            return None
        return self._top.get_info()

    # ----------------------------------------------------------
    def enqueue(self, info):
        """Añade un nuevo elemento al final de la cola."""
        new_node = Node(info)
        if self.is_empty():
            # La cola estaba vacía: top y tail apuntan al mismo nodo
            self._top = new_node
            self._tail = new_node
        else:
            # Enlazamos el nuevo nodo tras el último y actualizamos tail
            self._tail.set_next(new_node)
            self._tail = new_node
        self._size += 1

    # ----------------------------------------------------------
    def dequeue(self):
        """
        Extrae y devuelve el primer elemento.
        Devuelve None si la cola está vacía.
        """
        if self.is_empty():
            return None
        info = self._top.get_info()
        self._top = self._top.get_next()   # Avanzamos la cabeza
        if self._top is None:
            # La cola quedó vacía; tail también debe resetearse
            self._tail = None
        self._size -= 1
        return info

    # ----------------------------------------------------------
    def get_nth(self, pos: int):
        """
        Devuelve el n-ésimo elemento (base 1) sin eliminarlo.
        Devuelve None si la posición no es válida.
        """
        if pos < 1 or pos > self._size:
            return None
        node = self._top
        for _ in range(pos - 1):       # Avanzamos (pos-1) veces
            node = node.get_next()
        return node.get_info()

    # ----------------------------------------------------------
    def print_info(self):
        """Muestra en consola el número de elementos y el detalle de cada uno."""
        print("********* QUEUE DUMP *********")
        print(f"   Size: {self._size}")
        node = self._top
        count = 1
        while node is not None:
            print(f"   ** Element {count}")
            # Si el objeto almacenado es un Order, usamos su método print_info
            if hasattr(node.get_info(), "print_info"):
                node.get_info().print_info()
            else:
                print(f"     Value: {node.get_info()}")
                print( "     ------------")
            node = node.get_next()
            count += 1
        print("******************************")


# ==============================================================
#  TestQueue – clase de prueba (equivalente al main de Java)
# ==============================================================

if __name__ == "__main__":
    cola = Queue()

    # --- Creamos los pedidos ---
    o1 = Order(20, "cust1")
    o2 = Order(30, "cust2")
    o3 = Order(40, "cust3")
    o4 = Order(50, "cust3")

    # --- Insertamos en la cola ---
    print(">> enqueue(o1)")
    cola.enqueue(o1)
    cola.print_info()

    print(">> enqueue(o2)")
    cola.enqueue(o2)
    cola.print_info()

    print(">> enqueue(o3)")
    cola.enqueue(o3)
    cola.print_info()

    print(">> enqueue(o4)")
    cola.enqueue(o4)
    cola.print_info()

    # --- Probamos front (no extrae) ---
    print(">> front()  →  Customer:", cola.front().get_customer())
    cola.print_info()

    # --- Probamos dequeue (extrae el primero) ---
    extraido = cola.dequeue()
    print(f">> dequeue() → Customer: {extraido.get_customer()}, Quantity: {extraido.get_qtty()}")
    cola.print_info()

    # --- Probamos get_nth ---
    # La cola ahora tiene 3 elementos (o2, o3, o4); pedimos el 2.º
    tercero = cola.get_nth(2)
    if tercero:
        print(f">> get_nth(2) → Customer: {tercero.get_customer()}, Quantity: {tercero.get_qtty()}")
    else:
        print(">> get_nth(2) → posición no válida")

    # Posición fuera de rango
    invalido = cola.get_nth(10)
    print(f">> get_nth(10) → {invalido}")   # None