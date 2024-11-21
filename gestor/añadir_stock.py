from tkinter import ttk

from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import mysql.connector
import usuario_actual


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
        CTkMessagebox(title="Error de conexión", message=f"No se pudo conectar a la base de datos: {err}", icon="cancel")
        return None


# Función para actualizar la lista de productos en el Treeview
def actualizar_lista_stock(tree):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Obtener la sucursal del usuario actual
            id_sucursal = usuario_actual.usuario_actual[3]

            # Modificar la consulta para filtrar por sucursal
            cursor.execute("""
                SELECT p.DESCRIPCION, s.CANTIDAD 
                FROM productos p 
                JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO 
                WHERE s.ID_SUCURSAL = %s
            """, (id_sucursal,))
            resultados = cursor.fetchall()

            # Limpiar el Treeview antes de insertar nuevos datos
            for item in tree.get_children():
                tree.delete(item)

            # Insertar productos y cantidades en el Treeview
            for descripcion, cantidad in resultados:
                estado = " (Disponible)" if cantidad > 0 else " (Agotado)"
                cantidad_con_estado = f"{cantidad}{estado}"
                tree.insert("", ctk.END, values=(descripcion, cantidad_con_estado))

        except mysql.connector.Error as err:
            CTkMessagebox(title="Error", message=f"No se pudo recuperar la información del stock: {err}", icon="cancel")
        finally:
            cursor.close()
            conexion.close()

# Función para registrar un movimiento en el historial
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
            CTkMessagebox(title="Error", message=f"No se pudo registrar el movimiento: {err}", icon="cancel")
        finally:
            cursor.close()
            conexion.close()


# Función para añadir más stock a un producto
def anadir_stock_producto(producto, cantidad_anadir):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Obtener la sucursal del usuario actual
            id_sucursal = usuario_actual.usuario_actual[3]

            # Modificar la consulta para considerar la sucursal
            consulta = """
                UPDATE stock s 
                JOIN productos p ON s.ID_PRODUCTO = p.ID_PRODUCTO 
                SET s.CANTIDAD = s.CANTIDAD + %s 
                WHERE p.DESCRIPCION = %s AND s.ID_SUCURSAL = %s
            """
            cursor.execute(consulta, (cantidad_anadir, producto, id_sucursal))

            # Consultar el ID del producto y la sucursal
            cursor.execute("""
                SELECT p.ID_PRODUCTO 
                FROM productos p 
                JOIN stock s ON p.ID_PRODUCTO = s.ID_PRODUCTO 
                WHERE p.DESCRIPCION = %s AND s.ID_SUCURSAL = %s
            """, (producto, id_sucursal))
            resultado = cursor.fetchone()

            if resultado:
                id_usuario = usuario_actual.usuario_actual[0]
                id_producto = resultado[0]

                # Registrar el movimiento de entrada
                registrar_movimiento(id_producto, id_sucursal, id_usuario, 'entrada', cantidad_anadir,
                                     f"Se añadió stock de {cantidad_anadir} unidades")

                conexion.commit()
                CTkMessagebox(title="Éxito", message=f"Se ha añadido {cantidad_anadir} unidades al producto '{producto}'", icon="info")
            else:
                CTkMessagebox(title="Error", message="El producto no se encontró en la base de datos o no pertenece a su sucursal.", icon="cancel")

        except mysql.connector.Error as err:
            CTkMessagebox(title="Error", message=f"No se pudo añadir stock: {err}", icon="cancel")
        finally:
            cursor.close()
            conexion.close()


# Función para manejar el efecto hover en los botones
def on_enter(button):
    button.configure(fg_color="#2677cc", cursor="hand2")

def on_leave(button):
    button.configure(fg_color="#3399FF", cursor="arrow")


# Función para la ventana de gestión de stock
def ventana_anadir_stock():
    root = ctk.CTk()
    root.title("Gestión de Stock - Añadir Stock")
    root.geometry("600x400")
    root.configure(fg_color="#2E2E2E")  # Fondo de la ventana en oscuro

    # Función para volver al menú principal
    def volver_menu_principal():
        root.destroy()
        from gestor.menu_principal import menu_principal
        menu_principal()

    # Botón de volver al menú principal con efecto hover
    volver_btn = ctk.CTkButton(root, text="Volver", fg_color="#3399FF", font=("Helvetica", 12, "bold"), text_color="white", command=volver_menu_principal)
    volver_btn.grid(row=2, column=2, stick="w", padx=10, pady=10)
    volver_btn.bind("<Enter>", lambda event: on_enter(volver_btn))
    volver_btn.bind("<Leave>", lambda event: on_leave(volver_btn))

    # Treeview para mostrar productos y cantidades
    tree = ttk.Treeview(root, columns=("Producto", "Cantidad"), show='headings', height=10)
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

    # Botón para actualizar la lista de productos
    actualizar_btn = ctk.CTkButton(root, text="Actualizar Lista", fg_color="#3399FF", font=("Helvetica", 12, "bold"), text_color="white", command=lambda: actualizar_lista_stock(tree))
    actualizar_btn.grid(row=1, column=0, padx=10, pady=10)
    actualizar_btn.bind("<Enter>", lambda event: on_enter(actualizar_btn))
    actualizar_btn.bind("<Leave>", lambda event: on_leave(actualizar_btn))

    # Entrada para cantidad a añadir
    cantidad_label = ctk.CTkLabel(root, text="Cantidad a añadir:", font=("Helvetica", 12, "bold"), text_color="white", fg_color="#2E2E2E")
    cantidad_label.grid(row=1, column=1, padx=10, pady=10)

    cantidad_entry = ctk.CTkEntry(root, font=("Helvetica", 12), fg_color="white", text_color="black")
    cantidad_entry.grid(row=1, column=2, padx=10, pady=10)

    # Función para agregar stock
    def agregar_stock():
        selected_item = tree.selection()
        if selected_item:
            producto = tree.item(selected_item)["values"][0]
            cantidad = cantidad_entry.get()
            try:
                cantidad = int(cantidad)
                if cantidad > 0:
                    anadir_stock_producto(producto, cantidad)
                    actualizar_lista_stock(tree)  # Actualizar la lista después de añadir stock
                    cantidad_entry.delete(0, ctk.END)
                else:
                    CTkMessagebox(title="Error", message="La cantidad debe ser mayor que cero.", icon="cancel")
            except ValueError:
                CTkMessagebox(title="Error", message="La cantidad debe ser un número válido.", icon="cancel")
        else:
            CTkMessagebox(title="Error", message="Seleccione un producto de la lista.", icon="cancel")

    # Botón para añadir stock con efecto hover
    anadir_btn = ctk.CTkButton(root, text="Añadir Stock", fg_color="#3399FF", font=("Helvetica", 12, "bold"), text_color="white", command=agregar_stock)
    anadir_btn.grid(row=2, column=1, padx=10, pady=10)
    anadir_btn.bind("<Enter>", lambda event: on_enter(anadir_btn))
    anadir_btn.bind("<Leave>", lambda event: on_leave(anadir_btn))

    # Inicializar la lista de productos al iniciar la ventana
    actualizar_lista_stock(tree)

    root.mainloop()


if __name__ == "__main__":
    ventana_anadir_stock()
