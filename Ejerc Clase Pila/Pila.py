import tkinter as tk
from tkinter import messagebox
import time

# ─────────────────────────────────────────────
#  Colores y constantes
# ─────────────────────────────────────────────
BG         = "#0D0D1A"
PANEL_BG   = "#13132B"
ACCENT     = "#7C3AED"
ACCENT2    = "#A78BFA"
BTN_PUSH   = "#059669"
BTN_POP    = "#DC2626"
BTN_PEEK   = "#D97706"
BTN_CLEAR  = "#1D4ED8"
TEXT_LIGHT = "#F0EEFF"
TEXT_DIM   = "#6B6B9A"
BLOCK_H    = 54           # Altura de cada bloque de la pila
BLOCK_W    = 220          # Ancho de cada bloque
MAX_ITEMS  = 9            # Máximo de elementos

class PilaVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("🗂  Visualizador de Pila (Stack)")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.stack   = []      # La pila lógica
        self.animating = False

        self._build_ui()

    # ─────────────────────────────────────────
    #  Construcción de la interfaz
    # ─────────────────────────────────────────
    def _build_ui(self):
        # Título
        tk.Label(self.root, text="PILA  /  STACK",
                 font=("Courier New", 20, "bold"),
                 bg=BG, fg=ACCENT2).pack(pady=(20, 4))
        tk.Label(self.root, text="Estructura LIFO  —  Last In, First Out",
                 font=("Courier New", 10),
                 bg=BG, fg=TEXT_DIM).pack(pady=(0, 16))

        # Contenedor principal
        main = tk.Frame(self.root, bg=BG)
        main.pack(padx=30, pady=4)

        # ── Panel izquierdo: canvas de la pila ──────────────
        left = tk.Frame(main, bg=PANEL_BG, bd=0, relief="flat",
                        highlightbackground=ACCENT, highlightthickness=1)
        left.grid(row=0, column=0, padx=(0, 20), pady=4, sticky="n")

        tk.Label(left, text="📦  Memoria de la Pila",
                 font=("Courier New", 11, "bold"),
                 bg=PANEL_BG, fg=ACCENT2).pack(pady=(12, 6))

        canvas_h = MAX_ITEMS * BLOCK_H + 60
        self.canvas = tk.Canvas(left, width=BLOCK_W + 60,
                                height=canvas_h,
                                bg=PANEL_BG, bd=0, highlightthickness=0)
        self.canvas.pack(padx=16, pady=(0, 16))

        # Dibujar base de la pila
        bx0 = 30; bx1 = bx0 + BLOCK_W
        by  = canvas_h - 20
        self.canvas.create_line(bx0 - 8, by, bx1 + 8, by,
                                fill=ACCENT, width=3)
        self.canvas.create_line(bx0 - 8, by - MAX_ITEMS * BLOCK_H,
                                bx0 - 8, by, fill=ACCENT, width=3)
        self.canvas.create_line(bx1 + 8, by - MAX_ITEMS * BLOCK_H,
                                bx1 + 8, by, fill=ACCENT, width=3)

        # Flechas de referencia
        self.arrow_label = self.canvas.create_text(
            bx1 + 35, by, text="BASE", fill=TEXT_DIM,
            font=("Courier New", 8), anchor="e")
        self.top_arrow = self.canvas.create_text(
            bx1 + 35, by, text="", fill=ACCENT2,
            font=("Courier New", 9, "bold"), anchor="e")

        self.base_y   = by
        self.origin_x = bx0
        self.block_rects  = []
        self.block_texts  = []
        self.block_idx    = []

        # ── Panel derecho: controles ─────────────────────────
        right = tk.Frame(main, bg=BG)
        right.grid(row=0, column=1, sticky="n")

        # Entrada
        tk.Label(right, text="Valor a insertar:",
                 font=("Courier New", 10),
                 bg=BG, fg=TEXT_DIM).pack(anchor="w")
        self.entry = tk.Entry(right, font=("Courier New", 16, "bold"),
                              bg=PANEL_BG, fg=TEXT_LIGHT,
                              insertbackground=ACCENT2, bd=0,
                              highlightbackground=ACCENT,
                              highlightthickness=1, width=14)
        self.entry.pack(pady=(4, 14))
        self.entry.bind("<Return>", lambda e: self._push())

        # Botones
        self._btn(right, "▲  PUSH  (Apilar)",   BTN_PUSH,  self._push)
        self._btn(right, "▼  POP   (Desapilar)", BTN_POP,   self._pop)
        self._btn(right, "👁  PEEK  (Ver cima)", BTN_PEEK,  self._peek)
        self._btn(right, "🗑  CLEAR (Vaciar)",   BTN_CLEAR, self._clear)

        # Panel de estado
        tk.Label(right, text="─" * 26,
                 bg=BG, fg=TEXT_DIM).pack(pady=(18, 4))

        self.lbl_size = tk.Label(right, text="Tamaño:  0",
                                 font=("Courier New", 11, "bold"),
                                 bg=BG, fg=TEXT_LIGHT)
        self.lbl_size.pack(anchor="w")

        self.lbl_top = tk.Label(right, text="Cima:      —",
                                font=("Courier New", 11, "bold"),
                                bg=BG, fg=ACCENT2)
        self.lbl_top.pack(anchor="w")

        self.lbl_empty = tk.Label(right, text="Estado:  vacía ✓",
                                  font=("Courier New", 11),
                                  bg=BG, fg=BTN_PUSH)
        self.lbl_empty.pack(anchor="w", pady=(4, 0))

        # Log
        tk.Label(right, text="─" * 26,
                 bg=BG, fg=TEXT_DIM).pack(pady=(14, 4))
        tk.Label(right, text="Historial de operaciones:",
                 font=("Courier New", 9),
                 bg=BG, fg=TEXT_DIM).pack(anchor="w")

        log_frame = tk.Frame(right, bg=PANEL_BG, highlightbackground=ACCENT,
                             highlightthickness=1)
        log_frame.pack(fill="both", expand=True, pady=(4, 0))
        self.log = tk.Text(log_frame, font=("Courier New", 9),
                           bg=PANEL_BG, fg=TEXT_LIGHT,
                           state="disabled", width=28, height=10,
                           bd=0, wrap="word")
        self.log.pack(padx=6, pady=6)

    def _btn(self, parent, text, color, cmd):
        tk.Button(parent, text=text,
                  font=("Courier New", 11, "bold"),
                  bg=color, fg="white",
                  activebackground=color, activeforeground="white",
                  relief="flat", cursor="hand2", width=22,
                  command=cmd).pack(pady=4, ipady=6)

    # ─────────────────────────────────────────
    #  Operaciones de la pila
    # ─────────────────────────────────────────
    def _push(self):
        if self.animating:
            return
        val = self.entry.get().strip()
        if not val:
            messagebox.showwarning("Sin valor", "Escribe un valor antes de apilar.")
            return
        if len(self.stack) >= MAX_ITEMS:
            messagebox.showerror("Pila llena", f"La pila alcanzó su límite de {MAX_ITEMS} elementos.")
            return
        self.stack.append(val)
        self.entry.delete(0, tk.END)
        idx = len(self.stack) - 1
        self._animate_push(val, idx)
        self._log(f"PUSH  → '{val}'", BTN_PUSH)
        self._update_status()

    def _pop(self):
        if self.animating:
            return
        if not self.stack:
            messagebox.showwarning("Pila vacía", "No hay elementos que desapilar.")
            return
        val = self.stack.pop()
        self._animate_pop()
        self._log(f"POP   ← '{val}'", BTN_POP)
        self._update_status()

    def _peek(self):
        if not self.stack:
            messagebox.showinfo("Pila vacía", "La pila está vacía.")
            return
        val = self.stack[-1]
        self._flash_top()
        self._log(f"PEEK    '{val}'", BTN_PEEK)
        messagebox.showinfo("Cima de la pila", f"El elemento en la cima es:\n\n  ➤  {val}")

    def _clear(self):
        if self.animating or not self.stack:
            return
        self.stack.clear()
        for r in self.block_rects:
            self.canvas.delete(r)
        for t in self.block_texts:
            self.canvas.delete(t)
        for i in self.block_idx:
            self.canvas.delete(i)
        self.block_rects.clear()
        self.block_texts.clear()
        self.block_idx.clear()
        self.canvas.itemconfig(self.top_arrow, text="")
        self._log("CLEAR  ✕  (vaciada)", BTN_CLEAR)
        self._update_status()

    # ─────────────────────────────────────────
    #  Animaciones
    # ─────────────────────────────────────────
    def _animate_push(self, val, idx):
        self.animating = True
        bx0 = self.origin_x
        by  = self.base_y - (idx + 1) * BLOCK_H + 2

        # Color degradado según posición
        hue = idx / MAX_ITEMS
        r_col = self._lerp_color("#1E3A5F", "#4C1D95", hue)

        rect = self.canvas.create_rectangle(
            bx0, by - 20, bx0 + BLOCK_W, by + BLOCK_H - 22,
            fill=r_col, outline=ACCENT2, width=1)
        text = self.canvas.create_text(
            bx0 + BLOCK_W // 2, by + BLOCK_H // 2 - 22,
            text=val, fill=TEXT_LIGHT,
            font=("Courier New", 14, "bold"))
        idxt = self.canvas.create_text(
            bx0 + 10, by + BLOCK_H // 2 - 22,
            text=f"[{idx}]", fill=TEXT_DIM,
            font=("Courier New", 8), anchor="w")

        self.block_rects.append(rect)
        self.block_texts.append(text)
        self.block_idx.append(idxt)

        # Animación de caída
        target_y = by
        steps = 12
        delta = BLOCK_H // steps

        def drop(step=0):
            if step < steps:
                self.canvas.move(rect, 0, delta)
                self.canvas.move(text, 0, delta)
                self.canvas.move(idxt, 0, delta)
                self.root.after(18, drop, step + 1)
            else:
                self._update_top_arrow()
                self.animating = False

        self.canvas.move(rect, 0, -BLOCK_H)
        self.canvas.move(text, 0, -BLOCK_H)
        self.canvas.move(idxt, 0, -BLOCK_H)
        drop()

    def _animate_pop(self):
        self.animating = True
        if not self.block_rects:
            self.animating = False
            return
        rect = self.block_rects.pop()
        text = self.block_texts.pop()
        idxt = self.block_idx.pop()
        steps = 12
        delta = BLOCK_H // steps

        def rise(step=0):
            if step < steps:
                self.canvas.move(rect, 0, -delta)
                self.canvas.move(text, 0, -delta)
                self.canvas.move(idxt, 0, -delta)
                self.root.after(18, rise, step + 1)
            else:
                self.canvas.delete(rect)
                self.canvas.delete(text)
                self.canvas.delete(idxt)
                self._update_top_arrow()
                self.animating = False

        rise()

    def _flash_top(self):
        if not self.block_rects:
            return
        rect = self.block_rects[-1]
        orig = self.canvas.itemcget(rect, "outline")
        for i in range(6):
            color = BTN_PEEK if i % 2 == 0 else ACCENT2
            self.root.after(i * 100,
                lambda c=color: self.canvas.itemconfig(rect, outline=c, width=3))
        self.root.after(700,
            lambda: self.canvas.itemconfig(rect, outline=orig, width=1))

    def _update_top_arrow(self):
        if self.stack:
            idx = len(self.stack) - 1
            y   = self.base_y - (idx + 1) * BLOCK_H + BLOCK_H // 2 - 2
            self.canvas.coords(self.top_arrow,
                               self.origin_x + BLOCK_W + 38, y)
            self.canvas.itemconfig(self.top_arrow, text="◄ TOP")
        else:
            self.canvas.itemconfig(self.top_arrow, text="")

    # ─────────────────────────────────────────
    #  Estado y log
    # ─────────────────────────────────────────
    def _update_status(self):
        n = len(self.stack)
        self.lbl_size.config(text=f"Tamaño:  {n}")
        if self.stack:
            self.lbl_top.config(text=f"Cima:      {self.stack[-1]}")
            self.lbl_empty.config(text=f"Estado:  con datos ({n}/{MAX_ITEMS})",
                                  fg=ACCENT2)
        else:
            self.lbl_top.config(text="Cima:      —")
            self.lbl_empty.config(text="Estado:  vacía ✓", fg=BTN_PUSH)

    def _log(self, msg, color):
        self.log.config(state="normal")
        self.log.insert("end", f"  {msg}\n")
        self.log.see("end")
        self.log.config(state="disabled")

    # ─────────────────────────────────────────
    #  Utilidad de color
    # ─────────────────────────────────────────
    @staticmethod
    def _lerp_color(c1, c2, t):
        r1,g1,b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
        r2,g2,b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
        r = int(r1 + (r2-r1)*t)
        g = int(g1 + (g2-g1)*t)
        b = int(b1 + (b2-b1)*t)
        return f"#{r:02x}{g:02x}{b:02x}"


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = PilaVisual(root)
    root.mainloop()