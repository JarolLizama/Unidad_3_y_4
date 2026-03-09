import tkinter as tk
from tkinter import font as tkfont

MAX_CAPACIDAD = 8

OPERACIONES = [
    {"label": "Estado Inicial",       "op": None,   "elem": None},
    {"label": "a. Insertar(PILA, X)", "op": "push", "elem": "X"},
    {"label": "b. Insertar(PILA, Y)", "op": "push", "elem": "Y"},
    {"label": "   Insertar(PILA, Z)", "op": "push", "elem": "Z"},
    {"label": "c. Eliminar(PILA, Z)", "op": "pop",  "elem": "Z"},
    {"label": "   Insertar(PILA, T)", "op": "push", "elem": "T"},
    {"label": "d. Eliminar(PILA, T)", "op": "pop",  "elem": "T"},
    {"label": "   Insertar(PILA, U)", "op": "push", "elem": "U"},
    {"label": "e. Eliminar(PILA, U)", "op": "pop",  "elem": "U"},
    {"label": "f. Insertar(PILA, V)", "op": "push", "elem": "V"},
    {"label": "g. Insertar(PILA, W)", "op": "push", "elem": "W"},
    {"label": "   Insertar(PILA, p)", "op": "push", "elem": "p"},
    {"label": "h. Eliminar(PILA, p)", "op": "pop",  "elem": "p"},
    {"label": "i. Insertar(PILA, R)", "op": "push", "elem": "R"},
]

COLORES_SLOTS = [
    "#ef4444","#f97316","#eab308","#84cc16",
    "#22c55e","#06b6d4","#6366f1","#ec4899",
]

BG           = "#0f172a"
BG_PANEL     = "#1e293b"
BG_BTN       = "#334155"
BG_BTN_ACT   = "#0369a1"
BG_BTN_ERR   = "#7f1d1d"
COLOR_TEXT   = "#e2e8f0"
COLOR_MUTED  = "#64748b"
COLOR_TOPE   = "#38bdf8"
COLOR_ERR    = "#f87171"
COLOR_OK     = "#4ade80"
COLOR_SLOT_EMPTY = "#1e293b"
COLOR_SLOT_BORDER = "#334155"


