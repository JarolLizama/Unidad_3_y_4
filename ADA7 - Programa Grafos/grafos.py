import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import heapq
from collections import defaultdict

# ─────────────────────────────────────────────
#  DATOS DEL GRAFO
# ─────────────────────────────────────────────
ESTADOS = [
    "Ciudad de México",
    "Puebla",
    "Veracruz",
    "Oaxaca",
    "Guerrero",
    "Morelos",
    "Tlaxcala"
]

# Aristas (estado1, estado2, costo en km aprox)
ARISTAS = [
    ("Ciudad de México", "Puebla",         130),
    ("Ciudad de México", "Morelos",         90),
    ("Ciudad de México", "Tlaxcala",       120),
    ("Ciudad de México", "Guerrero",       260),
    ("Puebla",           "Tlaxcala",        30),
    ("Puebla",           "Veracruz",       220),
    ("Puebla",           "Oaxaca",         350),
    ("Veracruz",         "Oaxaca",         310),
    ("Oaxaca",           "Guerrero",       380),
    ("Morelos",          "Guerrero",       195),
    ("Morelos",          "Puebla",         160),
    ("Tlaxcala",         "Veracruz",       200),
]

# ─────────────────────────────────────────────
#  CLASE GRAFO
# ─────────────────────────────────────────────
class Grafo:
    def __init__(self):
        self.vertices = []
        self.adyacencia = defaultdict(dict)  # {u: {v: peso}}

    def agregar_vertice(self, v):
        if v not in self.vertices:
            self.vertices.append(v)

    def agregar_arista(self, u, v, peso):
        self.adyacencia[u][v] = peso
        self.adyacencia[v][u] = peso

    def vecinos(self, u):
        return self.adyacencia[u]

    def mostrar_relaciones(self):
        lines = []
        vistas = set()
        for u in self.vertices:
            for v, p in self.adyacencia[u].items():
                key = tuple(sorted([u, v]))
                if key not in vistas:
                    lines.append(f"  {u}  ↔  {v}   [{p} km]")
                    vistas.add(key)
        return "\n".join(lines)

    # ── Camino Hamiltoniano (visita todos sin repetir) ──────────────────
    def camino_hamiltoniano(self, inicio):
        """Backtracking para encontrar un camino hamiltoniano desde 'inicio'."""
        n = len(self.vertices)
        mejor = {"costo": float("inf"), "ruta": []}

        def bt(actual, visitados, ruta, costo):
            if len(visitados) == n:
                if costo < mejor["costo"]:
                    mejor["costo"] = costo
                    mejor["ruta"] = ruta[:]
                return
            for vecino, peso in self.adyacencia[actual].items():
                if vecino not in visitados:
                    visitados.add(vecino)
                    ruta.append(vecino)
                    bt(vecino, visitados, ruta, costo + peso)
                    ruta.pop()
                    visitados.remove(vecino)

        bt(inicio, {inicio}, [inicio], 0)
        return mejor["ruta"], mejor["costo"]

    # ── Recorrido repitiendo al menos un estado (TSP aprox) ─────────────
    def recorrido_con_repeticion(self, inicio):
        """
        Dijkstra entre cada par para garantizar conectividad.
        Greedy: visita todos los estados usando caminos más cortos,
        lo que puede repetir intermedios.
        """
        # Precalcular Dijkstra desde cada nodo
        def dijkstra(src):
            dist = {v: float("inf") for v in self.vertices}
            prev = {v: None for v in self.vertices}
            dist[src] = 0
            pq = [(0, src)]
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[u]:
                    continue
                for v, w in self.adyacencia[u].items():
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        prev[v] = u
                        heapq.heappush(pq, (dist[v], v))
            return dist, prev

        def reconstruir(prev, src, dst):
            path = []
            cur = dst
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            path.reverse()
            return path

        dists = {}
        prevs = {}
        for v in self.vertices:
            dists[v], prevs[v] = dijkstra(v)

        # Greedy: desde inicio, ir al no-visitado más cercano
        visitados_set = {inicio}
        ruta_completa = [inicio]
        costo_total = 0
        actual = inicio

        while len(visitados_set) < len(self.vertices):
            mejor_costo = float("inf")
            mejor_dest = None
            for v in self.vertices:
                if v not in visitados_set:
                    if dists[actual][v] < mejor_costo:
                        mejor_costo = dists[actual][v]
                        mejor_dest = v
            # Agregar camino completo (con posibles intermedios)
            camino = reconstruir(prevs[actual], actual, mejor_dest)
            ruta_completa.extend(camino[1:])
            costo_total += mejor_costo
            visitados_set.add(mejor_dest)
            actual = mejor_dest

        return ruta_completa, costo_total


