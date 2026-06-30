import tkinter as tk
from tkinter import ttk, filedialog
import database
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- DIÁLOGOS RETRO ESTILO WINDOWS XP ---
class RetroDialog(tk.Toplevel):
    def __init__(self, parent, title, message, is_question=False, is_input=False, input_default="", height=350):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"650x{height}")
        self.config(bg="#ece9d8") # XP default greyish color
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        
        lbl = tk.Label(self, text=message, font=("Arial", 16), bg="#ece9d8", fg="black", wraplength=600, justify=tk.CENTER)
        lbl.pack(pady=30, padx=20, fill=tk.BOTH, expand=True)
        
        self.entry = None
        if is_input:
            self.entry = tk.Entry(self, font=("Arial", 20), width=30)
            self.entry.insert(0, input_default)
            self.entry.pack(pady=10)
            self.entry.focus()
            self.entry.bind("<Return>", lambda e: self.on_ok())
        
        btn_frame = tk.Frame(self, bg="#ece9d8")
        btn_frame.pack(pady=20)
        
        btn_style = {"font": ("Arial", 14, "bold"), "bg": "#d4d0c8", "relief": tk.RAISED, "bd": 3, "width": 12, "pady": 5}
        
        if is_question:
            btn_yes = tk.Button(btn_frame, text="Sí", command=self.on_yes, **btn_style)
            btn_yes.pack(side=tk.LEFT, padx=15)
            btn_no = tk.Button(btn_frame, text="No", command=self.on_no, **btn_style)
            btn_no.pack(side=tk.LEFT, padx=15)
        elif is_input:
            btn_ok = tk.Button(btn_frame, text="Aceptar", command=self.on_ok, **btn_style)
            btn_ok.pack(side=tk.LEFT, padx=15)
            btn_cancel = tk.Button(btn_frame, text="Cancelar", command=self.on_cancel, **btn_style)
            btn_cancel.pack(side=tk.LEFT, padx=15)
        else:
            btn_ok = tk.Button(btn_frame, text="Aceptar", command=self.on_ok, **btn_style)
            btn_ok.pack()

        self.update_idletasks()
        if parent:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
            y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
            self.geometry(f"+{x}+{y}")

        self.wait_window()

    def on_ok(self):
        if self.entry:
            self.result = self.entry.get()
        else:
            self.result = True
        self.destroy()
        
    def on_cancel(self):
        self.result = None
        self.destroy()
        
    def on_yes(self):
        self.result = True
        self.destroy()
        
    def on_no(self):
        self.result = False
        self.destroy()

def retro_showinfo(title, message, parent=None):
    RetroDialog(parent, title, message)

def retro_showerror(title, message, parent=None):
    RetroDialog(parent, title, message)

def retro_showwarning(title, message, parent=None):
    RetroDialog(parent, title, message)

def retro_askyesno(title, message, parent=None, height=350):
    d = RetroDialog(parent, title, message, is_question=True, height=height)
    return d.result

def retro_askstring(title, message, parent=None, default="", height=350):
    d = RetroDialog(parent, title, message, is_input=True, input_default=default, height=height)
    return d.result

class RetroProductEdit(tk.Toplevel):
    def __init__(self, parent, prod_data):
        super().__init__(parent)
        self.title("Editar Producto")
        self.geometry("550x450")
        self.config(bg="#ece9d8")
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        
        tk.Label(self, text="Modificar Datos", font=("Arial", 18, "bold"), bg="#ece9d8").pack(pady=20)
        
        frame = tk.Frame(self, bg="#ece9d8")
        frame.pack(pady=10)
        
        font_lbl = ("Arial", 16)
        font_ent = ("Arial", 16)
        
        tk.Label(frame, text="Código:", font=font_lbl, bg="#ece9d8").grid(row=0, column=0, sticky=tk.E, pady=10, padx=5)
        self.e_cod = tk.Entry(frame, font=font_ent)
        self.e_cod.insert(0, prod_data[1])
        self.e_cod.grid(row=0, column=1, pady=10)
        
        tk.Label(frame, text="Nombre:", font=font_lbl, bg="#ece9d8").grid(row=1, column=0, sticky=tk.E, pady=10, padx=5)
        self.e_nom = tk.Entry(frame, font=font_ent, width=25)
        self.e_nom.insert(0, prod_data[2])
        self.e_nom.grid(row=1, column=1, pady=10)
        
        tk.Label(frame, text="Precio:", font=font_lbl, bg="#ece9d8").grid(row=2, column=0, sticky=tk.E, pady=10, padx=5)
        self.e_pre = tk.Entry(frame, font=font_ent)
        self.e_pre.insert(0, str(prod_data[3]))
        self.e_pre.grid(row=2, column=1, pady=10)
        
        tk.Label(frame, text="Stock:", font=font_lbl, bg="#ece9d8").grid(row=3, column=0, sticky=tk.E, pady=10, padx=5)
        self.e_stk = tk.Entry(frame, font=font_ent)
        self.e_stk.insert(0, str(prod_data[4]))
        self.e_stk.grid(row=3, column=1, pady=10)
        
        btn_frame = tk.Frame(self, bg="#ece9d8")
        btn_frame.pack(pady=30)
        
        btn_style = {"font": ("Arial", 14, "bold"), "bg": "#d4d0c8", "relief": tk.RAISED, "bd": 3, "pady": 5}
        tk.Button(btn_frame, text="Guardar Cambios", command=self.on_ok, **btn_style).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text="Cancelar", command=self.on_cancel, **btn_style).pack(side=tk.LEFT, padx=15)
        
        self.update_idletasks()
        if parent:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
            y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
            self.geometry(f"+{x}+{y}")

        self.wait_window()
        
    def on_ok(self):
        self.result = {
            'codigo': self.e_cod.get().strip(),
            'nombre': self.e_nom.get().strip(),
            'precio': self.e_pre.get().strip(),
            'stock': self.e_stk.get().strip()
        }
        self.destroy()
        
    def on_cancel(self):
        self.destroy()