def simular():
    estados = []
    pila = []
    for i, op_data in enumerate(OPERACIONES):
        error = None
        popped = None
        resultado = None
        op = op_data["op"]
        elem = op_data["elem"]

        if op == "push":
            if len(pila) == MAX_CAPACIDAD:
                error = f"❌ DESBORDAMIENTO (Overflow)\nPila llena — no se puede insertar '{elem}'"
            else:
                pila.append(elem)
                resultado = f"✅ '{elem}' insertado correctamente"
        elif op == "pop":
            if len(pila) == 0:
                error = f"❌ SUBDESBORDAMIENTO (Underflow)\nPila vacía — no se puede eliminar en '{elem}'"
            else:
                popped = pila.pop()
                resultado = f"✅ Extraído '{popped}' → asignado a {elem}"

        estados.append({
            "stack":     list(pila),
            "tope":      len(pila),
            "error":     error,
            "popped":    popped,
            "resultado": resultado,
        })
    return estados


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulación de Pila — Máx. 8 elementos")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.estados = simular()
        self.idx_actual = 0

        self._build_ui()
        self._render(0)

    # ─── Construcción de la UI ───────────────────────────────────────────────

    def _build_ui(self):
        FONT_TITLE  = ("Courier New", 15, "bold")
        FONT_LABEL  = ("Courier New", 10)
        FONT_BTN    = ("Courier New",  9)
        FONT_TOPE   = ("Courier New", 13, "bold")
        FONT_SLOT   = ("Courier New", 14, "bold")
        FONT_INFO   = ("Courier New", 10)

        # ── Título
        tk.Label(self, text="▶  SIMULACIÓN DE ESTRUCTURA PILA",
                 font=FONT_TITLE, bg=BG, fg=COLOR_TOPE,
                 pady=14).grid(row=0, column=0, columnspan=3, sticky="ew")

        tk.Label(self, text=f"Capacidad máxima: {MAX_CAPACIDAD} elementos",
                 font=FONT_LABEL, bg=BG, fg=COLOR_MUTED,
                 pady=2).grid(row=1, column=0, columnspan=3)

        # ── Panel izquierdo: botones de operaciones
        frame_ops = tk.Frame(self, bg=BG_PANEL, padx=12, pady=12, bd=0)
        frame_ops.grid(row=2, column=0, padx=(16,8), pady=16, sticky="ns")

        tk.Label(frame_ops, text="OPERACIONES", font=("Courier New", 9, "bold"),
                 bg=BG_PANEL, fg=COLOR_MUTED).pack(anchor="w", pady=(0,8))

        self.botones = []
        for i, op in enumerate(OPERACIONES):
            estado = self.estados[i]
            color_bg = BG_BTN_ERR if estado["error"] else BG_BTN
            btn = tk.Button(
                frame_ops, text=op["label"],
                font=FONT_BTN, bg=color_bg, fg=COLOR_TEXT,
                activebackground=BG_BTN_ACT, activeforeground="white",
                relief="flat", cursor="hand2", padx=10, pady=5,
                width=28, anchor="w",
                command=lambda i=i: self._render(i)
            )
            btn.pack(pady=2)
            self.botones.append(btn)

        # ── Panel central: diagrama de la pila
        frame_pila = tk.Frame(self, bg=BG, padx=16)
        frame_pila.grid(row=2, column=1, padx=8, pady=16)

        self.lbl_tope = tk.Label(frame_pila, text="TOPE = 0",
                                  font=FONT_TOPE, bg=BG, fg=COLOR_TOPE)
        self.lbl_tope.pack(pady=(0, 6))

        # Celdas de la pila (de arriba hacia abajo = índice 7 a 0)
        self.celdas_frame = tk.Frame(frame_pila, bg=BG)
        self.celdas_frame.pack()

        self.celdas = []        # canvas por cada slot
        self.txt_celdas = []    # id de texto en canvas
        self.lbl_indices = []   # etiqueta de índice
        self.lbl_tope_arr = []  # flecha TOPE

        CELL_W, CELL_H = 90, 44

        for vis_i in range(MAX_CAPACIDAD):
            slot_idx = MAX_CAPACIDAD - 1 - vis_i   # 7..0

            row_frame = tk.Frame(self.celdas_frame, bg=BG)
            row_frame.pack()

            # flecha TOPE
            arr = tk.Label(row_frame, text="", font=("Courier New", 10, "bold"),
                           bg=BG, fg=COLOR_TOPE, width=8)
            arr.pack(side="left")
            self.lbl_tope_arr.append(arr)

            # celda
            c = tk.Canvas(row_frame, width=CELL_W, height=CELL_H,
                          bg=COLOR_SLOT_EMPTY, highlightthickness=2,
                          highlightbackground=COLOR_SLOT_BORDER)
            c.pack(side="left", padx=2, pady=1)
            txt_id = c.create_text(CELL_W//2, CELL_H//2, text="",
                                   font=FONT_SLOT, fill=COLOR_TEXT)
            self.celdas.append(c)
            self.txt_celdas.append(txt_id)

            # índice
            lbl = tk.Label(row_frame, text=f"[{slot_idx}]",
                           font=("Courier New", 9), bg=BG, fg=COLOR_MUTED, width=5)
            lbl.pack(side="left")
            self.lbl_indices.append(lbl)

        # ── Panel derecho: información / resultado
        frame_info = tk.Frame(self, bg=BG_PANEL, padx=14, pady=14)
        frame_info.grid(row=2, column=2, padx=(8,16), pady=16, sticky="nsew")

        tk.Label(frame_info, text="RESULTADO", font=("Courier New", 9, "bold"),
                 bg=BG_PANEL, fg=COLOR_MUTED).pack(anchor="w", pady=(0,8))

        self.txt_resultado = tk.Label(
            frame_info, text="", font=FONT_INFO,
            bg=BG_PANEL, fg=COLOR_OK,
            wraplength=230, justify="left"
        )
        self.txt_resultado.pack(anchor="w", pady=(0,12))

        self.txt_error = tk.Label(
            frame_info, text="", font=FONT_INFO,
            bg=BG_PANEL, fg=COLOR_ERR,
            wraplength=230, justify="left"
        )
        self.txt_error.pack(anchor="w", pady=(0,16))

        tk.Frame(frame_info, bg=COLOR_SLOT_BORDER, height=1).pack(fill="x", pady=8)

        tk.Label(frame_info, text="CONTENIDO ACTUAL",
                 font=("Courier New", 9, "bold"),
                 bg=BG_PANEL, fg=COLOR_MUTED).pack(anchor="w")

        self.txt_contenido = tk.Label(
            frame_info, text="", font=FONT_INFO,
            bg=BG_PANEL, fg=COLOR_TEXT,
            wraplength=230, justify="left"
        )
        self.txt_contenido.pack(anchor="w", pady=(4, 12))

        tk.Frame(frame_info, bg=COLOR_SLOT_BORDER, height=1).pack(fill="x", pady=8)

        # Resumen final
        tk.Label(frame_info, text="RESUMEN FINAL",
                 font=("Courier New", 9, "bold"),
                 bg=BG_PANEL, fg=COLOR_MUTED).pack(anchor="w")

        estado_final = self.estados[-1]
        errores = [e for e in self.estados if e["error"]]
        resumen = (
            f"Elementos finales: {estado_final['tope']}\n"
            f"Contenido: {estado_final['stack'] if estado_final['stack'] else 'Vacía'}\n\n"
            f"Errores ocurridos: {len(errores)}\n"
        )
        for e in errores:
            resumen += f"\n• {e['error']}"

        tk.Label(frame_info, text=resumen, font=FONT_INFO,
                 bg=BG_PANEL, fg=COLOR_TEXT,
                 wraplength=230, justify="left").pack(anchor="w", pady=(4,0))

        # ── Navegación
        nav = tk.Frame(self, bg=BG)
        nav.grid(row=3, column=0, columnspan=3, pady=(0,16))

        tk.Button(nav, text="◀  Anterior", font=("Courier New", 10),
                  bg=BG_BTN, fg=COLOR_TEXT, activebackground=BG_BTN_ACT,
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._anterior).pack(side="left", padx=8)

        self.lbl_nav = tk.Label(nav, text="", font=("Courier New", 10),
                                 bg=BG, fg=COLOR_MUTED, width=18)
        self.lbl_nav.pack(side="left")

        tk.Button(nav, text="Siguiente  ▶", font=("Courier New", 10),
                  bg=BG_BTN, fg=COLOR_TEXT, activebackground=BG_BTN_ACT,
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._siguiente).pack(side="left", padx=8)

    # ─── Renderizado de un estado ────────────────────────────────────────────

    def _render(self, idx):
        self.idx_actual = idx
        estado = self.estados[idx]
        pila   = estado["stack"]
        tope   = estado["tope"]

        # Actualizar botones
        for i, btn in enumerate(self.botones):
            e = self.estados[i]
            if i == idx:
                btn.config(bg=BG_BTN_ACT if not e["error"] else "#991b1b")
            else:
                btn.config(bg=BG_BTN_ERR if e["error"] else BG_BTN)

        # Actualizar TOPE label
        self.lbl_tope.config(text=f"TOPE = {tope}")

        # Actualizar celdas (vis_i 0 = slot MAX-1, vis_i 7 = slot 0)
        for vis_i in range(MAX_CAPACIDAD):
            slot_idx = MAX_CAPACIDAD - 1 - vis_i
            c       = self.celdas[vis_i]
            txt_id  = self.txt_celdas[vis_i]
            arr_lbl = self.lbl_tope_arr[vis_i]

            if slot_idx < len(pila):
                color = COLORES_SLOTS[slot_idx % len(COLORES_SLOTS)]
                c.config(bg=color, highlightbackground=color)
                c.itemconfig(txt_id, text=pila[slot_idx], fill="#0f172a")
            else:
                c.config(bg=COLOR_SLOT_EMPTY, highlightbackground=COLOR_SLOT_BORDER)
                c.itemconfig(txt_id, text="")

            # Flecha TOPE apunta al slot donde está el tope (tope-1 si >0, slot 0 si vacío)
            if tope > 0 and slot_idx == tope - 1:
                arr_lbl.config(text="TOPE ▶", fg=COLOR_TOPE)
            elif tope == 0 and slot_idx == 0:
                arr_lbl.config(text="TOPE ▶", fg=COLOR_MUTED)
            else:
                arr_lbl.config(text="")

        # Panel de resultado
        if estado["error"]:
            self.txt_resultado.config(text="")
            self.txt_error.config(text=estado["error"])
        else:
            self.txt_error.config(text="")
            self.txt_resultado.config(text=estado["resultado"] or "Pila en estado inicial")

        contenido = (
            f"Pila: {pila}\nElementos: {tope}"
            if pila else "Pila vacía\nElementos: 0"
        )
        self.txt_contenido.config(text=contenido)

        # Navegación
        self.lbl_nav.config(text=f"Paso {idx + 1} / {len(OPERACIONES)}")

    def _anterior(self):
        if self.idx_actual > 0:
            self._render(self.idx_actual - 1)

    def _siguiente(self):
        if self.idx_actual < len(OPERACIONES) - 1:
            self._render(self.idx_actual + 1)


if __name__ == "__main__":
    app = App()
    app.mainloop()