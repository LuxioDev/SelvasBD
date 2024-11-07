import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import usuario_actual
import openpyxl
from openpyxl.styles import Font
from datetime import datetime

# Función para conectar con la base de datos
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bd1"
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
        return None

# Genera un informe en formato Excel
def generar_informe_excel(producto, cantidad, precio, usuario, sucursal):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Informe de Ventas"
    headers = ["Fecha", "Usuario", "Sucursal", "Producto", "Cantidad", "Precio Unitario", "Total"]
    for col, header in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=col)
        cell.value = header
        cell.font = Font(bold=True)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = cantidad * precio
    datos = [fecha, usuario, sucursal, producto, cantidad, precio, total]
    for col, dato in enumerate(datos, start=1):
        sheet.cell(row=2, column=col, value=dato)

    filename = f"Informe_Ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    wb.save(filename)
    return filename

# Función para mostrar los movimientos del usuario en el Treeview
def mostrar_movimientos(tree):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            id_usuario = usuario_actual.usuario_actual[0]
            consulta = "SELECT m.id_movimiento, p.descripcion, DATE_FORMAT(m.fecha, '%d/%m') as fecha_movimiento, m.cantidad, (m.cantidad * p.precio) as total FROM historial_movimientos m JOIN productos p ON m.id_producto = p.id_producto WHERE m.id_usuario = %s"
            cursor.execute(consulta, (id_usuario,))
            movimientos = cursor.fetchall()

            for row in tree.get_children():
                tree.delete(row)

            for movimiento in movimientos:
                tree.insert("", "end", iid=movimiento[0], values=movimiento[1:])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo obtener el historial de compras: {err}")
        finally:
            cursor.close()
            conexion.close()

# Función para mostrar detalles de la compra seleccionada
def mostrar_detalle_compra(root, tree):
    seleccionado = tree.focus()
    if seleccionado:
        id_movimiento = seleccionado
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            try:
                consulta = "SELECT fecha, descripcion FROM historial_movimientos WHERE id_movimiento = %s"
                cursor.execute(consulta, (id_movimiento,))
                resultado = cursor.fetchone()
                if resultado:
                    fecha_exacta = resultado[0]
                    descripcion_completa = resultado[1]

                    ventana_detalle = tk.Toplevel(root)
                    ventana_detalle.title("Detalles de la compra")
                    ventana_detalle.configure(bg="#2E2E2E")

                    label_fecha = tk.Label(ventana_detalle, text="Fecha exacta:", font=("Helvetica", 12), fg="white", bg="#2E2E2E")
                    label_fecha.grid(row=0, column=0, padx=10, pady=10)
                    label_fecha_valor = tk.Label(ventana_detalle, text=fecha_exacta, font=("Helvetica", 12), fg="white", bg="#2E2E2E")
                    label_fecha_valor.grid(row=0, column=1, padx=10, pady=10)

                    label_descripcion = tk.Label(ventana_detalle, text="Descripción completa:", font=("Helvetica", 12), fg="white", bg="#2E2E2E")
                    label_descripcion.grid(row=1, column=0, padx=10, pady=10)
                    label_descripcion_valor = tk.Label(ventana_detalle, text=descripcion_completa, font=("Helvetica", 12), fg="white", bg="#2E2E2E", wraplength=400)
                    label_descripcion_valor.grid(row=1, column=1, padx=10, pady=10)

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo obtener los detalles de la compra: {err}")
            finally:
                cursor.close()
                conexion.close()

# Función principal que define la interfaz gráfica
def historial_compras():
    root = tk.Tk()
    root.title("Historial de Compras")
    root.configure(bg="#2E2E2E")
    root.resizable(False, False)

    altura_ventana = 350
    ancho_ventana = 450
    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))
    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    # Definir el Treeview para mostrar los movimientos
    columnas = ("descripcion_producto", "fecha_movimiento", "cantidad", "total")
    tree = ttk.Treeview(root, columns=columnas, show="headings")
    tree.heading("descripcion_producto", text="Producto")
    tree.heading("fecha_movimiento", text="Fecha (Día/Mes)")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("total", text="Total")
    tree.column("descripcion_producto", width=150, anchor="center")
    tree.column("fecha_movimiento", width=100, anchor="center")
    tree.column("cantidad", width=80, anchor="center")
    tree.column("total", width=100, anchor="center")
    tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    # Función para volver al menú de usuario
    def volver_menu_usuario():
        from usuario.menu_usuario import menu_usuario
        root.destroy()
        menu_usuario()

    # Funciones de hover para los botones
    def on_enter(e):
        e.widget.config(relief="raised", bd=4)

    def on_leave(e):
        e.widget.config(relief="flat", bd=2)

    # Botón para volver al menú de usuario
    volver_btn = tk.Button(root, text="Volver", bg="#3399FF", fg="white", font=("Helvetica", 12, "bold"), command=volver_menu_usuario, relief="flat", bd=2)
    volver_btn.grid(row=2, column=3, sticky="w", padx=10, pady=10)
    volver_btn.bind("<Enter>", on_enter)
    volver_btn.bind("<Leave>", on_leave)

    # Título
    titulo_label = tk.Label(root, text="Historial de compras", font=("Helvetica", 16, "bold"), fg="white", bg="#2E2E2E")
    titulo_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # Botón para más detalles
    mas_detalle_btn = tk.Button(root, text="Más detalles", bg="#3399FF", fg="white", font=("Helvetica", 12, "bold"), command=lambda: mostrar_detalle_compra(root, tree), relief="flat", bd=2)
    mas_detalle_btn.grid(row=2, column=2, sticky="w", padx=10, pady=10)
    mas_detalle_btn.bind("<Enter>", on_enter)
    mas_detalle_btn.bind("<Leave>", on_leave)

    mostrar_movimientos(tree)
    root.mainloop()

if __name__ == "__main__":
    historial_compras()
