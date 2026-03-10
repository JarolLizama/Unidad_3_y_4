class Cola:
    def __init__(self):
        self.elementos = []

    def encolar(self, valor):
        self.elementos.append(valor)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.elementos.pop(0)

    def esta_vacia(self):
        return len(self.elementos) == 0

    def tamanio(self):
        return len(self.elementos)

    def __str__(self):
        return str(self.elementos)


def sumar_colas(cola_a, cola_b):
    
    resultado = Cola()

    while not cola_a.esta_vacia() and not cola_b.esta_vacia():
        suma = cola_a.desencolar() + cola_b.desencolar()
        resultado.encolar(suma)

    while not cola_a.esta_vacia():
        resultado.encolar(cola_a.desencolar())

    while not cola_b.esta_vacia():
        resultado.encolar(cola_b.desencolar())

    return resultado


if __name__ == "__main__":
    cola_a = Cola()
    cola_b = Cola()

    for valor in [3, 4, 2, 8, 12]:
        cola_a.encolar(valor)

    for valor in [6, 2, 9, 11, 3]:
        cola_b.encolar(valor)

    print("Cola A:         ", cola_a)
    print("Cola B:         ", cola_b)

    cola_resultado = sumar_colas(cola_a, cola_b)

    print("Cola Resultado: ", cola_resultado)
