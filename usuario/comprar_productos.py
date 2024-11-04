import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import openpyxl
from openpyxl import Workbook
from pathlib import Path
import usuario_actual
from datetime import datetime

# Ruta del archivo de registro en Excel
# Ruta del archivo de registro en Excel
ruta_archivo_excel = Path("registro_compras.xlsx")

# Función para crear o cargar el archivo Excel y preparar encabezados en español si es necesario
def inicializar_excel(ruta_archivo_excel):
    if ruta_archivo_excel.exists():
        # Si el archivo ya existe, lo abre
        libro = openpyxl.load_workbook(ruta_archivo_excel)
        hoja = libro.active
    else:
        # Si el archivo no existe, lo crea y añade los encabezados
        libro = Workbook()
        hoja = libro.active
        encabezados = ["Fecha y Hora", "ID Usuario", "Usuario", "Producto", "Precio Unitario", "Cantidad", "Total Compra", "Descuento", "Total con Descuento", "Sucursal", "Ganancia"]
        hoja.append(encabezados)
        libro.save(ruta_archivo_excel)  # Guarda el archivo con los encabezados

    return libro, hoja

# Función para registrar cada compra en el archivo Excel, incluyendo la columna de "Ganancia"
def registrar_compra_excel(fecha_hora, id_usuario, nombre_usuario, producto, precio_unitario, cantidad_productos, monto_total, descuento, total_con_descuento, sucursal, ganancia, ruta_archivo_excel):
    libro, hoja = inicializar_excel(ruta_archivo_excel)
    nueva_fila = [fecha_hora, id_usuario, nombre_usuario, producto, precio_unitario, cantidad_productos, monto_total, descuento, total_con_descuento, sucursal, ganancia]
    hoja.append(nueva_fila)
    libro.save(ruta_archivo_excel)



# Función para conectar a la base de datos
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

# Función para verificar el código de descuento en la base de datos
def verificar_cupon(codigo):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT descuento FROM cupones WHERE codigo = %s AND activo = TRUE", (codigo,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo verificar el cupón: {err}")
            return None
        finally:
            cursor.close()
            conexion.close()
# Se actualiza la lista de productos con sus atributos
def actualizar_lista_stock(tree):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT p.DESCRIPCION, s.CANTIDAD, p.PRECIO FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO")
            resultados = cursor.fetchall()

            for item in tree.get_children():
                tree.delete(item)

            for descripcion, cantidad, precio in resultados:
                estado = " (Disponible)" if cantidad > 0 else " (Agotado)"
                cantidad_con_estado = f"{cantidad}{estado}"
                tree.insert("", tk.END, values=(descripcion, cantidad_con_estado, f"${precio:.2f}"))

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo recuperar la información del stock: {err}")
        finally:
            cursor.close()
            conexion.close()

