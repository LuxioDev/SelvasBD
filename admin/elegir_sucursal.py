import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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


def obtener_sucursales():
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT ID_SUCURSAL, DIRECCION FROM sucursales")
            sucursales = cursor.fetchall()
            return sucursales
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo recuperar las sucursales: {err}")
        finally:
            cursor.close()
            conexion.close()
    return []

def cambiar_sucursal(id_sucursal):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Obtenie el id del usuario actual
            id_usuario = usuario_actual.usuario_actual[0]

            # Realizar la actualizacion de la sucursal del usuario actual
            query = "UPDATE usuarios SET ID_SUCURSAL = %s WHERE ID_USUARIO = %s"

            cursor.execute(query, (id_sucursal, id_usuario))

            # Confirmar los cambios en la base de datos
            conexion.commit()

            messagebox.showinfo("Éxito", "Sucursal cambiada correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cambiar la sucursal: {err}")
        finally:
            cursor.close()
            conexion.close()

def elegir_sucursal():
    root = tk.Tk()
    root.title("Por favor eliga una sucursal")
    root.resizable(False, False)

    altura_ventana = 250
    ancho_ventana = 500

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()

    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))

    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    def continuar():
        sucursal_seleccionada = sucursal_combobox.get()
        # Confirma la sucursal seleccionada para enviarla
        id_sucursal = next((s[0] for s in sucursales if s[1] == sucursal_seleccionada), None)
        if id_sucursal:
            # Llama a cambiar_sucursal con el id_sucursal seleccionado
            cambiar_sucursal(id_sucursal)
            root.destroy()
            from gestor.menu_principal import menu_principal
            menu_principal()
        else:
            messagebox.showerror("Error", "Sucursal no válida.")

    # Función para cerrar sesión
    def cerrar_sesion():
        root.destroy()
        from login import login
        login()

    volver_btn = tk.Button(root, text="Volver", bg="White", font=("Helvetica", 12), width=15, command=cerrar_sesion)
    volver_btn.grid(row=0, column=0, stick="w", padx=10, pady=10)

    menu_principal_lbl = tk.Label(root, text="Por favor eliga la sucursal que desea administrar", font=("Helvetica", 16))
    menu_principal_lbl.grid(row=1, column=0, columnspan=3, pady=20)

    tk.Label(root, text="Sucursal:", font=("Helvetica", 12)).grid(row=4, column=0, padx=20, pady=10)
    sucursales = obtener_sucursales()
    sucursal_combobox = ttk.Combobox(root, values=[f"{s[1]}" for s in sucursales], state="readonly", font=("Helvetica", 12))
    sucursal_combobox.grid(row=4, column=1, padx=20, pady=10)

    # Solo seleccionamos el primer elemento si hay datos
    if sucursales:
        sucursal_combobox.current(0)

    gestor_stock_btn = tk.Button(root, text="Continuar", bg="White", font=("Helvetica", 12), width=15, command=continuar)
    gestor_stock_btn.grid(row=5, column=1, padx=10, pady=10)


    root.mainloop()


if __name__ == "__main__":
    elegir_sucursal()

