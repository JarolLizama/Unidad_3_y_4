"""
Algoritmo de Floyd-Warshall
Encuentra los caminos más cortos entre TODOS los pares de vértices.
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

INF = float('inf')

# ─── FLOYD-WARSHALL ───────────────────────────────────────────────────────────
def floyd_warshall(estados, aristas):
    n = len(estados)
    idx = {e: i for i, e in enumerate(estados)}

    dist = [[INF]*n for _ in range(n)]
    nxt  = [[None]*n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, v, p in aristas:
        i, j = idx[u], idx[v]
        dist[i][j] = p
        dist[j][i] = p
        nxt[i][j] = j
        nxt[j][i] = i

    iteraciones = []
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j]  = nxt[i][k]
        iteraciones.append((estados[k], [row[:] for row in dist]))

    return dist, nxt, iteraciones, idx

def reconstruir(nxt, idx, u, v):
    if nxt[idx[u]][idx[v]] is None:
        return []
    path = [u]
    i = idx[u]
    j = idx[v]
    while i != j:
        i = nxt[i][j]
        path.append(ESTADOS[i])
    return path

# ─── GUI ─────────────────────────────────────────────────────────────────────
C = {
    "bg": "#0d1117", "panel": "#161b22", "card": "#1c2333",
    "border": "#30363d", "morado": "#bc8cff", "verde": "#3fb950",
    "rojo": "#f78166", "oro": "#e3b341", "texto": "#e6edf3",
    "sub": "#8b949e", "nodo": "#6e40c9",
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algoritmo de Floyd-Warshall — Todos los caminos mínimos")
        self.configure(bg=C["bg"])
        self.geometry("1100x700")

        self.dist, self.nxt, self.iteraciones, self.idx = floyd_warshall(ESTADOS, ARISTAS)
        self.orig_var = tk.StringVar(value=ESTADOS[0])
        self.dest_var = tk.StringVar(value=ESTADOS[3])
        self._build()

    def _build(self):
        tk.Label(self, text="ALGORITMO DE FLOYD-WARSHALL",
                 font=("Courier New",18,"bold"), fg=C["morado"], bg=C["bg"]).pack(anchor="w", padx=20, pady=(14,0))
        tk.Label(self, text="Caminos mínimos entre TODOS los pares de vértices — Estados de México",
                 font=("Courier New",9), fg=C["sub"], bg=C["bg"]).pack(anchor="w", padx=20)
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x", padx=20, pady=8)

        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=20, pady=(0,16))

        # Izquierda: matriz
        left = tk.Frame(body, bg=C["bg"])
        left.pack(side="left", fill="both", expand=True)

        mf = tk.Frame(left, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        mf.pack(fill="both", expand=True)
        tk.Label(mf, text="MATRIZ DE DISTANCIAS MÍNIMAS (km)",
                 font=("Courier New",9,"bold"), fg=C["morado"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))

        self.mat_frame = tk.Frame(mf, bg=C["panel"])
        self.mat_frame.pack(padx=10, pady=(0,10))
        self._dibujar_matriz()

        # Iteraciones
        itf = tk.Frame(left, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        itf.pack(fill="x", pady=(8,0))
        tk.Label(itf, text="ITERACIONES (vértice intermedio k)",
                 font=("Courier New",9,"bold"), fg=C["oro"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        self.out_it = scrolledtext.ScrolledText(itf, font=("Courier New",8),
            bg=C["bg"], fg=C["texto"], relief="flat", height=6)
        self.out_it.pack(fill="x", padx=8, pady=(0,8))
        self._mostrar_iteraciones()

        # Derecha
        right = tk.Frame(body, bg=C["bg"], width=300)
        right.pack(side="right", fill="y", padx=(12,0))
        right.pack_propagate(False)

        # Consulta par
        cf = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        cf.pack(fill="x", pady=(0,8))
        tk.Label(cf, text="CONSULTAR PAR", font=("Courier New",9,"bold"),
                 fg=C["morado"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        for lbl, var in [("Origen:", self.orig_var), ("Destino:", self.dest_var)]:
            row = tk.Frame(cf, bg=C["panel"])
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=lbl, font=("Courier New",8), fg=C["texto"],
                     bg=C["panel"], width=8, anchor="w").pack(side="left")
            ttk.Combobox(row, textvariable=var, values=ESTADOS, state="readonly", width=12).pack(side="left")
        tk.Button(cf, text="▶  Consultar camino",
                  font=("Courier New",9,"bold"), fg=C["bg"], bg=C["morado"],
                  relief="flat", cursor="hand2", pady=6,
                  command=self._consultar).pack(fill="x", padx=10, pady=8)

        # Resultado
        rf = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        rf.pack(fill="both", expand=True)
        tk.Label(rf, text="RESULTADO", font=("Courier New",9,"bold"),
                 fg=C["morado"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        self.out = scrolledtext.ScrolledText(rf, font=("Courier New",9),
            bg=C["bg"], fg=C["texto"], relief="flat", wrap="word")
        self.out.pack(fill="both", expand=True, padx=8, pady=(0,8))
        self.out.tag_config("t", foreground=C["morado"], font=("Courier New",9,"bold"))
        self.out.tag_config("ok", foreground=C["verde"])
        self.out.tag_config("hl", foreground=C["oro"])
        self.out.tag_config("s", foreground=C["sub"])

        # Todos los caminos
        tk.Button(right, text="Mostrar TODOS los caminos",
                  font=("Courier New",8), fg=C["texto"], bg=C["card"],
                  relief="flat", cursor="hand2", pady=4,
                  command=self._todos_caminos).pack(fill="x", pady=4)

    def _dibujar_matriz(self):
        for w in self.mat_frame.winfo_children(): w.destroy()
        n = len(ESTADOS)
        # Encabezado columnas
        tk.Label(self.mat_frame, text="", font=("Courier New",7),
                 bg=C["panel"], width=9).grid(row=0, column=0)
        for j, e in enumerate(ESTADOS):
            tk.Label(self.mat_frame, text=e[:6], font=("Courier New",7,"bold"),
                     fg=C["morado"], bg=C["card"], width=9,
                     relief="flat", pady=2).grid(row=0, column=j+1, padx=1, pady=1)
        for i, u in enumerate(ESTADOS):
            tk.Label(self.mat_frame, text=u[:6], font=("Courier New",7,"bold"),
                     fg=C["morado"], bg=C["card"], width=9,
                     relief="flat", pady=2).grid(row=i+1, column=0, padx=1, pady=1)
            for j, v in enumerate(ESTADOS):
                d = self.dist[i][j]
                txt = "0" if i==j else (str(d) if d!=INF else "∞")
                bg = "#0d2b0d" if i==j else (C["card"] if d!=INF else "#2b0d0d")
                fg = C["verde"] if i==j else (C["texto"] if d!=INF else "#555")
                tk.Label(self.mat_frame, text=txt, font=("Courier New",7),
                         fg=fg, bg=bg, width=9, relief="flat", pady=2).grid(
                    row=i+1, column=j+1, padx=1, pady=1)

    def _mostrar_iteraciones(self):
        self.out_it.delete("1.0","end")
        for k_name, mat in self.iteraciones:
            self.out_it.insert("end", f"  k={k_name}: ", "")
            mins = []
            for i in range(len(ESTADOS)):
                for j in range(len(ESTADOS)):
                    if i!=j and mat[i][j]!=INF:
                        pass
            self.out_it.insert("end", f"Actualización con vértice intermedio '{k_name}' completada\n")

    def _consultar(self):
        u = self.orig_var.get()
        v = self.dest_var.get()
        self.out.delete("1.0","end")
        self.out.insert("end", f"Camino: {u} → {v}\n","t")
        self.out.insert("end","─"*30+"\n","s")
        d = self.dist[self.idx[u]][self.idx[v]]
        ruta = reconstruir(self.nxt, self.idx, u, v)
        if ruta:
            self.out.insert("end", "  " + " → ".join(ruta) + "\n","ok")
            self.out.insert("end", f"  Distancia mínima: {d} km\n","hl")
            self.out.insert("end", f"  Saltos: {len(ruta)-1}\n","s")
        else:
            self.out.insert("end", "  Sin camino posible\n","s")

    def _todos_caminos(self):
        self.out.delete("1.0","end")
        self.out.insert("end","Todos los caminos mínimos:\n","t")
        self.out.insert("end","─"*30+"\n","s")
        for u in ESTADOS:
            for v in ESTADOS:
                if u >= v: continue
                d = self.dist[self.idx[u]][self.idx[v]]
                ruta = reconstruir(self.nxt, self.idx, u, v)
                if ruta:
                    self.out.insert("end", f"  {u[:4]}→{v[:4]}: {d}km  [{' → '.join(r[:4] for r in ruta)}]\n","ok")

if __name__ == "__main__":
    App().mainloop()