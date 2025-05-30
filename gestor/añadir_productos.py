import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
import mysql.connector
import usuario_actual

ctk.set_appearance_mode("dark")  # Opciones: "light" o "dark"
ctk.set_default_color_theme("blue")  # Otros temas disponibles: "green", "dark-blue"


# Conexión a la base de datos MySQL
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


# Función para obtener sucursales y proveedores de la base de datos
def obtener_categorias():
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT ID_CATEGORIA, DESCRIPCION FROM categorias")
            categorias = cursor.fetchall()
            return categorias
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo recuperar las categorias: {err}")
        finally:
            cursor.close()
            conexion.close()
    return []

def obtener_sucursal_cliente(id_usuario):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            consulta = "SELECT sucursales.DIRECCION FROM sucursales INNER JOIN usuarios ON sucursales.ID_SUCURSAL = usuarios.ID_SUCURSAL WHERE usuarios.ID_USUARIO = %s"
            cursor.execute(consulta, (id_usuario,))
            sucursal = cursor.fetchone()
            return sucursal[0] if sucursal else "Sucursal no encontrada"
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo recuperar la sucursal: {err}")
        finally:
            cursor.close()
            conexion.close()
    return "Error al recuperar sucursal"

def obtener_sucursal_cliente_id(id_usuario):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            consulta = "SELECT sucursales.ID_SUCURSAL FROM sucursales INNER JOIN usuarios ON sucursales.ID_SUCURSAL = usuarios.ID_SUCURSAL WHERE usuarios.ID_USUARIO = %s"
            cursor.execute(consulta, (id_usuario,))
            sucursal = cursor.fetchone()
            return sucursal[0] if sucursal else None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo recuperar la sucursal: {err}")
        finally:
            cursor.close()
            conexion.close()
    return None



# Obtiene los proveedores desde la base de datos.
def obtener_proveedores():
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT ID_PROVEEDOR, NOMBRE FROM proveedores")
            proveedores = cursor.fetchall()
            return proveedores
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo recuperar los proveedores: {err}")
        finally:
            cursor.close()
            conexion.close()
    return []

