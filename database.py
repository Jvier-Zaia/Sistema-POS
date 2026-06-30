import sqlite3
import os
import datetime

DB_NAME = 'sistema_ventas.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            metodo_pago TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            FOREIGN KEY (id_venta) REFERENCES ventas(id),
            FOREIGN KEY (id_producto) REFERENCES productos(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS caja_operaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL, 
            monto_declarado REAL NOT NULL,
            diferencia REAL NOT NULL DEFAULT 0,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- NUEVAS TABLAS PARA COMPRAS Y PROVEEDORES ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            telefono TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_proveedor INTEGER NOT NULL,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            metodo_pago TEXT NOT NULL,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_compra INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_costo REAL NOT NULL,
            FOREIGN KEY (id_compra) REFERENCES compras(id),
            FOREIGN KEY (id_producto) REFERENCES productos(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- FUNCIONES DE PRODUCTOS ---
def add_producto(codigo, nombre, precio, stock):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)", 
                       (codigo, nombre, precio, stock))
        conn.commit()
        return True, "Producto agregado correctamente."
    except sqlite3.IntegrityError:
        return False, "Error: El código de producto ya existe."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"
    finally:
        conn.close()

def update_producto(prod_id, codigo, nombre, precio, stock):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET codigo=?, nombre=?, precio=?, stock=? WHERE id=?", 
                       (codigo, nombre, precio, stock, prod_id))
        conn.commit()
        return True, "Producto actualizado correctamente."
    except sqlite3.IntegrityError:
        return False, "Error: El código de producto ya existe en otro artículo."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"
    finally:
        conn.close()

def get_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_producto_por_codigo(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
    row = cursor.fetchone()
    conn.close()
    return row

def delete_producto(prod_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (prod_id,))
    conn.commit()
    conn.close()

# --- FUNCIONES DE PROVEEDORES Y COMPRAS ---
def add_proveedor(nombre, telefono):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO proveedores (nombre, telefono) VALUES (?, ?)", (nombre, telefono))
        conn.commit()
        return True, "Proveedor agregado correctamente."
    except sqlite3.IntegrityError:
        return False, "Error: Ya existe un proveedor con ese nombre."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"
    finally:
        conn.close()

def get_proveedores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proveedores")
    rows = cursor.fetchall()
    conn.close()
    return rows

def registrar_compra(id_proveedor, lista_productos, total, metodo_pago):
    # lista_productos debe ser un listado de dicts: [{'id_producto': x, 'cantidad': y, 'precio_costo': z}, ...]
    conn = get_connection()
    cursor = conn.cursor()
    try:
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO compras (id_proveedor, total, metodo_pago, fecha_hora) VALUES (?, ?, ?, ?)", 
                       (id_proveedor, total, metodo_pago, ahora))
        id_compra = cursor.lastrowid
        
        for item in lista_productos:
            cursor.execute("INSERT INTO detalle_compras (id_compra, id_producto, cantidad, precio_costo) VALUES (?, ?, ?, ?)",
                           (id_compra, item['id_producto'], item['cantidad'], item['precio_costo']))
            # Aumentar stock
            cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (item['cantidad'], item['id_producto']))
        
        # Si se pagó en efectivo, asentar el Egreso en caja_operaciones
        if metodo_pago == "Efectivo":
            # Guardamos como monto_declarado pero negativo, o con tipo 'Egreso Compra'
            cursor.execute("INSERT INTO caja_operaciones (tipo, monto_declarado, fecha_hora) VALUES ('Egreso Compra', ?, ?)", 
                           (total, ahora))
            
        conn.commit()
        return True, "Compra registrada y stock actualizado."
    except Exception as e:
        conn.rollback()
        print("Error en registrar_compra:", e)
        return False, str(e)
    finally:
        conn.close()

def get_historial_compras_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, c.fecha_hora, p.nombre, c.total, c.metodo_pago
        FROM compras c
        JOIN proveedores p ON c.id_proveedor = p.id
        ORDER BY c.id DESC LIMIT 50
    ''')
    compras = cursor.fetchall()
    
    rows = []
    for c in compras:
        id_compra = c[0]
        cursor.execute('''
            SELECT prod.nombre, dc.cantidad
            FROM detalle_compras dc
            JOIN productos prod ON dc.id_producto = prod.id
            WHERE dc.id_compra = ?
        ''', (id_compra,))
        detalles = cursor.fetchall()
        detalles_str = ", ".join([f"{d[0]} x{d[1]}" for d in detalles])
        fecha_sola = c[1].split(' ')[0] if ' ' in c[1] else c[1]
        rows.append((fecha_sola, c[2], detalles_str, c[3], c[4]))

    conn.close()
    return rows


# --- FUNCIONES DE VENTAS Y CAJA ---
def registrar_venta(ticket_items, total, metodo_pago):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO ventas (total, metodo_pago, fecha_hora) VALUES (?, ?, ?)", (total, metodo_pago, ahora))
        id_venta = cursor.lastrowid
        
        for item in ticket_items:
            cursor.execute("INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                           (id_venta, item['id_producto'], item['cantidad'], item['precio_unitario']))
            
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (item['cantidad'], item['id_producto']))
            
        conn.commit()
        return True, id_venta, ahora
    except Exception as e:
        conn.rollback()
        print("Error en registrar_venta:", e)
        return False, 0, ""
    finally:
        conn.close()

def registrar_apertura_caja(monto_inicial):
    conn = get_connection()
    cursor = conn.cursor()
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO caja_operaciones (tipo, monto_declarado, fecha_hora) VALUES ('Apertura', ?, ?)", (monto_inicial, ahora))
    conn.commit()
    conn.close()

def registrar_cierre_caja(efectivo_esperado, efectivo_declarado, diferencia):
    conn = get_connection()
    cursor = conn.cursor()
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO caja_operaciones (tipo, monto_declarado, diferencia, fecha_hora) VALUES ('Cierre', ?, ?, ?)", 
                   (efectivo_declarado, diferencia, ahora))
    conn.commit()
    conn.close()

def obtener_ultima_operacion_caja():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo, fecha_hora FROM caja_operaciones WHERE tipo IN ('Apertura', 'Cierre') ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row

def get_totales_por_metodo(fecha_desde):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT metodo_pago, SUM(total) FROM ventas WHERE fecha_hora >= ? GROUP BY metodo_pago", (fecha_desde,))
    rows = cursor.fetchall()
    
    # También hay que descontar los EGRESOS por COMPRAS en Efectivo
    cursor.execute("SELECT SUM(monto_declarado) FROM caja_operaciones WHERE tipo = 'Egreso Compra' AND fecha_hora >= ?", (fecha_desde,))
    egresos_efectivo = cursor.fetchone()[0]
    if not egresos_efectivo:
        egresos_efectivo = 0.0

    conn.close()
    
    totales = {'Efectivo': 0.0, 'Transferencia': 0.0, 'Crédito': 0.0}
    for metodo, total in rows:
        totales[metodo] = total
        
    totales['Efectivo_Neto'] = totales['Efectivo'] - egresos_efectivo
    totales['Egresos_Efectivo'] = egresos_efectivo
    
    return totales
