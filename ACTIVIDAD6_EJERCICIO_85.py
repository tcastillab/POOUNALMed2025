import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import pickle

# 1. CONSTANTE para el nombre del archivo de carga/guardado automático
ARCHIVO_NOMINA = "nomina_binaria.dat"

class NominaApp:
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Nómina")
        self.ventana.geometry("1050x650") 
        self.empleados = [] 
        self.controles = {} 
        self._empleado_seleccionado_index = -1 
        
        self._configurar_estilos()
        self._crear_interfaz()
        
        # Cargar datos al inicio (si existe el archivo en la ruta por defecto)
        self.cargar_nomina_binario(silent_load=True) 
        self.actualizar_tabla()
        
    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=6)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Treeview", font=('Arial', 9))
        
        
    def _crear_interfaz(self):
        
        main_frame = ttk.Frame(self.ventana, padding="10")
        main_frame.pack(fill='both', expand=True)
        main_frame.grid_columnconfigure(0, weight=0) 
        main_frame.grid_columnconfigure(1, weight=1) 
        main_frame.grid_rowconfigure(0, weight=1)

        marco_entrada = ttk.Frame(main_frame, padding="10", relief="groove")
        marco_entrada.grid(row=0, column=0, sticky='nsew', padx=10, pady=5)
        
        ttk.Label(marco_entrada, text="Datos del Empleado", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")
        
        campos_entrada = [
            ("Nombre:", "nombre", 1),
            ("Apellidos:", "apellidos", 2),
            ("Cargo:", "cargo", 3, True, ["Operativo", "Estratégico", "Directivo"]), 
            ("Género:", "genero", 4, True, ["Masculino", "Femenino"]), 
            ("Salario por Día (COP):", "salario_dia", 6),
            ("Días Trabajados (1-31):", "dias_trabajados", 7),
            ("Otros Ingresos:", "otros_ingresos", 8),
            ("Pagos Salud:", "pagos_salud", 9),
            ("Aporte Pensiones:", "aporte_pensiones", 10),
        ]
        
        for label_text, key, row_num, is_combobox, values in [(c[0], c[1], c[2], c[3] if len(c) > 3 else False, c[4] if len(c) > 4 else []) for c in campos_entrada]:
            ttk.Label(marco_entrada, text=label_text).grid(row=row_num, column=0, padx=5, pady=2, sticky="w")
            
            if is_combobox:
                control = ttk.Combobox(marco_entrada, values=values, state="readonly", width=25)
                control.set(values[0])
            else:
                control = ttk.Entry(marco_entrada, width=28)
                
            control.grid(row=row_num, column=1, padx=5, pady=2, sticky="e")
            self.controles[key] = control
            
        self.btn_agregar = ttk.Button(marco_entrada, text="Agregar Empleado", command=self.agregar_empleado)
        self.btn_agregar.grid(row=12, column=0, columnspan=2, pady=(15, 5), sticky="ew")
        
        self.btn_guardar_edicion = ttk.Button(marco_entrada, text="Guardar Edición", command=self.guardar_edicion)
        self.btn_guardar_edicion.grid(row=12, column=0, columnspan=2, pady=(15, 5), sticky="ew")
        self.btn_guardar_edicion.grid_remove() 
        
        self.btn_limpiar = ttk.Button(marco_entrada, text="Limpiar Campos", command=self.limpiar_campos)
        self.btn_limpiar.grid(row=13, column=0, columnspan=2, pady=5, sticky="ew")

        marco_tabla = ttk.Frame(main_frame, padding="10")
        marco_tabla.grid(row=0, column=1, sticky='nsew', padx=10, pady=5) 
        marco_tabla.grid_columnconfigure(0, weight=1) 
        marco_tabla.grid_rowconfigure(0, weight=1) 

        columnas = ("Nombre", "Cargo", "Días", "Salario/Día", "Salario Neto")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show='headings')
        
        self.tabla.heading("Nombre", text="Nombre y Apellido", anchor=tk.W)
        self.tabla.column("Nombre", width=180, anchor=tk.W) 
        self.tabla.heading("Cargo", text="Cargo", anchor=tk.CENTER)
        self.tabla.column("Cargo", width=100, anchor=tk.CENTER)
        self.tabla.heading("Días", text="Días Trab.", anchor=tk.CENTER)
        self.tabla.column("Días", width=70, anchor=tk.CENTER)
        self.tabla.heading("Salario/Día", text="Salario por Día", anchor=tk.E)
        self.tabla.column("Salario/Día", width=110, anchor=tk.E)
        self.tabla.heading("Salario Neto", text="SALARIO NETO (COP)", anchor=tk.E)
        self.tabla.column("Salario Neto", width=160, anchor=tk.E)

        v_scrollbar = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=v_scrollbar.set)
        
        self.tabla.grid(row=0, column=0, sticky='nsew') 
        v_scrollbar.grid(row=0, column=1, sticky='ns')

        self.tabla.bind('<<TreeviewSelect>>', self.cargar_empleado_seleccionado) 

        marco_botones_tabla = ttk.Frame(marco_tabla, padding="5")
        marco_botones_tabla.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))

        ttk.Button(marco_botones_tabla, text="Eliminar Seleccionado", command=self.eliminar_empleado).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_botones_tabla, text="Cancelar Edición", command=lambda: self.limpiar_campos(limpiar_seleccion=True)).pack(side=tk.LEFT, padx=5)

        marco_resumen = ttk.Frame(main_frame, padding="10")
        marco_resumen.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(5, 0))

        self.etiqueta_total = ttk.Label(marco_resumen, text="Total Nómina: 0.00 COP", font=('Arial', 14, 'bold'))
        self.etiqueta_total.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(marco_resumen, text="Guardar Nómina (Binario)", command=self.guardar_nomina_binario).pack(side=tk.LEFT, padx=10)
        ttk.Button(marco_resumen, text="Cargar Nómina (Binario)", command=self.cargar_nomina_binario).pack(side=tk.LEFT, padx=10)
        ttk.Button(marco_resumen, text="Exportar a Texto", command=self.exportar_nomina).pack(side=tk.LEFT, padx=10)


    
    def _validar_numero(self, valor, campo, es_entero=False):
        
        try:
            val = int(valor) if es_entero else float(valor)
            if val < 0:
                 raise ValueError(f"El campo '{campo}' no puede ser negativo.")
            return val
        except ValueError:
            raise ValueError(f"El campo '{campo}' debe ser un {'número entero' if es_entero else 'número decimal'} válido.")

    def calcular_salario_mensual(self, datos):
        
        salario_dia = self._validar_numero(str(datos["salario_dia"]), "Salario por Día")
        dias_trabajados = self._validar_numero(str(datos["dias_trabajados"]), "Días Trabajados", es_entero=True)
        otros_ingresos = self._validar_numero(str(datos["otros_ingresos"]), "Otros Ingresos")
        pagos_salud = self._validar_numero(str(datos["pagos_salud"]), "Pagos Salud")
        aporte_pensiones = self._validar_numero(str(datos["aporte_pensiones"]), "Aporte Pensiones")
        
        if not (1 <= dias_trabajados <= 31):
            raise ValueError("Los Días Trabajados deben estar entre 1 y 31.")

        salario_base = dias_trabajados * salario_dia
        salario = salario_base + otros_ingresos - pagos_salud - aporte_pensiones
        
        return round(salario, 2)
        
    def _get_validated_employee_data(self, datos):
        
        required_text_fields = ["nombre", "apellidos"]
        if not all(datos.get(k, '').strip() for k in required_text_fields):
            raise ValueError("Por favor, complete los campos Nombre y Apellidos.")

        salario_neto = self.calcular_salario_mensual(datos) 

        empleado_final = {
            "nombre": datos["nombre"],
            "apellidos": datos["apellidos"],
            "cargo": datos["cargo"],
            "genero": datos["genero"],
            "salario_dia": self._validar_numero(datos["salario_dia"], "Salario por Día"),
            "dias_trabajados": self._validar_numero(datos["dias_trabajados"], "Días Trabajados", True),
            "otros_ingresos": self._validar_numero(datos["otros_ingresos"], "Otros Ingresos"),
            "pagos_salud": self._validar_numero(datos["pagos_salud"], "Pagos Salud"),
            "aporte_pensiones": self._validar_numero(datos["aporte_pensiones"], "Aporte Pensiones"),
            "salario_neto": salario_neto
        }
        return empleado_final

    
    def agregar_empleado(self):
        
        datos = {key: control.get() for key, control in self.controles.items()}
        try:
            empleado_final = self._get_validated_employee_data(datos)
            self.empleados.append(empleado_final)
            self.actualizar_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error de Datos", str(e))

    def limpiar_campos(self, limpiar_seleccion=False):
        
        for key, control in self.controles.items():
            if isinstance(control, (tk.Entry, ttk.Entry, tk.Spinbox)):
                control.delete(0, tk.END)
            if key == "cargo" or key == "genero":
                control.set(control['values'][0])
        
        self._empleado_seleccionado_index = -1
        self.btn_guardar_edicion.grid_remove()
        self.btn_agregar.grid()
        
        if limpiar_seleccion and self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])
            
    def actualizar_tabla(self):
        
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        total_nomina = 0.0
        
        for emp in self.empleados:
            try:
                salario_neto = self.calcular_salario_mensual(emp)
            except ValueError:
                salario_neto = 0.0
            
            total_nomina += salario_neto
            
            self.tabla.insert('', tk.END, values=(
                f"{emp['nombre']} {emp['apellidos']}", 
                emp["cargo"], 
                emp["dias_trabajados"],
                f"{emp['salario_dia']:,.2f}", 
                f"{salario_neto:,.2f}"
            ))

        self.etiqueta_total.config(text=f"Total de la Nómina Empresarial: {total_nomina:,.2f} COP")

    
    def cargar_empleado_seleccionado(self, event):
        
        if not self.tabla.selection():
            return
            
        selected_item = self.tabla.selection()[0]
        try:
            fila_indice = self.tabla.get_children().index(selected_item)
            self._empleado_seleccionado_index = fila_indice
            empleado_datos = self.empleados[fila_indice]

            self.limpiar_campos() 

            for key, control in self.controles.items():
                valor = empleado_datos.get(key)
                if valor is not None:
                    if isinstance(valor, (int, float)):
                        valor = str(valor)
                        
                    if isinstance(control, (tk.Entry, ttk.Entry)):
                        control.insert(0, valor)
                    elif isinstance(control, ttk.Combobox):
                        control.set(valor)
            
            self.btn_agregar.grid_remove()
            self.btn_guardar_edicion.grid()
            
        except (IndexError, ValueError):
            self._empleado_seleccionado_index = -1

    def guardar_edicion(self):
        
        if self._empleado_seleccionado_index == -1:
            messagebox.showwarning("Edición", "Primero debe seleccionar un empleado para editar.")
            return

        datos_modificados = {key: control.get() for key, control in self.controles.items()}

        try:
            empleado_final = self._get_validated_employee_data(datos_modificados)
            self.empleados[self._empleado_seleccionado_index] = empleado_final 
            self.actualizar_tabla()
            self.limpiar_campos(limpiar_seleccion=True)
            messagebox.showinfo("Éxito", "Empleado editado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error de Datos", str(e))

    def eliminar_empleado(self):
        
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar", "Seleccione un empleado para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar el empleado?"):
            selected_item = seleccion[0]
            try:
                fila_indice = self.tabla.get_children().index(selected_item)
                del self.empleados[fila_indice] 
                
                if self._empleado_seleccionado_index == fila_indice:
                    self.limpiar_campos(limpiar_seleccion=True)
                    
                self.actualizar_tabla()
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

    
    def guardar_nomina_binario(self):
        
        if not self.empleados:
            messagebox.showwarning("Guardar", "No hay empleados para guardar.")
            return

        # Si el usuario presiona el botón, usamos filedialog para preguntar la ruta
        ruta = filedialog.asksaveasfilename(
            defaultextension=".dat",
            filetypes=[("Archivo Binario de Nómina", "*.dat")],
            initialfile=ARCHIVO_NOMINA 
        )
        if not ruta:
            return

        try:
            with open(ruta, 'wb') as archivo:
                pickle.dump(self.empleados, archivo) 
            messagebox.showinfo("Guardado", f"Nómina guardada exitosamente en formato binario:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {str(e)}")

    def cargar_nomina_binario(self, silent_load=False):
        
        ruta = ""
        
        if silent_load:
            # 2. Si es carga silenciosa (inicio), intentamos la ruta por defecto
            ruta = ARCHIVO_NOMINA
            if not os.path.exists(ruta):
                return # Si no existe el archivo por defecto, termina silenciosamente
        else:
            # Si NO es carga silenciosa (botón "Cargar"), pedimos confirmación y abrimos filedialog
            if not messagebox.askyesno("Cargar Nómina", "¿Desea reemplazar la nómina actual cargando un archivo?"):
                return

            ruta = filedialog.askopenfilename(
                defaultextension=".dat",
                filetypes=[("Archivo Binario de Nómina", "*.dat")],
                initialfile=ARCHIVO_NOMINA
            )
            if not ruta:
                return


        try:
            with open(ruta, 'rb') as archivo:
                datos_cargados = pickle.load(archivo) 
                
                if isinstance(datos_cargados, list):
                    self.empleados = datos_cargados
                    self.actualizar_tabla()
                    self.limpiar_campos(limpiar_seleccion=True)
                    if not silent_load:
                        messagebox.showinfo("Cargado", f"{len(self.empleados)} empleados cargados exitosamente.")
                else:
                    messagebox.showerror("Error", "El archivo no contiene un formato de lista válido.")

        except FileNotFoundError:
            # Solo mostramos el error si la carga no era silenciosa
            if not silent_load:
                messagebox.showwarning("Error", "No se encontró el archivo binario especificado.")
        except Exception as e:
            if not silent_load:
                messagebox.showerror("Error", f"Ocurrió un error al cargar el archivo: {str(e)}")
            self.empleados = []

    
    def exportar_nomina(self):
        
        if not self.empleados:
            messagebox.showwarning("Exportar", "No hay empleados para exportar.")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de Texto", "*.txt")],
            initialfile="Nomina.txt" 
        )
        if not ruta:
            return

        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                total = sum(e["salario_neto"] for e in self.empleados)
                archivo.write("=== RESUMEN DE NÓMINA ===\n")
                archivo.write(f"Total Empleados: {len(self.empleados)}\n")
                archivo.write(f"Total a Desembolsar (COP): {total:,.2f}\n\n")

                for i, empleado in enumerate(self.empleados, 1):
                    archivo.write(f"--- Empleado {i} ---\n")
                    archivo.write(f"Nombre: {empleado['nombre']} {empleado['apellidos']}\n")
                    archivo.write(f"Cargo: {empleado['cargo']}\n")
                    archivo.write(f"Salario Neto: {empleado['salario_neto']:,.2f} COP\n\n")
            
            messagebox.showinfo("Exportado", f"Nómina guardada en:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {str(e)}")

    def ejecutar(self):
        
        self.ventana.mainloop()

if __name__ == "__main__":
    app = NominaApp()
    app.ejecutar()
