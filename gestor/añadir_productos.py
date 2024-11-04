import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import usuario_actual
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
            #selecciona los valores de ID_SUCURSAL de la tabla sucursales donde el ID_USUARIO en la tabla usuarios coincide con el valor proporcionado, (INNER JOIN) para enlazar ambas tablas a través de ID_SUCURSAL
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

# Función para añadir un producto
def anadir_producto(producto, precio, precio_venta, id_categoria, id_proveedor, id_sucursal):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Inserta el producto junto con la categoria, el proveedor y la sucursal en la tabla productos
            consulta = "INSERT INTO productos (DESCRIPCION, PRECIO, ID_CATEGORIA, ID_PROVEEDOR,ID_SUCURSAL) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(consulta, (producto, precio, id_categoria, id_proveedor, id_sucursal))
            id_producto = cursor.lastrowid  # Obtener el ID del producto recién insertado

            # Inserta el producto en la tabla ventas con el precio de venta
            consulta_venta = "INSERT INTO venta (ID_PRODUCTO, DESCRIPCION, PRECIO, ID_CATEGORIA, ID_PROVEEDOR, ID_SUCURSAL) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(consulta_venta, (id_producto, producto, precio_venta, id_categoria, id_proveedor, id_sucursal))

            # Commit de ambas transacciones
            conexion.commit()

            # Inserta un registro en la tabla stock con cantidad 0 para la sucursal seleccionada
            consulta_stock = "INSERT INTO stock (ID_PRODUCTO, ID_SUCURSAL, CANTIDAD) VALUES (%s, %s, 0)"
            cursor.execute(consulta_stock, (id_producto, id_sucursal))
            id_usuario = usuario_actual.usuario_actual[0]

            # Registra el movimiento en el historial
            registrar_movimiento(id_producto, id_sucursal, id_usuario, 'entrada', 0, "Producto nuevo añadido con stock inicial de 0")

            conexion.commit()
            messagebox.showinfo("Éxito", f"Producto '{producto}' añadido con éxito en productos y ventas")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo añadir el producto: {err}")
        finally:
            cursor.close()
            conexion.close()




# Ventana para añadir productos
def ventana_anadir_productos():
    root = tk.Tk()
    root.title("Añadir Producto")
    root.resizable(False, False)

    # Tamaño de la ventana
    altura_ventana = 450
    ancho_ventana = 600
    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))
    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    def volver_menu_principal():
        root.destroy()
        from gestor.menu_principal import menu_principal
        menu_principal()

    # Etiqueta y entrada para el nombre del producto
    tk.Label(root, text="Nombre del producto:", font=("Helvetica", 12)).grid(row=0, column=0, padx=20, pady=10)
    producto_entry = tk.Entry(root, font=("Helvetica", 12))
    producto_entry.grid(row=0, column=1, padx=20, pady=10)

    # Etiqueta y entrada para el precio original del producto
    tk.Label(root, text="Precio original del producto:", font=("Helvetica", 12)).grid(row=1, column=0, padx=20, pady=10)
    precio_entry = tk.Entry(root, font=("Helvetica", 12))
    precio_entry.grid(row=1, column=1, padx=20, pady=10)

    # Etiqueta y entrada para el precio de venta del producto
    tk.Label(root, text="Precio de venta del producto:", font=("Helvetica", 12)).grid(row=2, column=0, padx=20, pady=10)
    precio_venta_entry = tk.Entry(root, font=("Helvetica", 12))
    precio_venta_entry.grid(row=2, column=1, padx=20, pady=10)

    # Menú desplegable para seleccionar la categoria
    tk.Label(root, text="Categoria:", font=("Helvetica", 12)).grid(row=3, column=0, padx=20, pady=10)
    categorias = obtener_categorias()
    categoria_combobox = ttk.Combobox(root, values=[f"{s[1]}" for s in categorias], state="readonly", font=("Helvetica", 12))
    categoria_combobox.grid(row=3, column=1, padx=20, pady=10)

    # Solo seleccionamos el primer elemento si hay datos
    if categorias:
        categoria_combobox.current(0)

    # Menú desplegable para seleccionar el proveedor
    tk.Label(root, text="Proveedor:", font=("Helvetica", 12)).grid(row=4, column=0, padx=20, pady=10)
    proveedores = obtener_proveedores()
    proveedor_combobox = ttk.Combobox(root, values=[f"{p[1]}" for p in proveedores], state="readonly", font=("Helvetica", 12))
    proveedor_combobox.grid(row=4, column=1, padx=20, pady=10)

    # Solo seleccionamos el primer elemento si hay datos
    if proveedores:
        proveedor_combobox.current(0)

    # Obtener el ID del usuario actual (se supone que lo tienes almacenado)
    if usuario_actual.usuario_actual is not None:
        id_usuario = usuario_actual.usuario_actual[0]
    else:
        messagebox.showerror("Error", "No se ha iniciado sesión")
        return

    # Mostrar la sucursal automáticamente en lugar de pedir que se elija
    tk.Label(root, text="Sucursal:", font=("Helvetica", 12)).grid(row=5, column=0, padx=20, pady=10)
    sucursal_cliente = obtener_sucursal_cliente(id_usuario)
    tk.Label(root, text=sucursal_cliente, font=("Helvetica", 12)).grid(row=5, column=1, padx=20, pady=10)
    id_sucursal = obtener_sucursal_cliente_id(id_usuario)

    # Función para agregar el producto seleccionado
    def agregar_producto():
        producto = producto_entry.get()
        try:
            precio = float(precio_entry.get())
            precio_venta = float(precio_venta_entry.get())  # Nuevo: precio de venta
            categoria_seleccionada = categoria_combobox.get()
            proveedor_seleccionado = proveedor_combobox.get()

            # Buscar los IDs correspondientes a la sucursal y proveedor seleccionados
            id_categoria = next((c[0] for c in categorias if c[1] == categoria_seleccionada), None)
            id_proveedor = next((p[0] for p in proveedores if p[1] == proveedor_seleccionado), None)

            if id_categoria and id_proveedor and id_sucursal:
                anadir_producto(producto, precio, precio_venta, id_categoria, id_proveedor, id_sucursal)
            else:
                messagebox.showerror("Error", "Categoria, proveedor o sucursal no válida.")
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")

    # Botón para añadir producto
    tk.Button(root, text="Añadir Producto", font=("Helvetica", 12), width=20, command=agregar_producto).grid(row=6, column=1, pady=20)

    # Botón para volver
    tk.Button(root, text="Volver", font=("Helvetica", 12), width=20, command=volver_menu_principal).grid(row=7, column=1, pady=20)

    root.mainloop()

if __name__ == "__main__":
    ventana_anadir_productos()
