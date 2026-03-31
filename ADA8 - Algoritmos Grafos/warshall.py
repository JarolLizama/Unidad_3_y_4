"""
Algoritmo de Warshall (Clausura Transitiva)
Determina si existe un camino (alcanzabilidad) entre cada par de vértices.
Aplicado al grafo de 7 estados de la República Mexicana.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext

# ─── DATOS ───────────────────────────────────────────────────────────────────
ESTADOS = [
    "CDMX", "Puebla", "Veracruz", "Oaxaca",
    "Guerrero", "Morelos", "Tlaxcala"
]
ARISTAS = [
    ("CDMX",     "Puebla",    130),
    ("CDMX",     "Morelos",    90),
    ("CDMX",     "Tlaxcala",  120),
    ("CDMX",     "Guerrero",  260),
    ("Puebla",   "Tlaxcala",   30),
    ("Puebla",   "Veracruz",  220),
    ("Puebla",   "Oaxaca",    350),
    ("Puebla",   "Morelos",   160),
    ("Veracruz", "Oaxaca",    310),
    ("Oaxaca",   "Guerrero",  380),
    ("Morelos",  "Guerrero",  195),
    ("Tlaxcala", "Veracruz",  200),
]

# ─── WARSHALL ────────────────────────────────────────────────────────────────
def warshall(estados, aristas):
    n = len(estados)
    idx = {e: i for i, e in enumerate(estados)}

    # Matriz de alcanzabilidad inicial
    R = [[False]*n for _ in range(n)]
    for i in range(n):
        R[i][i] = True
    for u, v, _ in aristas:
        i, j = idx[u], idx[v]
        R[i][j] = True
        R[j][i] = True

    pasos = [("Inicial", [row[:] for row in R])]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if R[i][k] and R[k][j]:
                    R[i][j] = True
        pasos.append((estados[k], [row[:] for row in R]))

    return R, pasos, idx

# ─── GUI ─────────────────────────────────────────────────────────────────────
C = {
    "bg": "#0d1117", "panel": "#161b22", "card": "#1c2333",
    "border": "#30363d", "cyan": "#39d353", "verde": "#3fb950",
    "rojo": "#f78166", "oro": "#e3b341", "texto": "#e6edf3",
    "sub": "#8b949e", "nodo": "#1a7f37",
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algoritmo de Warshall — Clausura Transitiva")
        self.configure(bg=C["bg"])
        self.geometry("1100x700")

        self.R, self.pasos, self.idx = warshall(ESTADOS, ARISTAS)
        self.paso_actual = 0
        self.orig_var = tk.StringVar(value=ESTADOS[0])
        self.dest_var = tk.StringVar(value=ESTADOS[3])
        self._build()

    def _build(self):
        tk.Label(self, text="ALGORITMO DE WARSHALL",
                 font=("Courier New",18,"bold"), fg=C["cyan"], bg=C["bg"]).pack(anchor="w", padx=20, pady=(14,0))
        tk.Label(self, text="Clausura transitiva — ¿Existe camino entre cada par? — Estados de México",
                 font=("Courier New",9), fg=C["sub"], bg=C["bg"]).pack(anchor="w", padx=20)
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x", padx=20, pady=8)

        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=20, pady=(0,16))

        # Izquierda
        left = tk.Frame(body, bg=C["bg"])
        left.pack(side="left", fill="both", expand=True)

        # Matriz actual
        mf = tk.Frame(left, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        mf.pack(fill="x")
        tk.Label(mf, text="MATRIZ DE ALCANZABILIDAD",
                 font=("Courier New",9,"bold"), fg=C["cyan"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        self.mat_frame = tk.Frame(mf, bg=C["panel"])
        self.mat_frame.pack(padx=10, pady=(0,10))

        # Control paso a paso
        pf = tk.Frame(left, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        pf.pack(fill="x", pady=(8,0))
        tk.Label(pf, text="EVOLUCIÓN PASO A PASO",
                 font=("Courier New",9,"bold"), fg=C["oro"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))

        nav = tk.Frame(pf, bg=C["panel"])
        nav.pack(fill="x", padx=10, pady=4)
        tk.Button(nav, text="◀ Anterior", font=("Courier New",8), fg=C["texto"],
                  bg=C["card"], relief="flat", cursor="hand2",
                  command=self._anterior).pack(side="left", padx=(0,4))
        tk.Button(nav, text="Siguiente ▶", font=("Courier New",8), fg=C["texto"],
                  bg=C["card"], relief="flat", cursor="hand2",
                  command=self._siguiente).pack(side="left")
        tk.Button(nav, text="Ver final", font=("Courier New",8,"bold"), fg=C["bg"],
                  bg=C["cyan"], relief="flat", cursor="hand2",
                  command=self._final).pack(side="right")
        self.lbl_paso = tk.Label(pf, text="", font=("Courier New",9),
                                 fg=C["oro"], bg=C["panel"])
        self.lbl_paso.pack(anchor="w", padx=10, pady=(0,8))

        self._actualizar_matriz()

        # Derecha
        right = tk.Frame(body, bg=C["bg"], width=310)
        right.pack(side="right", fill="y", padx=(12,0))
        right.pack_propagate(False)

        # Consulta
        cf = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        cf.pack(fill="x", pady=(0,8))
        tk.Label(cf, text="CONSULTAR ALCANZABILIDAD",
                 font=("Courier New",9,"bold"), fg=C["cyan"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        for lbl, var in [("Origen:", self.orig_var), ("Destino:", self.dest_var)]:
            row = tk.Frame(cf, bg=C["panel"])
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=lbl, font=("Courier New",8), fg=C["texto"],
                     bg=C["panel"], width=8, anchor="w").pack(side="left")
            ttk.Combobox(row, textvariable=var, values=ESTADOS, state="readonly", width=12).pack(side="left")
        tk.Button(cf, text="▶  Consultar",
                  font=("Courier New",9,"bold"), fg=C["bg"], bg=C["cyan"],
                  relief="flat", cursor="hand2", pady=6,
                  command=self._consultar).pack(fill="x", padx=10, pady=8)

        # Output
        of = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        of.pack(fill="both", expand=True)
        tk.Label(of, text="RESULTADO Y ANÁLISIS",
                 font=("Courier New",9,"bold"), fg=C["cyan"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        self.out = scrolledtext.ScrolledText(of, font=("Courier New",9),
            bg=C["bg"], fg=C["texto"], relief="flat", wrap="word")
        self.out.pack(fill="both", expand=True, padx=8, pady=(0,8))
        self.out.tag_config("t", foreground=C["cyan"], font=("Courier New",9,"bold"))
        self.out.tag_config("ok", foreground=C["verde"])
        self.out.tag_config("no", foreground=C["rojo"])
        self.out.tag_config("hl", foreground=C["oro"])
        self.out.tag_config("s", foreground=C["sub"])

        tk.Button(right, text="Mostrar resumen completo",
                  font=("Courier New",8), fg=C["texto"], bg=C["card"],
                  relief="flat", cursor="hand2", pady=4,
                  command=self._resumen).pack(fill="x", pady=4)

        # Inicializar
        self._resumen()

    def _actualizar_matriz(self):
        for w in self.mat_frame.winfo_children(): w.destroy()
        nombre, mat = self.pasos[self.paso_actual]
        self.lbl_paso.config(text=f"Paso {self.paso_actual}: k = {nombre}")

        tk.Label(self.mat_frame, text="", font=("Courier New",7),
                 bg=C["panel"], width=9).grid(row=0, column=0)
        for j, e in enumerate(ESTADOS):
            tk.Label(self.mat_frame, text=e[:6], font=("Courier New",7,"bold"),
                     fg=C["cyan"], bg=C["card"], width=9, pady=2).grid(row=0, column=j+1, padx=1, pady=1)
        for i, u in enumerate(ESTADOS):
            tk.Label(self.mat_frame, text=u[:6], font=("Courier New",7,"bold"),
                     fg=C["cyan"], bg=C["card"], width=9, pady=2).grid(row=i+1, column=0, padx=1, pady=1)
            for j in range(len(ESTADOS)):
                val = mat[i][j]
                bg = "#0d2b0d" if val else "#2b0d0d"
                fg = C["verde"] if val else C["rojo"]
                txt = "1" if val else "0"
                if i == j: bg, fg, txt = C["card"], C["sub"], "─"
                tk.Label(self.mat_frame, text=txt, font=("Courier New",8,"bold"),
                         fg=fg, bg=bg, width=9, pady=2).grid(row=i+1, column=j+1, padx=1, pady=1)

    def _anterior(self):
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self._actualizar_matriz()

    def _siguiente(self):
        if self.paso_actual < len(self.pasos)-1:
            self.paso_actual += 1
            self._actualizar_matriz()

    def _final(self):
        self.paso_actual = len(self.pasos)-1
        self._actualizar_matriz()

    def _consultar(self):
        u = self.orig_var.get()
        v = self.dest_var.get()
        i, j = self.idx[u], self.idx[v]
        alcanza = self.R[i][j]
        self.out.delete("1.0","end")
        self.out.insert("end", f"¿{u} puede alcanzar {v}?\n","t")
        self.out.insert("end","─"*30+"\n","s")
        if alcanza:
            self.out.insert("end", f"  ✓ SÍ existe camino\n","ok")
        else:
            self.out.insert("end", f"  ✗ NO existe camino\n","no")
        self.out.insert("end",f"\n  R[{u}][{v}] = {'1 (verdadero)' if alcanza else '0 (falso)'}\n","hl")

    def _resumen(self):
        self.out.delete("1.0","end")
        self.out.insert("end","Clausura Transitiva — Resumen:\n","t")
        self.out.insert("end","─"*30+"\n","s")
        conectados = sum(1 for i in range(len(ESTADOS)) for j in range(len(ESTADOS)) if i!=j and self.R[i][j])
        total = len(ESTADOS)*(len(ESTADOS)-1)
        self.out.insert("end",f"  Pares con camino: {conectados}/{total}\n","ok")
        self.out.insert("end",f"  Grafo {'fuertemente ' if conectados==total else 'NO '}conexo\n",
                        "ok" if conectados==total else "no")
        self.out.insert("end","\n  Relaciones posibles:\n","s")
        for u in ESTADOS:
            alcanza = [v for v in ESTADOS if v!=u and self.R[self.idx[u]][self.idx[v]]]
            self.out.insert("end",f"  {u}: → {', '.join(alcanza)}\n","ok")

if __name__ == "__main__":
    App().mainloop()