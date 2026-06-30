import pandas as pd

productos = {
    'Codigo': ['P011', 'P012', 'P013', 'P014', 'P015', 'P016', 'P017', 'P018', 'P019', 'P020'],
    'Nombre': [
        'Cuaderno Universitario 100 Hojas', 
        'Resaltador Fluo Amarillo', 
        'Caja de Clips Metálicos', 
        'Tijera Escolar', 
        'Pegamento en Barra 40g', 
        'Goma de Borrar Blanca', 
        'Regla de Acero 30cm', 
        'Cinta Adhesiva Transparente', 
        'Marcador Permanente Negro', 
        'Pack Cartulinas de Colores'
    ],
    'Precio': [1200, 350, 450, 600, 300, 150, 800, 250, 400, 1000],
    'Stock': [50, 100, 30, 20, 40, 80, 15, 60, 45, 25]
}

df = pd.DataFrame(productos)
df.to_excel('productos_nuevos.xlsx', index=False)
print("Archivo 'productos_nuevos.xlsx' creado exitosamente.")
