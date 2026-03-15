import tkinter as tk
from tkinter import messagebox, simpledialog

# ─────────────────────────────────────────────
#  ESTRUCTURA DE DATOS
# ─────────────────────────────────────────────

class NodoIngrediente:
    def __init__(self, ingrediente):
        self.ingrediente = ingrediente
        self.siguiente = None


class ListaIngredientes:
    def __init__(self):
        self.cabeza = None

    def insertar(self, ingrediente):
        nuevo = NodoIngrediente(ingrediente)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def eliminar(self, ingrediente):
        if self.cabeza is None:
            return False
        if self.cabeza.ingrediente.lower() == ingrediente.lower():
            self.cabeza = self.cabeza.siguiente
            return True
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.ingrediente.lower() == ingrediente.lower():
                actual.siguiente = actual.siguiente.siguiente
                return True
            actual = actual.siguiente
        return False

    def obtener_lista(self):
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.ingrediente)
            actual = actual.siguiente
        return resultado


class EstructuraPostres:
    def __init__(self):
        self.postres = []

    def _buscar_indice(self, nombre):
        izq, der = 0, len(self.postres) - 1
        nombre = nombre.strip().lower()
        while izq <= der:
            mid = (izq + der) // 2
            if self.postres[mid][0].lower() == nombre:
                return mid
            elif self.postres[mid][0].lower() < nombre:
                izq = mid + 1
            else:
                der = mid - 1
        return -1

    def _posicion_insercion(self, nombre):
        nombre = nombre.lower()
        for i, (n, _) in enumerate(self.postres):
            if nombre < n.lower():
                return i
        return len(self.postres)

    def nombres(self):
        return [p[0] for p in self.postres]

    def obtener_ingredientes(self, nombre):
        idx = self._buscar_indice(nombre)
        if idx == -1:
            return None
        return self.postres[idx][1].obtener_lista()

    def insertar_ingredientes(self, nombre, nuevos):
        idx = self._buscar_indice(nombre)
        if idx == -1:
            return False, f"El postre '{nombre}' no existe."
        existentes = [e.lower() for e in self.postres[idx][1].obtener_lista()]
        agregados, duplicados = [], []
        for ing in nuevos:
            ing = ing.strip()
            if not ing:
                continue
            if ing.lower() in existentes:
                duplicados.append(ing)
            else:
                self.postres[idx][1].insertar(ing)
                existentes.append(ing.lower())
                agregados.append(ing)
        msg = ""
        if agregados:
            msg += f"Agregados: {', '.join(agregados)}. "
        if duplicados:
            msg += f"Ya existian: {', '.join(duplicados)}."
        return True, msg.strip() or "Sin cambios."

    def eliminar_ingrediente(self, nombre, ingrediente):
        idx = self._buscar_indice(nombre)
        if idx == -1:
            return False, f"El postre '{nombre}' no existe."
        ok = self.postres[idx][1].eliminar(ingrediente)
        if ok:
            return True, f"'{ingrediente}' eliminado de '{nombre}'."
        return False, f"'{ingrediente}' no existe en '{nombre}'."

    def alta_postre(self, nombre, ingredientes):
        if self._buscar_indice(nombre) != -1:
            return False, f"El postre '{nombre}' ya existe."
        lista = ListaIngredientes()
        for ing in ingredientes:
            if ing.strip():
                lista.insertar(ing.strip())
        pos = self._posicion_insercion(nombre)
        self.postres.insert(pos, (nombre, lista))
        return True, f"Postre '{nombre}' dado de alta."

    def baja_postre(self, nombre):
        idx = self._buscar_indice(nombre)
        if idx == -1:
            return False, f"El postre '{nombre}' no existe."
        self.postres.pop(idx)
        return True, f"Postre '{nombre}' eliminado con todos sus ingredientes."

    def eliminar_repetidos(self):
        vistos = {}
        indices = []
        eliminados = []
        for i, (nombre, _) in enumerate(self.postres):
            clave = nombre.lower()
            if clave in vistos:
                indices.append(i)
                eliminados.append(nombre)
            else:
                vistos[clave] = i
        for i in sorted(indices, reverse=True):
            self.postres.pop(i)
        return eliminados


# ─────────────────────────────────────────────
#  COLORES Y FUENTES
# ─────────────────────────────────────────────