def registrar_movimiento(id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            consulta = """
            INSERT INTO historial_movimientos 
            (id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion, id_cupon, mpago) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(consulta, (id_producto, id_sucursal, id_usuario, tipo_movimiento, cantidad, descripcion, 1 ,'Efectivo'))
            conexion.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo registrar el movimiento: {err}")
        finally:
            cursor.close()
            conexion.close()

# Función para añadir un producto
def anadir_producto(producto, precio, id_categoria, id_proveedor, id_sucursal):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Inserta el producto junto con la categoria, el proveedor y la sucursal
            consulta = "INSERT INTO productos (DESCRIPCION, PRECIO, ID_CATEGORIA, ID_PROVEEDOR,ID_SUCURSAL) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(consulta, (producto, precio, id_categoria, id_proveedor, id_sucursal))
            id_producto = cursor.lastrowid  # Obtener el ID del producto recién insertado

            conexion.commit()

            # Inserta un registro en la tabla stock con cantidad 0 para la sucursal seleccionada
            consulta_stock = "INSERT INTO stock (ID_PRODUCTO, ID_SUCURSAL, CANTIDAD) VALUES (%s, %s, 0)"
            cursor.execute(consulta_stock, (id_producto, id_sucursal))
            id_usuario = usuario_actual.usuario_actual[0]

            # Registra el movimiento en el historial
            registrar_movimiento(id_producto, id_sucursal, id_usuario, 'entrada', 0, "Producto nuevo añadido con stock inicial de 0")

            conexion.commit()
            messagebox.showinfo("Éxito", f"Producto '{producto}' añadido con éxito")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo añadir el producto: {err}")
        finally:
            cursor.close()
            conexion.close()



# Ventana para añadir productos
def ventana_anadir_productos():
    root = ctk.CTk()  # Cambiar la raíz de tkinter a CTk de customtkinter
    root.title("Añadir Producto")
    root.resizable(False, False)

    # Tamaño de la ventana
    altura_ventana = 400
    ancho_ventana = 600
    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))
    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    # Función para volver al menú principal
    def volver_menu_principal():
        root.destroy()
        from gestor.menu_principal import menu_principal
        menu_principal()

    # Etiqueta y entrada para el nombre del producto
    ctk.CTkLabel(root, text="Nombre del producto:", font=("Helvetica", 12)).grid(row=0, column=0, padx=20, pady=10)
    producto_entry = ctk.CTkEntry(root, font=("Helvetica", 12))
    producto_entry.grid(row=0, column=1, padx=20, pady=10)

    # Etiqueta y entrada para el precio del producto
    ctk.CTkLabel(root, text="Precio del producto:", font=("Helvetica", 12)).grid(row=1, column=0, padx=20, pady=10)
    precio_entry = ctk.CTkEntry(root, font=("Helvetica", 12))
    precio_entry.grid(row=1, column=1, padx=20, pady=10)

    # Menú desplegable para seleccionar la categoría
    ctk.CTkLabel(root, text="Categoría:", font=("Helvetica", 12)).grid(row=2, column=0, padx=20, pady=10)
    categorias = obtener_categorias()
    categoria_combobox = ctk.CTkComboBox(root, values=[f"{s[1]}" for s in categorias], font=("Helvetica", 12))
    categoria_combobox.grid(row=2, column=1, padx=20, pady=10)

    # Seleccionar el primer elemento si hay datos
    if categorias:
        categoria_combobox.set(categorias[0][1])

    # Menú desplegable para seleccionar el proveedor
    ctk.CTkLabel(root, text="Proveedor:", font=("Helvetica", 12)).grid(row=3, column=0, padx=20, pady=10)
    proveedores = obtener_proveedores()
    proveedor_combobox = ctk.CTkComboBox(root, values=[f"{p[1]}" for p in proveedores], font=("Helvetica", 12))
    proveedor_combobox.grid(row=3, column=1, padx=20, pady=10)

    # Seleccionar el primer elemento si hay datos
    if proveedores:
        proveedor_combobox.set(proveedores[0][1])

    # Etiqueta para la sucursal
    ctk.CTkLabel(root, text="Sucursal:", font=("Helvetica", 12)).grid(row=4, column=0, padx=20, pady=10)

    # Obtener el ID del usuario actual
    if usuario_actual.usuario_actual is not None:
        id_usuario = usuario_actual.usuario_actual[0]
    else:
        ctk.CTkMessageBox.show_error("Error", "No se ha iniciado sesión")
        return

    # Llamada a la función que obtiene la sucursal del cliente
    sucursal_cliente = obtener_sucursal_cliente(id_usuario)
    ctk.CTkLabel(root, text=sucursal_cliente, font=("Helvetica", 12)).grid(row=4, column=1, padx=20, pady=10)

    # Obtener el ID de la sucursal
    id_sucursal = obtener_sucursal_cliente_id(id_usuario)

    # Función para agregar el producto
    def agregar_producto():
        producto = producto_entry.get()
        try:
            precio = float(precio_entry.get())
            categoria_seleccionada = categoria_combobox.get()
            proveedor_seleccionado = proveedor_combobox.get()

            # Buscar los IDs correspondientes a la categoría y proveedor seleccionados
            id_categoria = next((c[0] for c in categorias if c[1] == categoria_seleccionada), None)
            id_proveedor = next((p[0] for p in proveedores if p[1] == proveedor_seleccionado), None)

            if id_categoria and id_proveedor and id_sucursal:
                anadir_producto(producto, precio, id_categoria, id_proveedor, id_sucursal)
            else:
                ctk.CTkMessageBox.show_error("Error", "Categoría, proveedor o sucursal no válida.")
        except ValueError:
            ctk.CTkMessageBox.show_error("Error", "El precio debe ser un número válido.")

    # Botón para añadir producto
    ctk.CTkButton(root, text="Añadir Producto", font=("Helvetica", 12), command=agregar_producto).grid(row=5, column=1, pady=20)

    # Botón para volver
    ctk.CTkButton(root, text="Volver", font=("Helvetica", 12), command=volver_menu_principal).grid(row=6, column=1, pady=20)

    root.mainloop()


if __name__ == "__main__":
    ventana_anadir_productos()