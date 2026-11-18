import tkinter as tk
from tkinter import ttk, messagebox, filedialog


def intercalar(lista_a, lista_b, clave=lambda x: x):
    """Mezcla dos listas ordenadas en una sola lista ordenada."""
    resultado = []
    i = j = 0
    while i < len(lista_a) and j < len(lista_b):
        if clave(lista_a[i]) <= clave(lista_b[j]):
            resultado.append(lista_a[i])
            i += 1
        else:
            resultado.append(lista_b[j])
            j += 1
    resultado.extend(lista_a[i:])
    resultado.extend(lista_b[j:])
    return resultado


class IntercalacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intercalación de Listas Ordenadas - O(n + m)")
        self.root.geometry("850x550")
        self.root.resizable(False, False)

        # Listas de datos: tuplas (matricula, nombre)
        self.grupo_a = []
        self.grupo_b = []
        self.lista_general = []

        # Variables para el modo paso a paso
        self.paso_i = 0
        self.paso_j = 0
        self.en_modo_pasos = False

        self._construir_interfaz()

    def _construir_interfaz(self):
        # --- MARCO SUPERIOR: Entrada manual de datos ---
        frame_entrada = ttk.LabelFrame(self.root, text="1. Agregar Alumno Manualmente", padding=10)
        frame_entrada.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_entrada, text="Matrícula:").grid(row=0, column=0, padx=5)
        self.entry_mat = ttk.Entry(frame_entrada, width=12)
        self.entry_mat.grid(row=0, column=1, padx=5)

        ttk.Label(frame_entrada, text="Nombre:").grid(row=0, column=2, padx=5)
        self.entry_nom = ttk.Entry(frame_entrada, width=25)
        self.entry_nom.grid(row=0, column=3, padx=5)

        ttk.Button(frame_entrada, text="+ Grupo A", command=lambda: self.agregar_alumno("A")).grid(row=0, column=4, padx=5)
        ttk.Button(frame_entrada, text="+ Grupo B", command=lambda: self.agregar_alumno("B")).grid(row=0, column=5, padx=5)
        ttk.Button(frame_entrada, text="Cargar Ejemplo", command=self.cargar_ejemplo).grid(row=0, column=6, padx=15)
        ttk.Button(frame_entrada, text="Limpiar Todo", command=self.limpiar_todo).grid(row=0, column=7, padx=5)

        # --- MARCO CENTRAL: Visualización de las 3 listas ---
        frame_listas = ttk.Frame(self.root, padding=10)
        frame_listas.pack(fill="both", expand=True, padx=15)

        self.tree_a = self._crear_tabla(frame_listas, "Grupo A (Ordenado)", 0)
        self.tree_b = self._crear_tabla(frame_listas, "Grupo B (Ordenado)", 1)
        self.tree_res = self._crear_tabla(frame_listas, "Lista General Intercalada", 2)

        # --- MARCO INFERIOR: Controles de ejecución y guardado ---
        frame_controles = ttk.LabelFrame(self.root, text="2. Ejecución y Archivo", padding=10)
        frame_controles.pack(fill="x", padx=15, pady=10)

        ttk.Button(frame_controles, text="Intercalar Completo", command=self.ejecutar_completo).pack(side="left", padx=5)
        self.btn_paso = ttk.Button(frame_controles, text="Siguiente Paso (i vs j)", command=self.ejecutar_paso)
        self.btn_paso.pack(side="left", padx=5)

        self.lbl_estado = ttk.Label(frame_controles, text="Estado: Esperando datos...", foreground="blue")
        self.lbl_estado.pack(side="left", padx=20)

        ttk.Button(frame_controles, text="Guardar .TXT", command=self.guardar_archivo).pack(side="right", padx=5)

    def _crear_tabla(self, parent, titulo, columna):
        frame = ttk.LabelFrame(parent, text=titulo, padding=5)
        frame.grid(row=0, column=columna, padx=8, sticky="nsew")
        parent.columnconfigure(columna, weight=1)

        tree = ttk.Treeview(frame, columns=("mat", "nom"), show="headings", height=12)
        tree.heading("mat", text="Matrícula")
        tree.heading("nom", text="Nombre")
        tree.column("mat", width=80, anchor="center")
        tree.column("nom", width=150, anchor="w")
        tree.pack(fill="both", expand=True)
        return tree

    def agregar_alumno(self, grupo):
        mat_str = self.entry_mat.get().strip()
        nom = self.entry_nom.get().strip()

        if not mat_str.isdigit() or not nom:
            messagebox.showwarning("Dato inválido", "La matrícula debe ser un número entero y el nombre no puede estar vacío.")
            return

        mat = int(mat_str)
        lista_objetivo = self.grupo_a if grupo == "A" else self.grupo_b

        if any(m == mat for m, _ in lista_objetivo):
            messagebox.showerror("Duplicado", f"La matrícula {mat} ya existe en el Grupo {grupo}.")
            return

        if lista_objetivo and mat < lista_objetivo[-1][0]:
            messagebox.showinfo(
                "Ordenamiento automático",
                f"La intercalación requiere listas previamente ordenadas.\nSe insertará {mat} en su posición correspondiente."
            )

        lista_objetivo.append((mat, nom))
        lista_objetivo.sort(key=lambda x: x[0])

        self.entry_mat.delete(0, tk.END)
        self.entry_nom.delete(0, tk.END)
        self.reiniciar_estado_intercalacion()
        self.actualizar_tablas()

    def cargar_ejemplo(self):
        self.grupo_a = [(1001, "Ana"), (1004, "Carlos"), (1008, "Elena"), (1012, "Gabriela")]
        self.grupo_b = [(1002, "Bruno"), (1003, "Diana"), (1009, "Fernando"), (1015, "Hugo"), (1020, "Iris")]
        self.reiniciar_estado_intercalacion()
        self.actualizar_tablas()
        self.lbl_estado.config(text="Estado: Datos de ejemplo cargados.")

    def limpiar_todo(self):
        self.grupo_a.clear()
        self.grupo_b.clear()
        self.reiniciar_estado_intercalacion()
        self.actualizar_tablas()
        self.lbl_estado.config(text="Estado: Listas vacías.")

    def reiniciar_estado_intercalacion(self):
        self.lista_general.clear()
        self.paso_i = 0
        self.paso_j = 0
        self.en_modo_pasos = False

    def actualizar_tablas(self):
        for tree, datos in [(self.tree_a, self.grupo_a), (self.tree_b, self.grupo_b), (self.tree_res, self.lista_general)]:
            for item in tree.get_children():
                tree.delete(item)
            for idx, (mat, nom) in enumerate(datos):
                item_id = tree.insert("", "end", values=(mat, nom))
                if self.en_modo_pasos:
                    if tree == self.tree_a and idx == self.paso_i:
                        tree.selection_set(item_id)
                    elif tree == self.tree_b and idx == self.paso_j:
                        tree.selection_set(item_id)

    def ejecutar_completo(self):
        if not self.grupo_a and not self.grupo_b:
            messagebox.showinfo("Aviso", "Agrega alumnos primero.")
            return
        self.en_modo_pasos = False
        self.lista_general = intercalar(self.grupo_a, self.grupo_b, clave=lambda r: r[0])
        self.actualizar_tablas()
        self.lbl_estado.config(text=f"Completado: {len(self.lista_general)} alumnos intercalados.")

    def ejecutar_paso(self):
        if not self.grupo_a and not self.grupo_b:
            messagebox.showinfo("Aviso", "Agrega alumnos primero.")
            return

        if not self.en_modo_pasos:
            self.reiniciar_estado_intercalacion()
            self.en_modo_pasos = True
            self.actualizar_tablas()
            self.lbl_estado.config(text="Modo paso a paso iniciado. Presiona 'Siguiente Paso'.")
            return

        if self.paso_i < len(self.grupo_a) and self.paso_j < len(self.grupo_b):
            val_a = self.grupo_a[self.paso_i]
            val_b = self.grupo_b[self.paso_j]
            if val_a[0] <= val_b[0]:
                self.lista_general.append(val_a)
                self.lbl_estado.config(text=f"Comparado {val_a[0]} <= {val_b[0]} -> Entra {val_a[1]} (Grupo A)")
                self.paso_i += 1
            else:
                self.lista_general.append(val_b)
                self.lbl_estado.config(text=f"Comparado {val_a[0]} > {val_b[0]} -> Entra {val_b[1]} (Grupo B)")
                self.paso_j += 1
        elif self.paso_i < len(self.grupo_a):
            val_a = self.grupo_a[self.paso_i]
            self.lista_general.append(val_a)
            self.lbl_estado.config(text=f"Grupo B terminó -> Copia restante {val_a[1]} (Grupo A)")
            self.paso_i += 1
        elif self.paso_j < len(self.grupo_b):
            val_b = self.grupo_b[self.paso_j]
            self.lista_general.append(val_b)
            self.lbl_estado.config(text=f"Grupo A terminó -> Copia restante {val_b[1]} (Grupo B)")
            self.paso_j += 1
        else:
            self.en_modo_pasos = False
            self.lbl_estado.config(text="¡Intercalación paso a paso finalizada!")

        self.actualizar_tablas()

    def guardar_archivo(self):
        if not self.lista_general:
            messagebox.showwarning("Sin datos", "Primero debes generar la lista general intercalada.")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile="lista_general.txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if ruta:
            with open(ruta, "w", encoding="utf-8") as f:
                for matricula, nombre in self.lista_general:
                    f.write(f"{matricula},{nombre}\n")
            messagebox.showinfo("Guardado", f"Archivo guardado exitosamente en:\n{ruta}")


if __name__ == "__main__":
    root = tk.Tk()
    app = IntercalacionApp(root)
    
    # Forzar que la ventana aparezca al frente en Windows
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    root.mainloop()