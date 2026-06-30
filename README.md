# 🛒 Sistema-POS: Gestión de Ventas y Organización Empresarial

Bienvenido al repositorio de **Sistema-POS**, un completo software de Punto de Venta (Point of Sale) desarrollado en **Python** con una interfaz gráfica estilizada al estilo *Retro Windows XP*. Este proyecto fue diseñado como trabajo práctico integrador para la asignatura de **Organización Empresarial** en la **Universidad Tecnológica Nacional (UTN)**.

## 🌟 Características Principales

El sistema está compuesto por varias pestañas que emulan el funcionamiento real de un comercio minorista, implementando las reglas de la partida doble y la gestión del negocio:

- **💵 Control de Caja**: Apertura y cierre de caja. Calcula automáticamente el efectivo esperado, el sobrante/faltante físico y genera un reporte Excel detallado con el **Libro Diario** de la jornada.
- **📟 Registradora (Checkout)**: Interfaz de cobro rápida con buscador integrado, carrito de compras (ticket) y soporte para pagos en *Efectivo*, *Transferencia* o *Crédito*. Genera comprobantes de compra.
- **📜 Historial del Turno**: Registro en tiempo real de todas las ventas procesadas.
- **📦 Inventario**: Gestión completa de stock. Permite agregar, editar y eliminar productos, además de importar o exportar el inventario desde/hacia plantillas de Excel/CSV.
- **🚚 Compras a Proveedores**: Permite registrar nuevos proveedores, asentar compras de mercadería (órdenes de compra) y afectar tanto el stock como los egresos de la caja.
- **📊 Inteligencia de Negocio**: Gráficos analíticos automáticos (usando `matplotlib`) para visualizar:
  - Ventas por Método de Pago (Torta).
  - Top 5 Productos más Vendidos (Barras).
  - Evolución de Ingresos y Egresos Diarios (Líneas).

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.12
- **Interfaz Gráfica:** `tkinter` (Librería estándar)
- **Base de Datos:** `sqlite3` local (`sistema_ventas.db`)
- **Procesamiento de Datos y Reportes:** `pandas`, `openpyxl`
- **Visualización:** `matplotlib`, `matplotlib.backends.backend_tkagg`

## 🚀 Ejecución del Proyecto

### Prerrequisitos
Debes tener Python instalado. Luego, instala las dependencias necesarias:

```bash
pip install pandas openpyxl matplotlib
```

### Iniciar la Aplicación
Para correr la aplicación directamente desde el código fuente, ejecuta:

```bash
python main.py
```

*Nota: Asegúrate de tener los archivos `database.py` y los assets en la misma carpeta.*

## 📂 Estructura del Repositorio

- `main.py`: Lógica principal de la interfaz de usuario (UI), sistema de pestañas y eventos.
- `database.py`: Capa de acceso a datos (Queries de SQLite) para ventas, inventario y caja.
- `convert.py`, `generar_excel.py`, `empaquetar.py`: Scripts auxiliares de desarrollo.
- `Comprobantes/`, `Reportes/`, `tickets/`: Directorios donde se generan automáticamente los recibos, reportes de cierre de caja en `.xlsx` y logs.

---
*Desarrollado por **Javier Zaia** - Estudiante de la Tecnicatura Universitaria en Programación (TUP) - UTN.*
