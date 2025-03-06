import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import Frame, Canvas, Scrollbar

class ScrollableFrame(Frame):
    def __init__(self, parent, bg="white", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Canvas para el desplazamiento
        self.canvas = Canvas(self, bg=bg)
        self.scrollbar_y = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        # Frame interno donde van los widgets
        self.inner_frame = Frame(self.canvas, bg=bg)

        # Configurar el canvas
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Ubicar en la interfaz
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Configurar expansión
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        # Configurar eventos para actualizar el tamaño del contenido
        self.inner_frame.bind("<Configure>", self.update_scroll_region)

        # Eventos de desplazamiento con el mouse y teclado
        self.canvas.bind_all("<MouseWheel>", self.scroll_mouse)
        self.canvas.bind_all("<Shift-MouseWheel>", self.scroll_mouse_horizontal)
        self.canvas.bind_all("<Up>", self.scroll_up)
        self.canvas.bind_all("<Down>", self.scroll_down)
        self.canvas.bind_all("<Left>", self.scroll_left)
        self.canvas.bind_all("<Right>", self.scroll_right)

    def update_scroll_region(self, event=None):
        """Actualizar la región de scroll cuando cambie el tamaño del contenido."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def scroll_mouse(self, event):
        """Desplazamiento vertical con la rueda del mouse."""
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def scroll_mouse_horizontal(self, event):
        """Desplazamiento horizontal con Shift + rueda del mouse."""
        self.canvas.xview_scroll(-1 * (event.delta // 120), "units")

    def scroll_up(self, event):
        """Desplazar arriba con la tecla de flecha."""
        self.canvas.yview_scroll(-1, "units")

    def scroll_down(self, event):
        """Desplazar abajo con la tecla de flecha."""
        self.canvas.yview_scroll(1, "units")

    def scroll_left(self, event):
        """Desplazar a la izquierda con la tecla de flecha."""
        self.canvas.xview_scroll(-1, "units")

    def scroll_right(self, event):
        """Desplazar a la derecha con la tecla de flecha."""
        self.canvas.xview_scroll(1, "units")
"""
# Prueba del módulo
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ejemplo de ScrollFrame")

    scroll_frame = ScrollableFrame(root)
    scroll_frame.pack(fill="both", expand=True)

    # Agregar contenido de prueba (una tabla grande)
    for i in range(50):
        for j in range(10):
            ttk.Label(scroll_frame.inner_frame, text=f"Fila {i+1}, Columna {j+1}", borderwidth=1, relief="solid").grid(row=i, column=j, padx=5, pady=5)

    root.mainloop()
"""