# Registrar movimiento de stock en la base de datos
def registrar_movimiento(id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            consulta = "INSERT INTO historial_movimientos (id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(consulta, (id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion))
            conexion.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo registrar el movimiento: {err}")
        finally:
            cursor.close()
            conexion.close()

# Modificar stock con control de que no dé menos que 0
def modificar_stock_producto(producto, cantidad_anadir):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT s.CANTIDAD FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO WHERE p.DESCRIPCION = %s", (producto,))
            resultado = cursor.fetchone()

            if resultado:
                stock_actual = resultado[0]
                if stock_actual + cantidad_anadir >= 0:
                    consulta = "UPDATE stock s JOIN productos p ON s.ID_PRODUCTO = p.ID_PRODUCTO SET s.CANTIDAD = s.CANTIDAD + %s WHERE p.DESCRIPCION = %s"
                    cursor.execute(consulta, (cantidad_anadir, producto))

                    cursor.execute("SELECT p.ID_PRODUCTO, s.ID_SUCURSAL FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO WHERE p.DESCRIPCION = %s",(producto,))
                    resultado = cursor.fetchone()
                    id_usuario = usuario_actual.usuario_actual[0]
                    id_producto, id_sucursal = resultado

                    registrar_movimiento(id_producto, id_sucursal, id_usuario, 'salida' if cantidad_anadir < 0 else 'entrada', -cantidad_anadir, f"Se modificó el stock en {-cantidad_anadir} unidades")

                    conexion.commit()
                    messagebox.showinfo("Éxito", f"Se ha comprado {-cantidad_anadir} unidades de '{producto}'")
                    return True  # Éxito en la transacción
                else:
                    messagebox.showerror("Error", f"No es posible comprar el producto debido a falta de existencias. Stock actual: {stock_actual}")
                    return False  # Stock insuficiente
            else:
                messagebox.showerror("Error", "El producto no se encontró en la base de datos.")
                return False
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo modificar el stock: {err}")
            return False
        finally:
            cursor.close()
            conexion.close()
            



# Función para calcular y registrar la compra con ganancia
def comprar_productos(tree, cantidad_entry, cupon_entry, metodo_pago_var):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)["values"]
        if len(values) < 3:
            messagebox.showerror("Error", "No se pudo obtener la información completa del producto.")
            return

        producto = values[0]
        try:
            cantidad = -int(cantidad_entry.get())  # Negativo porque se va a restar
            if cantidad < 0:
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                id_usuario = usuario_actual.usuario_actual[0]
                nombre_usuario = usuario_actual.usuario_actual[1]
                precio_unitario = float(values[2].replace("$", "").strip())
                monto_total = abs(cantidad) * precio_unitario
                cantidad_productos = abs(cantidad)
                sucursal = usuario_actual.usuario_actual[3]
                
                # Verificar si el cupón es válido y obtener el descuento
                codigo_cupon = cupon_entry.get().strip()
                descuento = verificar_cupon(codigo_cupon) or 0

                # Aplicar un 15% de descuento si el método de pago es "efectivo"
                if metodo_pago_var.get() == "efectivo":
                    descuento = 15
                
                # Calcular el total con descuento
                total_con_descuento = monto_total * (1 - descuento / 100)
                
                # Consulta del precio de compra (de la tabla productos)
                conexion = conectar_bd()
                if conexion:
                    cursor = conexion.cursor()
                    try:
                        cursor.execute("SELECT PRECIO FROM productos WHERE DESCRIPCION = %s", (producto,))
                        resultado = cursor.fetchone()
                        precio_compra = resultado[0] if resultado else 0  # Asigna 0 si no se encuentra el producto
                    except mysql.connector.Error as err:
                        messagebox.showerror("Error", f"No se pudo obtener el precio de compra: {err}")
                        conexion.close()
                        return
                    finally:
                        cursor.close()
                        conexion.close()


                # Calcular la ganancia
                ganancia = (precio_unitario - precio_compra) * cantidad_productos
                
                # Intentar modificar el stock, solo registrar si el stock es suficiente
                exito = modificar_stock_producto(producto, cantidad)
                
                if exito:  # Solo registrar en Excel si la modificación de stock fue exitosa
                    actualizar_lista_stock(tree)
                    cantidad_entry.delete(0, tk.END)
                    cupon_entry.delete(0, tk.END)

                    # Registrar la compra en el archivo Excel con los datos completos, incluyendo la ganancia
                    registrar_compra_excel(fecha_hora, id_usuario, nombre_usuario, producto, precio_unitario, cantidad_productos, monto_total, descuento, total_con_descuento, sucursal, ganancia, ruta_archivo_excel)

                else:
                    messagebox.showerror("Error", "Stock insuficiente para completar la compra.")
            else:
                messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido.")
    else:
        messagebox.showerror("Error", "Seleccione un producto de la lista.")



def ventana_comprar_productos():
    root = tk.Tk()
    root.title("Compra de productos")
    root.resizable(False, False)
    altura_ventana = 500
    ancho_ventana = 650
    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))
    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    def volver_menu_usuario():
        from usuario.menu_usuario import menu_usuario
        root.destroy()
        menu_usuario()

    volver_btn = tk.Button(root, text="Volver", bg="White", font=("Helvetica", 12), command=lambda: volver_menu_usuario())
    volver_btn.grid(row=0, column=0, stick="w", padx=10, pady=10)
    
    tree = ttk.Treeview(root, columns=("Producto", "Cantidad", "Precio"), show='headings', height=10)
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Precio", text="Precio")
    tree.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

    actualizar_btn = tk.Button(root, text="Actualizar Lista", command=lambda: actualizar_lista_stock(tree))
    actualizar_btn.grid(row=4, column=2, padx=10, pady=10)

    cantidad_label = tk.Label(root, text="Cantidad a comprar:")
    cantidad_label.grid(row=2, column=0, padx=10, pady=10)

    cantidad_entry = tk.Entry(root)
    cantidad_entry.grid(row=2, column=1, padx=10, pady=10)

    # Campo para ingresar el código de descuento
    cupon_label = tk.Label(root, text="Código de descuento:")
    cupon_label.grid(row=3, column=0, padx=10, pady=10)

    cupon_entry = tk.Entry(root)
    cupon_entry.grid(row=3, column=1, padx=10, pady=10)

    # Botón para realizar la compra, ahora incluye el campo de cupones
    anadir_btn = tk.Button(root, text="Comprar producto", command=lambda: comprar_productos(tree, cantidad_entry, cupon_entry, metodo_pago_var))
    anadir_btn.grid(row=4, column=1, padx=10, pady=10)

    metodo_pago_var = tk.StringVar(value="efectivo") 

    efectivo_radio = tk.Radiobutton(root, text="Efectivo -15%", variable=metodo_pago_var, value="efectivo")
    efectivo_radio.grid(row=2, column=2)

    # Opción de tarjeta (o cualquier otra opción)
    tarjeta_radio = tk.Radiobutton(root, text="Tarjeta", variable=metodo_pago_var, value="tarjeta")
    tarjeta_radio.grid(row=3, column=2)



    actualizar_lista_stock(tree)
    root.mainloop()

if __name__ == "__main__":
    ventana_comprar_productos()

