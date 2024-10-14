import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import usuario_actual


# Se realiza la conexion con la base de datos
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


# Se actualiza la lista de productos con sus atributos
def actualizar_lista_stock(tree):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Consulta para obtener la descripción, cantidad y precio de cada producto
            cursor.execute("SELECT p.DESCRIPCION, s.CANTIDAD, p.PRECIO FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO")
            resultados = cursor.fetchall()

            # Limpiar la lista antes de insertar nuevos datos
            for item in tree.get_children():
                tree.delete(item)

            # Insertar los productos, cantidades (con estado) y precios en la lista
            for descripcion, cantidad, precio in resultados:
                estado = " (Disponible)" if cantidad > 0 else " (Agotado)"
                cantidad_con_estado = f"{cantidad}{estado}"
                tree.insert("", tk.END, values=(descripcion, cantidad_con_estado, f"${precio:.2f}"))

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo recuperar la información del stock: {err}")
        finally:
            cursor.close()
            conexion.close()

# Al realizar un movimiento en la base de datos se guardan los datos respectivos del movimiento
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
            # Consulta para verificar el stock actual
            cursor.execute("SELECT s.CANTIDAD FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO WHERE p.DESCRIPCION = %s", (producto,))
            resultado = cursor.fetchone()

            if resultado:
                stock_actual = resultado[0]

                # Verificar que el stock no sea menor que 0
                if stock_actual + cantidad_anadir >= 0:
                    # Actualizar la cantidad de stock
                    consulta = "UPDATE stock s JOIN productos p ON s.ID_PRODUCTO = p.ID_PRODUCTO SET s.CANTIDAD = s.CANTIDAD + %s WHERE p.DESCRIPCION = %s"
                    cursor.execute(consulta, (cantidad_anadir, producto))

                    cursor.execute("SELECT p.ID_PRODUCTO, s.ID_SUCURSAL FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO WHERE p.DESCRIPCION = %s",(producto,))
                    resultado = cursor.fetchone()
                    id_usuario = usuario_actual.usuario_actual[0]
                    id_producto, id_sucursal = resultado

                    # Registrar el movimiento en el historial
                    registrar_movimiento(id_producto, id_sucursal, id_usuario, 'salida' if cantidad_anadir < 0 else 'entrada', -cantidad_anadir,f"Se modificó el stock en {-cantidad_anadir} unidades")

                    conexion.commit()
                    messagebox.showinfo("Éxito", f"Se ha comprado {-cantidad_anadir} unidades de '{producto}'")
                else:
                    messagebox.showerror("Error", f"No es posible comprar el producto debido a falta de existencias. Stock actual: {stock_actual}")
            else:
                messagebox.showerror("Error", "El producto no se encontró en la base de datos.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo modificar el stock: {err}")
        finally:
            cursor.close()
            conexion.close()

# Se crea la ventana para visualizar la lista
def ventana_comprar_productos():
    root = tk.Tk()
    root.title("Compra de productos")
    root.resizable(False, False)

    altura_ventana = 400
    ancho_ventana = 750

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()

    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))

    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    def volver_menu_usuario():
        from usuario.menu_usuario import menu_usuario
        root.destroy()
        menu_usuario()

    volver_btn = tk.Button(root, text="Volver", bg="White", font=("Helvetica", 12), command=volver_menu_usuario)
    volver_btn.grid(row=2, column=2, stick="w", padx=10, pady=10)

    # Treeview con solo tres columnas: Producto, Cantidad (que incluirá el estado), Precio
    tree = ttk.Treeview(root, columns=("Producto", "Cantidad", "Precio"), show='headings', height=10)
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")  # Aquí también aparecerá el estado
    tree.heading("Precio", text="Precio")
    tree.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

    actualizar_btn = tk.Button(root, text="Actualizar Lista", command=lambda: actualizar_lista_stock(tree))
    actualizar_btn.grid(row=1, column=0, padx=10, pady=10)

    cantidad_label = tk.Label(root, text="Cantidad a comprar:")
    cantidad_label.grid(row=1, column=1, padx=10, pady=10)

    cantidad_entry = tk.Entry(root)
    cantidad_entry.grid(row=1, column=2, padx=10, pady=10)

    def comprar_productos():
        selected_item = tree.selection()
        if selected_item:
            producto = tree.item(selected_item)["values"][0]
            cantidad = cantidad_entry.get()
            try:
                cantidad = -int(cantidad)  # Negativo porque se va a restar
                if cantidad < 0:
                    modificar_stock_producto(producto, cantidad)
                    actualizar_lista_stock(tree)  # Actualizar la lista después de modificar stock
                    cantidad_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número válido.")
        else:
            messagebox.showerror("Error", "Seleccione un producto de la lista.")

    anadir_btn = tk.Button(root, text="Comprar producto", command=comprar_productos)
    anadir_btn.grid(row=2, column=1, padx=10, pady=10)

    actualizar_lista_stock(tree)

    root.mainloop()


if __name__ == "__main__":
    ventana_comprar_productos()
