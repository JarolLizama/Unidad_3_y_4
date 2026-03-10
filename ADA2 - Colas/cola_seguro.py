class Cola:
    def __init__(self):
        self.elementos = []

    def encolar(self, valor):
        self.elementos.append(valor)

    def desencolar(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop(0)

    def esta_vacia(self):
        return len(self.elementos) == 0

    def tamanio(self):
        return len(self.elementos)

    def __str__(self):
        return str(self.elementos)


class SistemaAtencion:
    """
    Maneja múltiples colas de servicio para una compañía de seguros.

    Comandos:
        C <numero_servicio>  → Llega un cliente al servicio indicado.
                               El sistema le asigna y muestra su número de atención.
        A <numero_servicio>  → El personal atiende al siguiente cliente
                               del servicio indicado.
                               El sistema muestra el número llamado.
        S                   → Muestra el estado de todas las colas.
        Q                   → Sale del programa.
    """

    def __init__(self, servicios: list):
        # Crea una Cola independiente por cada servicio
        self.colas = {str(s): Cola() for s in servicios}
        # Contador de turnos por servicio
        self.contadores = {str(s): 0 for s in servicios}

    def cliente_llega(self, servicio: str):
        servicio = str(servicio)
        if servicio not in self.colas:
            print(f"  ✗ El servicio '{servicio}' no existe.")
            return

        self.contadores[servicio] += 1
        turno = self.contadores[servicio]
        # Formato de número: S<servicio>-<turno con 3 dígitos>  ej. S1-001
        numero_atencion = f"S{servicio}-{turno:03d}"
        self.colas[servicio].encolar(numero_atencion)
        print(f"  Cliente registrado en servicio {servicio}. "
              f"Su número de atención es: {numero_atencion}")

    def atender_cliente(self, servicio: str):
        servicio = str(servicio)
        if servicio not in self.colas:
            print(f"  ✗ El servicio '{servicio}' no existe.")
            return

        if self.colas[servicio].esta_vacia():
            print(f"  ℹ No hay clientes en espera para el servicio {servicio}.")
            return

        numero = self.colas[servicio].desencolar()
        print(f"  >>> Llamando número: {numero}  (Servicio {servicio}) <<<")

    def mostrar_estado(self):
        print("\n  ── Estado de las colas ──────────────────")
        for servicio, cola in self.colas.items():
            if cola.esta_vacia():
                estado = "(vacía)"
            else:
                estado = str(cola)
            print(f"  Servicio {servicio}: {estado}")
        print("  ─────────────────────────────────────────\n")

    def ejecutar(self):
        print("=" * 52)
        print("  SISTEMA DE ATENCIÓN - COMPAÑÍA DE SEGUROS")
        print("=" * 52)
        print("  Servicios disponibles:", list(self.colas.keys()))
        print("  Comandos:")
        print("    C <servicio>  → Registrar llegada de cliente")
        print("    A <servicio>  → Atender siguiente cliente")
        print("    S             → Ver estado de las colas")
        print("    Q             → Salir")
        print("=" * 52)

        while True:
            entrada = input("\nIngrese comando: ").strip().upper()

            if not entrada:
                continue

            partes = entrada.split()
            comando = partes[0]

            if comando == "Q":
                print("  Sistema cerrado. ¡Hasta luego!")
                break

            elif comando == "S":
                self.mostrar_estado()

            elif comando == "C":
                if len(partes) < 2:
                    print("  ✗ Uso: C <numero_servicio>")
                else:
                    self.cliente_llega(partes[1])

            elif comando == "A":
                if len(partes) < 2:
                    print("  ✗ Uso: A <numero_servicio>")
                else:
                    self.atender_cliente(partes[1])

            else:
                print("  ✗ Comando no reconocido. Use C, A, S o Q.")


# ── Punto de entrada ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Define los servicios disponibles (pueden ser números o letras)
    servicios_disponibles = [1, 2, 3]
    sistema = SistemaAtencion(servicios_disponibles)
    sistema.ejecutar()