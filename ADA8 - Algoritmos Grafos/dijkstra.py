"""
Algoritmo de Dijkstra
Encuentra el camino más corto desde un vértice origen a todos los demás.
Aplicado al grafo de 7 estados de la República Mexicana.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import heapq
from collections import defaultdict

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
POSICIONES = {
    "CDMX":     (200, 200), "Tlaxcala": (340, 140),
    "Puebla":   (360, 220), "Morelos":  (200, 310),
    "Guerrero": (130, 390), "Veracruz": (490, 270),
    "Oaxaca":   (420, 380),
}

# ─── GRAFO ───────────────────────────────────────────────────────────────────
class Grafo:
    def __init__(self):
        self.ady = defaultdict(dict)
        self.vertices = []

    def agregar_vertice(self, v):
        if v not in self.vertices:
            self.vertices.append(v)

    def agregar_arista(self, u, v, p):
        self.ady[u][v] = p
        self.ady[v][u] = p

# ─── DIJKSTRA ────────────────────────────────────────────────────────────────
def dijkstra(grafo, origen):
    dist = {v: float('inf') for v in grafo.vertices}
    prev = {v: None for v in grafo.vertices}
    dist[origen] = 0
    pq = [(0, origen)]
    pasos = []

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        pasos.append((u, dict(dist)))
        for v, peso in grafo.ady[u].items():
            nueva = dist[u] + peso
            if nueva < dist[v]:
                dist[v] = nueva
                prev[v] = u
                heapq.heappush(pq, (nueva, v))

    return dist, prev, pasos

def reconstruir_camino(prev, origen, destino):
    path = []
    cur = destino
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path[0] == origen else []

# ─── GUI ─────────────────────────────────────────────────────────────────────
C = {
    "bg": "#0d1117", "panel": "#161b22", "card": "#1c2333",
    "border": "#30363d", "azul": "#58a6ff", "verde": "#3fb950",
    "rojo": "#f78166", "oro": "#e3b341", "texto": "#e6edf3",
    "sub": "#8b949e", "nodo": "#1f6feb", "nodo_ok": "#238636",
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algoritmo de Dijkstra — Camino más corto")
        self.configure(bg=C["bg"])
        self.geometry("1100x700")

        self.grafo = Grafo()
        for e in ESTADOS: self.grafo.agregar_vertice(e)
        for u, v, p in ARISTAS: self.grafo.agregar_arista(u, v, p)

        self.origen_var = tk.StringVar(value=ESTADOS[0])
        self.dest_var   = tk.StringVar(value=ESTADOS[3])
        self.ruta_hl    = []
        self._build()
        self._dibujar()

    def _build(self):
        # Encabezado
        tk.Label(self, text="ALGORITMO DE DIJKSTRA",
                 font=("Courier New", 18, "bold"), fg=C["azul"],
                 bg=C["bg"]).pack(anchor="w", padx=20, pady=(14,0))
        tk.Label(self, text="Camino más corto en un grafo ponderado — Estados de México",
                 font=("Courier New", 9), fg=C["sub"], bg=C["bg"]).pack(anchor="w", padx=20)
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x", padx=20, pady=8)

        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=20, pady=(0,16))

        # Canvas
        cf = tk.Frame(body, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        cf.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(cf, bg=C["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas.bind("<Configure>", lambda e: self._dibujar())

        # Panel derecho
        right = tk.Frame(body, bg=C["bg"], width=360)
        right.pack(side="right", fill="y", padx=(12,0))
        right.pack_propagate(False)

        # Controles
        ctrl = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        ctrl.pack(fill="x", pady=(0,10))
        tk.Label(ctrl, text="PARÁMETROS", font=("Courier New",10,"bold"),
                 fg=C["azul"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))

        for lbl, var in [("Origen:", self.origen_var), ("Destino:", self.dest_var)]:
            row = tk.Frame(ctrl, bg=C["panel"])
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=lbl, font=("Courier New",9), fg=C["texto"],
                     bg=C["panel"], width=9, anchor="w").pack(side="left")
            ttk.Combobox(row, textvariable=var, values=ESTADOS,
                         state="readonly", width=14).pack(side="left")

        tk.Button(ctrl, text="▶  Ejecutar Dijkstra",
                  font=("Courier New",9,"bold"), fg=C["bg"], bg=C["verde"],
                  relief="flat", cursor="hand2", pady=6,
                  command=self._ejecutar).pack(fill="x", padx=10, pady=8)

        # Tabla de distancias
        tf = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        tf.pack(fill="x", pady=(0,8))
        tk.Label(tf, text="TABLA DE DISTANCIAS MÍNIMAS",
                 font=("Courier New",9,"bold"), fg=C["oro"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        self.tabla_frame = tk.Frame(tf, bg=C["panel"])
        self.tabla_frame.pack(fill="x", padx=10, pady=(0,8))

        # Output
        of = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        of.pack(fill="both", expand=True)
        tk.Label(of, text="TRAZA DEL ALGORITMO",
                 font=("Courier New",9,"bold"), fg=C["azul"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        self.out = scrolledtext.ScrolledText(of, font=("Courier New",9),
            bg=C["bg"], fg=C["texto"], relief="flat", wrap="word", height=12)
        self.out.pack(fill="both", expand=True, padx=8, pady=(0,8))
        self.out.tag_config("t", foreground=C["azul"], font=("Courier New",9,"bold"))
        self.out.tag_config("ok", foreground=C["verde"])
        self.out.tag_config("hl", foreground=C["oro"])
        self.out.tag_config("sub", foreground=C["sub"])

    def _ejecutar(self):
        origen  = self.origen_var.get()
        destino = self.dest_var.get()
        dist, prev, pasos = dijkstra(self.grafo, origen)
        ruta = reconstruir_camino(prev, origen, destino)
        self.ruta_hl = ruta

        # Tabla
        for w in self.tabla_frame.winfo_children(): w.destroy()
        hdrs = [("Estado", C["texto"]), ("Dist.", C["texto"]), ("Prev", C["texto"])]
        for c, (h, col) in enumerate(hdrs):
            tk.Label(self.tabla_frame, text=h, font=("Courier New",8,"bold"),
                     fg=col, bg=C["card"], width=10 if c==0 else 6,
                     relief="flat", pady=2).grid(row=0, column=c, sticky="ew", padx=1, pady=1)
        for r, v in enumerate(self.grafo.vertices, 1):
            d = dist[v]
            p = prev[v] or "—"
            en_ruta = v in ruta
            bg = C["nodo"] if en_ruta else C["card"]
            for c2, txt in enumerate([v, str(d) if d != float('inf') else "∞", p]):
                tk.Label(self.tabla_frame, text=txt, font=("Courier New",8),
                         fg=C["oro"] if en_ruta else C["texto"],
                         bg=bg, width=10 if c2==0 else 6,
                         relief="flat", pady=2).grid(row=r, column=c2, sticky="ew", padx=1, pady=1)

        # Traza
        self.out.delete("1.0","end")
        self.out.insert("end", f"Dijkstra desde: {origen}\n","t")
        self.out.insert("end", "─"*38+"\n","sub")
        for i,(u,ds) in enumerate(pasos):
            self.out.insert("end", f"  Paso {i+1}: procesando {u}\n","sub")
        self.out.insert("end", "─"*38+"\n","sub")
        self.out.insert("end", f"Camino {origen} → {destino}:\n","t")
        if ruta:
            self.out.insert("end", "  " + " → ".join(ruta) + "\n","ok")
            costo = dist[destino]
            self.out.insert("end", f"  Costo total: {costo} km\n","hl")
        else:
            self.out.insert("end", "  Sin camino disponible\n","sub")

        self._dibujar()

    def _dibujar(self):
        c = self.canvas
        c.delete("all")
        W = c.winfo_width() or 620
        H = c.winfo_height() or 500
        xs = [p[0] for p in POSICIONES.values()]
        ys = [p[1] for p in POSICIONES.values()]
        sc = min(W/(max(xs)+80), H/(max(ys)+80))

        def pos(e):
            x,y = POSICIONES[e]
            return x*sc+20, y*sc+20

        ruta_pares = set()
        for i in range(len(self.ruta_hl)-1):
            u,v = self.ruta_hl[i], self.ruta_hl[i+1]
            ruta_pares.add((u,v)); ruta_pares.add((v,u))

        vistas = set()
        for u in self.grafo.vertices:
            for v,p in self.grafo.ady[u].items():
                key = tuple(sorted([u,v]))
                if key in vistas: continue
                vistas.add(key)
                x1,y1 = pos(u); x2,y2 = pos(v)
                hl = (u,v) in ruta_pares
                c.create_line(x1,y1,x2,y2, fill=C["azul"] if hl else C["border"],
                              width=3 if hl else 1.5, dash=() if hl else (4,3))
                mx,my = (x1+x2)/2,(y1+y2)/2
                c.create_text(mx,my-8,text=str(p),font=("Courier New",8),
                              fill=C["oro"] if hl else C["sub"])

        r = max(20, int(20*sc))
        for e in self.grafo.vertices:
            x,y = pos(e)
            en = e in self.ruta_hl
            c.create_oval(x-r+2,y-r+2,x+r+2,y+r+2,fill="#000",outline="")
            c.create_oval(x-r,y-r,x+r,y+r,
                          fill=C["nodo"] if en else "#1c2333",
                          outline=C["azul"] if en else C["verde"], width=2 if en else 1.5)
            c.create_text(x,y,text=e,font=("Courier New",max(7,int(8*sc)),"bold"),
                          fill=C["texto"],width=r*2-2)

if __name__ == "__main__":
    App().mainloop()