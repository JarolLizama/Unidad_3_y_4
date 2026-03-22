"""
╔══════════════════════════════════════════════════════════════════╗
║           MyLinkedList — Visualizador Educativo                  ║
║                                                                  ║
║  ¿Qué es una Linked List (Lista Enlazada)?                       ║
║  Es una estructura de datos donde cada elemento (NODO) guarda:   ║
║    1. El DATO  → el valor que almacena (ej: 10, "hola")          ║
║    2. El PUNTERO → una "flecha" que apunta al siguiente nodo     ║
║                                                                  ║
║  Se ve así en memoria:                                           ║
║  HEAD → [10|→] → [20|→] → [30|→] → [40|None]                   ║
║                                                                  ║
║  HEAD = cabeza = primer nodo de la lista                         ║
║  None = el último nodo no apunta a nadie (fin de la lista)       ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
import time


# ══════════════════════════════════════════════════════════════════
#   PARTE 1: EL NODO
#   Un Nodo es la "caja" más pequeña de la lista.
#   Cada caja tiene: un dato y un puntero al siguiente.
# ══════════════════════════════════════════════════════════════════

class Nodo:
    """
    Representa UNA casilla de la lista enlazada.

    Ejemplo visual de un Nodo con dato=42:
    ┌────────┬──────────┐
    │  dato  │siguiente │
    │   42   │  →Nodo   │
    └────────┴──────────┘
    """
    def __init__(self, dato):
        self.dato = dato        # El valor que guarda este nodo
        self.siguiente = None   # Puntero al próximo nodo (None = no hay siguiente)


# ══════════════════════════════════════════════════════════════════
#   PARTE 2: LA LISTA ENLAZADA
#   La lista solo guarda la "cabeza" (primer nodo).
#   Para llegar a cualquier nodo, hay que recorrer desde la cabeza.
# ══════════════════════════════════════════════════════════════════

class MyLinkedList:
    """Lista Enlazada Simple."""

    def __init__(self):
        self.cabeza = None   # Al inicio la lista está vacía (sin cabeza)
        self._tamano = 0     # Contador de nodos

    # ──────────────────────────────────────────
    # INSERTAR AL INICIO  — O(1): muy rápido
    # ──────────────────────────────────────────
    def insertar_al_inicio(self, dato):
        """
        Crea un nodo nuevo y lo pone ANTES de la cabeza actual.

        Antes:   HEAD → [20] → [30] → None
        Nuevo:           [10]
        Después: HEAD → [10] → [20] → [30] → None

        Pasos:
          1. Crear el nuevo nodo
          2. Hacer que el nuevo apunte a quien era la cabeza
          3. La cabeza ahora es el nuevo nodo
        """
        nuevo = Nodo(dato)             # Paso 1: crear nodo
        nuevo.siguiente = self.cabeza  # Paso 2: nuevo → antigua cabeza
        self.cabeza = nuevo            # Paso 3: la cabeza es el nuevo nodo
        self._tamano += 1

    # ──────────────────────────────────────────
    # INSERTAR AL FINAL  — O(n): hay que recorrer
    # ──────────────────────────────────────────
    def insertar_al_final(self, dato):
        """
        Recorre TODA la lista hasta el último nodo y agrega ahí.

        Antes:   HEAD → [10] → [20] → None
        Después: HEAD → [10] → [20] → [30] → None

        Pasos:
          1. Crear el nuevo nodo
          2. Si la lista está vacía, el nuevo ES la cabeza
          3. Si no, recorrer hasta el último y apuntarlo al nuevo
        """
        nuevo = Nodo(dato)  # Paso 1

        if self.cabeza is None:        # Paso 2: lista vacía
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:  # Paso 3: llegar al final
                actual = actual.siguiente
            actual.siguiente = nuevo   # el último ahora apunta al nuevo
        self._tamano += 1

    # ──────────────────────────────────────────
    # INSERTAR EN POSICIÓN  — O(n)
    # ──────────────────────────────────────────
    def insertar_en_posicion(self, dato, posicion):
        """
        Para insertar entre dos nodos A y B:
          Antes:  A → B
          Nuevo:  A → NUEVO → B

        Pasos:
          1. Llegar al nodo ANTERIOR a la posición deseada
          2. El nuevo apunta al que era siguiente de ese anterior
          3. El anterior apunta al nuevo
        """
        if posicion < 0 or posicion > self._tamano:
            raise IndexError(
                f"Posición {posicion} no existe "
                f"(la lista tiene {self._tamano} nodos, índices 0..{self._tamano})."
            )
        if posicion == 0:
            self.insertar_al_inicio(dato)
            return

        nuevo = Nodo(dato)
        actual = self.cabeza
        for _ in range(posicion - 1):   # Paso 1: llegar al anterior
            actual = actual.siguiente

        nuevo.siguiente = actual.siguiente  # Paso 2
        actual.siguiente = nuevo            # Paso 3
        self._tamano += 1

    # ──────────────────────────────────────────
    # ELIMINAR AL INICIO  — O(1)
    # ──────────────────────────────────────────
    def eliminar_al_inicio(self):
        """
        Quita el primer nodo y mueve la cabeza al siguiente.

        Antes:   HEAD → [10] → [20] → [30]
        Después: HEAD → [20] → [30]

        Pasos:
          1. Guardar el dato del primer nodo
          2. Mover la cabeza al segundo nodo
        """
        if self.cabeza is None:
            raise IndexError("La lista está vacía, no hay nada que eliminar.")
        dato = self.cabeza.dato                  # Paso 1
        self.cabeza = self.cabeza.siguiente      # Paso 2
        self._tamano -= 1
        return dato

    # ──────────────────────────────────────────
    # ELIMINAR AL FINAL  — O(n)
    # ──────────────────────────────────────────
    def eliminar_al_final(self):
        """
        Recorre hasta el penúltimo y le corta el enlace al último.

        Antes:   [10] → [20] → [30] → None
        Después: [10] → [20] → None

        Pasos:
          1. Recorrer hasta el nodo PENÚLTIMO
          2. Guardar el dato del último
          3. El penúltimo ahora apunta a None
        """
        if self.cabeza is None:
            raise IndexError("La lista está vacía.")

        if self.cabeza.siguiente is None:  # Solo hay un nodo
            dato = self.cabeza.dato
            self.cabeza = None
            self._tamano -= 1
            return dato

        actual = self.cabeza
        while actual.siguiente.siguiente is not None:  # Paso 1
            actual = actual.siguiente

        dato = actual.siguiente.dato   # Paso 2
        actual.siguiente = None        # Paso 3
        self._tamano -= 1
        return dato

    # ──────────────────────────────────────────
    # ELIMINAR POR VALOR  — O(n)
    # ──────────────────────────────────────────
    def eliminar_por_valor(self, dato):
        """
        Busca y elimina "saltando" el nodo con ese dato.

        Para eliminar B en:  A → B → C
        Solo hacemos:        A → C
        (B queda desconectado → Python lo borra de memoria)
        """
        if self.cabeza is None:
            return False

        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            self._tamano -= 1
            return True

        actual = self.cabeza
        while actual.siguiente is not None:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente  # saltar el nodo
                self._tamano -= 1
                return True
            actual = actual.siguiente
        return False

    # ──────────────────────────────────────────
    # BUSCAR  — O(n)
    # ──────────────────────────────────────────
    def buscar(self, dato):
        """
        Recorre de izquierda a derecha comparando cada nodo.
        Retorna el índice si lo encuentra, -1 si no existe.
        """
        actual = self.cabeza
        indice = 0
        while actual is not None:
            if actual.dato == dato:
                return indice
            actual = actual.siguiente
            indice += 1
        return -1

    # ──────────────────────────────────────────
    # OBTENER POR POSICIÓN  — O(n)
    # ──────────────────────────────────────────
    def obtener(self, posicion):
        """
        Avanza 'posicion' pasos desde HEAD y devuelve el dato.
        A diferencia de un arreglo, NO hay acceso directo.
        """
        if posicion < 0 or posicion >= self._tamano:
            raise IndexError(f"Posición {posicion} no existe.")
        actual = self.cabeza
        for _ in range(posicion):
            actual = actual.siguiente
        return actual.dato

    # ──────────────────────────────────────────
    # INVERTIR  — O(n)
    # ──────────────────────────────────────────
    def invertir(self):
        """
        Da vuelta todos los punteros usando 3 variables:
        anterior, actual, siguiente.
        En cada paso hacemos que actual apunte hacia atrás.
        """
        anterior = None
        actual = self.cabeza
        while actual is not None:
            siguiente = actual.siguiente   # guardar antes de perderlo
            actual.siguiente = anterior    # invertir puntero
            anterior = actual              # avanzar anterior
            actual = siguiente             # avanzar actual
        self.cabeza = anterior  # nueva cabeza = el que era el último

    # ── Utilidades ───────────────────────────

    def limpiar(self):
        self.cabeza = None
        self._tamano = 0

    def tamano(self):
        return self._tamano

    def esta_vacia(self):
        return self._tamano == 0

    def a_lista(self):
        """Convierte la lista enlazada a una lista Python normal."""
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado


# ══════════════════════════════════════════════════════════════════
#   PARTE 3: INTERFAZ GRÁFICA (Tkinter)
# ══════════════════════════════════════════════════════════════════

# ── Paleta de colores ─────────────────────
BG       = "#1a1f2e"
PANEL    = "#242938"
CARD     = "#2d3347"
BORDER   = "#3d4460"
AZUL     = "#4e9de8"
VERDE    = "#4ecb71"
ROJO     = "#e85f5f"
AMARILLO = "#e8c14e"
NARANJA  = "#e8954e"
TEXTO    = "#dde3f5"
DIM      = "#7a85a8"
NODO_BG  = "#1e3a6e"
NODO_BD  = "#4e9de8"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MyLinkedList — Visualizador Educativo")
        self.configure(bg=BG)
        self.minsize(1020, 700)

        self.lista = MyLinkedList()
        self._construir_ui()

        # Datos de ejemplo para empezar
        # (esto va DESPUÉS de _construir_ui para que lbl_exp ya exista)
        for v in [10, 20, 30]:
            self.lista.insertar_al_final(v)
        self.after(100, self._init_visual)  # esperar a que Tkinter termine de dibujar

    def _init_visual(self):
        """Se llama 100ms después de iniciar, cuando todos los widgets ya existen."""
        self._dibujar()
        self._explicar(
            "Bienvenido al visualizador de Linked List.\n\n"
            "La lista tiene 3 nodos de ejemplo: 10 → 20 → 30\n"
            "HEAD apunta al primer nodo (10).\n"
            "Cada nodo apunta al siguiente con un puntero (flecha).\n"
            "El último nodo apunta a None (fin de la lista).\n\n"
            "Usa los botones de la izquierda para ver cómo funciona cada operación."
        )

    # ══════════════════════════════════════════
    #   CONSTRUCCIÓN DE LA UI
    # ══════════════════════════════════════════

    def _construir_ui(self):
        # Título
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=22, pady=(16, 0))
        tk.Label(header, text="🔗  MyLinkedList — Visualizador Educativo",
                 font=("Courier", 17, "bold"), fg=AZUL, bg=BG).pack(side="left")
        self.lbl_tam = tk.Label(header, text="",
                                font=("Courier", 10), fg=DIM, bg=BG)
        self.lbl_tam.pack(side="right")
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=22, pady=10)

        # Cuerpo
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=(0, 16))

        self._panel_controles(body)
        self._panel_visual(body)

    # ── Panel izquierdo ───────────────────────

    def _panel_controles(self, padre):
        frame = tk.Frame(padre, bg=PANEL, width=290,
                         highlightbackground=BORDER, highlightthickness=1)
        frame.pack(side="left", fill="y", padx=(0, 14))
        frame.pack_propagate(False)

        # Campo dato
        self._sep(frame, "✏  DATO A INGRESAR")
        self.e_dato = self._entry(frame)

        # Insertar
        self._sep(frame, "➕  INSERTAR un nuevo nodo")
        self._btn(frame, "Al INICIO",
                  VERDE, self._ins_inicio)
        self._btn(frame, "Al FINAL",
                  VERDE, self._ins_final)

        fpos = tk.Frame(frame, bg=PANEL)
        fpos.pack(fill="x", padx=12, pady=(4, 0))
        tk.Label(fpos, text="Posición (0, 1, 2...):",
                 font=("Courier", 9), fg=DIM, bg=PANEL).pack(side="left")
        self.e_pos = tk.Entry(fpos, width=5, bg=CARD, fg=TEXTO,
                              insertbackground=TEXTO, font=("Courier", 11),
                              relief="flat", highlightbackground=BORDER,
                              highlightthickness=1)
        self.e_pos.pack(side="left", padx=(6, 0))
        self._btn(frame, "En POSICIÓN específica",
                  VERDE, self._ins_pos)

        # Eliminar
        self._sep(frame, "➖  ELIMINAR un nodo")
        self._btn(frame, "Del INICIO",
                  ROJO, self._del_inicio)
        self._btn(frame, "Del FINAL",
                  ROJO, self._del_final)
        self._btn(frame, "Por VALOR",
                  ROJO, self._del_valor)

        # Buscar
        self._sep(frame, "🔍  BUSCAR / OBTENER")
        self._btn(frame, "Buscar VALOR",
                  AMARILLO, self._buscar)

        fget = tk.Frame(frame, bg=PANEL)
        fget.pack(fill="x", padx=12, pady=(4, 0))
        tk.Label(fget, text="Posición a obtener:",
                 font=("Courier", 9), fg=DIM, bg=PANEL).pack(side="left")
        self.e_get = tk.Entry(fget, width=5, bg=CARD, fg=TEXTO,
                              insertbackground=TEXTO, font=("Courier", 11),
                              relief="flat", highlightbackground=BORDER,
                              highlightthickness=1)
        self.e_get.pack(side="left", padx=(6, 0))
        self._btn(frame, "Obtener por POSICIÓN",
                  AMARILLO, self._obtener)

        # Utilidades
        self._sep(frame, "⚙  UTILIDADES")
        self._btn(frame, "Invertir lista",
                  AZUL, self._invertir)
        self._btn(frame, "Limpiar todo",
                  ROJO, self._limpiar)

    # ── Panel derecho ─────────────────────────

    def _panel_visual(self, padre):
        frame = tk.Frame(padre, bg=BG)
        frame.pack(side="left", fill="both", expand=True)

        # ── Canvas de nodos ──────────────────
        tk.Label(frame,
                 text="📊  Representación visual en memoria:",
                 font=("Courier", 10, "bold"), fg=AZUL, bg=BG
                 ).pack(anchor="w", pady=(0, 4))

        canvas_wrap = tk.Frame(frame, bg=PANEL,
                               highlightbackground=BORDER, highlightthickness=1)
        canvas_wrap.pack(fill="x")
        # Altura fija grande para que los nodos siempre quepan completos
        self.canvas = tk.Canvas(canvas_wrap, bg=PANEL, height=200,
                                highlightthickness=0)
        self.canvas.pack(fill="x", padx=10, pady=14)

        # ── Caja de explicación ──────────────
        tk.Label(frame,
                 text="💡  ¿Qué está pasando paso a paso?",
                 font=("Courier", 10, "bold"), fg=AMARILLO, bg=BG
                 ).pack(anchor="w", pady=(10, 4))

        exp_wrap = tk.Frame(frame, bg=PANEL,
                            highlightbackground=BORDER, highlightthickness=1)
        exp_wrap.pack(fill="x")
        self.lbl_exp = tk.Label(exp_wrap, text="",
                                font=("Courier", 10), fg=TEXTO, bg=PANEL,
                                wraplength=660, justify="left", anchor="nw")
        self.lbl_exp.pack(fill="x", padx=14, pady=10)

        # ── Historial / consola ──────────────
        tk.Label(frame, text="📋  Historial de operaciones:",
                 font=("Courier", 10, "bold"), fg=AZUL, bg=BG
                 ).pack(anchor="w", pady=(10, 4))

        log_wrap = tk.Frame(frame, bg=PANEL,
                            highlightbackground=BORDER, highlightthickness=1)
        log_wrap.pack(fill="both", expand=True)
        self.log = tk.Text(log_wrap, bg=CARD, fg=DIM,
                           font=("Courier", 10), relief="flat",
                           state="disabled", wrap="word", height=6)
        self.log.pack(fill="both", expand=True, padx=8, pady=8)

        self.log.tag_config("info",   foreground=DIM)
        self.log.tag_config("ok",     foreground=VERDE)
        self.log.tag_config("error",  foreground=ROJO)
        self.log.tag_config("warn",   foreground=AMARILLO)
        self.log.tag_config("find",   foreground=NARANJA)

    # ══════════════════════════════════════════
    #   DIBUJAR LISTA EN EL CANVAS
    # ══════════════════════════════════════════

    def _dibujar(self, resaltar=None):
        """
        Dibuja cada nodo como una caja:
            ┌──────────┐
            │  [idx]   │
            │   dato   │ ──►
            └──────────┘
        Conectados por flechas. El último apunta a None.
        """
        self.canvas.delete("all")
        items = self.lista.a_lista()
        n = len(items)

        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 200

        NW, NH = 88, 58    # ancho y alto de cada nodo
        FLECHA = 46        # espacio entre nodos (para la flecha)
        PASO = NW + FLECHA

        sx = max(16, (cw - n * PASO) // 2)
        cy = ch // 2

        if n == 0:
            self.canvas.create_text(cw // 2, cy,
                text="[ lista vacía ]   HEAD = None",
                font=("Courier", 13), fill=DIM)
            self.lbl_tam.config(text="0 nodos  |  HEAD = None")
            return

        # Etiqueta HEAD
        hx = sx + NW // 2
        self.canvas.create_text(hx, cy - NH // 2 - 22,
            text="HEAD", font=("Courier", 10, "bold"), fill=AZUL)
        self.canvas.create_line(hx, cy - NH // 2 - 12,
                                hx, cy - NH // 2,
                                fill=AZUL, width=2, arrow="last")

        for i, val in enumerate(items):
            x = sx + i * PASO

            # Color especial para nodo resaltado
            fill = NARANJA if (resaltar is not None and i == resaltar) else NODO_BG
            borde = "#ffb347" if (resaltar is not None and i == resaltar) else NODO_BD

            # Caja del nodo
            self.canvas.create_rectangle(
                x, cy - NH // 2, x + NW, cy + NH // 2,
                fill=fill, outline=borde, width=2)

            # Índice pequeño arriba
            self.canvas.create_text(x + NW // 2, cy - NH // 2 + 13,
                text=f"[{i}]", font=("Courier", 8), fill="#99aacc")

            # Dato grande al centro
            self.canvas.create_text(x + NW // 2, cy + 7,
                text=str(val), font=("Courier", 14, "bold"), fill="#ffffff")

            # Flecha al siguiente o "→ None"
            ax = x + NW
            if i < n - 1:
                self.canvas.create_line(ax + 2, cy, ax + FLECHA - 2, cy,
                    fill=AZUL, width=2, arrow="last")
            else:
                self.canvas.create_line(ax + 2, cy, ax + 32, cy,
                    fill=DIM, width=2, arrow="last", dash=(4, 3))
                self.canvas.create_text(ax + 44, cy,
                    text="None", font=("Courier", 10, "italic"), fill=DIM)

        self.lbl_tam.config(
            text=f"{n} nodo{'s' if n != 1 else ''}  |  HEAD→[{items[0]}]→...→[{items[-1]}]→None"
        )

    # ══════════════════════════════════════════
    #   OPERACIONES
    # ══════════════════════════════════════════

    def _ins_inicio(self):
        dato = self._dato()
        if dato is None: return
        self.lista.insertar_al_inicio(dato)
        self._log(f"Insertado '{dato}' al inicio. Lista: {self.lista.a_lista()}", "ok")
        self._dibujar(resaltar=0)
        self.after(1500, self._dibujar)

    def _ins_final(self):
        dato = self._dato()
        if dato is None: return
        self.lista.insertar_al_final(dato)
        idx = self.lista.tamano() - 1
        self._log(f"Insertado '{dato}' al final (pos {idx}). Lista: {self.lista.a_lista()}", "ok")
        self._dibujar(resaltar=idx)
        self.after(1500, self._dibujar)

    def _ins_pos(self):
        dato = self._dato()
        if dato is None: return
        pos = self._pos(self.e_pos)
        if pos is None: return
        try:
            self.lista.insertar_en_posicion(dato, pos)
            self._log(f"Insertado '{dato}' en pos [{pos}]. Lista: {self.lista.a_lista()}", "ok")
            self._dibujar(resaltar=pos)
            self.after(1500, self._dibujar)
        except IndexError as e:
            self._log(str(e), "error")

    def _del_inicio(self):
        try:
            dato = self.lista.eliminar_al_inicio()
            self._explicar(
                f"ELIMINAR DEL INICIO  —  O(1): muy rápido\n\n"
                f"  Paso 1: Se guardó el dato del primer nodo: '{dato}'\n"
                f"  Paso 2: HEAD avanzó al segundo nodo\n"
                f"  Paso 3: El nodo eliminado quedó desconectado\n"
                f"          → Python lo borra de memoria automáticamente\n\n"
                f"  Lista resultante: {self.lista.a_lista()}"
            )
            self._log(f"Eliminado del inicio: '{dato}'. Lista: {self.lista.a_lista()}", "warn")
            self._dibujar()
        except IndexError as e:
            self._log(str(e), "error")
            self._explicar(f"⚠ ERROR: {e}")

    def _del_final(self):
        try:
            dato = self.lista.eliminar_al_final()
            n = self.lista.tamano()
            self._explicar(
                f"ELIMINAR DEL FINAL  —  O(n): recorre {n} nodo(s)\n\n"
                f"  Paso 1: Se recorrió la lista hasta el nodo PENÚLTIMO\n"
                f"  Paso 2: Se guardó el dato del último nodo: '{dato}'\n"
                f"  Paso 3: El penúltimo nodo ahora apunta a None\n"
                f"          (se convirtió en el nuevo final)\n\n"
                f"  Lista resultante: {self.lista.a_lista()}"
            )
            self._log(f"Eliminado del final: '{dato}'. Lista: {self.lista.a_lista()}", "warn")
            self._dibujar()
        except IndexError as e:
            self._log(str(e), "error")
            self._explicar(f"⚠ ERROR: {e}")

    def _del_valor(self):
        dato = self._dato()
        if dato is None: return
        ok = self.lista.eliminar_por_valor(dato)
        if ok:
            self._explicar(
                f"ELIMINAR POR VALOR '{dato}'  —  O(n)\n\n"
                f"  Se recorrió la lista buscando el nodo con dato='{dato}'.\n\n"
                f"  Cuando se encontró, se aplicó el 'salto':\n"
                f"    nodo_anterior.siguiente = nodo_siguiente\n"
                f"    (el nodo '{dato}' quedó excluido de la cadena)\n\n"
                f"  Python borra de memoria el nodo sin referencias.\n"
                f"  Lista resultante: {self.lista.a_lista()}"
            )
            self._log(f"Eliminado '{dato}' por valor. Lista: {self.lista.a_lista()}", "warn")
        else:
            self._explicar(
                f"ELIMINAR POR VALOR '{dato}'  —  No encontrado\n\n"
                f"  Se recorrió toda la lista desde HEAD hasta None.\n"
                f"  Ningún nodo tenía dato='{dato}'.\n"
                f"  La lista no cambió."
            )
            self._log(f"'{dato}' no está en la lista.", "error")
        self._dibujar()

    def _buscar(self):
        dato = self._dato()
        if dato is None: return
        idx = self.lista.buscar(dato)
        if idx != -1:
            self._explicar(
                f"BUSCAR '{dato}'  —  O(n)\n\n"
                f"  Se recorrió la lista desde HEAD comparando cada nodo:\n"
                f"  nodo[0], nodo[1], ... → encontrado en posición [{idx}]\n\n"
                f"  El nodo naranja en el canvas es el que se encontró.\n\n"
                f"  Nota: en una Linked List NO hay acceso directo.\n"
                f"  Siempre hay que recorrer desde el inicio."
            )
            self._log(f"'{dato}' encontrado en posición [{idx}].", "find")
            self._dibujar(resaltar=idx)
            self.after(2000, self._dibujar)
        else:
            self._explicar(
                f"BUSCAR '{dato}'  —  No encontrado\n\n"
                f"  Se recorrió toda la lista desde HEAD hasta None.\n"
                f"  Ningún nodo tenía dato='{dato}'.\n"
                f"  Retorna -1 (convención para 'no encontrado')."
            )
            self._log(f"'{dato}' NO está en la lista.", "error")

    def _obtener(self):
        pos = self._pos(self.e_get)
        if pos is None: return
        try:
            val = self.lista.obtener(pos)
            self._explicar(
                f"OBTENER EN POSICIÓN [{pos}]  —  O(n)\n\n"
                f"  Se avanzó {pos} paso(s) desde HEAD nodo por nodo.\n\n"
                f"  ⚠ Diferencia con arreglos:\n"
                f"    En un arreglo: arr[{pos}] → acceso directo O(1)\n"
                f"    En Linked List: hay que recorrer {pos} nodos O(n)\n\n"
                f"  El dato en posición [{pos}] es: '{val}'"
            )
            self._log(f"Posición [{pos}] → dato: '{val}'", "find")
            self._dibujar(resaltar=pos)
            self.after(2000, self._dibujar)
        except IndexError as e:
            self._log(str(e), "error")
            self._explicar(f"⚠ ERROR: {e}")

    def _invertir(self):
        if self.lista.esta_vacia():
            self._log("Lista vacía, nada que invertir.", "warn"); return
        antes = self.lista.a_lista()[:]
        self.lista.invertir()
        self._explicar(
            f"INVERTIR LISTA  —  O(n)\n\n"
            f"  Se usaron 3 variables: anterior, actual, siguiente\n"
            f"  En cada paso se invirtió el puntero de 'actual':\n"
            f"    actual.siguiente = anterior\n\n"
            f"  Antes:   {' → '.join(str(x) for x in antes)}\n"
            f"  Después: {' → '.join(str(x) for x in self.lista.a_lista())}\n\n"
            f"  HEAD ahora apunta al que era el último nodo."
        )
        self._log(f"Lista invertida. Lista: {self.lista.a_lista()}", "ok")
        self._dibujar()

    def _limpiar(self):
        if self.lista.esta_vacia():
            self._log("La lista ya estaba vacía.", "warn"); return
        self.lista.limpiar()
        self._explicar(
            "LIMPIAR LISTA\n\n"
            "  self.cabeza = None\n"
            "  self._tamano = 0\n\n"
            "  Al quitar la referencia de la cabeza, todos los nodos\n"
            "  quedan sin referencia y Python los elimina de memoria.\n\n"
            "  La lista está completamente vacía. HEAD = None."
        )
        self._log("Lista limpiada. HEAD = None.", "warn")
        self._dibujar()

    # ══════════════════════════════════════════
    #   HELPERS DE UI
    # ══════════════════════════════════════════

    def _sep(self, p, t):
        f = tk.Frame(p, bg=PANEL)
        f.pack(fill="x", padx=12, pady=(11, 2))
        tk.Label(f, text=t, font=("Courier", 8, "bold"),
                 fg=DIM, bg=PANEL).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(6, 0))

    def _entry(self, p):
        PLACEHOLDER = "Escribe un número o texto..."
        e = tk.Entry(p, bg=CARD, fg=DIM, insertbackground=TEXTO,
                     font=("Courier", 12), relief="flat",
                     highlightbackground=BORDER, highlightthickness=1)
        e.pack(fill="x", padx=12, pady=4, ipady=6)
        e.insert(0, PLACEHOLDER)

        def fi(_):
            if e.get() == PLACEHOLDER:
                e.delete(0, "end"); e.config(fg=TEXTO)
        def fo(_):
            if not e.get():
                e.insert(0, PLACEHOLDER); e.config(fg=DIM)

        e.bind("<FocusIn>", fi)
        e.bind("<FocusOut>", fo)
        e.bind("<Return>", lambda _: self._ins_final())
        e._placeholder = PLACEHOLDER
        return e

    def _btn(self, p, txt, color, cmd):
        b = tk.Button(p, text=txt, font=("Courier", 9),
                      fg=TEXTO, bg=CARD,
                      activebackground=color, activeforeground="#fff",
                      relief="flat", cursor="hand2", bd=0,
                      pady=7, anchor="w", padx=10,
                      highlightbackground=BORDER, highlightthickness=1,
                      command=cmd)
        b.pack(fill="x", padx=12, pady=2)
        b.bind("<Enter>", lambda _: b.config(bg=color, fg="#fff"))
        b.bind("<Leave>", lambda _: b.config(bg=CARD, fg=TEXTO))

    def _dato(self):
        PLACEHOLDER = "Escribe un número o texto..."
        v = self.e_dato.get().strip()
        if not v or v == PLACEHOLDER:
            self._log("⚠ Escribe un dato en el campo de arriba.", "error")
            self._explicar("Escribe un valor en el campo 'DATO A INGRESAR' antes de operar.")
            return None
        try:    return int(v)
        except: 
            try:    return float(v)
            except: return v

    def _pos(self, entry):
        v = entry.get().strip()
        if not v:
            self._log("⚠ Escribe un número de posición (0, 1, 2...).", "error")
            return None
        try:    return int(v)
        except:
            self._log("⚠ La posición debe ser un entero (0, 1, 2...).", "error")
            return None

    def _log(self, msg, tag="info"):
        self.log.config(state="normal")
        ts = time.strftime("%H:%M:%S")
        icons = {"info":"·","ok":"✔","error":"✖","warn":"⚠","find":"◉"}
        self.log.insert("end", f"[{ts}] {icons.get(tag,'·')}  {msg}\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _explicar(self, texto):
        self.lbl_exp.config(text=texto)


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    App().mainloop()