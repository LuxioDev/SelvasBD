import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import usuario_actual


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


    # Función para obtener y mostrar productos y cantidades en el Treeview.
def actualizar_lista_stock(tree):

    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Consulta para obtener productos y stock
            cursor.execute("SELECT p.DESCRIPCION, s.CANTIDAD FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO")
            # Meter todos los productos en una lista
            resultados = cursor.fetchall()

            # Limpiar el Treeview antes de insertar nuevos datos
            for item in tree.get_children():
                tree.delete(item)

            # Insertar los productos y cantidades en el Treeview
            for descripcion, cantidad in resultados:
                tree.insert("", tk.END, values=(descripcion, cantidad))

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo recuperar la información del stock: {err}")
        finally:
            cursor.close()
            conexion.close()

def registrar_movimiento(id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion):
    conexion = conectar_bd()
    if conexion:

        cursor = conexion.cursor()
        try:
            consulta = """
            INSERT INTO historial_movimientos 
            (id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(consulta, (id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion))
            conexion.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo registrar el movimiento: {err}")
        finally:
            cursor.close()
            conexion.close()


# Función que añade más stock a un producto en la base de datos.
def anadir_stock_producto(producto, cantidad_anadir):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Actualizar la cantidad de stock del producto seleccionado
            consulta = "UPDATE stock s JOIN productos p ON s.ID_PRODUCTO = p.ID_PRODUCTO SET s.CANTIDAD = s.CANTIDAD + %s WHERE p.DESCRIPCION = %s"
            cursor.execute(consulta, (cantidad_anadir, producto))

            cursor.execute(
                "SELECT p.ID_PRODUCTO, s.ID_SUCURSAL FROM productos p JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO WHERE p.DESCRIPCION = %s",
                (producto,))
            resultado = cursor.fetchone()
            id_usuario = usuario_actual.usuario_actual[0]
            id_producto, id_sucursal = resultado

            # Registrar el movimiento en el historial (aquí el usuario se asume, puedes adaptarlo según tu sistema)
            registrar_movimiento(id_producto, id_sucursal, id_usuario, 'entrada', cantidad_anadir,
                                 f"Se añadió stock de {cantidad_anadir} unidades")

            conexion.commit()
            messagebox.showinfo("Éxito", f"Se ha añadido {cantidad_anadir} unidades al producto '{producto}'")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo añadir stock: {err}")
        finally:
            cursor.close()
            conexion.close()

# Crea una ventana para gestionar el stock con la funcionalidad de añadir más a un producto seleccionado.
def ventana_anadir_stock():
    root = tk.Tk()
    root.title("Gestión de Stock - Añadir Stock")
    root.geometry("600x400")

    def volver_menu_principal():
        root.destroy()
        from gestor.menu_principal import menu_principal
        menu_principal()

    volver_btn = tk.Button(root, text="Volver", bg="White", font=("Helvetica", 12), command=volver_menu_principal)
    volver_btn.grid(row=2, column=2, stick="w", padx=10, pady=10)

    # Treeview para mostrar los productos y sus cantidades
    tree = ttk.Treeview(root, columns=("Producto", "Cantidad"), show='headings', height=10)
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

    # Botón para actualizar la lista de productos
    actualizar_btn = tk.Button(root, text="Actualizar Lista", command=lambda: actualizar_lista_stock(tree))
    actualizar_btn.grid(row=1, column=0, padx=10, pady=10)

    # Entrada para cantidad a añadir
    cantidad_label = tk.Label(root, text="Cantidad a añadir:")
    cantidad_label.grid(row=1, column=1, padx=10, pady=10)

    cantidad_entry = tk.Entry(root)
    cantidad_entry.grid(row=1, column=2, padx=10, pady=10)

    # Función para manejar la adición de stock al producto seleccionado
    def agregar_stock():
        selected_item = tree.selection()
        if selected_item:
            producto = tree.item(selected_item)["values"][0]  # Obtener el producto seleccionado
            cantidad = cantidad_entry.get()
            try:
                cantidad = int(cantidad)
                if cantidad > 0:
                    anadir_stock_producto(producto, cantidad)
                    actualizar_lista_stock(tree)  # Actualizar la lista después de añadir stock
                    cantidad_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número válido.")
        else:
            messagebox.showerror("Error", "Seleccione un producto de la lista.")

    # Botón para añadir stock
    anadir_btn = tk.Button(root, text="Añadir Stock", command=agregar_stock)
    anadir_btn.grid(row=2, column=1, padx=10, pady=10)

    # Inicializar la lista de productos al iniciar la ventana
    actualizar_lista_stock(tree)

    root.mainloop()


if __name__ == "__main__":
    ventana_anadir_stock()
