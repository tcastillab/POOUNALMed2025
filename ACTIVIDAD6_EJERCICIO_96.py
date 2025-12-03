import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pickle
from datetime import datetime
from tkcalendar import DateEntry 
import os 

ARCHIVO_BINARIO = "agenda_contactos.dat"

class AgendaApp:
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Agenda de Contactos Personal")
        self.ventana.geometry("750x650") 
        self.contactos = [] 
        self.controles = {} 
        self._contacto_seleccionado_index = -1 
        
        self._configurar_estilos()
        self._crear_interfaz()
        
        self.cargar_contactos_binario(silent_load=True) 
        self.actualizar_lista()
        
    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=6)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Treeview", font=('Arial', 9))
        
    def _crear_interfaz(self):
        
        main_frame = ttk.Frame(self.ventana, padding="10")
        main_frame.pack(fill='both', expand=True)
        main_frame.grid_columnconfigure(0, weight=1) 
        main_frame.grid_rowconfigure(1, weight=1) 

        marco_entrada = ttk.Frame(main_frame, padding="10", relief="groove")
        marco_entrada.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        marco_entrada.columnconfigure(1, weight=1)
        marco_entrada.columnconfigure(3, weight=1)
        
        ttk.Label(marco_entrada, text="Datos del Contacto", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="w")
        
        ttk.Label(marco_entrada, text="Nombre:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        entry_nombre = ttk.Entry(marco_entrada, width=30)
        entry_nombre.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        self.controles["nombre"] = entry_nombre
        
        ttk.Label(marco_entrada, text="Apellido:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        entry_apellido = ttk.Entry(marco_entrada, width=30)
        entry_apellido.grid(row=1, column=3, padx=5, pady=2, sticky="ew")
        self.controles["apellido"] = entry_apellido

        ttk.Label(marco_entrada, text="Fecha Nacimiento:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        entry_fecha = DateEntry(marco_entrada, selectmode='day', date_pattern='dd/MM/yyyy', width=27)
        entry_fecha.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        self.controles["fecha_nacimiento"] = entry_fecha

        ttk.Label(marco_entrada, text="Teléfono:").grid(row=2, column=2, padx=5, pady=2, sticky="w")
        entry_telefono = ttk.Entry(marco_entrada, width=30)
        entry_telefono.grid(row=2, column=3, padx=5, pady=2, sticky="ew")
        self.controles["telefono"] = entry_telefono

        ttk.Label(marco_entrada, text="Dirección:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        entry_direccion = ttk.Entry(marco_entrada, width=30)
        entry_direccion.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        self.controles["direccion"] = entry_direccion

        ttk.Label(marco_entrada, text="Correo Electrónico:").grid(row=3, column=2, padx=5, pady=2, sticky="w")
        entry_correo = ttk.Entry(marco_entrada, width=30)
        entry_correo.grid(row=3, column=3, padx=5, pady=2, sticky="ew")
        self.controles["correo"] = entry_correo
        
        self.btn_agregar = ttk.Button(marco_entrada, text="Agregar Contacto", command=self.agregar_contacto)
        self.btn_agregar.grid(row=4, column=0, columnspan=2, pady=(15, 5), padx=5, sticky="ew")
        
        self.btn_guardar_edicion = ttk.Button(marco_entrada, text="Guardar Edición", command=self.guardar_edicion)
        self.btn_guardar_edicion.grid(row=4, column=0, columnspan=2, pady=(15, 5), padx=5, sticky="ew")
        self.btn_guardar_edicion.grid_remove() 
        
        self.btn_limpiar = ttk.Button(marco_entrada, text="Limpiar Campos / Cancelar", command=lambda: self.limpiar_campos(limpiar_seleccion=True))
        self.btn_limpiar.grid(row=4, column=2, columnspan=2, pady=(15, 5), padx=5, sticky="ew")


        marco_lista = ttk.Frame(main_frame, padding="10")
        marco_lista.grid(row=1, column=0, sticky='nsew', padx=5, pady=5) 
        marco_lista.grid_columnconfigure(0, weight=1) 
        marco_lista.grid_rowconfigure(0, weight=1) 

        columnas = ("Nombre", "Teléfono", "Correo", "Nacimiento")
        self.lista_view = ttk.Treeview(marco_lista, columns=columnas, show='headings')
        
        self.lista_view.heading("Nombre", text="Nombre Completo", anchor=tk.W)
        self.lista_view.column("Nombre", width=180, anchor=tk.W) 
        self.lista_view.heading("Teléfono", text="Teléfono", anchor=tk.CENTER)
        self.lista_view.column("Teléfono", width=120, anchor=tk.CENTER)
        self.lista_view.heading("Correo", text="Correo Electrónico", anchor=tk.W)
        self.lista_view.column("Correo", width=200, anchor=tk.W)
        self.lista_view.heading("Nacimiento", text="F. Nacimiento", anchor=tk.CENTER)
        self.lista_view.column("Nacimiento", width=100, anchor=tk.CENTER)

        v_scrollbar = ttk.Scrollbar(marco_lista, orient="vertical", command=self.lista_view.yview)
        self.lista_view.configure(yscrollcommand=v_scrollbar.set)
        
        self.lista_view.grid(row=0, column=0, sticky='nsew') 
        v_scrollbar.grid(row=0, column=1, sticky='ns')

        self.lista_view.bind('<<TreeviewSelect>>', self.cargar_contacto_seleccionado) 

        marco_botones_lista = ttk.Frame(marco_lista, padding="5")
        marco_botones_lista.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))

        ttk.Button(marco_botones_lista, text="Eliminar Contacto", command=self.eliminar_contacto).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(marco_botones_lista, text="Guardar Binario", command=self.guardar_contactos_binario).pack(side=tk.RIGHT, padx=5)
        ttk.Button(marco_botones_lista, text="Cargar Binario", command=self.cargar_contactos_binario).pack(side=tk.RIGHT, padx=5)

    def _validar_datos(self, datos):
        required_fields = {
            "nombre": "Nombre", 
            "apellido": "Apellido", 
            "telefono": "Teléfono", 
            "correo": "Correo Electrónico",
            "direccion": "Dirección"
        }
        
        for key, name in required_fields.items():
            if not datos.get(key, '').strip():
                raise ValueError(f"El campo '{name}' es obligatorio.")

        if "@" not in datos["correo"] or "." not in datos["correo"]:
            raise ValueError("El correo electrónico no es válido.")

        fecha_str = datos["fecha_nacimiento"]
        
        contacto_final = {
            "nombre": datos["nombre"].strip(),
            "apellido": datos["apellido"].strip(),
            "fecha_nacimiento": fecha_str,
            "direccion": datos["direccion"].strip(),
            "telefono": datos["telefono"].strip(),
            "correo": datos["correo"].strip(),
        }
        return contacto_final

    def agregar_contacto(self):
        datos = {key: control.get() for key, control in self.controles.items()}
        try:
            contacto_final = self._validar_datos(datos)
            self.contactos.append(contacto_final)
            self.actualizar_lista()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Contacto agregado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error de Datos", str(e))

    def limpiar_campos(self, limpiar_seleccion=False):
        for key, control in self.controles.items():
            if isinstance(control, (tk.Entry, ttk.Entry)):
                control.delete(0, tk.END)
            elif isinstance(control, DateEntry):
                control.set_date(datetime.now().date()) 
        
        self._contacto_seleccionado_index = -1
        self.btn_guardar_edicion.grid_remove()
        self.btn_agregar.grid()
        
        if limpiar_seleccion and self.lista_view.selection():
            self.lista_view.selection_remove(self.lista_view.selection()[0])
            
    def actualizar_lista(self):
        for item in self.lista_view.get_children():
            self.lista_view.delete(item)

        for contacto in self.contactos:
            self.lista_view.insert('', tk.END, values=(
                f"{contacto['nombre']} {contacto['apellido']}", 
                contacto["telefono"], 
                contacto["correo"],
                contacto["fecha_nacimiento"]
            ))
            
    def cargar_contacto_seleccionado(self, event):
        if not self.lista_view.selection():
            return
            
        selected_item = self.lista_view.selection()[0]
        try:
            fila_indice = self.lista_view.get_children().index(selected_item)
            self._contacto_seleccionado_index = fila_indice
            contacto_datos = self.contactos[fila_indice]

            self.limpiar_campos() 

            for key, control in self.controles.items():
                valor = contacto_datos.get(key)
                if valor is not None:
                    if isinstance(control, (tk.Entry, ttk.Entry)):
                        control.insert(0, valor)
                    elif isinstance(control, DateEntry):
                        try:
                            date_obj = datetime.strptime(valor, '%d/%m/%Y').date()
                            control.set_date(date_obj)
                        except:
                            pass 
            
            self.btn_agregar.grid_remove()
            self.btn_guardar_edicion.grid()
            
        except (IndexError, ValueError):
            self._contacto_seleccionado_index = -1

    def guardar_edicion(self):
        if self._contacto_seleccionado_index == -1:
            messagebox.showwarning("Edición", "Primero debe seleccionar un contacto para editar.")
            return

        datos_modificados = {key: control.get() for key, control in self.controles.items()}

        try:
            contacto_final = self._validar_datos(datos_modificados)
            self.contactos[self._contacto_seleccionado_index] = contacto_final 
            self.actualizar_lista()
            self.limpiar_campos(limpiar_seleccion=True)
            messagebox.showinfo("Éxito", "Contacto editado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error de Datos", str(e))

    def eliminar_contacto(self):
        seleccion = self.lista_view.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar", "Seleccione un contacto para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar el contacto?"):
            selected_item = seleccion[0]
            try:
                fila_indice = self.lista_view.get_children().index(selected_item)
                del self.contactos[fila_indice] 
                
                if self._contacto_seleccionado_index == fila_indice:
                    self.limpiar_campos(limpiar_seleccion=True)
                    
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Contacto eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

    def guardar_contactos_binario(self):
        if not self.contactos:
            messagebox.showwarning("Guardar", "No hay contactos para guardar.")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".dat",
            filetypes=[("Archivo Binario de Agenda", "*.dat")],
            initialfile=ARCHIVO_BINARIO 
        )
        if not ruta:
            return

        try:
            with open(ruta, 'wb') as archivo:
                pickle.dump(self.contactos, archivo) 
            messagebox.showinfo("Guardado", f"Contactos guardados exitosamente en formato binario:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {str(e)}")

    def cargar_contactos_binario(self, silent_load=False):
        
        ruta = ""
        
        if silent_load:
            ruta = ARCHIVO_BINARIO
            if not os.path.exists(ruta): 
                return 
        else:
            if not messagebox.askyesno("Cargar Contactos", "¿Desea reemplazar la agenda actual cargando un archivo?"):
                return

            ruta = filedialog.askopenfilename(
                defaultextension=".dat",
                filetypes=[("Archivo Binario de Agenda", "*.dat")],
                initialfile=ARCHIVO_BINARIO
            )
            if not ruta:
                return 

        try:
            with open(ruta, 'rb') as archivo:
                datos_cargados = pickle.load(archivo)
                
                if isinstance(datos_cargados, list):
                    self.contactos = datos_cargados
                    self.actualizar_lista()
                    self.limpiar_campos(limpiar_seleccion=True)
                    if not silent_load:
                        messagebox.showinfo("Cargado", f"{len(self.contactos)} contactos cargados exitosamente.")
                else:
                    messagebox.showerror("Error", "El archivo no contiene un formato de lista válido.")

        except FileNotFoundError:
            if not silent_load:
                messagebox.showwarning("Error", "No se encontró el archivo binario especificado.")
        except Exception as e:
            if not silent_load:
                messagebox.showerror("Error", f"Ocurrió un error al cargar el archivo: {str(e)}")
            self.contactos = []

    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = AgendaApp()
    app.ejecutar()
