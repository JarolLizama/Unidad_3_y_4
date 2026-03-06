"""
Torres de Hanói — Interactivo + Panel de Análisis
Clic en torre origen → clic en torre destino.
Botón 📊 ANÁLISIS abre ventana con métodos, benchmark y conclusiones.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import time, sys, threading, math, random

W, H        = 900, 600
BG          = "#0A0A14"
GROUND_Y    = 460
PEG_H       = 300
PEG_W       = 12
BASE_H      = 18
BASE_W      = 220
DISC_H      = 28
MIN_DISC_W  = 48
MAX_DISC_W  = 190
PEG_X       = [180, 450, 720]

DISC_PALETTE = ["#EF4444","#F97316","#F59E0B","#84CC16",
                "#10B981","#06B6D4","#6366F1","#A855F7"]

FONT_TITLE = ("Courier New", 22, "bold")
FONT_SUB   = ("Courier New", 10)
FONT_LABEL = ("Courier New", 12, "bold")
FONT_COUNT = ("Courier New", 28, "bold")
FONT_BTN   = ("Courier New", 10, "bold")
ANIM_FPS   = 16
ANIM_STEPS = 22

METHODS_DATA = [
    ("1",  "__init__",           "Inicializa estado, variables y llama a _build_ui",                 "Ciclo de vida"),
    ("2",  "_build_ui",          "Construye toda la interfaz: canvas, botones, labels, panel",       "Interfaz"),
    ("3",  "_btn",               "Factory para crear botones con estilo uniforme",                   "Interfaz"),
    ("4",  "_new_game",          "Reinicia pila logica, contador y redibuja desde cero",             "Juego"),
    ("5",  "_set_discs",         "Cambia la cantidad de discos activos y reinicia",                  "Juego"),
    ("6",  "_draw_scene",        "Orquesta el redibujo completo del canvas",                         "Dibujo"),
    ("7",  "_draw_static",       "Dibuja elementos fijos: suelo, tres postes y bases",               "Dibujo"),
    ("8",  "_disc_width",        "Calcula el ancho en px de un disco segun su tamano relativo",      "Dibujo"),
    ("9",  "_disc_y",            "Calcula la coordenada Y de un disco en la pila",                   "Dibujo"),
    ("10", "_draw_disc",         "Dibuja un disco con color degradado, brillo y numero",             "Dibujo"),
    ("11", "_rounded_rect",      "Dibuja un poligono con esquinas redondeadas",                      "Dibujo"),
    ("12", "_lighten (static)",  "Aclara un color hexadecimal para simular brillo",                  "Utilidad"),
    ("13", "_peg_from_x",        "Detecta en que torre hizo clic el usuario por coordenada X",       "Interaccion"),
    ("14", "_on_click",          "Manejador principal de clic: seleccion y disparo de movimiento",   "Interaccion"),
    ("15", "_try_move",          "Valida la regla LIFO antes de ejecutar el movimiento",             "Juego"),
    ("16", "_execute_move",      "Realiza el movimiento logico y lanza animacion en 3 fases",        "Juego"),
    ("17", "_draw_traveler",     "Dibuja el disco en vuelo frame a frame durante animacion",         "Dibujo"),
    ("18", "_ease (static)",     "Curva de interpolacion suave ease in-out para animaciones",        "Utilidad"),
    ("19", "_highlight_peg",     "Dibuja recuadro dorado punteado en torre seleccionada",            "Visual"),
    ("20", "_clear_highlights",  "Elimina el recuadro de seleccion del canvas",                      "Visual"),
    ("21", "_flash_empty",       "Parpadeo rojo al hacer clic en torre vacia",                       "Visual"),
    ("22", "_flash_invalid",     "Parpadeo rojo al intentar movimiento invalido",                    "Visual"),
    ("23", "_auto_solve",        "Prepara y lanza la resolucion automatica completa",                "Auto-solver"),
    ("24", "_hanoi_moves",       "Algoritmo recursivo O(2^n) que genera la secuencia optima",        "Auto-solver"),
    ("25", "_play_next_auto",    "Reproduce un movimiento de la cola y encadena el siguiente",       "Auto-solver"),
    ("26", "_check_win",         "Detecta si los n discos llegaron a la torre C",                   "Juego"),
    ("27", "_celebrate",         "Lluvia de destellos dorados al ganar el puzzle",                  "Visual"),
    ("28", "_open_analysis",     "Abre la ventana de analisis tecnico con 3 pestanas",              "Interfaz"),
    ("29", "_build_methods_tab", "Construye la tabla de metodos en el panel de analisis",           "Interfaz"),
    ("30", "_build_bench_tab",   "Construye la pestana de benchmark con ejecucion en vivo",         "Interfaz"),
    ("31", "_run_benchmark",     "Ejecuta el benchmark real en un hilo secundario",                 "Utilidad"),
    ("32", "_build_concl_tab",   "Construye la pestana de conclusiones con texto formateado",       "Interfaz"),
]

CAT_COLORS = {
    "Ciclo de vida": "#64748B", "Interfaz": "#3B82F6",
    "Juego": "#10B981",         "Dibujo": "#8B5CF6",
    "Utilidad": "#F59E0B",      "Interaccion": "#06B6D4",
    "Visual": "#EC4899",        "Auto-solver": "#EF4444",
}

CONCLUSIONS = [
    ("1.  Complejidad exponencial O(2^n)",
     "El algoritmo pertenece a la clase O(2^n): cada disco adicional DUPLICA exactamente\n"
     "el numero de movimientos. La formula 2^n - 1 es exacta. Pasar de 30 a 31 discos\n"
     "no es 'un poco mas dificil': es exactamente el doble de trabajo."),
    ("2.  La elegancia recursiva oculta el costo",
     "_hanoi_moves() tiene 6 lineas y es hermoso de leer. Pero esa elegancia esconde\n"
     "un crecimiento explosivo que vuelve al algoritmo inviable mas alla de ~25 discos.\n"
     "La legibilidad del codigo NO garantiza su escalabilidad."),
    ("3.  El cuello de botella es la memoria, no el CPU",
     "Para 30 discos Python necesita ~1,073 millones de tuplas, aprox. 16 GB de RAM.\n"
     "La mayoria de PCs quedaria sin memoria antes de terminar la generacion.\n"
     "El problema no es la velocidad del CPU, sino almacenar la secuencia completa."),
    ("4.  Separacion entre logica y animacion",
     "_hanoi_moves() genera TODOS los movimientos de golpe en una lista.\n"
     "_play_next_auto() los consume uno a uno con root.after(), manteniendo la GUI\n"
     "responsiva. Funciona bien hasta ~20 discos; mas alla bloquea la interfaz."),
    ("5.  El limite no es tecnologico, es matematico",
     "Con 64 discos, a 1,000,000,000 movimientos/segundo tardaria ~585 ANOS.\n"
     "Ninguna mejora de hardware cambia este hecho: la complejidad exponencial\n"
     "convierte el problema en computacionalmente IMPOSIBLE a escalas modestas."),
]


class HanoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanoi")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.n_discs = 5
        self.pegs = [[], [], []]
        self.selected = None
        self.animating = False
        self.moves = 0
        self.auto_seq = []
        self.won = False
        self.disc_items = {}
        self._build_ui()
        self._new_game()

    def _build_ui(self):
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=30, pady=(18, 0))
        tk.Label(top, text="TORRES DE HANOI", font=FONT_TITLE, bg=BG, fg="#F59E0B").pack(side="left")
        tk.Label(top, text="clic en torre origen  ->  clic en torre destino",
                 font=FONT_SUB, bg=BG, fg="#444466").pack(side="left", padx=24)

        self.canvas = tk.Canvas(self.root, width=W, height=H-130,
                                bg=BG, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        bot = tk.Frame(self.root, bg="#0D0D1E")
        bot.pack(fill="x")

        disc_frame = tk.Frame(bot, bg="#0D0D1E")
        disc_frame.pack(side="left", padx=24, pady=10)
        tk.Label(disc_frame, text="Discos:", font=FONT_BTN, bg="#0D0D1E", fg="#888899").pack(side="left")
        self.disc_var = tk.IntVar(value=5)
        for n in range(3, 8):
            tk.Radiobutton(disc_frame, text=str(n), variable=self.disc_var, value=n,
                           font=FONT_BTN, bg="#0D0D1E", fg="#CCCCDD",
                           selectcolor="#1A1A30", activebackground="#0D0D1E",
                           command=lambda v=n: self._set_discs(v)).pack(side="left", padx=4)

        btn_frame = tk.Frame(bot, bg="#0D0D1E")
        btn_frame.pack(side="left", padx=10, pady=10)
        self._btn(btn_frame, "Reiniciar",      "#6366F1", self._new_game)
        self._btn(btn_frame, "Auto-Resolver",  "#D97706", self._auto_solve)
        self._btn(btn_frame, "Analisis",        "#0F766E", self._open_analysis)

        cnt = tk.Frame(bot, bg="#0D0D1E")
        cnt.pack(side="right", padx=30, pady=6)
        tk.Label(cnt, text="MOVIMIENTOS", font=FONT_BTN, bg="#0D0D1E", fg="#444466").pack()
        self.lbl_moves = tk.Label(cnt, text="0", font=FONT_COUNT, bg="#0D0D1E", fg="#F59E0B")
        self.lbl_moves.pack()

        opt = tk.Frame(bot, bg="#0D0D1E")
        opt.pack(side="right", padx=20, pady=6)
        tk.Label(opt, text="OPTIMO", font=FONT_BTN, bg="#0D0D1E", fg="#444466").pack()
        self.lbl_opt = tk.Label(opt, text="", font=FONT_COUNT, bg="#0D0D1E", fg="#10B981")
        self.lbl_opt.pack()

    def _btn(self, parent, text, color, cmd):
        tk.Button(parent, text=text, font=FONT_BTN, bg=color, fg="white",
                  activebackground=color, activeforeground="white",
                  relief="flat", cursor="hand2", padx=12, pady=6,
                  command=cmd).pack(side="left", padx=6)

    # ── ANÁLISIS ─────────────────────────────────────────
    def _open_analysis(self):
        win = tk.Toplevel(self.root)
        win.title("Analisis Tecnico  -  Torres de Hanoi")
        win.configure(bg="#0D0D1E")
        win.geometry("1040x700")

        tk.Label(win, text="ANALISIS TECNICO",
                 font=("Courier New", 18, "bold"), bg="#0D0D1E", fg="#F59E0B").pack(pady=(16,2))
        tk.Label(win, text="Torres de Hanoi  |  Metodos  *  Benchmark  *  Conclusiones",
                 font=("Courier New", 10), bg="#0D0D1E", fg="#444466").pack(pady=(0,10))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("D.TNotebook", background="#0D0D1E", borderwidth=0)
        style.configure("D.TNotebook.Tab", background="#1A1A30", foreground="#AAAACC",
                         font=("Courier New", 11, "bold"), padding=[20, 8])
        style.map("D.TNotebook.Tab",
                  background=[("selected","#0F766E")],
                  foreground=[("selected","white")])

        nb = ttk.Notebook(win, style="D.TNotebook")
        nb.pack(fill="both", expand=True, padx=14, pady=(0,14))

        t1 = tk.Frame(nb, bg="#0D0D1E")
        t2 = tk.Frame(nb, bg="#0D0D1E")
        t3 = tk.Frame(nb, bg="#0D0D1E")
        nb.add(t1, text="  Metodos (%d)  " % len(METHODS_DATA))
        nb.add(t2, text="  Benchmark  ")
        nb.add(t3, text="  Conclusiones  ")

        self._build_methods_tab(t1)
        self._build_bench_tab(t2)
        self._build_concl_tab(t3)

    def _build_methods_tab(self, parent):
        tk.Label(parent,
                 text="  La clase HanoiApp contiene %d metodos distribuidos en 8 categorias." % len(METHODS_DATA),
                 font=("Courier New", 10), bg="#111124", fg="#94A3B8",
                 anchor="w", pady=6).pack(fill="x", padx=10, pady=(8,2))

        leg = tk.Frame(parent, bg="#0D0D1E")
        leg.pack(fill="x", padx=10, pady=4)
        for cat, col in CAT_COLORS.items():
            f = tk.Frame(leg, bg=col)
            f.pack(side="left", padx=2)
            tk.Label(f, text="  %s  " % cat, font=("Courier New", 8, "bold"),
                     bg=col, fg="white").pack()

        frame = tk.Frame(parent, bg="#0D0D1E")
        frame.pack(fill="both", expand=True, padx=10, pady=6)

        vsb = tk.Scrollbar(frame)
        vsb.pack(side="right", fill="y")

        style = ttk.Style()
        style.configure("M.Treeview", background="#111124", foreground="#E2E8F0",
                         fieldbackground="#111124", font=("Courier New", 10), rowheight=26)
        style.configure("M.Treeview.Heading", background="#1E3A5F", foreground="white",
                         font=("Courier New", 10, "bold"))
        style.map("M.Treeview", background=[("selected","#1E40AF")], foreground=[("selected","white")])

        cols = ("#", "Metodo", "Descripcion", "Categoria")
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            style="M.Treeview", yscrollcommand=vsb.set)
        vsb.config(command=tree.yview)

        for col, w in zip(cols, [38, 175, 555, 115]):
            tree.heading(col, text=col)
            tree.column(col, width=w, minwidth=w, anchor="center" if col=="#" else "w")

        for i, (num, name, desc, cat) in enumerate(METHODS_DATA):
            tag = "r%d" % i
            tree.insert("", "end", values=(num, name, desc, cat), tags=(tag,))
            tree.tag_configure(tag,
                background="#111124" if i%2==0 else "#161628",
                foreground="#E2E8F0")

        tree.pack(fill="both", expand=True)

    def _build_bench_tab(self, parent):
        tk.Label(parent,
                 text="  Tiempo de ejecucion del algoritmo recursivo _hanoi_moves() para distintos tamanos de entrada",
                 font=("Courier New", 10), bg="#111124", fg="#94A3B8",
                 anchor="w", pady=6).pack(fill="x", padx=10, pady=(8,6))

        tbl = tk.Frame(parent, bg="#0D0D1E")
        tbl.pack(fill="x", padx=10, pady=4)

        hdrs  = ["Discos", "Movimientos  (2^n - 1)", "Tiempo medido", "RAM requerida", "Estado"]
        widths= [7,         29,                        14,               14,              24]
        for c, (h, w) in enumerate(zip(hdrs, widths)):
            tk.Label(tbl, text=h, font=("Courier New", 10, "bold"),
                     bg="#1E3A5F", fg="white", width=w,
                     padx=6, pady=6, anchor="center").grid(row=0, column=c, sticky="nsew", padx=1, pady=1)

        placeholders = [
            ("5",  "31",                         "...", "< 1 KB",      "esperando..."),
            ("10", "1,023",                       "...", "~16 KB",      "esperando..."),
            ("30", "1,073,741,823",               "...", "~16 GB",      "esperando..."),
            ("64", "18,446,744,073,709,551,615",  "...", "~295 Exabytes","esperando..."),
        ]
        row_bgs = ["#0D2B1F","#0D2B1F","#2D1B00","#2B0000"]
        self._bench_cells = []
        for r, (vals, bg) in enumerate(zip(placeholders, row_bgs), 1):
            row = []
            for c, (v, w) in enumerate(zip(vals, widths)):
                lbl = tk.Label(tbl, text=v, font=("Courier New", 9 if c==1 else 10),
                               bg=bg, fg="#E2E8F0", width=w,
                               padx=6, pady=5, anchor="center")
                lbl.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
                row.append(lbl)
            self._bench_cells.append(row)

        self._run_btn = tk.Button(parent, text="EJECUTAR BENCHMARK",
                                  font=("Courier New", 11, "bold"),
                                  bg="#0F766E", fg="white",
                                  activebackground="#0D9488",
                                  relief="flat", cursor="hand2", padx=20, pady=8,
                                  command=lambda: self._run_benchmark(self._run_btn))
        self._run_btn.pack(pady=10)

        self._bench_log = tk.Text(parent, height=5, font=("Courier New", 10),
                                   bg="#080812", fg="#86EFAC",
                                   insertbackground="#86EFAC",
                                   bd=0, padx=10, pady=8, state="disabled")
        self._bench_log.pack(fill="x", padx=10, pady=(0,8))

        # Barras log-escala
        tk.Label(parent, text="  Escala relativa de movimientos  (log2)",
                 font=("Courier New", 9), bg="#0D0D1E", fg="#64748B").pack(anchor="w", padx=12)
        bar_frame = tk.Frame(parent, bg="#0D0D1E")
        bar_frame.pack(fill="x", padx=12, pady=2)
        bar_colors = ["#10B981","#3B82F6","#F59E0B","#EF4444"]
        bar_labels  = ["n= 5  (31 movs)", "n=10  (1,023 movs)",
                        "n=30  (1,073 M movs)", "n=64  (18,446 Q movs)"]
        max_log = math.log2(2**64)
        for d, col, lbl in zip([5,10,30,64], bar_colors, bar_labels):
            pix = max(4, int(math.log2(2**d) / max_log * 820))
            row = tk.Frame(bar_frame, bg="#0D0D1E")
            row.pack(fill="x", pady=1)
            tk.Label(row, text=lbl, font=("Courier New", 8),
                     bg="#0D0D1E", fg="#64748B", width=22, anchor="e").pack(side="left")
            tk.Frame(row, bg=col, height=14, width=pix).pack(side="left", padx=(4,0))

    def _run_benchmark(self, btn):
        btn.config(state="disabled", text="Ejecutando...")
        self._bench_log.config(state="normal")
        self._bench_log.delete("1.0", "end")
        self._bench_log.insert("end", "  Iniciando benchmark...\n")
        self._bench_log.config(state="disabled")

        STATUS_COLORS = ["#10B981","#3B82F6","#F59E0B","#EF4444"]
        STATUS_TEXT   = ["Completado","Completado",
                          "Estimado (20 discos medidos)",
                          "Imposible (~585 anos)"]

        sys.setrecursionlimit(2_000_000)

        def hanoi(n, s, d, a, out):
            if n==1: out.append((s,d)); return
            hanoi(n-1,s,a,d,out); out.append((s,d)); hanoi(n-1,a,d,s,out)

        def worker():
            results = []
            for d in [5, 10]:
                m=[]; t0=time.perf_counter(); hanoi(d,0,2,1,m); t1=time.perf_counter()
                ms = (t1-t0)*1000
                results.append((d, f"{len(m):,}", f"{ms:.4f} ms",
                                 "< 1 KB" if d==5 else "~16 KB"))
            # 20 discos como proxy de 30
            m=[]; t0=time.perf_counter(); hanoi(20,0,2,1,m); t1=time.perf_counter()
            t30 = (t1-t0)*1024
            results.append((30, "1,073,741,823",
                             f"~{t30:.1f} s  (est.)", "~16 GB"))
            # 64 matematico
            years = (2**64-1)/(1e9*60*60*24*365)
            results.append((64, "18,446,744,073,709,551,615",
                             f"~{years:,.0f} anos", "~295 EB"))

            def ui():
                for i, (d, movs, t_str, ram) in enumerate(results):
                    self._bench_cells[i][2].config(text=t_str, fg=STATUS_COLORS[i])
                    self._bench_cells[i][3].config(text=ram)
                    self._bench_cells[i][4].config(text=STATUS_TEXT[i], fg=STATUS_COLORS[i])
                self._bench_log.config(state="normal")
                self._bench_log.delete("1.0","end")
                for d, movs, t_str, ram in results:
                    self._bench_log.insert("end","  n=%-2d  |  %-30s  movs  |  %s\n" % (d, movs, t_str))
                self._bench_log.insert("end","\n  Benchmark completado.\n")
                self._bench_log.config(state="disabled")
                btn.config(state="normal", text="Ejecutar de nuevo")
            self.root.after(0, ui)

        threading.Thread(target=worker, daemon=True).start()

    def _build_concl_tab(self, parent):
        cv = tk.Canvas(parent, bg="#0D0D1E", bd=0, highlightthickness=0)
        sb = tk.Scrollbar(parent, orient="vertical", command=cv.yview)
        cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        cv.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(cv, bg="#0D0D1E")
        wid = cv.create_window((0,0), window=inner, anchor="nw")
        cv.bind("<Configure>", lambda e: cv.itemconfig(wid, width=e.width))
        inner.bind("<Configure>", lambda e: cv.config(scrollregion=cv.bbox("all")))

        COLS = ["#10B981","#3B82F6","#8B5CF6","#F59E0B","#EF4444"]
        for (title, body), col in zip(CONCLUSIONS, COLS):
            card = tk.Frame(inner, bg="#111124", highlightbackground=col, highlightthickness=2)
            card.pack(fill="x", padx=14, pady=7, ipady=2)
            tk.Label(card, text="  " + title, font=("Courier New", 12, "bold"),
                     bg=col, fg="white", anchor="w", pady=6).pack(fill="x")
            tk.Label(card, text=body, font=("Courier New", 10),
                     bg="#111124", fg="#CBD5E1", justify="left",
                     anchor="w", wraplength=950, pady=8, padx=14).pack(fill="x")

        gold = tk.Frame(inner, bg="#292000", highlightbackground="#F59E0B", highlightthickness=2)
        gold.pack(fill="x", padx=14, pady=(12,20), ipady=6)
        tk.Label(gold, text="  Regla de oro", font=("Courier New", 12, "bold"),
                 bg="#F59E0B", fg="white", anchor="w", pady=6).pack(fill="x")
        tk.Label(gold,
                 text="Si el numero de discos crece aritmeticamente, el trabajo crece geometricamente.\n\n"
                      "La diferencia entre O(n) y O(2^n) no es una cuestion de optimizacion:\n"
                      "es la diferencia entre POSIBLE e IMPOSIBLE.",
                 font=("Courier New", 11), bg="#292000", fg="#FDE68A",
                 justify="center", pady=14).pack()

    # ── JUEGO ─────────────────────────────────────────────
    def _new_game(self):
        self.auto_seq = []; self.animating = False; self.selected = None
        self.moves = 0; self.won = False
        self.n_discs = self.disc_var.get()
        self.pegs = [list(range(self.n_discs, 0, -1)), [], []]
        self.disc_items = {}
        self.lbl_moves.config(text="0", fg="#F59E0B")
        self.lbl_opt.config(text=str(2**self.n_discs - 1))
        self._draw_scene()

    def _set_discs(self, n):
        self.n_discs = n; self._new_game()

    def _draw_scene(self):
        self.canvas.delete("all"); self.disc_items = {}
        self._draw_static()
        for p in range(3):
            for i, d in enumerate(self.pegs[p]):
                self._draw_disc(d, p, i)

    def _draw_static(self):
        c = self.canvas
        c.create_rectangle(0, GROUND_Y, W, GROUND_Y+6, fill="#1A1A2E", outline="")
        c.create_rectangle(0, GROUND_Y+4, W, GROUND_Y+6, fill="#F59E0B", outline="")
        for i, x in enumerate(PEG_X):
            c.create_rectangle(x-BASE_W//2, GROUND_Y, x+BASE_W//2, GROUND_Y+BASE_H,
                                fill="#1C1C3A", outline="#333355")
            c.create_rectangle(x-PEG_W//2, GROUND_Y-PEG_H, x+PEG_W//2, GROUND_Y,
                                fill="#2A2A50", outline="#3D3D6B")
            c.create_rectangle(x-PEG_W//2+2, GROUND_Y-PEG_H, x-PEG_W//2+4, GROUND_Y,
                                fill="#4A4A80", outline="")
            c.create_text(x, GROUND_Y+BASE_H+14, text=["A","B","C"][i],
                          fill="#555580", font=FONT_LABEL)

    def _disc_width(self, size):
        ratio = (size-1) / max(self.n_discs-1, 1)
        return int(MIN_DISC_W + ratio*(MAX_DISC_W-MIN_DISC_W))

    def _disc_y(self, peg, idx):
        return GROUND_Y - (idx+1)*DISC_H + DISC_H//2

    def _draw_disc(self, size, peg, idx, xo=None, yo=None):
        color = DISC_PALETTE[(size-1) % len(DISC_PALETTE)]
        w = self._disc_width(size)
        x = xo if xo is not None else PEG_X[peg]
        y = yo if yo is not None else self._disc_y(peg, idx)
        item = self._rounded_rect(x-w//2, y-DISC_H//2+2, x+w//2, y+DISC_H//2-2,
                                   8, fill=color, outline="")
        self.canvas.create_rectangle(x-w//2+6, y-DISC_H//2+4, x+w//2-6, y-DISC_H//2+8,
                                      fill=self._lighten(color, 0.35), outline="")
        self.canvas.create_text(x, y, text=str(size), fill="white",
                                 font=("Courier New", 9, "bold"))
        self.disc_items[size] = item
        return item

    def _rounded_rect(self, x1, y1, x2, y2, r, **kw):
        pts = [x1+r,y1, x2-r,y1, x2,y1, x2,y1+r,
               x2,y2-r, x2,y2, x2-r,y2, x1+r,y2,
               x1,y2, x1,y2-r, x1,y1+r, x1,y1, x1+r,y1]
        return self.canvas.create_polygon(pts, smooth=True, **kw)

    @staticmethod
    def _lighten(c, a):
        r,g,b = int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)
        return "#%02x%02x%02x" % (min(255,int(r+(255-r)*a)),
                                   min(255,int(g+(255-g)*a)),
                                   min(255,int(b+(255-b)*a)))

    def _peg_from_x(self, x):
        best = min(range(3), key=lambda i: abs(PEG_X[i]-x))
        return best if abs(PEG_X[best]-x) < BASE_W//2 else None

    def _on_click(self, event):
        if self.animating or self.won: return
        peg = self._peg_from_x(event.x)
        if peg is None: return
        if self.selected is None:
            if self.pegs[peg]:
                self.selected = peg; self._highlight_peg(peg, "#F59E0B")
            else:
                self._flash_empty(peg)
        else:
            src = self.selected; self.selected = None; self._clear_highlights()
            if src != peg: self._try_move(src, peg)

    def _try_move(self, src, dst):
        if not self.pegs[src]: return
        disc = self.pegs[src][-1]
        if self.pegs[dst] and self.pegs[dst][-1] < disc:
            self._flash_invalid(dst)
            messagebox.showwarning("Movimiento invalido",
                                   "No puedes poner el disco %d sobre el disco %d.\n"
                                   "Solo se puede colocar sobre uno mas grande." % (disc, self.pegs[dst][-1]))
            return
        self._execute_move(src, dst)

    def _execute_move(self, src, dst, callback=None):
        disc = self.pegs[src].pop(); self.pegs[dst].append(disc)
        self.moves += 1; self.lbl_moves.config(text=str(self.moves))
        sx, sy = PEG_X[src], self._disc_y(src, len(self.pegs[src]))
        ex, ey = PEG_X[dst], self._disc_y(dst, len(self.pegs[dst])-1)
        fy = GROUND_Y - PEG_H - 30
        self.canvas.delete("all"); self._draw_static()
        for p in range(3):
            for i, d in enumerate(self.pegs[p]):
                if not (p==dst and d==disc and i==len(self.pegs[dst])-1):
                    self._draw_disc(d, p, i)
        self.animating = True
        color = DISC_PALETTE[(disc-1) % len(DISC_PALETTE)]
        w = self._disc_width(disc)

        def lift(s=0):
            if s > ANIM_STEPS: travel(0); return
            t = s/ANIM_STEPS; self._draw_traveler(disc, sx, sy+(fy-sy)*self._ease(t), w, color)
            self.root.after(ANIM_FPS, lift, s+1)
        def travel(s=0):
            if s > ANIM_STEPS: drop(0); return
            t = s/ANIM_STEPS; self._draw_traveler(disc, sx+(ex-sx)*self._ease(t), fy, w, color)
            self.root.after(ANIM_FPS, travel, s+1)
        def drop(s=0):
            if s > ANIM_STEPS:
                self.animating = False; self._draw_scene(); self._check_win()
                if callback: callback(); return
            t = s/ANIM_STEPS; self._draw_traveler(disc, ex, fy+(ey-fy)*self._ease(t), w, color)
            self.root.after(ANIM_FPS, drop, s+1)
        lift()

    def _draw_traveler(self, disc, cx, cy, w, color):
        self.canvas.delete("traveler")
        r=8; x1,y1=cx-w//2,cy-DISC_H//2+2; x2,y2=cx+w//2,cy+DISC_H//2-2
        pts=[x1+r,y1,x2-r,y1,x2,y1,x2,y1+r,x2,y2-r,x2,y2,x2-r,y2,x1+r,y2,
             x1,y2,x1,y2-r,x1,y1+r,x1,y1,x1+r,y1]
        self.canvas.create_polygon(pts, smooth=True, fill=color, outline="white",
                                    width=2, tags="traveler")
        self.canvas.create_rectangle(cx-w//2+6, cy-DISC_H//2+4, cx+w//2-6, cy-DISC_H//2+9,
                                      fill=self._lighten(color, 0.35), outline="", tags="traveler")
        self.canvas.create_text(cx, cy, text=str(disc), fill="white",
                                 font=("Courier New", 9, "bold"), tags="traveler")
        self.canvas.create_oval(cx-w//3, GROUND_Y+2, cx+w//3, GROUND_Y+10,
                                 fill="#000000", outline="", tags="traveler", stipple="gray25")

    @staticmethod
    def _ease(t): return t*t*(3-2*t)

    def _highlight_peg(self, peg, color):
        x = PEG_X[peg]; self.canvas.delete("highlight")
        self.canvas.create_rectangle(x-BASE_W//2-4, GROUND_Y-PEG_H-10,
                                      x+BASE_W//2+4, GROUND_Y+BASE_H+4,
                                      outline=color, width=2, dash=(6,4), tags="highlight")
        self.canvas.create_text(x, GROUND_Y-PEG_H-22, text="Seleccionada",
                                 fill=color, font=("Courier New", 9, "bold"), tags="highlight")

    def _clear_highlights(self): self.canvas.delete("highlight")

    def _flash_empty(self, peg):
        x = PEG_X[peg]
        for i in range(5):
            c = "#FF4444" if i%2==0 else BG
            self.root.after(i*80, lambda col=c: self.canvas.create_rectangle(
                x-30, GROUND_Y-40, x+30, GROUND_Y, fill=col, outline="", tags="fe"))
        self.root.after(500, lambda: self.canvas.delete("fe"))

    def _flash_invalid(self, peg):
        x = PEG_X[peg]
        for i in range(6):
            c = "#FF2222" if i%2==0 else BG
            self.root.after(i*70, lambda col=c: self.canvas.create_rectangle(
                x-BASE_W//2, GROUND_Y-PEG_H, x+BASE_W//2, GROUND_Y+BASE_H,
                fill=col, outline="", tags="fi"))
        self.root.after(500, lambda: (self.canvas.delete("fi"), self._draw_scene()))

    def _auto_solve(self):
        if self.animating or self.won: return
        if any(self.pegs[1]) or any(self.pegs[2]):
            self._new_game(); self.root.after(300, self._auto_solve); return
        moves = []; self._hanoi_moves(self.n_discs, 0, 2, 1, moves)
        self.auto_seq = moves; self._play_next_auto()

    def _hanoi_moves(self, n, s, d, a, out):
        if n==1: out.append((s,d)); return
        self._hanoi_moves(n-1,s,a,d,out); out.append((s,d)); self._hanoi_moves(n-1,a,d,s,out)

    def _play_next_auto(self):
        if not self.auto_seq or self.won: return
        s, d = self.auto_seq.pop(0)
        self._execute_move(s, d, callback=lambda: self.root.after(80, self._play_next_auto))

    def _check_win(self):
        if len(self.pegs[2]) == self.n_discs:
            self.won = True
            opt = 2**self.n_discs - 1
            self._celebrate()
            msg = ("Completaste las Torres de Hanoi!\n\n"
                   "  Discos:      %d\n  Movimientos: %d\n  Optimo:      %d\n  %s"
                   % (self.n_discs, self.moves, opt, "PERFECTO!" if self.moves==opt else ""))
            self.root.after(800, lambda: messagebox.showinfo("Victoria!", msg))

    def _celebrate(self):
        for _ in range(28):
            x,y,s,d = (random.randint(50,W-50), random.randint(80,GROUND_Y-20),
                       random.randint(4,12), random.randint(0,600))
            self.root.after(d, lambda x=x,y=y,s=s: self.canvas.create_oval(
                x-s,y-s,x+s,y+s, fill="#F59E0B", outline="#FBBF24", tags="celebrate"))
        self.root.after(1400, lambda: self.canvas.delete("celebrate"))


if __name__ == "__main__":
    root = tk.Tk()
    HanoiApp(root)
    root.mainloop()