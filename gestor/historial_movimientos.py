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


# Función para mostrar los movimientos de la sucursal gestionada en la lista
def mostrar_movimientos(tree):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            sucursal_gestor = usuario_actual.usuario_actual[3]
            consulta = "SELECT hm.id_movimiento, p.descripcion AS nombre_producto, hm.tipo_movimiento, hm.cantidad, hm.descripcion, CASE WHEN hm.tipo_movimiento = 'salida' THEN hm.cantidad * p.precio ELSE 0 END AS total_dinero FROM historial_movimientos hm JOIN productos p ON hm.id_producto = p.id_producto WHERE hm.id_sucursal = %s"
            cursor.execute(consulta, (sucursal_gestor,))  # Pasar el parámetro como una tupla
            movimientos = cursor.fetchall()

            for row in tree.get_children():
                tree.delete(row)

            # Ordenar los movimientos por id_movimiento de mayor a menor
            movimientos_ordenados = sorted(movimientos, key=lambda x: x[0], reverse=True)

            # Insertar los datos obtenidos en la lista
            for movimiento in movimientos_ordenados:
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
        id_movimiento = seleccionado

        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            try:
                consulta = "SELECT hm.fecha, hm.descripcion, p.precio FROM historial_movimientos hm JOIN productos p ON hm.id_producto = p.id_producto WHERE hm.id_movimiento = %s"
                cursor.execute(consulta, (id_movimiento,))
                resultado = cursor.fetchone()
                if resultado:
                    fecha_exacta = resultado[0]
                    descripcion_completa = resultado[1]
                    precio_producto = resultado[2]

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

                    label_precio = tk.Label(ventana_detalle, text="Precio del producto:", font=("Helvetica", 12))
                    label_precio.grid(row=2, column=0, padx=10, pady=10)

                    label_precio_valor = tk.Label(ventana_detalle, text=f"${precio_producto:.2f}", font=("Helvetica", 12))
                    label_precio_valor.grid(row=2, column=1, padx=10, pady=10)

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo obtener los detalles del movimiento: {err}")
            finally:
                cursor.close()
                conexion.close()


# Función para el efecto hover en los botones
def on_enter(button):
    button.config(bg="#2677cc", cursor="hand2")

def on_leave(button):
    button.config(bg="#3399FF", cursor="arrow")


# Función principal que define la interfaz gráfica
def historial_movimientos():
    root = tk.Tk()
    root.title("Historial de movimientos de la sucursal")
    root.resizable(False, False)

    altura_ventana = 600
    ancho_ventana = 800

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()

    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))

    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    # Fondo oscuro
    root.config(bg="#2E2E2E")

    # Definir la lista para mostrar los detalles de los movimientos
    columnas = ("producto", "tipo_movimiento", "cantidad", "descripcion", "total_dinero")
    tree = ttk.Treeview(root, columns=columnas, show="headings")

    tree.heading("producto", text="Producto")
    tree.heading("tipo_movimiento", text="Tipo de Movimiento")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("descripcion", text="Descripción")
    tree.heading("total_dinero", text="Total Dinero (Salida)")

    tree.column("producto", width=150, anchor="center")
    tree.column("tipo_movimiento", width=150, anchor="center")
    tree.column("cantidad", width=80, anchor="center")
    tree.column("descripcion", width=250, anchor="center")
    tree.column("total_dinero", width=120, anchor="center")

    tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    # Botón para volver al menú del gestor
    def volver_menu_usuario():
        from gestor.menu_principal import menu_principal
        root.destroy()
        menu_principal()

    # Botón volver con estilo y hover
    volver_btn = tk.Button(root, text="Volver", bg="#3399FF", font=("Helvetica", 12, "bold"), fg="white", width=15, height=2, relief="flat", command=volver_menu_usuario)
    volver_btn.grid(row=2, column=3, sticky="w", padx=20, pady=20)
    volver_btn.bind("<Enter>", lambda event: on_enter(volver_btn))
    volver_btn.bind("<Leave>", lambda event: on_leave(volver_btn))

    # Título
    titulo_label = tk.Label(root, text="Historial de movimientos de la sucursal", font=("Helvetica", 16), fg="white", bg="#2E2E2E")
    titulo_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # Botón más detalles con estilo y hover
    mas_detalle_btn = tk.Button(root, text="Más detalles", bg="#3399FF", font=("Helvetica", 12, "bold"), fg="white", width=15, height=2, relief="flat", command=lambda: mostrar_detalle_movimiento(root, tree))
    mas_detalle_btn.grid(row=2, column=2, sticky="w", padx=10, pady=10)
    mas_detalle_btn.bind("<Enter>", lambda event: on_enter(mas_detalle_btn))
    mas_detalle_btn.bind("<Leave>", lambda event: on_leave(mas_detalle_btn))

    # Mostrar movimientos en la lista
    mostrar_movimientos(tree)

    root.mainloop()


if __name__ == "__main__":
    historial_movimientos()
