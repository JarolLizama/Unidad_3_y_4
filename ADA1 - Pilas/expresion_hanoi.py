"""
╔══════════════════════════════════════════════════════════╗
║   ESTRUCTURAS DE DATOS — PILAS                          ║
║   1. Evaluador de Expresiones (Posfija / Prefija)       ║
║   2. Torres de Hanoi (3 discos)                         ║
╚══════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, font
import time

# ══════════════════════════════════════════════════════════
#  CLASE PILA
# ══════════════════════════════════════════════════════════

class Pila:
    def __init__(self):
        self._datos = []

    def apilar(self, elemento):
        self._datos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("Desapilar sobre pila vacía")
        return self._datos.pop()

    def tope(self):
        if self.esta_vacia():
            raise IndexError("Pila vacía")
        return self._datos[-1]

    def esta_vacia(self):
        return len(self._datos) == 0

    def tamano(self):
        return len(self._datos)

    def contenido(self):
        return list(self._datos)


# ══════════════════════════════════════════════════════════
#  LÓGICA — EVALUADOR
# ══════════════════════════════════════════════════════════

OPERADORES = {'+', '-', '*', '/'}

def es_numero(t):
    try:
        float(t)
        return True
    except ValueError:
        return False

def aplicar(op, a, b):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0: raise ZeroDivisionError("División por cero")
        return a / b

def evaluar_posfija(expresion):
    pila = Pila()
    tokens = expresion.strip().split()
    pasos = []
    for token in tokens:
        if es_numero(token):
            pila.apilar(float(token))
            pasos.append((token, f"APILAR {token}", list(pila.contenido())))
        elif token in OPERADORES:
            if pila.tamano() < 2:
                raise ValueError("Operandos insuficientes")
            b = pila.desapilar()
            a = pila.desapilar()
            r = aplicar(token, a, b)
            pila.apilar(r)
            v = int(r) if r == int(r) else round(r, 4)
            pasos.append((token, f"{a} {token} {b} = {v}", list(pila.contenido())))
        else:
            raise ValueError(f"Token inválido: '{token}'")
    if pila.tamano() != 1:
        raise ValueError("Expresión mal formada")
    return pila.desapilar(), pasos

def evaluar_prefija(expresion):
    pila = Pila()
    tokens = expresion.strip().split()[::-1]
    pasos = []
    for token in tokens:
        if es_numero(token):
            pila.apilar(float(token))
            pasos.append((token, f"APILAR {token}", list(pila.contenido())))
        elif token in OPERADORES:
            if pila.tamano() < 2:
                raise ValueError("Operandos insuficientes")
            a = pila.desapilar()
            b = pila.desapilar()
            r = aplicar(token, a, b)
            pila.apilar(r)
            v = int(r) if r == int(r) else round(r, 4)
            pasos.append((token, f"{a} {token} {b} = {v}", list(pila.contenido())))
        else:
            raise ValueError(f"Token inválido: '{token}'")
    if pila.tamano() != 1:
        raise ValueError("Expresión mal formada")
    return pila.desapilar(), pasos


# ══════════════════════════════════════════════════════════
#  LÓGICA — TORRES DE HANOI
# ══════════════════════════════════════════════════════════

def generar_movimientos_hanoi(n):
    torres = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
    movs = [{'A': list(torres['A']), 'B': list(torres['B']),
              'C': list(torres['C']), 'desc': 'Estado inicial', 'desde': None, 'hacia': None}]

    def hanoi(k, orig, dest, aux):
        if k == 0: return
        hanoi(k-1, orig, aux, dest)
        disco = torres[orig].pop()
        torres[dest].append(disco)
        movs.append({'A': list(torres['A']), 'B': list(torres['B']),
                     'C': list(torres['C']),
                     'desc': f'Disco {disco}: Torre {orig} → Torre {dest}',
                     'desde': orig, 'hacia': dest, 'disco': disco})
        hanoi(k-1, aux, dest, orig)

    hanoi(n, 'A', 'C', 'B')
    return movs


# ══════════════════════════════════════════════════════════
#  PALETA DE COLORES
# ══════════════════════════════════════════════════════════

BG       = "#0d0f18"
PANEL    = "#13161f"
BORDER   = "#1e2333"
AMBER    = "#f0a500"
AMBER_DK = "#7a5200"
TEAL     = "#00c9a7"
TEXT     = "#e8dcc8"
TEXT_DIM = "#6b7280"
TEXT_FNT = "#343849"
RED      = "#ff5b5b"
GREEN    = "#4ade80"

DISK_COLORS = ["#f0a500", "#00c9a7", "#e05cff"]  # disco 1, 2, 3


# ══════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ══════════════════════════════════════════════════════════

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Estructuras de Datos — Pilas")
        self.configure(bg=BG)
        self.geometry("860x680")
        self.minsize(760, 600)
        self.resizable(True, True)
        self._build()

    def _build(self):
        # ── Header
        hdr = tk.Frame(self, bg=BG, pady=14, padx=24)
        hdr.pack(fill="x")
        tk.Label(hdr, text="● ESTRUCTURAS DE DATOS — PILA",
                 bg=BG, fg=TEXT_DIM, font=("Courier", 9)).pack(anchor="w")
        tk.Label(hdr, text="Algoritmos con Pilas",
                 bg=BG, fg=TEXT, font=("Courier", 20, "bold")).pack(anchor="w", pady=(4,0))

        # ── Tabs
        tab_bar = tk.Frame(self, bg=BG, padx=24)
        tab_bar.pack(fill="x")

        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x")

        self.tab_btns = {}
        self.active_tab = tk.StringVar(value="eval")
        self.content = tk.Frame(self, bg=BG, padx=24, pady=20)
        self.content.pack(fill="both", expand=True)

        tabs_info = [("eval", "01 · Evaluador de Expresiones"),
                     ("hanoi", "02 · Torres de Hanoi")]
        for tid, label in tabs_info:
            b = tk.Button(tab_bar, text=label, bg=BG, fg=TEXT_DIM,
                          relief="flat", bd=0, padx=16, pady=10,
                          font=("Courier", 10),
                          activebackground=BG, activeforeground=AMBER,
                          cursor="hand2",
                          command=lambda t=tid: self.switch_tab(t))
            b.pack(side="left")
            self.tab_btns[tid] = b

        self.frames = {}
        self.frames["eval"]  = EvalFrame(self.content)
        self.frames["hanoi"] = HanoiFrame(self.content)
        self.switch_tab("eval")

    def switch_tab(self, tab_id):
        for t, f in self.frames.items():
            f.pack_forget()
        self.frames[tab_id].pack(fill="both", expand=True)
        for t, b in self.tab_btns.items():
            if t == tab_id:
                b.config(fg=AMBER, font=("Courier", 10, "bold"))
                # underline trick via frame
            else:
                b.config(fg=TEXT_DIM, font=("Courier", 10))
        self.active_tab.set(tab_id)


# ══════════════════════════════════════════════════════════
#  PESTAÑA 1 — EVALUADOR
# ══════════════════════════════════════════════════════════

EJEMPLOS = {
    "posfija": ["3 4 +", "5 1 2 + 4 * + 3 -", "2 3 * 4 5 * +", "10 2 /"],
    "prefija": ["+ 3 4", "+ 5 * 4 + 1 2", "* + 2 3 - 8 3", "/ 10 2"],
}

class EvalFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.notacion = tk.StringVar(value="posfija")
        self.pasos = []
        self._build()

    def _build(self):
        # ── Subtítulo
        tk.Label(self, text="Ingrese una expresión y observe la pila paso a paso",
                 bg=BG, fg=TEXT_DIM, font=("Courier", 9)).pack(anchor="w", pady=(0,12))

        # ── Selector notación
        self.sel_frame = tk.Frame(self, bg=BG)
        self.sel_frame.pack(anchor="w", pady=(0,10))
        for n in ("posfija", "prefija"):
            rb = tk.Radiobutton(self.sel_frame, text=n.upper(), variable=self.notacion,
                                value=n, bg=BG, fg=TEXT_DIM,
                                selectcolor=BG, activebackground=BG,
                                activeforeground=AMBER,
                                font=("Courier", 10),
                                indicatoron=0, padx=14, pady=6,
                                relief="flat", bd=1,
                                command=self._on_notacion_change)
            rb.pack(side="left", padx=(0,6))

        # ── Ejemplos
        self.ej_frame = tk.Frame(self, bg=BG)
        self.ej_frame.pack(anchor="w", pady=(0,12))
        self._rebuild_ejemplos()
        self._update_rb_colors()

        # ── Input + botón
        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", pady=(0,12))
        self.entry = tk.Entry(row, bg=PANEL, fg=TEXT, insertbackground=AMBER,
                              font=("Courier", 13), relief="flat", bd=0,
                              highlightthickness=1, highlightbackground=BORDER,
                              highlightcolor=AMBER)
        self.entry.insert(0, "5 1 2 + 4 * + 3 -")
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, ipadx=10)
        self.entry.bind("<Return>", lambda e: self._evaluar())

        btn = tk.Button(row, text="EVALUAR", bg=AMBER, fg="#0d0f18",
                        font=("Courier", 11, "bold"), relief="flat",
                        padx=18, pady=8, cursor="hand2",
                        activebackground="#c98b00", activeforeground="#0d0f18",
                        command=self._evaluar)
        btn.pack(side="left", padx=(8,0))

        # ── Mensaje de error
        self.err_var = tk.StringVar()
        self.err_lbl = tk.Label(self, textvariable=self.err_var,
                                bg="#1a0808", fg=RED, font=("Courier", 10),
                                relief="flat", padx=10, pady=6)

        # ── Área de resultados (dos columnas)
        self.res_frame = tk.Frame(self, bg=BG)
        self.res_frame.pack(fill="both", expand=True)
        self.res_frame.columnconfigure(0, weight=1)
        self.res_frame.columnconfigure(1, weight=1)

        # Columna izq — traza
        left = tk.Frame(self.res_frame, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        tk.Label(left, text="TRAZA DE EJECUCIÓN",
                 bg=BG, fg=TEXT_DIM, font=("Courier", 8)).pack(anchor="w", pady=(0,6))
        self.traza_list = tk.Listbox(left, bg=PANEL, fg=TEXT,
                                     font=("Courier", 11), relief="flat",
                                     selectbackground=AMBER, selectforeground="#0d0f18",
                                     activestyle="none", bd=0,
                                     highlightthickness=1,
                                     highlightbackground=BORDER)
        self.traza_list.pack(fill="both", expand=True)
        self.traza_list.bind("<<ListboxSelect>>", self._on_traza_select)

        # Columna der — pila visual
        right = tk.Frame(self.res_frame, bg=BG)
        right.grid(row=0, column=1, sticky="nsew")
        tk.Label(right, text="PILA",
                 bg=BG, fg=TEXT_DIM, font=("Courier", 8)).pack(anchor="w", pady=(0,6))
        self.pila_canvas = tk.Canvas(right, bg=PANEL, relief="flat",
                                     highlightthickness=1,
                                     highlightbackground=BORDER)
        self.pila_canvas.pack(fill="both", expand=True)

        # Resultado
        self.result_lbl = tk.Label(self, text="", bg="#0d1a14", fg=TEAL,
                                   font=("Courier", 18, "bold"),
                                   relief="flat", pady=10)

    def _on_notacion_change(self):
        self._update_rb_colors()
        self._rebuild_ejemplos()
        self.err_var.set("")
        self.result_lbl.pack_forget()
        self.traza_list.delete(0, "end")
        self._draw_pila([])

    def _update_rb_colors(self):
        for rb in self.sel_frame.winfo_children():
            if isinstance(rb, tk.Radiobutton):
                if rb.cget("value") == self.notacion.get():
                    rb.config(fg=AMBER)
                else:
                    rb.config(fg=TEXT_DIM)

    def _rebuild_ejemplos(self):
        for w in self.ej_frame.winfo_children():
            w.destroy()
        tk.Label(self.ej_frame, text="Ejemplos: ", bg=BG, fg=TEXT_DIM,
                 font=("Courier", 9)).pack(side="left")
        for e in EJEMPLOS[self.notacion.get()]:
            b = tk.Button(self.ej_frame, text=e, bg=PANEL, fg=TEXT_DIM,
                          font=("Courier", 9), relief="flat", padx=8, pady=3,
                          cursor="hand2", activebackground=BORDER,
                          activeforeground=TEAL,
                          command=lambda ex=e: self._set_ejemplo(ex))
            b.pack(side="left", padx=3)

    def _set_ejemplo(self, ex):
        self.entry.delete(0, "end")
        self.entry.insert(0, ex)
        self._evaluar()

    def _evaluar(self):
        self.err_lbl.pack_forget()
        self.result_lbl.pack_forget()
        self.traza_list.delete(0, "end")
        self._draw_pila([])
        expr = self.entry.get().strip()
        if not expr:
            return
        try:
            if self.notacion.get() == "posfija":
                resultado, pasos = evaluar_posfija(expr)
            else:
                resultado, pasos = evaluar_prefija(expr)
            self.pasos = pasos
            for i, (tok, accion, _) in enumerate(pasos):
                simbolo = "▶" if tok in OPERADORES else "·"
                self.traza_list.insert("end", f"  {simbolo} [{tok}]  {accion}")
            # Animar traza
            self._animar_traza(0, pasos, resultado)
        except Exception as ex:
            self.err_var.set(f"⚠  {ex}")
            self.err_lbl.pack(fill="x", pady=(0,8))

    def _animar_traza(self, i, pasos, resultado):
        if i < len(pasos):
            self.traza_list.selection_clear(0, "end")
            self.traza_list.selection_set(i)
            self.traza_list.see(i)
            self._draw_pila(pasos[i][2])
            self.after(320, lambda: self._animar_traza(i+1, pasos, resultado))
        else:
            # Mostrar resultado
            v = int(resultado) if resultado == int(resultado) else round(resultado, 4)
            self.result_lbl.config(text=f"  Resultado =  {v}  ")
            self.result_lbl.pack(fill="x", pady=(10,0))

    def _on_traza_select(self, event):
        sel = self.traza_list.curselection()
        if sel and sel[0] < len(self.pasos):
            self._draw_pila(self.pasos[sel[0]][2])

    def _draw_pila(self, contenido):
        c = self.pila_canvas
        c.delete("all")
        c.update_idletasks()
        W = c.winfo_width() or 200
        H = c.winfo_height() or 300
        if not contenido:
            # Base vacía
            c.create_line(W//2-40, H-20, W//2+40, H-20, fill=BORDER, width=2)
            c.create_text(W//2, H//2, text="(vacía)", fill=TEXT_FNT, font=("Courier", 10))
            return
        cell_h = 38
        cell_w = min(W - 40, 160)
        total_h = len(contenido) * (cell_h + 6)
        start_y = H - 20 - cell_h
        for idx, val in enumerate(contenido):
            x1 = W//2 - cell_w//2
            x2 = W//2 + cell_w//2
            y1 = start_y - idx * (cell_h + 6)
            y2 = y1 + cell_h
            is_top = (idx == len(contenido) - 1)
            fill = "#1e2b1a" if is_top else PANEL
            outline = TEAL if is_top else BORDER
            # rect redondeado via polígono
            r = 6
            c.create_polygon(
                x1+r, y1, x2-r, y1,
                x2, y1+r, x2, y2-r,
                x2-r, y2, x1+r, y2,
                x1, y2-r, x1, y1+r,
                fill=fill, outline=outline, smooth=True, width=2
            )
            v = int(val) if val == int(val) else round(val, 3)
            txt_color = TEAL if is_top else TEXT
            c.create_text(W//2, (y1+y2)//2, text=str(v),
                          fill=txt_color, font=("Courier", 12, "bold"))
            if is_top:
                c.create_text(x2 + 6, (y1+y2)//2, text="← tope",
                              fill=TEXT_DIM, font=("Courier", 8), anchor="w")
        # Base
        c.create_line(W//2-cell_w//2-4, H-20, W//2+cell_w//2+4, H-20,
                      fill=BORDER, width=2)


# ══════════════════════════════════════════════════════════
#  PESTAÑA 2 — TORRES DE HANOI
# ══════════════════════════════════════════════════════════

class HanoiFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.movimientos = generar_movimientos_hanoi(3)
        self.paso = 0
        self.total = len(self.movimientos) - 1
        self._playing = False
        self._after_id = None
        self._build()
        self._render()

    def _build(self):
        tk.Label(self, text=f"3 discos · {self.total} movimientos mínimos (2³ − 1 = 7)",
                 bg=BG, fg=TEXT_DIM, font=("Courier", 9)).pack(anchor="w", pady=(0,12))

        # ── Canvas torres
        self.canvas = tk.Canvas(self, bg=PANEL, height=210, relief="flat",
                                highlightthickness=1, highlightbackground=BORDER)
        self.canvas.pack(fill="x", pady=(0,12))

        # ── Info paso
        self.desc_var = tk.StringVar(value="Estado inicial")
        self.desc_lbl = tk.Label(self, textvariable=self.desc_var,
                                 bg=PANEL, fg=AMBER, font=("Courier", 12, "bold"),
                                 pady=8, relief="flat",
                                 highlightthickness=1, highlightbackground=BORDER)
        self.desc_lbl.pack(fill="x", pady=(0,12))

        # ── Controles
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(pady=(0,14))

        btn_cfg = {"font": ("Courier", 10), "relief": "flat", "padx": 14, "pady": 7,
                   "cursor": "hand2", "bd": 0}

        self.btn_reset = tk.Button(ctrl, text="↺ REINICIAR", bg=PANEL, fg=TEXT_DIM,
                                   activebackground=BORDER, activeforeground=TEXT,
                                   command=self._reset, **btn_cfg)
        self.btn_reset.pack(side="left", padx=4)

        self.btn_prev = tk.Button(ctrl, text="← ANTERIOR", bg=PANEL, fg=TEXT_DIM,
                                  activebackground=BORDER, activeforeground=TEXT,
                                  command=self._prev, **btn_cfg)
        self.btn_prev.pack(side="left", padx=4)

        self.btn_play = tk.Button(ctrl, text="▶ AUTO", bg=AMBER, fg="#0d0f18",
                                  activebackground="#c98b00", activeforeground="#0d0f18",
                                  font=("Courier", 10, "bold"), relief="flat",
                                  padx=14, pady=7, cursor="hand2",
                                  command=self._toggle_play)
        self.btn_play.pack(side="left", padx=4)

        self.btn_next = tk.Button(ctrl, text="SIGUIENTE →", bg=PANEL, fg=TEXT_DIM,
                                  activebackground=BORDER, activeforeground=TEXT,
                                  command=self._next, **btn_cfg)
        self.btn_next.pack(side="left", padx=4)

        # ── Progress bar
        prog_frame = tk.Frame(self, bg=BG)
        prog_frame.pack(fill="x", pady=(0,14))
        self.prog_canvas = tk.Canvas(prog_frame, bg=PANEL, height=6,
                                     highlightthickness=0)
        self.prog_canvas.pack(fill="x")

        # ── Historial de movimientos
        tk.Label(self, text="HISTORIAL DE MOVIMIENTOS",
                 bg=BG, fg=TEXT_DIM, font=("Courier", 8)).pack(anchor="w", pady=(0,6))
        self.hist_frame = tk.Frame(self, bg=BG)
        self.hist_frame.pack(fill="x")
        self._build_hist()

    def _build_hist(self):
        for w in self.hist_frame.winfo_children():
            w.destroy()
        for i, m in enumerate(self.movimientos[1:], 1):
            color = AMBER if i == self.paso else (TEXT_DIM if i < self.paso else TEXT_FNT)
            bg_c  = "#1a1208" if i == self.paso else (PANEL if i < self.paso else BG)
            lbl = tk.Label(self.hist_frame,
                           text=f"{m['disco']}:{m['desde']}→{m['hacia']}",
                           bg=bg_c, fg=color,
                           font=("Courier", 9), padx=8, pady=4,
                           relief="flat", cursor="hand2",
                           highlightthickness=1,
                           highlightbackground=AMBER if i == self.paso else BORDER)
            lbl.grid(row=0, column=i-1, padx=3, pady=2)
            lbl.bind("<Button-1>", lambda e, idx=i: self._goto(idx))

    def _render(self):
        estado = self.movimientos[self.paso]
        self._draw_torres(estado)
        self.desc_var.set(estado['desc'])
        if self.paso == self.total:
            self.desc_lbl.config(fg=TEAL, bg="#0d1a14")
        elif self.paso == 0:
            self.desc_lbl.config(fg=TEXT_DIM, bg=PANEL)
        else:
            self.desc_lbl.config(fg=AMBER, bg="#1a1208")
        self._draw_progress()
        self._build_hist()
        # Estado botones
        self.btn_prev.config(state="normal" if self.paso > 0 else "disabled",
                             fg=TEXT_DIM if self.paso > 0 else TEXT_FNT)
        self.btn_next.config(state="normal" if self.paso < self.total else "disabled",
                             fg=TEXT_DIM if self.paso < self.total else TEXT_FNT)

    def _draw_torres(self, estado):
        c = self.canvas
        c.delete("all")
        c.update_idletasks()
        W = c.winfo_width() or 700
        H = c.winfo_height() or 210
        nombres = ['A', 'B', 'C']
        sec_w = W // 3
        disk_max_w = sec_w - 40
        disk_h = 26
        base_y = H - 26
        post_h = 140
        disk_widths = [disk_max_w * 0.45, disk_max_w * 0.65, disk_max_w * 0.88]

        for idx, nombre in enumerate(nombres):
            cx = sec_w * idx + sec_w // 2
            discos = estado[nombre]
            highlight = nombre in (estado.get('desde'), estado.get('hacia'))

            # Base
            bw = sec_w * 0.7
            c.create_rectangle(cx - bw//2, base_y, cx + bw//2, base_y + 8,
                                fill=AMBER if highlight else BORDER, outline="")

            # Poste
            c.create_rectangle(cx - 4, base_y - post_h, cx + 4, base_y,
                                fill=AMBER if highlight else BORDER, outline="")

            # Discos
            for di, disco in enumerate(discos):
                dw = disk_widths[disco - 1]
                dy = base_y - (di + 1) * (disk_h + 4) + 2
                color = DISK_COLORS[disco - 1]
                r = 5
                x1, y1 = cx - dw//2, dy
                x2, y2 = cx + dw//2, dy + disk_h
                c.create_polygon(
                    x1+r, y1, x2-r, y1,
                    x2, y1+r, x2, y2-r,
                    x2-r, y2, x1+r, y2,
                    x1, y2-r, x1, y1+r,
                    fill=color, outline="", smooth=True
                )
                c.create_text(cx, dy + disk_h//2, text=str(disco),
                              fill="#0d0f18", font=("Courier", 10, "bold"))

            # Etiqueta torre
            c.create_text(cx, base_y + 16, text=f"TORRE {nombre}",
                          fill=AMBER if highlight else TEXT_DIM,
                          font=("Courier", 9, "bold"))

    def _draw_progress(self):
        c = self.prog_canvas
        c.delete("all")
        c.update_idletasks()
        W = c.winfo_width() or 700
        pct = self.paso / self.total if self.total else 0
        c.create_rectangle(0, 0, W, 6, fill=PANEL, outline="")
        if pct > 0:
            c.create_rectangle(0, 0, int(W * pct), 6, fill=AMBER, outline="")

    def _next(self):
        if self.paso < self.total:
            self.paso += 1
            self._render()

    def _prev(self):
        if self.paso > 0:
            self.paso -= 1
            self._render()

    def _goto(self, idx):
        self.paso = idx
        self._render()

    def _reset(self):
        self._stop_play()
        self.paso = 0
        self._render()

    def _toggle_play(self):
        if self._playing:
            self._stop_play()
        else:
            if self.paso >= self.total:
                self.paso = 0
            self._playing = True
            self.btn_play.config(text="⏸ PAUSAR", bg=RED, fg="#0d0f18")
            self._auto_step()

    def _stop_play(self):
        self._playing = False
        self.btn_play.config(text="▶ AUTO", bg=AMBER, fg="#0d0f18")
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _auto_step(self):
        if not self._playing: return
        if self.paso < self.total:
            self.paso += 1
            self._render()
            self._after_id = self.after(850, self._auto_step)
        else:
            self._stop_play()


if __name__ == "__main__":
    app = App()
    app.mainloop()