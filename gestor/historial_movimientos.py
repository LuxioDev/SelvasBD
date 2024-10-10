import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import usuario_actual


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

 
# Función para mostrar los movimientos del usuario en el Treeview
def mostrar_movimientos(tree):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            sucursal_usuario = usuario_actual.usuario_actual[3]
            consulta = "SELECT id_movimiento, id_producto, id_sucursal, tipo_movimiento, cantidad, descripcion FROM historial_movimientos WHERE id_sucursal = %s"
            cursor.execute(consulta, (sucursal_usuario,))  # Pasar el parámetro como una tupla
            movimientos = cursor.fetchall()

            # Limpiar el Treeview antes de insertar nuevos datos
            for row in tree.get_children():
                tree.delete(row)

            # Insertar los datos obtenidos en el Treeview
            for movimiento in movimientos:
                # El primer campo ahora es id_movimiento, lo almacenamos como "iid"
                tree.insert("", "end", iid=movimiento[0], values=movimiento[1:])

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo obtener el historial de movimientos: {err}")
        finally:
            cursor.close()
            conexion.close()


def mostrar_detalle_movimiento(root, tree):
    # Obtener la fila seleccionada en el Treeview
    seleccionado = tree.focus()  # Devuelve el iid de la fila seleccionada directamente
    if seleccionado:
        id_movimiento = seleccionado  # El 'iid' ya es el ID de la fila seleccionada

        # Conectar a la base de datos y obtener los detalles de la compra
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            try:
                consulta = "SELECT fecha, descripcion FROM historial_movimientos WHERE id_movimiento = %s"
                cursor.execute(consulta, (id_movimiento,))  # Pasar el id_movimiento
                resultado = cursor.fetchone()
                if resultado:
                    fecha_exacta = resultado[0]
                    descripcion_completa = resultado[1]

                    # Crear ventana emergente con los detalles de la compra
                    ventana_detalle = tk.Toplevel(root)
                    ventana_detalle.title("Detalles del movimiento")

                    label_fecha = tk.Label(ventana_detalle, text="Fecha exacta:", font=("Helvetica", 12))
                    label_fecha.grid(row=0, column=0, padx=10, pady=10)

                    label_fecha_valor = tk.Label(ventana_detalle, text=fecha_exacta, font=("Helvetica", 12))
                    label_fecha_valor.grid(row=0, column=1, padx=10, pady=10)

                    label_descripcion = tk.Label(ventana_detalle, text="Descripción completa:", font=("Helvetica", 12))
                    label_descripcion.grid(row=1, column=0, padx=10, pady=10)

                    label_descripcion_valor = tk.Label(ventana_detalle, text=descripcion_completa, font=("Helvetica", 12), wraplength=400)
                    label_descripcion_valor.grid(row=1, column=1, padx=10, pady=10)

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo obtener los detalles del movimiento: {err}")
            finally:
                cursor.close()
                conexion.close()


# Función principal que define la interfaz gráfica
def historial_movimientos():
    root = tk.Tk()
    root.title("Historial de movimientos")
    root.resizable(False, False)

    altura_ventana = 500
    ancho_ventana = 600

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()

    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))

    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    # Definir el Treeview para mostrar los movimientos
    columnas = ("id_producto", "id_sucursal", "tipo_movimiento", "cantidad", "descripcion")
    tree = ttk.Treeview(root, columns=columnas, show="headings")

    # Definir los encabezados de las columnas
    tree.heading("id_producto", text="ID Producto")
    tree.heading("id_sucursal", text="ID Sucursal")
    tree.heading("tipo_movimiento", text="Tipo de Movimiento")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("descripcion", text="Descripción")

    tree.column("id_producto", width=100, anchor="center")
    tree.column("id_sucursal", width=100, anchor="center")
    tree.column("tipo_movimiento", width=150, anchor="center")
    tree.column("cantidad", width=80, anchor="center")
    tree.column("descripcion", width=170, anchor="center")

    tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    # Botón para volver al menú del usuario
    def volver_menu_usuario():
        from usuario.menu_usuario import menu_usuario
        root.destroy()
        menu_usuario()

    volver_btn = tk.Button(root, text="Volver", bg="White", font=("Helvetica", 12), command=volver_menu_usuario)
    volver_btn.grid(row=2, column=3, sticky="w", padx=10, pady=10)

    # Título
    titulo_label = tk.Label(root, text="Historial de movimientos", font=("Helvetica", 16))
    titulo_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    mas_detalle_btn = tk.Button(root, text="Más detalles", bg="White", font=("Helvetica", 12), command=lambda: mostrar_detalle_movimiento(root, tree))
    mas_detalle_btn.grid(row=2, column=2, sticky="w", padx=10, pady=10)
    mostrar_movimientos(tree)

    root.mainloop()


if __name__ == "__main__":
    historial_movimientos()