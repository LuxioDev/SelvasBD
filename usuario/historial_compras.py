import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import usuario_actual
import openpyxl
from openpyxl.styles import Font
from datetime import datetime
import os

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
        CTkMessagebox(title="Error de conexión", message=f"No se pudo conectar a la base de datos: {err}",
                      icon="cancel")
        return None

# Función para exportar el historial a Excel
def exportar_a_excel(tree):
    id_usuario = usuario_actual.usuario_actual[0]
    sucursal = "Sucursal_X"  # Cambia esto según cómo obtengas la sucursal del usuario
    filename = f"Informe_Ventas_Usuario_{id_usuario}_Sucursal_{sucursal}.xlsx"

    # Verificar si el archivo ya existe
    if os.path.exists(filename):
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active
    else:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Informe de Ventas"
        headers = ["Fecha", "Usuario", "Sucursal", "Producto", "Cantidad", "Precio Unitario", "Total"]
        sheet.append(headers)

    # Obtener datos del Treeview
    for item in tree.get_children():
        values = tree.item(item, 'values')
        # Desempaquetar correctamente todos los valores
        producto, fecha_movimiento, cantidad_str, total_str = values

        # Convertir cantidad y total a flotantes
        cantidad = float(cantidad_str) if cantidad_str else 0
        total = float(total_str) if total_str else 0
        precio_unitario = total / cantidad if cantidad > 0 else 0  # Cálculo del precio unitario

        # Obtener la fecha actual para la exportación
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Cambia esto si quieres una fecha diferente

        # Agregar fila al Excel
        fila = [fecha, id_usuario, sucursal, producto, cantidad, precio_unitario, total]
        sheet.append(fila)

    wb.save(filename)
    messagebox.showinfo("Exportación exitosa", f"Los movimientos han sido exportados a {filename}")

# Función para mostrar los movimientos del usuario en el Treeview
def mostrar_movimientos(tree):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            id_usuario = usuario_actual.usuario_actual[0]
            # Modificación aquí: agregar ORDER BY m.fecha DESC para mostrar los más nuevos primero
            consulta = """
                SELECT m.id_movimiento, p.descripcion, DATE_FORMAT(m.fecha, '%d/%m') as fecha_movimiento,
                       m.cantidad, (m.cantidad * p.precio) as total
                FROM historial_movimientos m
                JOIN productos p ON m.id_producto = p.id_producto
                WHERE m.id_usuario = %s
                ORDER BY m.fecha DESC
            """
            cursor.execute(consulta, (id_usuario,))
            movimientos = cursor.fetchall()

            # Limpiar el Treeview antes de insertar nuevos datos
            for row in tree.get_children():
                tree.delete(row)

            # Insertar los movimientos en el Treeview
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

                # Verificación de resultados
                print(f"Resultado de la consulta: {resultado}")  # Debugging
                if resultado:
                    fecha_exacta = resultado[0] or "No disponible"
                    descripcion_completa = resultado[1] or "No disponible"

                    ventana_detalle = ctk.CTkToplevel(root)
                    ventana_detalle.title("Detalles de la compra")
                    ventana_detalle.configure(bg="#2E2E2E")

                    label_fecha = ctk.CTkLabel(ventana_detalle, text="Fecha exacta:", font=("Helvetica", 12),
                                               text_color="white")
                    label_fecha.grid(row=0, column=0, padx=10, pady=10)
                    label_fecha_valor = ctk.CTkLabel(ventana_detalle, text=fecha_exacta, font=("Helvetica", 12),
                                                     text_color="white")
                    label_fecha_valor.grid(row=0, column=1, padx=10, pady=10)

                    label_descripcion = ctk.CTkLabel(ventana_detalle, text="Descripción completa:",
                                                     font=("Helvetica", 12), text_color="white")
                    label_descripcion.grid(row=1, column=0, padx=10, pady=10)
                    label_descripcion_valor = ctk.CTkLabel(ventana_detalle, text=descripcion_completa,
                                                           font=("Helvetica", 12), text_color="white", wraplength=400)
                    label_descripcion_valor.grid(row=1, column=1, padx=10, pady=10)
                else:
                    messagebox.showwarning("Sin resultados", "No se encontraron detalles para esta compra.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo obtener los detalles de la compra: {err}")
            finally:
                cursor.close()
                conexion.close()

# Función principal que define la interfaz gráfica
def historial_compras():
    ctk.set_appearance_mode("dark")  # Establecer el modo de apariencia
    ctk.set_default_color_theme("blue")  # Establecer el tema de color
    root = ctk.CTk()
    root.title("Historial de Compras")
    root.resizable(False, False)

    altura_ventana = 400
    ancho_ventana = 500
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

    # Botón para volver al menú de usuario
    volver_btn = ctk.CTkButton(root, text="Volver", command=volver_menu_usuario)
    volver_btn.grid(row=2, column=3, sticky="w", padx=10, pady=10)

    # Título
    titulo_label = ctk.CTkLabel(root, text="Historial de compras", font=("Helvetica", 16, "bold"))
    titulo_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # Botón para más detalles
    mas_detalle_btn = ctk.CTkButton(root, text="Más detalles", command=lambda: mostrar_detalle_compra(root, tree))
    mas_detalle_btn.grid(row=2, column=2, sticky="w", padx=10, pady=10)

    # Botón para exportar a Excel
    exportar_btn = ctk.CTkButton(root, text="Exportar a Excel", command=lambda: exportar_a_excel(tree))
    exportar_btn.grid(row=2, column=1, sticky="w", padx=10, pady=10)

    mostrar_movimientos(tree)
    root.mainloop()

if __name__ == "__main__":
    historial_compras()