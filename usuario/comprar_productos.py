import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import ttk
import mysql.connector
import usuario_actual
from datetime import datetime

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
        CTkMessagebox(title="Error de conexión", message=f"No se pudo conectar a la base de datos: {err}")
        return None

def verificar_cupon(codigo):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT descuento FROM cupones WHERE codigo = %s AND activo = TRUE", (codigo,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except mysql.connector.Error as err:
            CTkMessagebox(title="Error", message=f"No se pudo verificar el cupón: {err}")
            return None
        finally:
            cursor.close()
            conexion.close()

def actualizar_lista_stock(tree):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT p.DESCRIPCION, s.CANTIDAD, p.PRECIO FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO")
            resultados = cursor.fetchall()

            for item in tree.get_children():
                tree.delete(item)

            for descripcion, cantidad, precio in resultados:
                estado = " (Disponible)" if cantidad > 0 else " (Agotado)"
                cantidad_con_estado = f"{cantidad}{estado}"
                tree.insert("", ctk.END, values=(descripcion, cantidad_con_estado, f"${precio:.2f}"))

        except mysql.connector.Error as err:
            CTkMessagebox(title="Error", message=f"No se pudo recuperar la información del stock: {err}")
        finally:
            cursor.close()
            conexion.close()

def registrar_movimiento(id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            consulta = "INSERT INTO historial_movimientos (id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(consulta, (id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion))
            conexion.commit()
        except mysql.connector.Error as err:
            CTkMessagebox(title="Error", message=f"No se pudo registrar el movimiento: {err}")
        finally:
            cursor.close()
            conexion.close()

def modificar_stock_producto(producto, cantidad_anadir):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT s.CANTIDAD FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO WHERE p.DESCRIPCION = %s",
                (producto,))
            resultado = cursor.fetchone()

            if resultado:
                stock_actual = resultado[0]
                if stock_actual + cantidad_anadir >= 0:
                    consulta = "UPDATE stock s JOIN productos p ON s.ID_PRODUCTO = p.ID_PRODUCTO SET s.CANTIDAD = s.CANTIDAD + %s WHERE p.DESCRIPCION = %s"
                    cursor.execute(consulta, (cantidad_anadir, producto))

                    cursor.execute(
                        "SELECT p.ID_PRODUCTO, s.ID_SUCURSAL FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO WHERE p.DESCRIPCION = %s",
                        (producto,))
                    resultado = cursor.fetchone()
                    id_usuario = usuario_actual.usuario_actual[0]
                    id_producto, id_sucursal = resultado

                    registrar_movimiento(id_producto, id_sucursal, id_usuario,
                                         'salida' if cantidad_anadir < 0 else 'entrada', -cantidad_anadir,
                                         f"Venta del producto")

                    conexion.commit()
                    CTkMessagebox(title="Éxito", message=f"Se ha comprado {-cantidad_anadir} unidades de '{producto}'")
                    return True
                else:
                    CTkMessagebox(title="Error",
                                  message=f"No es posible comprar el producto debido a falta de existencias. Stock actual: {stock_actual}")
                    return False
            else:
                CTkMessagebox(title="Error", message="El producto no se encontró en la base de datos.")
                return False
        except mysql.connector.Error as err:
            CTkMessagebox(title="Error", message=f"No se pudo modificar el stock: {err}")
            return False
        finally:
            cursor.close()
            conexion.close()

def comprar_productos(tree, cantidad_entry, cupon_entry, metodo_pago_var):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)["values"]
        if len(values) < 3:
            CTkMessagebox(title="Error", message="No se pudo obtener la información completa del producto.")
            return

        producto = values[0]
        try:
            cantidad = -int(cantidad_entry.get())
            if cantidad < 0:
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                id_usuario = usuario_actual.usuario_actual[0]
                nombre_usuario = usuario_actual.usuario_actual[1]
                precio_unitario = float(values[2].replace("$", "").strip())
                monto_total = abs(cantidad) * precio_unitario
                cantidad_productos = abs(cantidad)
                sucursal = usuario_actual.usuario_actual[3]

                codigo_cupon = cupon_entry.get().strip()
                descuento = verificar_cupon(codigo_cupon) or 0

                if metodo_pago_var.get() == "efectivo":
                    descuento = 15

                total_con_descuento = monto_total * (1 - descuento / 100)
                ganancia = precio_unitario * 0.10 * cantidad_productos

                exito = modificar_stock_producto(producto, cantidad)

                if exito:
                    actualizar_lista_stock(tree)
                    cantidad_entry.delete(0, ctk.END)
                    cupon_entry.delete(0, ctk.END)

                else:
                    CTkMessagebox(title="Error", message="Stock insuficiente para completar la compra.")
            else:
                CTkMessagebox(title="Error", message="La cantidad debe ser mayor que cero.")
        except ValueError:
            CTkMessagebox(title="Error", message="La cantidad debe ser un número válido.")
    else:
        CTkMessagebox(title="Error", message="Seleccione un producto de la lista.")

def ventana_comprar_productos():
    root = ctk.CTk()
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

    volver_btn = ctk.CTkButton(root, text="Volver", fg_color="white", font=("Helvetica", 12), command=volver_menu_usuario)
    volver_btn.grid(row=0, column=0, stick="w", padx=10, pady=10)

    tree = ttk.Treeview(root, columns=("Producto", "Cantidad", "Precio"), show='headings', height=10)
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Precio", text="Precio")
    tree.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

    actualizar_btn = ctk.CTkButton(root, text="Actualizar Lista", command=lambda: actualizar_lista_stock(tree))
    actualizar_btn.grid(row=4, column=2, padx=10, pady=10)

    cantidad_label = ctk.CTkLabel(root, text="Cantidad a comprar:")
    cantidad_label.grid(row=2, column=0, padx=10, pady=10)

    cantidad_entry = ctk.CTkEntry(root)
    cantidad_entry.grid(row=2, column=1, padx=10, pady=10)

    cupon_label = ctk.CTkLabel(root, text="Código de descuento:")
    cupon_label.grid(row=3, column=0, padx=10, pady=10)

    cupon_entry = ctk.CTkEntry(root)
    cupon_entry.grid(row=3, column=1, padx=10, pady=10)

    anadir_btn = ctk.CTkButton(root, text="Comprar producto",
                               command=lambda: comprar_productos(tree, cantidad_entry, cupon_entry, metodo_pago_var))
    anadir_btn.grid(row=4, column=1, padx=10, pady=10)

    metodo_pago_var = ctk.StringVar(value="efectivo")

    efectivo_radio = ctk.CTkRadioButton(root, text="Efectivo -15%", variable=metodo_pago_var, value="efectivo")
    efectivo_radio.grid(row=2, column=2)

    tarjeta_radio = ctk.CTkRadioButton(root, text="Tarjeta", variable=metodo_pago_var, value="tarjeta")
    tarjeta_radio.grid(row=3, column=2)

    actualizar_lista_stock(tree)
    root.mainloop()

if __name__ == "__main__":
    ventana_comprar_productos()