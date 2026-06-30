import zipfile
import os

def empaquetar():
    zip_filename = 'SistemaVentas_Final.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.exists('dist/main.exe'):
            zipf.write('dist/main.exe', 'Sistema_Ventas.exe')
        else:
            print("Error: No se encontró dist/main.exe")
            return
            
        if os.path.exists('caja.ico'):
            zipf.write('caja.ico', 'caja.ico')
            
        instrucciones = """¡Hola!

Este es el Sistema de Registro de Ventas.
Para poder utilizarlo:
1. Extrae (Descomprime) esta carpeta en tu Escritorio o Documentos.
2. Haz doble clic en el archivo "Sistema_Ventas.exe".

¡Listo! La aplicación creará automáticamente su base de datos y la carpeta de tickets en el lugar donde la ejecutes."""
        zipf.writestr('Instrucciones.txt', instrucciones.encode('utf-8'))

    print(f"¡Se ha generado exitosamente el archivo {zip_filename}!")

if __name__ == '__main__':
    empaquetar()