# ─────────────────────────────────────────────
#  CONSTRUIR GRAFO GLOBAL
# ─────────────────────────────────────────────
def construir_grafo():
    g = Grafo()
    for e in ESTADOS:
        g.agregar_vertice(e)
    for u, v, p in ARISTAS:
        g.agregar_arista(u, v, p)
    return g


# ─────────────────────────────────────────────
#  INTERFAZ GRÁFICA
# ─────────────────────────────────────────────
COLORES = {
    "bg":        "#0d1117",
    "panel":     "#161b22",
    "card":      "#1c2333",
    "border":    "#30363d",
    "accent":    "#58a6ff",
    "accent2":   "#3fb950",
    "accent3":   "#f78166",
    "gold":      "#e3b341",
    "texto":     "#e6edf3",
    "subtexto":  "#8b949e",
    "nodo":      "#238636",
    "nodo_sel":  "#1f6feb",
    "arista":    "#444c56",
    "arista_hl": "#58a6ff",
}

FUENTE_TITULO = ("Courier New", 20, "bold")
FUENTE_SUBTITULO = ("Courier New", 12, "bold")
FUENTE_MONO = ("Courier New", 10)
FUENTE_SMALL = ("Courier New", 9)

# Posiciones en canvas para cada estado
POSICIONES = {
    "Ciudad de México": (280, 220),
    "Tlaxcala":         (410, 160),
    "Puebla":           (430, 240),
    "Morelos":          (280, 330),
    "Guerrero":         (180, 410),
    "Veracruz":         (560, 290),
    "Oaxaca":           (480, 400),
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grafos — Estados de México  |  TDA Grafo")
        self.configure(bg=COLORES["bg"])
        self.resizable(True, True)
        self.geometry("1200x780")

        self.grafo = construir_grafo()
        self.ruta_resaltada = []   # lista de vértices a resaltar
        self.aristas_hl = []       # lista de (u,v) resaltadas

        self._build_ui()
        self.dibujar_grafo()

    # ── Layout principal ────────────────────────────────────────────────
    def _build_ui(self):
        # Encabezado
        hdr = tk.Frame(self, bg=COLORES["bg"])
        hdr.pack(fill="x", padx=20, pady=(16, 0))

        tk.Label(hdr, text="◈ GRAFOS — ESTADOS DE MÉXICO",
                 font=FUENTE_TITULO, fg=COLORES["accent"], bg=COLORES["bg"]).pack(side="left")
        tk.Label(hdr, text="TDA Grafo  ·  Estructuras de Datos",
                 font=FUENTE_SMALL, fg=COLORES["subtexto"], bg=COLORES["bg"]).pack(side="right", pady=8)

        sep = tk.Frame(self, bg=COLORES["border"], height=1)
        sep.pack(fill="x", padx=20, pady=8)

        # Cuerpo principal: canvas + panel derecho
        body = tk.Frame(self, bg=COLORES["bg"])
        body.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Canvas
        canvas_frame = tk.Frame(body, bg=COLORES["panel"],
                                 highlightbackground=COLORES["border"], highlightthickness=1)
        canvas_frame.pack(side="left", fill="both", expand=True)

        tk.Label(canvas_frame, text="GRAFO VISUAL", font=FUENTE_SMALL,
                 fg=COLORES["subtexto"], bg=COLORES["panel"]).pack(anchor="nw", padx=10, pady=(6,0))

        self.canvas = tk.Canvas(canvas_frame, bg=COLORES["bg"],
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)
        self.canvas.bind("<Configure>", lambda e: self.dibujar_grafo())

        # Panel derecho
        right = tk.Frame(body, bg=COLORES["bg"], width=380)
        right.pack(side="right", fill="y", padx=(12, 0))
        right.pack_propagate(False)

        # ── Botones de acciones
        btn_frame = tk.Frame(right, bg=COLORES["panel"],
                             highlightbackground=COLORES["border"], highlightthickness=1)
        btn_frame.pack(fill="x", pady=(0, 10))

        tk.Label(btn_frame, text="ACCIONES", font=FUENTE_SUBTITULO,
                 fg=COLORES["accent"], bg=COLORES["panel"]).pack(anchor="nw", padx=10, pady=(8,4))

        btns = [
            ("① Mostrar estados y relaciones",  COLORES["accent"],  self.mostrar_relaciones),
            ("② Recorrido sin repetir (Hamilt.)", COLORES["accent2"], self.recorrido_sin_repetir),
            ("③ Recorrido con repetición",       COLORES["gold"],    self.recorrido_con_repeticion),
            ("④ Comparar costos (a vs b)",       COLORES["accent3"], self.comparar_costos),
            ("⟳ Limpiar resaltado",              COLORES["subtexto"], self.limpiar),
        ]
        for txt, color, cmd in btns:
            b = tk.Button(btn_frame, text=txt, font=FUENTE_SMALL,
                          fg=color, bg=COLORES["card"],
                          activebackground=COLORES["border"],
                          activeforeground=color,
                          relief="flat", cursor="hand2",
                          command=cmd, pady=6, anchor="w", padx=10)
            b.pack(fill="x", padx=8, pady=3)

        tk.Frame(btn_frame, bg=COLORES["panel"], height=8).pack()

        # ── Salida de texto
        out_frame = tk.Frame(right, bg=COLORES["panel"],
                             highlightbackground=COLORES["border"], highlightthickness=1)
        out_frame.pack(fill="both", expand=True)

        hdr2 = tk.Frame(out_frame, bg=COLORES["panel"])
        hdr2.pack(fill="x")
        tk.Label(hdr2, text="RESULTADO", font=FUENTE_SUBTITULO,
                 fg=COLORES["accent"], bg=COLORES["panel"]).pack(side="left", padx=10, pady=(8,4))
        tk.Button(hdr2, text="limpiar", font=FUENTE_SMALL,
                  fg=COLORES["subtexto"], bg=COLORES["panel"],
                  relief="flat", cursor="hand2",
                  command=lambda: self.output.delete("1.0", "end")).pack(side="right", padx=8)

        self.output = scrolledtext.ScrolledText(
            out_frame, font=FUENTE_MONO,
            bg=COLORES["bg"], fg=COLORES["texto"],
            insertbackground=COLORES["accent"],
            relief="flat", wrap="word",
            selectbackground=COLORES["border"])
        self.output.pack(fill="both", expand=True, padx=8, pady=8)

        # Tags de color para el output
        self.output.tag_config("titulo",   foreground=COLORES["accent"],  font=("Courier New", 11, "bold"))
        self.output.tag_config("ok",       foreground=COLORES["accent2"])
        self.output.tag_config("warn",     foreground=COLORES["gold"])
        self.output.tag_config("err",      foreground=COLORES["accent3"])
        self.output.tag_config("sub",      foreground=COLORES["subtexto"])
        self.output.tag_config("bold",     font=("Courier New", 10, "bold"), foreground=COLORES["texto"])

    # ── Dibujar grafo ───────────────────────────────────────────────────
    def dibujar_grafo(self, event=None):
        c = self.canvas
        c.delete("all")
        W = c.winfo_width()  or 720
        H = c.winfo_height() or 520

        # Calcular escala dinámica
        xs = [p[0] for p in POSICIONES.values()]
        ys = [p[1] for p in POSICIONES.values()]
        sx = W / (max(xs) + 80)
        sy = H / (max(ys) + 80)
        scale = min(sx, sy)

        def pos(estado):
            ox, oy = POSICIONES[estado]
            return ox * scale + 20, oy * scale + 20

        # Aristas resaltadas como set
        hl_set = set()
        for i in range(len(self.aristas_hl)):
            u, v = self.aristas_hl[i]
            hl_set.add((u, v))
            hl_set.add((v, u))

        # Dibujar aristas
        vistas = set()
        for u in self.grafo.vertices:
            for v, peso in self.grafo.adyacencia[u].items():
                key = tuple(sorted([u, v]))
                if key in vistas:
                    continue
                vistas.add(key)
                x1, y1 = pos(u)
                x2, y2 = pos(v)
                resaltada = (u, v) in hl_set

                color  = COLORES["arista_hl"] if resaltada else COLORES["arista"]
                ancho  = 3 if resaltada else 1.5
                dash   = () if resaltada else (4, 3)

                c.create_line(x1, y1, x2, y2, fill=color, width=ancho,
                              dash=dash, smooth=True)

                # Etiqueta del peso
                mx, my = (x1+x2)/2, (y1+y2)/2
                c.create_text(mx, my - 8, text=f"{peso}", font=("Courier New", 8),
                              fill=COLORES["subtexto"] if not resaltada else COLORES["gold"])

        # Dibujar nodos
        r = max(22, int(22 * scale))
        for estado in self.grafo.vertices:
            x, y = pos(estado)
            en_ruta = estado in self.ruta_resaltada

            color_nodo  = COLORES["nodo_sel"] if en_ruta else COLORES["nodo"]
            color_borde = COLORES["accent"]   if en_ruta else COLORES["accent2"]
            ancho_borde = 3 if en_ruta else 1.5

            # Sombra
            c.create_oval(x-r+3, y-r+3, x+r+3, y+r+3, fill="#000", outline="")
            # Nodo
            c.create_oval(x-r, y-r, x+r, y+r,
                          fill=color_nodo, outline=color_borde, width=ancho_borde)

            # Índice en ruta
            if en_ruta:
                idx = self.ruta_resaltada.index(estado) + 1
                c.create_text(x + r - 6, y - r + 6,
                              text=str(idx), font=("Courier New", 7, "bold"),
                              fill=COLORES["gold"])

            # Nombre (abreviado)
            nombre = estado.replace("Ciudad de México", "CDMX")
            c.create_text(x, y, text=nombre,
                          font=("Courier New", max(7, int(8*scale)), "bold"),
                          fill=COLORES["texto"], width=r*2-4)

    # ── Helpers output ──────────────────────────────────────────────────
    def escribir(self, texto, tag=None):
        self.output.insert("end", texto + "\n", tag or "")
        self.output.see("end")

    def limpiar(self):
        self.ruta_resaltada = []
        self.aristas_hl = []
        self.dibujar_grafo()

    def _separador(self):
        self.escribir("─" * 42, "sub")

    # ── Acción 1: estados y relaciones ─────────────────────────────────
    def mostrar_relaciones(self):
        self.output.delete("1.0", "end")
        self.limpiar()
        self.escribir("◈ ESTADOS DEL GRAFO", "titulo")
        self._separador()
        for i, e in enumerate(self.grafo.vertices, 1):
            vecinos = ", ".join(self.grafo.adyacencia[e].keys())
            self.escribir(f"  {i}. {e}", "bold")
            self.escribir(f"     → conecta con: {vecinos}", "sub")
        self._separador()
        self.escribir("◈ RELACIONES (ARISTAS)", "titulo")
        self._separador()
        self.escribir(self.grafo.mostrar_relaciones(), "ok")
        self.escribir(f"\n  Total aristas: {len(ARISTAS)}", "sub")

    # ── Acción 2: sin repetir ──────────────────────────────────────────
    def recorrido_sin_repetir(self):
        self.output.delete("1.0", "end")
        self.escribir("◈ RECORRIDO SIN REPETIR (Hamiltoniano)", "titulo")
        self._separador()

        inicio = ESTADOS[0]
        ruta, costo = self.grafo.camino_hamiltoniano(inicio)

        if not ruta:
            self.escribir("  ✗ No se encontró camino hamiltoniano.", "err")
            return

        self.escribir(f"  Inicio: {inicio}", "sub")
        self.escribir(f"  Nodos visitados: {len(ruta)}/7\n", "sub")

        for i, e in enumerate(ruta):
            flecha = "  START →" if i == 0 else f"  [{i+1}]    →"
            self.escribir(f"{flecha} {e}", "ok")

        self._separador()
        self.escribir(f"  💰 COSTO TOTAL: {costo} km", "bold")

        # Resaltar
        self.ruta_resaltada = ruta
        self.aristas_hl = list(zip(ruta, ruta[1:]))
        self.dibujar_grafo()

    # ── Acción 3: con repetición ───────────────────────────────────────
    def recorrido_con_repeticion(self):
        self.output.delete("1.0", "end")
        self.escribir("◈ RECORRIDO CON REPETICIÓN (Greedy + Dijkstra)", "titulo")
        self._separador()

        inicio = ESTADOS[0]
        ruta, costo = self.grafo.recorrido_con_repeticion(inicio)

        self.escribir(f"  Inicio: {inicio}", "sub")
        repetidos = [e for e in ruta if ruta.count(e) > 1]
        rep_set = set(repetidos)
        self.escribir(f"  Estados repetidos: {', '.join(rep_set) if rep_set else 'ninguno'}\n", "warn")

        for i, e in enumerate(ruta):
            marca = " ★" if e in rep_set and ruta.index(e) != i else ""
            flecha = "  START →" if i == 0 else f"  [{i+1}]    →"
            tag = "warn" if e in rep_set and i > ruta.index(e) else "ok"
            self.escribir(f"{flecha} {e}{marca}", tag)

        self._separador()
        self.escribir(f"  💰 COSTO TOTAL: {costo} km", "bold")

        # Resaltar
        únicos = list(dict.fromkeys(ruta))
        self.ruta_resaltada = únicos
        self.aristas_hl = list(zip(ruta, ruta[1:]))
        self.dibujar_grafo()

    # ── Acción 4: comparar costos ──────────────────────────────────────
    def comparar_costos(self):
        self.output.delete("1.0", "end")
        self.escribir("◈ COMPARACIÓN DE COSTOS", "titulo")
        self._separador()

        inicio = ESTADOS[0]
        ruta_a, costo_a = self.grafo.camino_hamiltoniano(inicio)
        ruta_b, costo_b = self.grafo.recorrido_con_repeticion(inicio)

        self.escribir("  INCISO a) Sin repetición (Hamiltoniano)", "bold")
        if ruta_a:
            self.escribir(f"  Ruta: {' → '.join(r[:3] for r in ruta_a)}…", "ok")
            self.escribir(f"  Nodos: {len(ruta_a)}   Costo: {costo_a} km\n", "ok")
        else:
            self.escribir("  No encontrado\n", "err")

        self.escribir("  INCISO b) Con repetición (Greedy)", "bold")
        self.escribir(f"  Ruta: {' → '.join(r[:3] for r in ruta_b[:4])}…", "warn")
        self.escribir(f"  Nodos recorridos: {len(ruta_b)}   Costo: {costo_b} km\n", "warn")

        self._separador()
        self.escribir("  VEREDICTO", "titulo")
        if costo_a != float("inf"):
            diff = abs(costo_b - costo_a)
            if costo_a <= costo_b:
                self.escribir(f"  ✓ El inciso (a) es {diff} km más barato.", "ok")
            else:
                self.escribir(f"  ✓ El inciso (b) es {diff} km más barato.", "warn")
            self.escribir(f"\n  a) {costo_a} km  vs  b) {costo_b} km", "sub")
        else:
            self.escribir("  No se pudo calcular inciso (a).", "err")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()