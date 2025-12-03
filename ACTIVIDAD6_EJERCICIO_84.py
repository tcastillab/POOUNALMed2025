import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import csv
from collections import defaultdict

class NominaApp:
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Nómina (Simple)")
        self.ventana.geometry("1000x600")
        self.empleados = [] 
        self.controles = {} 
        
        self._configurar_estilos()
        self._crear_interfaz()
        
        self.actualizar_tabla()
        
    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=6)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#DDD")
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
            
        ttk.Button(marco_entrada, text="➕ Agregar Empleado", command=self.agregar_empleado).grid(row=12, column=0, columnspan=2, pady=(15, 5), sticky="ew")
        ttk.Button(marco_entrada, text="🧹 Limpiar Campos", command=self.limpiar_campos).grid(row=13, column=0, columnspan=2, pady=5, sticky="ew")

        marco_tabla = ttk.Frame(main_frame, padding="10")
        
        marco_tabla.grid(row=0, column=1, sticky='nsew', padx=10, pady=5) 
        marco_tabla.grid_columnconfigure(0, weight=1) 
        marco_tabla.grid_rowconfigure(0, weight=1) 

        columnas = ("Nombre", "Cargo", "Días", "Salario/Día", "Salario Neto")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show='headings')
        
        self.tabla.heading("Nombre", text="Nombre y Apellido", anchor=tk.W)
        self.tabla.column("Nombre", width=200, anchor=tk.W) 
        self.tabla.heading("Cargo", text="Cargo", anchor=tk.CENTER)
        self.tabla.column("Cargo", width=100, anchor=tk.CENTER)
        self.tabla.heading("Días", text="Días Trab.", anchor=tk.CENTER)
        self.tabla.column("Días", width=70, anchor=tk.CENTER)
        self.tabla.heading("Salario/Día", text="Salario por Día", anchor=tk.E)
        self.tabla.column("Salario/Día", width=120, anchor=tk.E)
        self.tabla.heading("Salario Neto", text="SALARIO NETO (COP)", anchor=tk.E)
        self.tabla.column("Salario Neto", width=200, anchor=tk.E) 

        v_scrollbar = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=v_scrollbar.set)
        
        self.tabla.grid(row=0, column=0, sticky='nsew') 
        v_scrollbar.grid(row=0, column=1, sticky='ns')

        marco_resumen = ttk.Frame(main_frame, padding="10")
        marco_resumen.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(5, 0))

        self.etiqueta_total = ttk.Label(marco_resumen, text="Total Nómina: 0.00 COP", font=('Arial', 14, 'bold'), foreground="#333")
        self.etiqueta_total.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(marco_resumen, 
                   text="Exportar Nómina (TXT)", 
                   command=self.exportar_nomina, 
                   style='TButton').pack(side=tk.LEFT, padx=10)

    
    def _validar_numero(self, valor, campo, es_entero=False):
        
        try:
            if es_entero:
                val = int(valor)
            else:
                val = float(valor)
            
            if val < 0:
                 raise ValueError(f"El campo '{campo}' no puede ser negativo.")
            return val
        except ValueError:
            raise ValueError(f"El campo '{campo}' debe ser un {'número entero' if es_entero else 'número decimal'} válido.")

    def calcular_salario_mensual(self, datos):
        
        try:
            salario_dia = self._validar_numero(datos["salario_dia"], "Salario por Día")
            dias_trabajados = self._validar_numero(datos["dias_trabajados"], "Días Trabajados", es_entero=True)
            otros_ingresos = self._validar_numero(datos["otros_ingresos"], "Otros Ingresos")
            pagos_salud = self._validar_numero(datos["pagos_salud"], "Pagos Salud")
            aporte_pensiones = self._validar_numero(datos["aporte_pensiones"], "Aporte Pensiones")
            
            if not (1 <= dias_trabajados <= 31):
                raise ValueError("Los Días Trabajados deben estar entre 1 y 31.")

            salario_base = dias_trabajados * salario_dia
            salario = salario_base + otros_ingresos - pagos_salud - aporte_pensiones
            
            return round(salario, 2)
        except ValueError as e:
            raise e
        

    def _cargar_ejemplos(self):
        self.empleados = []

    def agregar_empleado(self):
        
        datos = {key: control.get() for key, control in self.controles.items()}
        
        required_text_fields = ["nombre", "apellidos"]
        if not all(datos[k].strip() for k in required_text_fields):
            messagebox.showwarning("Validación", "Por favor, complete los campos Nombre y Apellidos.")
            return

        try:
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
            
            self.empleados.append(empleado_final)
            self.actualizar_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Empleado agregado correctamente.")

        except ValueError as e:
            messagebox.showerror("Error de Datos", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Un error inesperado ocurrió: {str(e)}")

    def limpiar_campos(self):
        
        for key, control in self.controles.items():
            if isinstance(control, (tk.Entry, ttk.Entry, tk.Spinbox)):
                control.delete(0, tk.END)
            
            if key == "cargo" or key == "genero":
                control.set(control['values'][0])


    def actualizar_tabla(self):
        
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        total_nomina = 0.0
        
        for emp in self.empleados:
            try:
                salario_neto = self.calcular_salario_mensual({
                    "salario_dia": emp["salario_dia"],
                    "dias_trabajados": emp["dias_trabajados"],
                    "otros_ingresos": emp["otros_ingresos"],
                    "pagos_salud": emp["pagos_salud"],
                    "aporte_pensiones": emp["aporte_pensiones"],
                })
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
                archivo.write("================================================\n")
                archivo.write("               NÓMINA EMPRESARIAL\n")
                archivo.write("================================================\n\n")

                total = sum(e["salario_neto"] for e in self.empleados)
                archivo.write(f"RESUMEN GENERAL:\n")
                archivo.write(f"  Total de Personas Registradas: {len(self.empleados)}\n")
                archivo.write(f"  Total Desembolso Nómina (COP): {total:,.2f}\n\n")

                archivo.write("-" * 50 + "\n\n") 

                for i, empleado in enumerate(self.empleados, 1):
                    salario_base = empleado['dias_trabajados'] * empleado['salario_dia']
                    
                    archivo.write(f"--- DETALLE EMPLEADO N° {i} ---\n")
                    archivo.write(f"  Nombre Completo: {empleado['nombre']} {empleado['apellidos']}\n")
                    archivo.write(f"  Cargo: {empleado['cargo']} | Género: {empleado['genero']}\n\n")
                    
                    archivo.write(f"  >>> INGRESOS:\n")
                    archivo.write(f"    Salario Base ({empleado['dias_trabajados']} días): {salario_base:,.2f} COP\n")
                    archivo.write(f"    Otros Ingresos: + {empleado['otros_ingresos']:,.2f} COP\n")
                    
                    archivo.write(f"\n  <<< DEDUCCIONES:\n")
                    archivo.write(f"    Pagos Salud: - {empleado['pagos_salud']:,.2f} COP\n")
                    archivo.write(f"    Aporte Pensiones: - {empleado['aporte_pensiones']:,.2f} COP\n")
                    
                    archivo.write("\n" + "-" * 50 + "\n")
                    archivo.write(f"  TOTAL NETO A PAGAR: {empleado['salario_neto']:,.2f} COP\n")
                    archivo.write("-" * 50 + "\n\n\n")
            
            messagebox.showinfo("Exportado", f"Nómina guardada exitosamente en:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error de Archivo", f"Ocurrió un error al guardar: {str(e)}")

    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = NominaApp()
    app.ejecutar()