# --- APLICACIÓN PRINCIPAL ---
class POSApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Ventas")
        self.root.state('zoomed')
        self.root.minsize(800, 600) 
        
        try:
            self.root.iconbitmap('caja.ico')
        except Exception:
            pass
        
        style = ttk.Style()
        if 'winnative' in style.theme_names():
            style.theme_use('winnative')
        elif 'classic' in style.theme_names():
            style.theme_use('classic')

        style.configure("Treeview", font=('Arial', 14), rowheight=35)
        style.configure("Treeview.Heading", font=('Arial', 15, 'bold'))

        database.init_db()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_caja = ttk.Frame(self.notebook)
        self.tab_pos = ttk.Frame(self.notebook)
        self.tab_historial = ttk.Frame(self.notebook)
        self.tab_inventario = ttk.Frame(self.notebook)
        self.tab_compras = ttk.Frame(self.notebook) # NUEVA PESTAÑA COMPRAS
        self.tab_analitica = ttk.Frame(self.notebook) 

        style.configure("TNotebook.Tab", font=('Arial', 14, 'bold'), padding=[10, 5])

        self.notebook.add(self.tab_caja, text="Control de Caja")
        self.notebook.add(self.tab_pos, text="Registradora")
        self.notebook.add(self.tab_historial, text="Historial del Turno")
        self.notebook.add(self.tab_inventario, text="Inventario")
        self.notebook.add(self.tab_compras, text="Compras a Proveedores")
        self.notebook.add(self.tab_analitica, text="Inteligencia de Negocio")

        self.ticket = [] 
        self.carrito_compras = [] # NUEVO CARRITO PARA COMPRAS
        self.total_actual = 0.0
        self.total_compra_actual = 0.0
        self.producto_seleccionado_codigo = None

        self.setup_caja_tab()
        self.setup_pos_tab()
        self.setup_historial_tab()
        self.setup_inventario_tab()
        self.setup_compras_tab()
        self.setup_analitica_tab()

    # --- PANTALLA DE CAJA ---
    def setup_caja_tab(self):
        frame_info = tk.Frame(self.tab_caja, bd=2, relief=tk.SUNKEN)
        frame_info.pack(fill=tk.X, padx=10, pady=10)
        
        self.lbl_estado_caja = tk.Label(frame_info, text="Estado Actual: Desconocido", font=("Arial", 20, "bold"))
        self.lbl_estado_caja.pack(pady=20)

        frame_acciones = tk.Frame(self.tab_caja)
        frame_acciones.pack(pady=20)

        btn_apertura = tk.Button(frame_acciones, text="APERTURA DE CAJA", font=("Arial", 16, "bold"), bg="lightgreen", width=25, height=3, command=self.abrir_caja)
        btn_apertura.grid(row=0, column=0, padx=20)

        btn_cierre = tk.Button(frame_acciones, text="CIERRE DE CAJA\n(Genera Reporte Excel)", font=("Arial", 16, "bold"), bg="salmon", width=25, height=3, command=self.cerrar_caja)
        btn_cierre.grid(row=0, column=1, padx=20)

        self.actualizar_estado_caja()

    def actualizar_estado_caja(self):
        op = database.obtener_ultima_operacion_caja()
        if not op:
            self.lbl_estado_caja.config(text="Estado: Caja Cerrada (Nunca Abierta)", fg="red")
        else:
            tipo, fecha = op
            if tipo == 'Apertura':
                conn = database.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT monto_declarado, fecha_hora FROM caja_operaciones WHERE tipo = 'Apertura' ORDER BY id DESC LIMIT 1")
                apertura = cursor.fetchone()
                conn.close()
                monto_inicial = apertura[0] if apertura else 0.0
                fecha_desde = apertura[1] if apertura else "1970-01-01"
                totales = database.get_totales_por_metodo(fecha_desde)
                efectivo_actual = monto_inicial + totales['Efectivo_Neto']
                
                texto = f"CAJA ABIERTA\nFondo Físico Actual: ${efectivo_actual:.2f}"
                self.lbl_estado_caja.config(text=texto, fg="green")
            else:
                self.lbl_estado_caja.config(text=f"Estado: CAJA CERRADA (Último cierre: {fecha})", fg="red")

    def abrir_caja(self):
        op = database.obtener_ultima_operacion_caja()
        if op and op[0] == 'Apertura':
            retro_showwarning("Atención", "La caja ya está abierta.", self.root)
            return

        monto_str = retro_askstring("Apertura de Caja", "¿Cuánto efectivo hay inicialmente en la caja?", self.root)
        if not monto_str: return
        try:
            monto = float(monto_str)
            database.registrar_apertura_caja(monto)
            retro_showinfo("Éxito", f"Caja abierta con ${monto:.2f} iniciales.", self.root)
            self.actualizar_estado_caja()
            self.cargar_historial()
            self.cargar_historial_pos()
            self.actualizar_dashboard()
        except ValueError:
            retro_showerror("Error", "Monto inválido.", self.root)

    def cerrar_caja(self):
        op = database.obtener_ultima_operacion_caja()
        if not op or op[0] == 'Cierre':
            retro_showwarning("Atención", "La caja ya está cerrada.", self.root)
            return

        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT monto_declarado, fecha_hora FROM caja_operaciones WHERE tipo = 'Apertura' ORDER BY id DESC LIMIT 1")
        apertura = cursor.fetchone()
        conn.close()
        
        monto_inicial = apertura[0] if apertura else 0.0
        fecha_desde = apertura[1] if apertura else "1970-01-01"
        
        totales = database.get_totales_por_metodo(fecha_desde)
        efectivo_esperado = monto_inicial + totales['Efectivo_Neto']
        gran_total_ventas = totales['Efectivo'] + totales['Transferencia'] + totales['Crédito']
        
        resumen_msg = (
            f"--- RESUMEN DEL TURNO ---\n"
            f"Monto Inicial (Apertura): ${monto_inicial:.2f}\n"
            f"Ventas en Efectivo: ${totales['Efectivo']:.2f}\n"
            f"Ventas con Transferencia: ${totales['Transferencia']:.2f}\n"
            f"Ventas con Crédito: ${totales['Crédito']:.2f}\n"
            f"Compras Pagadas en Efectivo (Egresos): -${totales['Egresos_Efectivo']:.2f}\n"
            f"-------------------------\n"
            f"TOTAL VENTAS: ${gran_total_ventas:.2f}\n\n"
            f"► EFECTIVO ESPERADO EN CAJA: ${efectivo_esperado:.2f} ◄\n\n"
            f"Cuenta el dinero físico en la caja. ¿Cuánto efectivo hay?"
        )

        monto_str = retro_askstring("Cierre de Caja", resumen_msg, self.root, height=550)
        if not monto_str: return
        try:
            declarado = float(monto_str)
            diferencia = declarado - efectivo_esperado
            
            msg_final = f"Efectivo Esperado: ${efectivo_esperado:.2f}\n"
            msg_final += f"Efectivo Contado (Físico): ${declarado:.2f}\n\n"
            if diferencia == 0:
                msg_final += "¡LA CAJA CUADRA PERFECTAMENTE!"
            elif diferencia > 0:
                msg_final += f"Sobra: ${diferencia:.2f} (Hay más dinero del esperado)"
            else:
                msg_final += f"Falta: ${abs(diferencia):.2f} (Falta dinero)"
            
            if retro_askyesno("Confirmar Cierre", msg_final + "\n\n¿Registrar el cierre y generar Excel?", self.root):
                database.registrar_cierre_caja(efectivo_esperado, declarado, diferencia)
                self.actualizar_estado_caja()
                self.exportar_excel_cierre(fecha_desde, monto_inicial, gran_total_ventas, declarado, diferencia)
                self.cargar_historial()
                self.cargar_historial_pos()
                
        except ValueError:
            retro_showerror("Error", "Monto inválido.", self.root)

    def exportar_excel_cierre(self, fecha_desde, monto_inicial, gran_total_ventas, declarado, diferencia):
        conn = database.get_connection()
        
        # 1. Ventas
        query_ventas = '''
            SELECT v.id as VentaID, v.fecha_hora as Hora, p.codigo as Codigo, p.nombre as Producto, 
                   dv.cantidad as Cantidad, dv.precio_unitario as Precio, 
                   (dv.cantidad * dv.precio_unitario) as Total, v.metodo_pago as Metodo_Pago
            FROM ventas v
            JOIN detalle_ventas dv ON v.id = dv.id_venta
            JOIN productos p ON p.id = dv.id_producto
            WHERE v.fecha_hora >= ?
        '''
        df_ventas = pd.read_sql_query(query_ventas, conn, params=(fecha_desde,))
        
        # Agregamos una fila al final con el Total
        if not df_ventas.empty:
            total_row = pd.DataFrame([{
                'VentaID': '', 'Hora': '', 'Codigo': '', 'Producto': 'TOTAL DEL TURNO', 
                'Cantidad': '', 'Precio': '', 'Total': gran_total_ventas, 'Metodo_Pago': ''
            }])
            df_ventas = pd.concat([df_ventas, total_row], ignore_index=True)

        # 2. Stock
        query_stock = 'SELECT codigo as Codigo, nombre as Nombre, precio as Precio, stock as Stock FROM productos'
        df_stock = pd.read_sql_query(query_stock, conn)

        # 3. LIBRO DIARIO (Partida Doble)
        # Recuperamos Apertura, Ventas, Compras y Cierre del turno para armar los asientos
        asientos = []
        
        # a) Apertura
        asientos.append({'Asiento': '1', 'Fecha': fecha_desde, 'Cuenta': 'CAJA', 'Debe': monto_inicial, 'Haber': 0})
        asientos.append({'Asiento': '1', 'Fecha': fecha_desde, 'Cuenta': 'CAPITAL SOCIAL', 'Debe': 0, 'Haber': monto_inicial})
        
        # b) Ventas
        query_totales = "SELECT metodo_pago, SUM(total) FROM ventas WHERE fecha_hora >= ? GROUP BY metodo_pago"
        cursor = conn.cursor()
        cursor.execute(query_totales, (fecha_desde,))
        ventas_tot = cursor.fetchall()
        asiento_nro = 2
        
        for metodo, total_v in ventas_tot:
            cuenta_debe = 'CAJA'
            if metodo == 'Transferencia': cuenta_debe = 'BANCO'
            elif metodo == 'Crédito': cuenta_debe = 'DEUDORES POR VENTAS'
            
            asientos.append({'Asiento': str(asiento_nro), 'Fecha': 'Resumen Turno', 'Cuenta': cuenta_debe, 'Debe': total_v, 'Haber': 0})
            asientos.append({'Asiento': str(asiento_nro), 'Fecha': 'Resumen Turno', 'Cuenta': 'VENTAS (Ingreso)', 'Debe': 0, 'Haber': total_v})
            asiento_nro += 1

        # c) Compras
        query_compras = "SELECT metodo_pago, SUM(total) FROM compras WHERE fecha_hora >= ? GROUP BY metodo_pago"
        cursor.execute(query_compras, (fecha_desde,))
        compras_tot = cursor.fetchall()
        for metodo, total_c in compras_tot:
            cuenta_haber = 'CAJA' if metodo == 'Efectivo' else ('BANCO' if metodo == 'Transferencia' else 'PROVEEDORES')
            asientos.append({'Asiento': str(asiento_nro), 'Fecha': 'Resumen Turno', 'Cuenta': 'MERCADERIAS (Activo)', 'Debe': total_c, 'Haber': 0})
            asientos.append({'Asiento': str(asiento_nro), 'Fecha': 'Resumen Turno', 'Cuenta': cuenta_haber, 'Debe': 0, 'Haber': total_c})
            asiento_nro += 1

        # d) Cierre y Sobrante/Faltante
        if diferencia != 0:
            if diferencia > 0: # Sobrante
                asientos.append({'Asiento': str(asiento_nro), 'Fecha': 'Cierre', 'Cuenta': 'CAJA', 'Debe': diferencia, 'Haber': 0})
                asientos.append({'Asiento': str(asiento_nro), 'Fecha': 'Cierre', 'Cuenta': 'SOBRANTE DE CAJA (Ingreso)', 'Debe': 0, 'Haber': diferencia})
            else: # Faltante
                asientos.append({'Asiento': str(asiento_nro), 'Fecha': 'Cierre', 'Cuenta': 'FALTANTE DE CAJA (Egreso)', 'Debe': abs(diferencia), 'Haber': 0})
                asientos.append({'Asiento': str(asiento_nro), 'Fecha': 'Cierre', 'Cuenta': 'CAJA', 'Debe': 0, 'Haber': abs(diferencia)})

        df_diario = pd.DataFrame(asientos)
        
        # Calcular Sumas Iguales
        if not df_diario.empty:
            total_debe = df_diario['Debe'].sum()
            total_haber = df_diario['Haber'].sum()
            df_diario = pd.concat([df_diario, pd.DataFrame([{'Asiento':'', 'Fecha':'', 'Cuenta':'SUMAS IGUALES', 'Debe': total_debe, 'Haber': total_haber}])], ignore_index=True)

        conn.close()

        fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        carpeta_reportes = "Reportes"
        if not os.path.exists(carpeta_reportes):
            os.makedirs(carpeta_reportes)
            
        filename = os.path.join(carpeta_reportes, f"Cierre_Caja_{fecha_str}.xlsx")
        
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df_ventas.to_excel(writer, sheet_name='Ventas_del_Turno', index=False)
                df_stock.to_excel(writer, sheet_name='Stock_Actual', index=False)
                df_diario.to_excel(writer, sheet_name='Libro_Diario_Turno', index=False)
            
            filepath = os.path.abspath(filename)
            retro_showinfo("Cierre Exitoso", f"Caja cerrada.\nReporte y Libro Diario generados en:\n{filepath}", self.root)
        except Exception as e:
            retro_showerror("Error de Exportación", f"No se pudo crear el Excel:\n{e}", self.root)

    # --- PANTALLA REGISTRADORA ---
    def setup_pos_tab(self):
        frame_left = tk.Frame(self.tab_pos, width=650)
        frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        frame_right = tk.Frame(self.tab_pos, width=450, bd=2, relief=tk.SUNKEN)
        frame_right.pack(side=tk.RIGHT, fill=tk.Y, expand=False, padx=5, pady=5)

        tk.Label(frame_right, text="1. Buscar Producto", font=("Arial", 15, "bold"), bg="lightgray").pack(fill=tk.X, pady=5)
        
        self.entry_buscador = tk.Entry(frame_right, font=("Arial", 16))
        self.entry_buscador.pack(fill=tk.X, padx=10, pady=5)
        self.entry_buscador.bind('<KeyRelease>', self.filtrar_productos_buscador)
        self.entry_buscador.bind('<Return>', lambda e: self.agregar_desde_buscador_enter())

        cols_busqueda = ("codigo", "nombre", "precio")
        self.tree_busqueda = ttk.Treeview(frame_right, columns=cols_busqueda, show="headings", height=10)
        self.tree_busqueda.heading("codigo", text="Cód")
        self.tree_busqueda.heading("nombre", text="Descripción")
        self.tree_busqueda.heading("precio", text="Precio")
        self.tree_busqueda.column("codigo", width=60)
        self.tree_busqueda.column("nombre", width=250)
        self.tree_busqueda.column("precio", width=100, anchor=tk.E)
        self.tree_busqueda.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tree_busqueda.bind("<<TreeviewSelect>>", self.on_producto_seleccionado)

        frame_form_add = tk.Frame(frame_right, bd=2, relief=tk.GROOVE)
        frame_form_add.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_form_add, text="2. Ingresar Cantidad y presionar [ENTER]", font=("Arial", 13, "bold"), fg="darkgreen").pack(pady=5)
        
        self.lbl_prod_seleccionado = tk.Label(frame_form_add, text="Ningún producto seleccionado", fg="blue", wraplength=450, font=("Arial", 14))
        self.lbl_prod_seleccionado.pack(pady=5)
        
        frame_cant = tk.Frame(frame_form_add)
        frame_cant.pack(pady=10)
        tk.Label(frame_cant, text="Cantidad:", font=("Arial", 16)).pack(side=tk.LEFT)
        self.entry_cantidad_venta = tk.Entry(frame_cant, width=10, font=("Arial", 18))
        self.entry_cantidad_venta.insert(0, "1")
        self.entry_cantidad_venta.pack(side=tk.LEFT, padx=10)
        
        self.entry_cantidad_venta.bind('<Return>', lambda e: self.agregar_desde_form())

        self.cargar_lista_busqueda()

        # Zona Ticket Arriba
        frame_ticket = tk.Frame(frame_left)
        frame_ticket.pack(fill=tk.BOTH, expand=True, pady=2)
        
        frame_titulo_ticket = tk.Frame(frame_ticket)
        frame_titulo_ticket.pack(fill=tk.X)
        tk.Label(frame_titulo_ticket, text="TICKET ACTUAL", font=("Arial", 16, "bold")).pack(side=tk.LEFT, pady=2)
        btn_vaciar = tk.Button(frame_titulo_ticket, text="Vaciar Ticket", command=self.vaciar_ticket, bg="#ffcccc", font=("Arial", 14, "bold"), padx=10, pady=2)
        btn_vaciar.pack(side=tk.RIGHT, padx=5)

        cols_ticket = ("codigo", "nombre", "cantidad", "precio_u", "subtotal")
        self.tree_ticket = ttk.Treeview(frame_ticket, columns=cols_ticket, show="headings", height=6)
        self.tree_ticket.heading("codigo", text="Código")
        self.tree_ticket.heading("nombre", text="Descripción")
        self.tree_ticket.heading("cantidad", text="Cant.")
        self.tree_ticket.heading("precio_u", text="Precio U.")
        self.tree_ticket.heading("subtotal", text="Subtotal")
        self.tree_ticket.column("codigo", width=80)
        self.tree_ticket.column("nombre", width=250)
        self.tree_ticket.column("cantidad", width=60, anchor=tk.CENTER)
        self.tree_ticket.column("precio_u", width=90, anchor=tk.E)
        self.tree_ticket.column("subtotal", width=90, anchor=tk.E)
        self.tree_ticket.pack(fill=tk.BOTH, expand=True)

        # Zona Checkout Medio
        frame_checkout = tk.Frame(frame_left, bd=2, relief=tk.GROOVE)
        frame_checkout.pack(fill=tk.X, pady=5)

        self.lbl_total_ticket = tk.Label(frame_checkout, text="TOTAL: $0.00", font=("Arial", 32, "bold"), fg="#003366")
        self.lbl_total_ticket.pack(side=tk.LEFT, padx=10, pady=5)

        frame_botones_pago = tk.Frame(frame_checkout)
        frame_botones_pago.pack(side=tk.RIGHT, padx=5, pady=5)

        btn_efectivo = tk.Button(frame_botones_pago, text="Cobrar EFECTIVO", font=("Arial", 10, "bold"), bg="#99ff99", width=16, height=2, command=lambda: self.checkout("Efectivo"))
        btn_efectivo.grid(row=0, column=0, padx=2)
        btn_transf = tk.Button(frame_botones_pago, text="Cobrar TRANSFER", font=("Arial", 10, "bold"), bg="#99ccff", width=16, height=2, command=lambda: self.checkout("Transferencia"))
        btn_transf.grid(row=0, column=1, padx=2)
        btn_credito = tk.Button(frame_botones_pago, text="Cobrar CRÉDITO", font=("Arial", 10, "bold"), bg="#ffff99", width=16, height=2, command=lambda: self.checkout("Crédito"))
        btn_credito.grid(row=0, column=2, padx=2)

        # Visor del comprobante generado
        self.text_comprobante = tk.Text(frame_left, height=8, font=("Courier", 10), state=tk.DISABLED, bg="#ffffcc", fg="black")
        self.text_comprobante.pack(fill=tk.X, pady=5)
        self.text_comprobante.insert(tk.END, "VISOR DE TICKET...\nAquí aparecerá el comprobante de la última venta.")
        self.text_comprobante.config(state=tk.DISABLED)

        # Zona Historial Abajo (Ventas Realizadas Hoy)
        frame_hist_pos = tk.Frame(frame_left)
        frame_hist_pos.pack(fill=tk.BOTH, expand=True, pady=2)
        
        tk.Label(frame_hist_pos, text="ÚLTIMAS VENTAS REALIZADAS (Turno Actual)", font=("Arial", 12, "bold"), fg="gray").pack()
        
        cols_hist_pos = ("hora", "producto", "cantidad", "total", "metodo")
        self.tree_pos_hist = ttk.Treeview(frame_hist_pos, columns=cols_hist_pos, show="headings", height=5)
        self.tree_pos_hist.heading("hora", text="Hora")
        self.tree_pos_hist.heading("producto", text="Producto")
        self.tree_pos_hist.heading("cantidad", text="Cant.")
        self.tree_pos_hist.heading("total", text="Total Venta")
        self.tree_pos_hist.heading("metodo", text="Pago")
        self.tree_pos_hist.column("hora", width=80, anchor=tk.CENTER)
        self.tree_pos_hist.column("producto", width=250)
        self.tree_pos_hist.column("cantidad", width=60, anchor=tk.CENTER)
        self.tree_pos_hist.column("total", width=90, anchor=tk.E)
        self.tree_pos_hist.column("metodo", width=100, anchor=tk.CENTER)
        self.tree_pos_hist.pack(fill=tk.BOTH, expand=True)

        self.cargar_historial_pos()

    def cargar_historial_pos(self):
        for item in self.tree_pos_hist.get_children():
            self.tree_pos_hist.delete(item)
            
        op = database.obtener_ultima_operacion_caja()
        if not op or op[0] != 'Apertura':
            return # Caja cerrada, no mostrar ventas del turno actual.

        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT fecha_hora FROM caja_operaciones WHERE tipo = 'Apertura' ORDER BY id DESC LIMIT 1")
        apertura = cursor.fetchone()
        fecha_desde = apertura[0] if apertura else "1970-01-01"

        query = '''
            SELECT v.fecha_hora, p.nombre, dv.cantidad, (dv.cantidad * dv.precio_unitario), v.metodo_pago
            FROM ventas v
            JOIN detalle_ventas dv ON v.id = dv.id_venta
            JOIN productos p ON p.id = dv.id_producto
            WHERE v.fecha_hora >= ?
            ORDER BY v.id DESC LIMIT 50
        '''
        cursor.execute(query, (fecha_desde,))
        for row in cursor.fetchall():
            hora_completa = row[0]
            hora_corta = hora_completa.split(" ")[1] if " " in hora_completa else hora_completa
            formatted_row = (hora_corta, row[1], row[2], f"${row[3]:.2f}", row[4])
            self.tree_pos_hist.insert("", tk.END, values=formatted_row)
        conn.close()

    def cargar_lista_busqueda(self, filtro=""):
        for item in self.tree_busqueda.get_children():
            self.tree_busqueda.delete(item)
        
        productos = database.get_productos()
        for prod in productos:
            cod = str(prod[1]).lower()
            nom = str(prod[2]).lower()
            f = filtro.lower()
            if f in cod or f in nom:
                self.tree_busqueda.insert("", tk.END, values=(prod[1], prod[2], f"${prod[3]:.2f}"), iid=prod[1])

    def filtrar_productos_buscador(self, event):
        filtro = self.entry_buscador.get()
        self.cargar_lista_busqueda(filtro)

    def agregar_desde_buscador_enter(self):
        codigo = self.entry_buscador.get().strip()
        if not codigo: return
        
        producto = database.search_producto_por_codigo(codigo)
        if producto:
            self.producto_seleccionado_codigo = codigo
            self.lbl_prod_seleccionado.config(text=f"Seleccionado: {producto[2]}")
            self.entry_cantidad_venta.focus()
            self.entry_cantidad_venta.selection_range(0, tk.END)

    def on_producto_seleccionado(self, event):
        selected = self.tree_busqueda.selection()
        if not selected: return
        self.producto_seleccionado_codigo = selected[0]
        item = self.tree_busqueda.item(selected[0])
        nombre_prod = item['values'][1]
        self.lbl_prod_seleccionado.config(text=f"Seleccionado: {nombre_prod}")
        self.entry_cantidad_venta.focus()
        self.entry_cantidad_venta.selection_range(0, tk.END)

    def agregar_desde_form(self):
        if not self.producto_seleccionado_codigo:
            retro_showwarning("Atención", "Primero elige un producto de la lista.", self.root)
            return

        producto = database.search_producto_por_codigo(self.producto_seleccionado_codigo)
        if not producto: return

        prod_id, cod, nombre, precio, stock = producto
        cant_str = self.entry_cantidad_venta.get().strip()
        
        try:
            cant = int(cant_str)
            if cant <= 0: return
            
            cant_actual_en_ticket = sum(item['cantidad'] for item in self.ticket if item['id_producto'] == prod_id)
            if cant + cant_actual_en_ticket > stock:
                retro_showwarning("Stock Insuficiente", f"Solo quedan {stock} unidades en stock de {nombre}.", self.root)
                return

            encontrado = False
            for item in self.ticket:
                if item['id_producto'] == prod_id:
                    item['cantidad'] += cant
                    encontrado = True
                    break
            
            if not encontrado:
                self.ticket.append({
                    'id_producto': prod_id,
                    'codigo': cod,
                    'nombre': nombre,
                    'cantidad': cant,
                    'precio_unitario': float(precio)
                })

            self.actualizar_ticket_ui()
            
            self.entry_buscador.focus()
            self.entry_buscador.delete(0, tk.END)
            self.cargar_lista_busqueda()
            self.lbl_prod_seleccionado.config(text="Ningún producto seleccionado")
            self.producto_seleccionado_codigo = None
            self.entry_cantidad_venta.delete(0, tk.END)
            self.entry_cantidad_venta.insert(0, "1")

        except ValueError:
            retro_showerror("Error", "Cantidad inválida. Debe ser un número entero.", self.root)

    def actualizar_ticket_ui(self):
        for item in self.tree_ticket.get_children():
            self.tree_ticket.delete(item)
        
        total = 0.0
        for item in self.ticket:
            subtotal = item['cantidad'] * item['precio_unitario']
            total += subtotal
            self.tree_ticket.insert("", tk.END, values=(
                item['codigo'], item['nombre'], item['cantidad'], f"${item['precio_unitario']:.2f}", f"${subtotal:.2f}"
            ))
        self.lbl_total_ticket.config(text=f"TOTAL: ${total:.2f}")
        self.total_actual = total

    def vaciar_ticket(self):
        self.ticket = []
        self.actualizar_ticket_ui()

    def checkout(self, metodo_pago):
        if not self.ticket:
            retro_showinfo("Aviso", "No hay productos en la registradora.", self.root)
            return
        
        if metodo_pago == "Efectivo":
            op = database.obtener_ultima_operacion_caja()
            if not op or op[0] != 'Apertura':
                retro_showwarning("Caja Cerrada", "Debes ABRIR LA CAJA antes de cobrar en efectivo.", self.root)
                return

        if retro_askyesno("Confirmar", f"Total: ${self.total_actual:.2f}\nForma de pago: {metodo_pago}\n¿Completar venta?", self.root):
            success, id_venta, fecha_hora = database.registrar_venta(self.ticket, self.total_actual, metodo_pago)
            if success:
                self.imprimir_ticket_txt(id_venta, fecha_hora, metodo_pago)
                self.vaciar_ticket()
                self.cargar_inventario()
                self.cargar_lista_busqueda() 
                self.cargar_historial()
                self.cargar_historial_pos()
                self.actualizar_dashboard()
                self.cargar_productos_combobox() # Para la pestaña de compras
                self.actualizar_estado_caja()
            else:
                retro_showerror("Error", "Problema al registrar la venta.", self.root)

    def imprimir_ticket_txt(self, id_venta, fecha_hora, metodo_pago):
        carpeta = "Comprobantes"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        filename = os.path.join(carpeta, f"Ticket_{id_venta:04d}.txt")
        
        lines = []
        lines.append("="*40)
        lines.append("         REGISTRO DE VENTAS         ")
        lines.append("      (DOCUMENTO COMERCIAL)         ")
        lines.append("="*40)
        lines.append(f"TICKET NRO: {id_venta:04d}")
        lines.append(f"FECHA: {fecha_hora}")
        lines.append(f"METODO PAGO: {metodo_pago}")
        lines.append("-" * 40)
        lines.append(f"{'CANT':<5} | {'PRODUCTO':<20} | {'SUBT':<8}")
        lines.append("-" * 40)
        for item in self.ticket:
            subt = item['cantidad'] * item['precio_unitario']
            nom_corto = item['nombre'][:20]
            lines.append(f"{item['cantidad']:<5} | {nom_corto:<20} | ${subt:<7.2f}")
        lines.append("-" * 40)
        lines.append(f"TOTAL: ${self.total_actual:.2f}")
        lines.append("="*40)
        lines.append("       GRACIAS POR SU COMPRA        ")
        lines.append("="*40)
        
        contenido = "\n".join(lines)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(contenido)
            
        self.text_comprobante.config(state=tk.NORMAL)
        self.text_comprobante.delete(1.0, tk.END)
        self.text_comprobante.insert(tk.END, contenido)
        self.text_comprobante.config(state=tk.DISABLED)

    # --- PESTAÑA COMPRAS A PROVEEDORES ---
    def setup_compras_tab(self):
        f_top_compras = tk.Frame(self.tab_compras)
        f_top_compras.pack(fill=tk.X, padx=10, pady=2)
        
        frame_proveedor = tk.LabelFrame(f_top_compras, text="1. Gestión de Proveedores", font=("Arial", 14, "bold"))
        frame_proveedor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Formulario nuevo proveedor
        f_alta = tk.Frame(frame_proveedor)
        f_alta.pack(side=tk.LEFT, padx=10, pady=2)
        tk.Label(f_alta, text="Nuevo Proveedor:", font=("Arial", 12)).grid(row=0, column=0)
        self.entry_prov_nom = tk.Entry(f_alta, font=("Arial", 12))
        self.entry_prov_nom.grid(row=0, column=1, padx=5)
        tk.Label(f_alta, text="Teléfono:", font=("Arial", 12)).grid(row=1, column=0, pady=5)
        self.entry_prov_tel = tk.Entry(f_alta, font=("Arial", 12))
        self.entry_prov_tel.grid(row=1, column=1, padx=5)
        tk.Button(f_alta, text="Guardar Proveedor", command=self.agregar_proveedor, font=("Arial", 10, "bold"), bg="lightblue").grid(row=2, column=0, columnspan=2, pady=5)

        # Lista de proveedores
        self.tree_prov = ttk.Treeview(frame_proveedor, columns=("id", "nombre", "tel"), show="headings", height=3)
        self.tree_prov.heading("id", text="ID")
        self.tree_prov.heading("nombre", text="Nombre")
        self.tree_prov.heading("tel", text="Teléfono")
        self.tree_prov.column("id", width=50, anchor=tk.CENTER)
        self.tree_prov.column("nombre", width=150)
        self.tree_prov.column("tel", width=100)
        self.tree_prov.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=2)

        frame_historial_compras = tk.LabelFrame(f_top_compras, text="Historial de Compras", font=("Arial", 14, "bold"))
        frame_historial_compras.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.tree_hist_compras = ttk.Treeview(frame_historial_compras, columns=("fecha", "prov", "detalle", "total", "metodo"), show="headings", height=3)
        self.tree_hist_compras.heading("fecha", text="Fecha")
        self.tree_hist_compras.heading("prov", text="Proveedor")
        self.tree_hist_compras.heading("detalle", text="Productos Adquiridos")
        self.tree_hist_compras.heading("total", text="Total")
        self.tree_hist_compras.heading("metodo", text="Pago")
        self.tree_hist_compras.column("fecha", width=120)
        self.tree_hist_compras.column("prov", width=100)
        self.tree_hist_compras.column("detalle", width=250)
        self.tree_hist_compras.column("total", width=80)
        self.tree_hist_compras.column("metodo", width=100)
        self.tree_hist_compras.pack(fill=tk.BOTH, expand=True, padx=10, pady=2)

        frame_compra = tk.LabelFrame(self.tab_compras, text="2. Registrar Compra de Mercadería (Orden de Compra)", font=("Arial", 14, "bold"))
        frame_compra.pack(fill=tk.BOTH, expand=True, padx=10, pady=2)

        f_top_compra = tk.Frame(frame_compra)
        f_top_compra.pack(fill=tk.X, pady=2)

        font_l = ("Arial", 14)
        tk.Label(f_top_compra, text="Proveedor Principal:", font=font_l).pack(side=tk.LEFT, padx=10)
        self.cb_proveedores = ttk.Combobox(f_top_compra, font=font_l, state="readonly", width=30)
        self.cb_proveedores.pack(side=tk.LEFT, padx=10)

        f_mid_compra = tk.Frame(frame_compra)
        f_mid_compra.pack(fill=tk.BOTH, expand=True, pady=2)

        f_add_prod = tk.Frame(f_mid_compra, bd=1, relief=tk.RAISED)
        f_add_prod.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(f_add_prod, text="Agregar a la Orden", font=("Arial", 12, "bold")).pack(pady=5)
        
        tk.Label(f_add_prod, text="Producto:", font=font_l).pack(pady=5)
        self.cb_productos = ttk.Combobox(f_add_prod, font=font_l, state="readonly", width=25)
        self.cb_productos.pack(padx=10)

        tk.Label(f_add_prod, text="Cantidad ingresada:", font=font_l).pack(pady=5)
        self.entry_compra_cant = tk.Entry(f_add_prod, font=font_l, width=10)
        self.entry_compra_cant.pack()

        tk.Label(f_add_prod, text="Costo Total ($):", font=font_l).pack(pady=5)
        self.entry_compra_costo = tk.Entry(f_add_prod, font=font_l, width=15)
        self.entry_compra_costo.pack()

        tk.Button(f_add_prod, text="Añadir a la Orden", font=("Arial", 12, "bold"), bg="lightyellow", command=self.agregar_al_carrito_compras).pack(pady=15)

        f_carrito = tk.Frame(f_mid_compra)
        f_carrito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        cols_comp = ("producto", "cantidad", "subtotal")
        self.tree_compra = ttk.Treeview(f_carrito, columns=cols_comp, show="headings", height=3)
        self.tree_compra.heading("producto", text="Producto")
        self.tree_compra.heading("cantidad", text="Cant.")
        self.tree_compra.heading("subtotal", text="Costo Subtotal")
        self.tree_compra.column("producto", width=250)
        self.tree_compra.column("cantidad", width=80, anchor=tk.CENTER)
        self.tree_compra.column("subtotal", width=120, anchor=tk.E)
        self.tree_compra.pack(fill=tk.BOTH, expand=True)

        f_bot_compra = tk.Frame(frame_compra)
        f_bot_compra.pack(fill=tk.X, pady=2)

        self.lbl_total_compra = tk.Label(f_bot_compra, text="TOTAL ORDEN: $0.00", font=("Arial", 20, "bold"), fg="darkred")
        self.lbl_total_compra.pack(side=tk.LEFT, padx=20)

        tk.Label(f_bot_compra, text="Método de Pago:", font=font_l).pack(side=tk.LEFT, padx=10)
        self.cb_pago_compra = ttk.Combobox(f_bot_compra, font=font_l, values=["Efectivo", "Transferencia", "Cuenta Corriente (Crédito)"], state="readonly")
        self.cb_pago_compra.current(0)
        self.cb_pago_compra.pack(side=tk.LEFT)

        tk.Button(f_bot_compra, text="CERRAR COMPRA", font=("Arial", 14, "bold"), bg="#ffcc99", command=self.efectuar_compra).pack(side=tk.RIGHT, padx=20)

        self.cargar_proveedores()
        self.cargar_productos_combobox()
        self.cargar_historial_compras()

    def cargar_historial_compras(self):
        for item in self.tree_hist_compras.get_children(): self.tree_hist_compras.delete(item)
        import database
        for row in database.get_historial_compras_db():
            self.tree_hist_compras.insert("", tk.END, values=(row[0], row[1], row[2], f"${row[3]:.2f}", row[4]))

    def cargar_proveedores(self):
        for item in self.tree_prov.get_children(): self.tree_prov.delete(item)
        provs = database.get_proveedores()
        nombres = []
        for p in provs:
            self.tree_prov.insert("", tk.END, values=(p[0], p[1], p[2]))
            nombres.append(f"{p[0]} - {p[1]}")
        self.cb_proveedores['values'] = nombres

    def cargar_productos_combobox(self):
        prods = database.get_productos()
        nombres = []
        for p in prods:
            nombres.append(f"{p[0]} - {p[1]} - {p[2]}")
        self.cb_productos['values'] = nombres

    def agregar_proveedor(self):
        nom = self.entry_prov_nom.get().strip()
        tel = self.entry_prov_tel.get().strip()
        if nom:
            success, msg = database.add_proveedor(nom, tel)
            if success:
                self.cargar_proveedores()
                self.entry_prov_nom.delete(0, tk.END)
                self.entry_prov_tel.delete(0, tk.END)
            else:
                retro_showerror("Error", msg, self.root)
        else:
            retro_showerror("Error", "Nombre es obligatorio", self.root)

    def agregar_al_carrito_compras(self):
        val_prod = self.cb_productos.get()
        cant_str = self.entry_compra_cant.get()
        costo_str = self.entry_compra_costo.get()
        
        if not val_prod:
            retro_showwarning("Atención", "Selecciona un producto.", self.root)
            return
            
        try:
            cant = int(cant_str)
            costo = float(costo_str)
            if cant <= 0 or costo < 0: raise ValueError
        except:
            retro_showerror("Error", "Cant y Costo deben ser números válidos.", self.root)
            return
            
        id_prod = int(val_prod.split(" - ")[0])
        nombre_prod = val_prod.split(" - ")[1]
        
        self.carrito_compras.append({
            'id_producto': id_prod,
            'nombre': nombre_prod,
            'cantidad': cant,
            'precio_costo': costo
        })
        
        self.actualizar_carrito_compras_ui()
        self.entry_compra_cant.delete(0, tk.END)
        self.entry_compra_costo.delete(0, tk.END)
        
    def actualizar_carrito_compras_ui(self):
        for item in self.tree_compra.get_children():
            self.tree_compra.delete(item)
            
        self.total_compra_actual = 0.0
        for item in self.carrito_compras:
            self.total_compra_actual += item['precio_costo']
            self.tree_compra.insert("", tk.END, values=(
                item['nombre'], item['cantidad'], f"${item['precio_costo']:.2f}"
            ))
            
        self.lbl_total_compra.config(text=f"TOTAL ORDEN: ${self.total_compra_actual:.2f}")

    def efectuar_compra(self):
        val_prov = self.cb_proveedores.get()
        metodo = self.cb_pago_compra.get()

        if not val_prov:
            retro_showwarning("Atención", "Selecciona un proveedor principal para la orden.", self.root)
            return
            
        if not self.carrito_compras:
            retro_showwarning("Atención", "La orden está vacía. Añade productos primero.", self.root)
            return

        id_prov = int(val_prov.split(" - ")[0])

        if metodo == "Efectivo":
            op = database.obtener_ultima_operacion_caja()
            if not op or op[0] != 'Apertura':
                retro_showwarning("Caja Cerrada", "Debes ABRIR LA CAJA antes de pagar a proveedores en efectivo.", self.root)
                return

        if retro_askyesno("Confirmar Compra", f"¿Registrar compra total por ${self.total_compra_actual:.2f} y pagar con {metodo}?", self.root):
            success, msg = database.registrar_compra(id_prov, self.carrito_compras, self.total_compra_actual, metodo)
            if success:
                import os
                from datetime import datetime
                fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nombre_prov = val_prov.split(" - ")[1] if " - " in val_prov else val_prov
                
                ticket_compra_str = f"=== ORDEN DE COMPRA ===\n"
                ticket_compra_str += f"Fecha: {fecha_str}\n"
                ticket_compra_str += f"Proveedor: {nombre_prov}\n"
                ticket_compra_str += f"Método de Pago: {metodo}\n"
                ticket_compra_str += "--------------------------\n"
                for item in self.carrito_compras:
                    ticket_compra_str += f"{item['nombre']} x{item['cantidad']} ... ${item['precio_costo']:.2f}\n"
                ticket_compra_str += "--------------------------\n"
                ticket_compra_str += f"TOTAL ORDEN: ${self.total_compra_actual:.2f}\n"
                ticket_compra_str += "==========================\n"
                
                os.makedirs("tickets", exist_ok=True)
                nombre_archivo = f"tickets/Ticket_Compra_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(nombre_archivo, "w", encoding="utf-8") as f:
                    f.write(ticket_compra_str)
                
                retro_showinfo("Éxito", "Compra registrada y Ticket Guardado.", self.root)
                self.carrito_compras = []
                self.actualizar_carrito_compras_ui()
                self.cargar_inventario()
                self.cargar_historial_compras()
                self.actualizar_estado_caja()
            else:
                retro_showerror("Error", msg, self.root)


    # --- PANTALLA HISTORIAL DEL TURNO ---
    def setup_historial_tab(self):
        frame_top = tk.Frame(self.tab_historial)
        frame_top.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(frame_top, text="Ventas del Turno Actual", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        btn_refresh = tk.Button(frame_top, text="Actualizar Vista", font=("Arial", 12), command=self.cargar_historial)
        btn_refresh.pack(side=tk.RIGHT)

        cols = ("id", "hora", "producto", "cantidad", "total", "metodo")
        self.tree_hist = ttk.Treeview(self.tab_historial, columns=cols, show="headings")
        self.tree_hist.heading("id", text="ID Venta")
        self.tree_hist.heading("hora", text="Hora")
        self.tree_hist.heading("producto", text="Producto")
        self.tree_hist.heading("cantidad", text="Cant.")
        self.tree_hist.heading("total", text="Total")
        self.tree_hist.heading("metodo", text="Pago")
        
        self.tree_hist.column("id", width=80, anchor=tk.CENTER)
        self.tree_hist.column("hora", width=180)
        self.tree_hist.column("producto", width=300)
        self.tree_hist.column("cantidad", width=80, anchor=tk.CENTER)
        self.tree_hist.column("total", width=120, anchor=tk.E)
        self.tree_hist.column("metodo", width=150, anchor=tk.CENTER)

        self.tree_hist.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.frame_totales_hist = tk.Frame(self.tab_historial, bd=2, relief=tk.SUNKEN)
        self.frame_totales_hist.pack(fill=tk.X, padx=5, pady=5)
        
        self.lbl_tot_efec = tk.Label(self.frame_totales_hist, text="Efectivo: $0", font=("Arial", 14, "bold"), fg="green")
        self.lbl_tot_efec.pack(side=tk.LEFT, padx=15, pady=5)
        
        self.lbl_tot_trans = tk.Label(self.frame_totales_hist, text="Transferencia: $0", font=("Arial", 14, "bold"), fg="blue")
        self.lbl_tot_trans.pack(side=tk.LEFT, padx=15, pady=5)
        
        self.lbl_tot_cred = tk.Label(self.frame_totales_hist, text="Crédito: $0", font=("Arial", 14, "bold"), fg="orange")
        self.lbl_tot_cred.pack(side=tk.LEFT, padx=15, pady=5)
        
        self.lbl_gran_total = tk.Label(self.frame_totales_hist, text="TOTAL GENERAL: $0", font=("Arial", 18, "bold"))
        self.lbl_gran_total.pack(side=tk.RIGHT, padx=20, pady=5)

        self.cargar_historial()

    def cargar_historial(self):
        for item in self.tree_hist.get_children():
            self.tree_hist.delete(item)
            
        op = database.obtener_ultima_operacion_caja()
        if not op or op[0] != 'Apertura':
            self.lbl_tot_efec.config(text="Efectivo: $0")
            self.lbl_tot_trans.config(text="Transferencia: $0")
            self.lbl_tot_cred.config(text="Crédito: $0")
            self.lbl_gran_total.config(text="TOTAL VENTAS: $0")
            return
            
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT fecha_hora FROM caja_operaciones WHERE tipo = 'Apertura' ORDER BY id DESC LIMIT 1")
        apertura = cursor.fetchone()
        fecha_desde = apertura[0] if apertura else "1970-01-01"

        query = '''
            SELECT v.id, v.fecha_hora, p.nombre, dv.cantidad, (dv.cantidad * dv.precio_unitario), v.metodo_pago
            FROM ventas v
            JOIN detalle_ventas dv ON v.id = dv.id_venta
            JOIN productos p ON p.id = dv.id_producto
            WHERE v.fecha_hora >= ?
            ORDER BY v.id DESC
        '''
        cursor.execute(query, (fecha_desde,))
        for row in cursor.fetchall():
            formatted_row = (row[0], row[1], row[2], row[3], f"${row[4]:.2f}", row[5])
            self.tree_hist.insert("", tk.END, values=formatted_row)
        conn.close()

        totales = database.get_totales_por_metodo(fecha_desde)
        self.lbl_tot_efec.config(text=f"Ventas Efectivo: ${totales.get('Efectivo', 0):.2f}")
        self.lbl_tot_trans.config(text=f"Transferencia: ${totales.get('Transferencia', 0):.2f}")
        self.lbl_tot_cred.config(text=f"Crédito: ${totales.get('Crédito', 0):.2f}")
        
        gran_total = totales['Efectivo'] + totales['Transferencia'] + totales['Crédito']
        self.lbl_gran_total.config(text=f"TOTAL VENTAS: ${gran_total:.2f}")

    # --- PANTALLA DE INVENTARIO ---
    def setup_inventario_tab(self):
        frame_form = tk.Frame(self.tab_inventario, bd=1, relief=tk.RAISED)
        frame_form.pack(fill=tk.X, padx=5, pady=10)

        tk.Label(frame_form, text="Carga Manual", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5)

        font_lbl = ("Arial", 14)
        font_ent = ("Arial", 14)

        tk.Label(frame_form, text="Código:", font=font_lbl).grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_inv_cod = tk.Entry(frame_form, width=12, font=font_ent)
        self.entry_inv_cod.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Descripción:", font=font_lbl).grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
        self.entry_inv_nom = tk.Entry(frame_form, width=25, font=font_ent)
        self.entry_inv_nom.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Precio:", font=font_lbl).grid(row=1, column=4, padx=5, pady=5, sticky=tk.E)
        self.entry_inv_pre = tk.Entry(frame_form, width=8, font=font_ent)
        self.entry_inv_pre.grid(row=1, column=5, padx=5, pady=5)

        tk.Label(frame_form, text="Stock:", font=font_lbl).grid(row=1, column=6, padx=5, pady=5, sticky=tk.E)
        self.entry_inv_stk = tk.Entry(frame_form, width=8, font=font_ent)
        self.entry_inv_stk.grid(row=1, column=7, padx=5, pady=5)

        btn_agregar = tk.Button(frame_form, text="Guardar Manual", font=("Arial", 14, "bold"), command=self.agregar_producto, bg="#cceeff", padx=10, pady=5)
        btn_agregar.grid(row=1, column=8, padx=15, pady=5)

        # Treeview para Inventario
        columns = ("id", "codigo", "nombre", "precio", "stock")
        self.tree_inv = ttk.Treeview(self.tab_inventario, columns=columns, show="headings", height=5)
        self.tree_inv.heading("codigo", text="Código")
        self.tree_inv.heading("nombre", text="Descripción")
        self.tree_inv.heading("precio", text="Precio de Venta")
        self.tree_inv.heading("stock", text="Stock Físico")
        
        self.tree_inv.column("codigo", width=120)
        self.tree_inv.column("nombre", width=450)
        self.tree_inv.column("precio", width=150, anchor=tk.E)
        self.tree_inv.column("stock", width=150, anchor=tk.CENTER)

        self.tree_inv.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        frame_acciones = tk.Frame(self.tab_inventario)
        frame_acciones.pack(fill=tk.X, padx=5, pady=10)

        btn_eliminar = tk.Button(frame_acciones, text="Eliminar Producto", font=("Arial", 14), command=self.eliminar_producto, bg="#ffcccc", pady=5)
        btn_eliminar.pack(side=tk.LEFT, padx=10)

        btn_editar = tk.Button(frame_acciones, text="Editar Producto", font=("Arial", 14, "bold"), command=self.editar_producto, bg="#ffffcc", pady=5)
        btn_editar.pack(side=tk.LEFT, padx=10)

        btn_exportar = tk.Button(frame_acciones, text="Exportar Stock a Excel", font=("Arial", 14, "bold"), command=self.exportar_inventario, bg="#ccffcc", pady=5)
        btn_exportar.pack(side=tk.RIGHT, padx=10)

        btn_importar = tk.Button(frame_acciones, text="Importar desde Excel", font=("Arial", 14, "bold"), command=self.importar_excel, bg="#ccffcc", pady=5)
        btn_importar.pack(side=tk.RIGHT, padx=10)

        self.cargar_inventario()

    def cargar_inventario(self):
        for item in self.tree_inv.get_children(): self.tree_inv.delete(item)
        for row in database.get_productos():
            formatted_row = (row[1], row[2], f"${row[3]:.2f}", row[4])
            self.tree_inv.insert("", tk.END, values=formatted_row, iid=row[0]) 

    def agregar_producto(self):
        cod, nom = self.entry_inv_cod.get().strip(), self.entry_inv_nom.get().strip()
        try:
            pre, stk = float(self.entry_inv_pre.get()), int(self.entry_inv_stk.get())
            if cod and nom:
                success, msg = database.add_producto(cod, nom, pre, stk)
                if success:
                    self.cargar_inventario()
                    self.cargar_lista_busqueda()
                    self.cargar_productos_combobox()
                    for entry in [self.entry_inv_cod, self.entry_inv_nom, self.entry_inv_pre, self.entry_inv_stk]:
                        entry.delete(0, tk.END)
                else:
                    retro_showerror("Error", msg, self.root)
            else:
                retro_showerror("Error", "Código y Nombre son obligatorios.", self.root)
        except ValueError:
            retro_showerror("Error", "Precio y Stock deben ser numéricos.", self.root)

    def eliminar_producto(self):
        selected = self.tree_inv.selection()
        if not selected: return
        db_id = selected[0]
        item = self.tree_inv.item(db_id)
        if retro_askyesno("Confirmar", f"¿Eliminar permanentemente {item['values'][1]}?", self.root):
            database.delete_producto(db_id)
            self.cargar_inventario()
            self.cargar_lista_busqueda()
            self.cargar_productos_combobox()

    def editar_producto(self):
        selected = self.tree_inv.selection()
        if not selected:
            retro_showwarning("Aviso", "Primero selecciona un producto de la tabla.", self.root)
            return
            
        db_id = selected[0]
        item = self.tree_inv.item(db_id)
        cod_actual = str(item['values'][0])
        
        producto_completo = database.search_producto_por_codigo(cod_actual)
        if not producto_completo: return

        dialog = RetroProductEdit(self.root, producto_completo)
        res = dialog.result
        if res:
            try:
                precio_str = res['precio'].replace(',', '.')
                nuevo_pre = float(precio_str)
                nuevo_stk = int(res['stock'])
                if res['codigo'] and res['nombre']:
                    success, msg = database.update_producto(db_id, res['codigo'], res['nombre'], nuevo_pre, nuevo_stk)
                    if success:
                        self.cargar_inventario()
                        self.cargar_lista_busqueda()
                        self.cargar_productos_combobox()
                    else:
                        retro_showerror("Error", msg, self.root)
                else:
                    retro_showerror("Error", "Código y Nombre no pueden estar vacíos.", self.root)
            except ValueError:
                retro_showerror("Error", "Precio y Stock deben ser números válidos.", self.root)

    def importar_excel(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=(("Archivos Excel", "*.xlsx *.xls"), ("Todos", "*.*"))
        )
        if not filepath: return
        try:
            df = pd.read_excel(filepath)
            columnas_esperadas = ['Codigo', 'Nombre', 'Precio', 'Stock']
            for col in columnas_esperadas:
                if col not in df.columns:
                    retro_showerror("Error de Formato", f"El archivo debe tener la columna '{col}'", self.root)
                    return
            
            agregados = 0; errores = 0
            for index, row in df.iterrows():
                cod = str(row['Codigo']).strip()
                nom = str(row['Nombre']).strip()
                try:
                    pre = float(row['Precio'])
                    stk = int(row['Stock'])
                    success, _ = database.add_producto(cod, nom, pre, stk)
                    if success: agregados += 1
                    else: errores += 1
                except: errores += 1
            
            self.cargar_inventario()
            self.cargar_lista_busqueda()
            self.cargar_productos_combobox()
            retro_showinfo("Importación Completada", f"Se agregaron {agregados} productos nuevos.\nHubo {errores} omitidos.", self.root)
        except Exception as e:
            retro_showerror("Error de Lectura", f"No se pudo leer el archivo Excel:\n{e}", self.root)

    def exportar_inventario(self):
        try:
            conn = database.get_connection()
            query_stock = 'SELECT codigo as Codigo, nombre as Nombre, precio as Precio, stock as Stock FROM productos'
            df_stock = pd.read_sql_query(query_stock, conn)
            conn.close()
            
            filepath = filedialog.asksaveasfilename(
                title="Exportar Stock a Excel",
                defaultextension=".xlsx",
                initialfile=f"Stock_Inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                filetypes=(("Archivos Excel", "*.xlsx"), ("Todos", "*.*"))
            )
            
            if filepath:
                df_stock.to_excel(filepath, index=False)
                retro_showinfo("Éxito", f"Inventario exportado correctamente en:\n{filepath}", self.root)
        except Exception as e:
            retro_showerror("Error de Exportación", f"No se pudo exportar el Excel:\n{e}", self.root)

    # --- PANTALLA INTELIGENCIA DE NEGOCIO ---
    def setup_analitica_tab(self):
        frame_top = tk.Frame(self.tab_analitica)
        frame_top.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame_top, text="DASHBOARD DE NEGOCIO", font=("Arial", 20, "bold"), fg="#003366").pack(side=tk.LEFT)
        btn_refresh = tk.Button(frame_top, text="Recalcular Datos", bg="lightblue", font=("Arial", 12, "bold"), command=self.actualizar_dashboard)
        btn_refresh.pack(side=tk.RIGHT)

        self.frame_graficos = tk.Frame(self.tab_analitica)
        self.frame_graficos.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        frame_prediccion = tk.Frame(self.tab_analitica, bd=2, relief=tk.GROOVE)
        frame_prediccion.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame_prediccion, text="ALERTA INTELIGENTE DE STOCK", font=("Arial", 16, "bold"), fg="red").pack(pady=5)
        
        cols_pred = ("producto", "stock_actual", "vel_venta", "dias_restantes", "estado")
        self.tree_pred = ttk.Treeview(frame_prediccion, columns=cols_pred, show="headings", height=8)
        self.tree_pred.heading("producto", text="Producto")
        self.tree_pred.heading("stock_actual", text="Stock Físico")
        self.tree_pred.heading("vel_venta", text="Ventas por Día (Velocidad)")
        self.tree_pred.heading("dias_restantes", text="Días Estimados para Agotar")
        self.tree_pred.heading("estado", text="Nivel de Alarma")

        self.tree_pred.column("producto", width=350)
        self.tree_pred.column("stock_actual", width=120, anchor=tk.CENTER)
        self.tree_pred.column("vel_venta", width=180, anchor=tk.CENTER)
        self.tree_pred.column("dias_restantes", width=180, anchor=tk.CENTER)
        self.tree_pred.column("estado", width=180, anchor=tk.CENTER)

        self.tree_pred.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = None
        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        conn = database.get_connection()
        query_completa = '''
            SELECT v.fecha_hora, p.nombre, dv.cantidad, v.metodo_pago 
            FROM ventas v
            JOIN detalle_ventas dv ON v.id = dv.id_venta
            JOIN productos p ON p.id = dv.id_producto
        '''
        df_ventas = pd.read_sql_query(query_completa, conn)
        df_stock = pd.read_sql_query("SELECT nombre, stock FROM productos", conn)
        conn.close()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        if df_ventas.empty:
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.text(0.5, 0.5, "No hay datos de ventas aún", ha='center', va='center', fontsize=14)
            ax.axis('off')
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_graficos)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor('#f0f0f0')

        top_productos = df_ventas.groupby('nombre')['cantidad'].sum().nlargest(5).sort_values()
        top_productos.plot(kind='barh', ax=ax1, color='teal')
        ax1.set_title("Top 5 Productos Estrella", fontsize=14)
        ax1.set_xlabel("Unidades Vendidas", fontsize=12)
        ax1.set_ylabel("")

        metodos = df_ventas.groupby('metodo_pago').size()
        metodos.plot(kind='pie', ax=ax2, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'], textprops={'fontsize': 12})
        ax2.set_title("Uso de Métodos de Pago", fontsize=14)
        ax2.set_ylabel("")

        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_graficos)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        for item in self.tree_pred.get_children():
            self.tree_pred.delete(item)

        df_ventas['fecha_hora'] = pd.to_datetime(df_ventas['fecha_hora'])
        dias_historia = (datetime.now() - df_ventas['fecha_hora'].min()).days
        if dias_historia < 1: dias_historia = 1

        ventas_totales = df_ventas.groupby('nombre')['cantidad'].sum().reset_index()
        df_analisis = pd.merge(df_stock, ventas_totales, on='nombre', how='left').fillna(0)
        
        df_analisis['velocidad'] = df_analisis['cantidad'] / dias_historia
        
        df_analisis['dias_restantes'] = df_analisis.apply(
            lambda row: (row['stock'] / row['velocidad']) if row['velocidad'] > 0 else 9999, axis=1
        )
        
        df_analisis = df_analisis.sort_values('dias_restantes')

        for index, row in df_analisis.iterrows():
            dias = row['dias_restantes']
            velocidad = row['velocidad']
            stock = row['stock']
            nombre = row['nombre']

            if dias == 9999:
                estado = "Sin Datos/Ventas"
                dias_str = "∞"
            else:
                dias_str = f"{int(dias)} días"
                if dias <= 3:
                    estado = "¡CRÍTICO!"
                elif dias <= 7:
                    estado = "Próximo a agotar"
                else:
                    estado = "Saludable"

            self.tree_pred.insert("", tk.END, values=(
                nombre, int(stock), f"{velocidad:.1f}/día", dias_str, estado
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = POSApplication(root)
    root.mainloop()
