"""
Algoritmo de Kruskal
Encuentra el Árbol de Expansión Mínima (MST) de un grafo ponderado.
Aplicado al grafo de 7 estados de la República Mexicana.
"""
import tkinter as tk
from tkinter import scrolledtext

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

# ─── UNION-FIND ───────────────────────────────────────────────────────────────
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0]*n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
        return True

# ─── KRUSKAL ─────────────────────────────────────────────────────────────────
def kruskal(estados, aristas):
    n = len(estados)
    idx = {e: i for i, e in enumerate(estados)}
    uf  = UnionFind(n)

    ordenadas = sorted(aristas, key=lambda x: x[2])
    mst = []
    rechazadas = []
    pasos = []

    for u, v, p in ordenadas:
        i, j = idx[u], idx[v]
        if uf.union(i, j):
            mst.append((u, v, p))
            pasos.append(("AGREGAR", u, v, p, [a[:] for a in mst]))
        else:
            rechazadas.append((u, v, p))
            pasos.append(("RECHAZAR", u, v, p, [a[:] for a in mst]))
        if len(mst) == n-1:
            break

    costo_total = sum(p for _,_,p in mst)
    return mst, rechazadas, pasos, costo_total

# ─── GUI ─────────────────────────────────────────────────────────────────────
C = {
    "bg": "#0d1117", "panel": "#161b22", "card": "#1c2333",
    "border": "#30363d", "naranja": "#f0883e", "verde": "#3fb950",
    "rojo": "#f78166", "oro": "#e3b341", "texto": "#e6edf3",
    "sub": "#8b949e", "nodo": "#9e6a03", "mst": "#f0883e",
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algoritmo de Kruskal — Árbol de Expansión Mínima")
        self.configure(bg=C["bg"])
        self.geometry("1100x700")

        self.mst, self.rechazadas, self.pasos, self.costo = kruskal(ESTADOS, ARISTAS)
        self.paso_actual = -1   # -1 = mostrar todo el MST
        self.mostrar_todo = True
        self._build()
        self._dibujar_mst()
        self._mostrar_resultado()

    def _build(self):
        tk.Label(self, text="ALGORITMO DE KRUSKAL",
                 font=("Courier New",18,"bold"), fg=C["naranja"], bg=C["bg"]).pack(anchor="w", padx=20, pady=(14,0))
        tk.Label(self, text="Árbol de Expansión Mínima (MST) — Estados de México",
                 font=("Courier New",9), fg=C["sub"], bg=C["bg"]).pack(anchor="w", padx=20)
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x", padx=20, pady=8)

        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=20, pady=(0,16))

        # Canvas
        cf = tk.Frame(body, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        cf.pack(side="left", fill="both", expand=True)
        tk.Label(cf, text="GRAFO Y MST (naranja = árbol mínimo, gris = rechazada)",
                 font=("Courier New",8), fg=C["sub"], bg=C["panel"]).pack(anchor="nw", padx=10, pady=(6,0))
        self.canvas = tk.Canvas(cf, bg=C["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas.bind("<Configure>", lambda e: self._dibujar_mst())

        # Panel derecho
        right = tk.Frame(body, bg=C["bg"], width=370)
        right.pack(side="right", fill="y", padx=(12,0))
        right.pack_propagate(False)

        # Aristas ordenadas
        af = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        af.pack(fill="x", pady=(0,8))
        tk.Label(af, text="ARISTAS ORDENADAS POR PESO",
                 font=("Courier New",9,"bold"), fg=C["naranja"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))

        ordenadas = sorted(ARISTAS, key=lambda x: x[2])
        mst_set = {(u,v) for u,v,_ in self.mst} | {(v,u) for u,v,_ in self.mst}

        for u, v, p in ordenadas:
            en_mst = (u,v) in mst_set
            row = tk.Frame(af, bg=C["card"] if en_mst else C["panel"])
            row.pack(fill="x", padx=8, pady=1)
            marca = "✓" if en_mst else "✗"
            color = C["verde"] if en_mst else C["rojo"]
            tk.Label(row, text=marca, font=("Courier New",9,"bold"),
                     fg=color, bg=row["bg"], width=2).pack(side="left", padx=(6,2), pady=2)
            tk.Label(row, text=f"{u} ↔ {v}",
                     font=("Courier New",8), fg=C["texto"], bg=row["bg"], width=22, anchor="w").pack(side="left")
            tk.Label(row, text=f"{p} km",
                     font=("Courier New",8,"bold"), fg=C["oro"], bg=row["bg"]).pack(side="right", padx=6)

        # Controles paso a paso
        pf = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        pf.pack(fill="x", pady=(0,8))
        tk.Label(pf, text="PASO A PASO", font=("Courier New",9,"bold"),
                 fg=C["naranja"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        nav = tk.Frame(pf, bg=C["panel"])
        nav.pack(fill="x", padx=10, pady=4)
        tk.Button(nav, text="◀", font=("Courier New",9), fg=C["texto"],
                  bg=C["card"], relief="flat", cursor="hand2", width=3,
                  command=self._anterior).pack(side="left", padx=(0,4))
        tk.Button(nav, text="▶", font=("Courier New",9), fg=C["texto"],
                  bg=C["card"], relief="flat", cursor="hand2", width=3,
                  command=self._siguiente).pack(side="left", padx=(0,4))
        tk.Button(nav, text="MST Final", font=("Courier New",8,"bold"), fg=C["bg"],
                  bg=C["naranja"], relief="flat", cursor="hand2",
                  command=self._ver_final).pack(side="right")
        self.lbl_paso = tk.Label(pf, text="", font=("Courier New",8), fg=C["oro"], bg=C["panel"])
        self.lbl_paso.pack(anchor="w", padx=10, pady=(0,6))

        # Output
        of = tk.Frame(right, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
        of.pack(fill="both", expand=True)
        tk.Label(of, text="RESULTADO MST", font=("Courier New",9,"bold"),
                 fg=C["naranja"], bg=C["panel"]).pack(anchor="w", padx=10, pady=(8,4))
        self.out = scrolledtext.ScrolledText(of, font=("Courier New",9),
            bg=C["bg"], fg=C["texto"], relief="flat", wrap="word")
        self.out.pack(fill="both", expand=True, padx=8, pady=(0,8))
        self.out.tag_config("t",  foreground=C["naranja"], font=("Courier New",9,"bold"))
        self.out.tag_config("ok", foreground=C["verde"])
        self.out.tag_config("no", foreground=C["rojo"])
        self.out.tag_config("hl", foreground=C["oro"])
        self.out.tag_config("s",  foreground=C["sub"])

    def _mostrar_resultado(self):
        self.out.delete("1.0","end")
        self.out.insert("end","Árbol de Expansión Mínima:\n","t")
        self.out.insert("end","─"*32+"\n","s")
        for u,v,p in self.mst:
            self.out.insert("end", f"  ✓ {u} ↔ {v}: {p} km\n","ok")
        self.out.insert("end","─"*32+"\n","s")
        self.out.insert("end",f"\n  Aristas en MST: {len(self.mst)}/{len(ARISTAS)}\n","s")
        self.out.insert("end",f"  COSTO TOTAL MST: {self.costo} km\n","hl")
        self.out.insert("end",f"\n  Rechazadas ({len(self.rechazadas)}):\n","s")
        for u,v,p in self.rechazadas:
            self.out.insert("end", f"  ✗ {u} ↔ {v}: {p} km\n","no")

    def _dibujar_mst(self, paso=-1):
        c = self.canvas
        c.delete("all")
        W = c.winfo_width() or 600
        H = c.winfo_height() or 500
        xs = [p[0] for p in POSICIONES.values()]
        ys = [p[1] for p in POSICIONES.values()]
        sc = min(W/(max(xs)+80), H/(max(ys)+80))

        def pos(e):
            x,y = POSICIONES[e]
            return x*sc+20, y*sc+20

        # Determinar aristas activas en este paso
        if self.mostrar_todo:
            mst_activo = {(u,v) for u,v,_ in self.mst} | {(v,u) for u,v,_ in self.mst}
        else:
            if paso >= 0 and paso < len(self.pasos):
                action, pu, pv, pp, mst_parcial = self.pasos[paso]
                mst_activo = {(u,v) for u,v,_ in mst_parcial} | {(v,u) for u,v,_ in mst_parcial}
            else:
                mst_activo = set()

        # Dibujar aristas
        for u, v, p in ARISTAS:
            x1,y1 = pos(u); x2,y2 = pos(v)
            en_mst = (u,v) in mst_activo
            c.create_line(x1,y1,x2,y2,
                          fill=C["mst"] if en_mst else C["border"],
                          width=3.5 if en_mst else 1,
                          dash=() if en_mst else (4,3))
            mx,my = (x1+x2)/2,(y1+y2)/2
            c.create_text(mx,my-8,text=str(p),font=("Courier New",8),
                          fill=C["oro"] if en_mst else C["sub"])

        # Nodos
        r = max(20, int(20*sc))
        nodos_activos = set()
        for u,v in mst_activo:
            nodos_activos.add(u); nodos_activos.add(v)
        for e in ESTADOS:
            x,y = pos(e)
            activo = e in nodos_activos
            c.create_oval(x-r+2,y-r+2,x+r+2,y+r+2,fill="#000",outline="")
            c.create_oval(x-r,y-r,x+r,y+r,
                          fill=C["nodo"] if activo else C["card"],
                          outline=C["naranja"] if activo else C["border"],
                          width=2.5 if activo else 1)
            c.create_text(x,y,text=e,font=("Courier New",max(7,int(8*sc)),"bold"),
                          fill=C["texto"],width=r*2-2)

    def _anterior(self):
        self.mostrar_todo = False
        if self.paso_actual > 0:
            self.paso_actual -= 1
        self._actualizar_paso()

    def _siguiente(self):
        self.mostrar_todo = False
        if self.paso_actual < len(self.pasos)-1:
            self.paso_actual += 1
        self._actualizar_paso()

    def _ver_final(self):
        self.mostrar_todo = True
        self.paso_actual = len(self.pasos)-1
        self.lbl_paso.config(text="MST completo")
        self._dibujar_mst()

    def _actualizar_paso(self):
        if 0 <= self.paso_actual < len(self.pasos):
            action, u, v, p, _ = self.pasos[self.paso_actual]
            emoji = "✓ AGREGA" if action=="AGREGAR" else "✗ RECHAZA"
            color = C["verde"] if action=="AGREGAR" else C["rojo"]
            self.lbl_paso.config(text=f"Paso {self.paso_actual+1}: {emoji} {u}↔{v} ({p}km)", fg=color)
        self._dibujar_mst(self.paso_actual)

if __name__ == "__main__":
    App().mainloop()