DARK_BG    = "#1a1a2e"
PANEL_BG   = "#16213e"
CARD_BG    = "#0f3460"
ACCENT     = "#e94560"
ACCENT2    = "#f5a623"
TEXT_WHITE = "#eaeaea"
TEXT_MUTED = "#8892a4"
SUCCESS    = "#4caf82"

FONT_TITLE = ("Georgia", 20, "bold")
FONT_HEAD  = ("Georgia", 13, "bold")
FONT_BODY  = ("Consolas", 11)
FONT_BTN   = ("Consolas", 10, "bold")
FONT_SMALL = ("Consolas", 9)


# ─────────────────────────────────────────────
#  APLICACION
# ─────────────────────────────────────────────

class PostresApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("POSTRES - Estructura de Datos")
        self.configure(bg=DARK_BG)
        self.geometry("1000x660")
        self.resizable(True, True)
        self.minsize(800, 550)

        self.db = EstructuraPostres()

        # FIX: estado persistente, no depende de curselection
        self._postre_activo = None
        self._ingrediente_activo = None

        self._cargar_datos_demo()
        self._construir_ui()
        self._actualizar_lista_postres()

    def _cargar_datos_demo(self):
        self.db.alta_postre("Arroz con leche", ["Arroz", "Leche", "Azucar", "Canela", "Limon"])
        self.db.alta_postre("Brownie",         ["Chocolate", "Mantequilla", "Harina", "Huevo", "Azucar"])
        self.db.alta_postre("Churros",         ["Harina", "Agua", "Sal", "Aceite", "Azucar"])
        self.db.alta_postre("Flan",            ["Huevo", "Leche", "Azucar", "Vainilla", "Caramelo"])
        self.db.alta_postre("Gelatina",        ["Grenetina", "Agua", "Azucar", "Colorante"])

    def _btn(self, parent, text, cmd, color, fg=None):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=color, fg=fg or TEXT_WHITE,
            font=FONT_BTN, bd=0, relief="flat",
            padx=10, pady=5, cursor="hand2",
            activebackground=DARK_BG, activeforeground=color
        )

    def _log(self, msg, tipo="info"):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"> {msg}\n", tipo)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _construir_ui(self):
        header = tk.Frame(self, bg=DARK_BG, pady=10)
        header.pack(fill="x", padx=20)
        tk.Label(header, text="POSTRES", font=FONT_TITLE,
                 bg=DARK_BG, fg=ACCENT).pack(side="left")
        tk.Label(header, text="   Arreglo ordenado + Listas Enlazadas",
                 font=("Consolas", 10), bg=DARK_BG, fg=TEXT_MUTED).pack(side="left", pady=6)

        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x", padx=20)

        main = tk.Frame(self, bg=DARK_BG)
        main.pack(fill="both", expand=True, padx=20, pady=12)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        # Panel izquierdo
        left = tk.Frame(main, bg=PANEL_BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        tk.Label(left, text="POSTRES", font=FONT_HEAD,
                 bg=PANEL_BG, fg=ACCENT2, pady=8).grid(row=0, column=0, sticky="ew", padx=10)

        lf = tk.Frame(left, bg=PANEL_BG)
        lf.grid(row=1, column=0, sticky="nsew", padx=8)
        lf.rowconfigure(0, weight=1)
        lf.columnconfigure(0, weight=1)

        sb = tk.Scrollbar(lf, bg=PANEL_BG, troughcolor=DARK_BG)
        sb.grid(row=0, column=1, sticky="ns")

        self.listbox = tk.Listbox(
            lf, bg=CARD_BG, fg=TEXT_WHITE,
            selectbackground=ACCENT, selectforeground=TEXT_WHITE,
            font=FONT_BODY, bd=0, highlightthickness=0,
            yscrollcommand=sb.set, width=22, activestyle="none"
        )
        self.listbox.grid(row=0, column=0, sticky="nsew")
        sb.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self._on_select_postre)

        bf = tk.Frame(left, bg=PANEL_BG, pady=8)
        bf.grid(row=2, column=0)
        self._btn(bf, "+ Alta postre",     self._alta_postre,    ACCENT).pack(fill="x", padx=8, pady=2)
        self._btn(bf, "x Baja postre",     self._baja_postre,    "#c0392b").pack(fill="x", padx=8, pady=2)
        self._btn(bf, "* Elim. repetidos", self._elim_repetidos, TEXT_MUTED, fg=DARK_BG).pack(fill="x", padx=8, pady=2)

        # Panel derecho
        right = tk.Frame(main, bg=PANEL_BG)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(2, weight=1)
        right.columnconfigure(0, weight=1)

        self.lbl_postre = tk.Label(
            right, text="<- Selecciona un postre",
            font=FONT_HEAD, bg=PANEL_BG, fg=ACCENT2, anchor="w", pady=8, padx=12
        )
        self.lbl_postre.grid(row=0, column=0, sticky="ew")

        af = tk.Frame(right, bg=PANEL_BG)
        af.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))
        self._btn(af, "+ Insertar ingrediente", self._insertar_ing, SUCCESS).pack(side="left", padx=(0, 6))
        self._btn(af, "x Eliminar ingrediente", self._eliminar_ing, "#c0392b").pack(side="left")

        ing_frame = tk.Frame(right, bg=CARD_BG)
        ing_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 8))
        ing_frame.rowconfigure(0, weight=1)
        ing_frame.columnconfigure(0, weight=1)

        sb2 = tk.Scrollbar(ing_frame, bg=CARD_BG, troughcolor=DARK_BG)
        sb2.grid(row=0, column=1, sticky="ns")

        self.ing_listbox = tk.Listbox(
            ing_frame, bg=CARD_BG, fg=TEXT_WHITE,
            selectbackground=ACCENT2, selectforeground=DARK_BG,
            font=FONT_BODY, bd=0, highlightthickness=0,
            yscrollcommand=sb2.set, activestyle="none"
        )
        self.ing_listbox.grid(row=0, column=0, sticky="nsew")
        sb2.config(command=self.ing_listbox.yview)

        # FIX: capturar ingrediente al hacer clic
        self.ing_listbox.bind("<<ListboxSelect>>", self._on_select_ingrediente)

        tk.Label(right, text="LOG DE OPERACIONES", font=FONT_SMALL,
                 bg=PANEL_BG, fg=TEXT_MUTED, anchor="w", padx=12).grid(row=3, column=0, sticky="ew")

        log_frame = tk.Frame(right, bg=DARK_BG)
        log_frame.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 8))
        log_frame.columnconfigure(0, weight=1)

        sb3 = tk.Scrollbar(log_frame, bg=DARK_BG, troughcolor=DARK_BG)
        sb3.pack(side="right", fill="y")

        self.log_text = tk.Text(
            log_frame, height=5, bg=DARK_BG, fg=TEXT_MUTED,
            font=FONT_SMALL, bd=0, highlightthickness=0,
            state="disabled", wrap="word", yscrollcommand=sb3.set
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        sb3.config(command=self.log_text.yview)

        self.log_text.tag_config("ok",    foreground=SUCCESS)
        self.log_text.tag_config("error", foreground=ACCENT)
        self.log_text.tag_config("warn",  foreground=ACCENT2)
        self.log_text.tag_config("info",  foreground=TEXT_MUTED)

    # ── Eventos de seleccion ──────────────────────────────────

    def _on_select_postre(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        nombre = self.db.nombres()[sel[0]]
        self._postre_activo = nombre       # FIX: guardar en variable de instancia
        self._ingrediente_activo = None
        self._mostrar_ingredientes(nombre)

    def _on_select_ingrediente(self, event=None):
        """FIX PRINCIPAL: guarda el nombre real del ingrediente en el momento
        del clic, antes de que el foco se mueva al boton."""
        sel = self.ing_listbox.curselection()
        if not sel or not self._postre_activo:
            return
        ings = self.db.obtener_ingredientes(self._postre_activo)
        if ings and sel[0] < len(ings):
            self._ingrediente_activo = ings[sel[0]]

    def _postre_seleccionado(self):
        return self._postre_activo  # FIX: no usar curselection

    def _actualizar_lista_postres(self, seleccionar=None):
        self.listbox.delete(0, "end")
        for nombre in self.db.nombres():
            self.listbox.insert("end", f"  {nombre}")
        if seleccionar:
            nombres = self.db.nombres()
            if seleccionar in nombres:
                idx = nombres.index(seleccionar)
                self.listbox.selection_set(idx)
                self.listbox.see(idx)
                self._postre_activo = seleccionar
                self._mostrar_ingredientes(seleccionar)

    def _mostrar_ingredientes(self, nombre):
        self.lbl_postre.config(text=f">> {nombre}")
        self.ing_listbox.delete(0, "end")
        self._ingrediente_activo = None
        ings = self.db.obtener_ingredientes(nombre)
        if ings is None:
            return
        if not ings:
            self.ing_listbox.insert("end", "  (sin ingredientes)")
        else:
            for i, ing in enumerate(ings, 1):
                self.ing_listbox.insert("end", f"  {i:02d}.  {ing}")

    # ── Operaciones ───────────────────────────────────────────

    def _insertar_ing(self):
        nombre = self._postre_seleccionado()
        if not nombre:
            messagebox.showwarning("Sin seleccion", "Selecciona primero un postre de la lista.")
            return
        raw = simpledialog.askstring(
            "Insertar ingredientes",
            f"Ingredientes para '{nombre}'\n(separa varios con comas):",
            parent=self
        )
        if not raw or not raw.strip():
            return
        nuevos = [x.strip() for x in raw.split(",") if x.strip()]
        ok, msg = self.db.insertar_ingredientes(nombre, nuevos)
        self._log(msg, "ok" if ok else "error")
        self._mostrar_ingredientes(nombre)

    def _eliminar_ing(self):
        nombre = self._postre_seleccionado()
        if not nombre:
            messagebox.showwarning("Sin seleccion", "Selecciona primero un postre de la lista.")
            return

        # FIX: usar _ingrediente_activo en lugar de ing_listbox.curselection()
        ingrediente = self._ingrediente_activo
        if not ingrediente:
            messagebox.showwarning(
                "Sin seleccion",
                "Haz clic en un ingrediente de la lista\nantes de presionar el boton eliminar."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"Eliminar '{ingrediente}' de '{nombre}'?"
        )
        if not confirmar:
            return

        ok, msg = self.db.eliminar_ingrediente(nombre, ingrediente)
        self._log(msg, "ok" if ok else "error")
        self._ingrediente_activo = None
        self._mostrar_ingredientes(nombre)

    def _alta_postre(self):
        nombre = simpledialog.askstring("Alta de postre", "Nombre del nuevo postre:", parent=self)
        if not nombre or not nombre.strip():
            return
        nombre = nombre.strip()
        raw = simpledialog.askstring(
            "Ingredientes",
            f"Ingredientes de '{nombre}'\n(separa con comas, puede dejarse vacio):",
            parent=self
        )
        ings = [x.strip() for x in raw.split(",")] if raw and raw.strip() else []
        ok, msg = self.db.alta_postre(nombre, ings)
        self._log(msg, "ok" if ok else "error")
        if ok:
            self._actualizar_lista_postres(seleccionar=nombre)

    def _baja_postre(self):
        nombre = self._postre_seleccionado()
        if not nombre:
            messagebox.showwarning("Sin seleccion", "Selecciona primero un postre de la lista.")
            return
        confirmar = messagebox.askyesno(
            "Confirmar baja",
            f"Eliminar '{nombre}' y todos sus ingredientes?\nEsta accion no se puede deshacer."
        )
        if not confirmar:
            return
        ok, msg = self.db.baja_postre(nombre)
        self._log(msg, "ok" if ok else "error")
        if ok:
            self._postre_activo = None
            self._ingrediente_activo = None
            self.lbl_postre.config(text="<- Selecciona un postre")
            self.ing_listbox.delete(0, "end")
            self._actualizar_lista_postres()

    def _elim_repetidos(self):
        self.db.alta_postre("Flan", ["Huevo", "Leche", "Caramelo"])
        self._log("Demo: se inserto 'Flan' duplicado.", "warn")
        self._actualizar_lista_postres()

        eliminados = self.db.eliminar_repetidos()
        if eliminados:
            msg = (
                f"Se eliminaron {len(eliminados)} postre(s) repetido(s):\n"
                f"{', '.join(eliminados)}\n\n"
                "CONCLUSION:\n"
                "Al eliminar un postre duplicado, su lista enlazada\n"
                "de ingredientes se pierde completamente. Si ambas\n"
                "entradas tenian ingredientes distintos, esos datos\n"
                "desaparecen. La solucion correcta es FUSIONAR las\n"
                "listas antes de eliminar el duplicado."
            )
            messagebox.showinfo("Repetidos eliminados", msg)
            self._log(f"Eliminados: {', '.join(eliminados)}", "warn")
        else:
            messagebox.showinfo("Sin repetidos", "No se encontraron postres repetidos.")
            self._log("No se encontraron repetidos.", "info")

        self._postre_activo = None
        self._ingrediente_activo = None
        self.lbl_postre.config(text="<- Selecciona un postre")
        self.ing_listbox.delete(0, "end")
        self._actualizar_lista_postres()


if __name__ == "__main__":
    app = PostresApp()
    app.mainloop()