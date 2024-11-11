from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
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
        CTkMessagebox(title="Error de conexión", message=f"No se pudo conectar a la base de datos: {err}", icon="cancel")
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
            CTkMessagebox(title="Error", message=f"No se pudo recuperar las sucursales: {err}", icon="cancel")
        finally:
            cursor.close()
            conexion.close()
    return []


def cambiar_sucursal(id_sucursal):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        try:
            id_usuario = usuario_actual.usuario_actual[0]

            query = "UPDATE usuarios SET ID_SUCURSAL = %s WHERE ID_USUARIO = %s"
            cursor.execute(query, (id_sucursal, id_usuario))
            conexion.commit()

            # Mostrar mensaje de éxito y luego cerrar la ventana principal
            CTkMessagebox(title="Éxito", message="Sucursal cambiada correctamente.", icon="check")
        except mysql.connector.Error as err:
            CTkMessagebox(title="Error", message=f"No se pudo cambiar la sucursal: {err}", icon="cancel")
        finally:
            cursor.close()
            conexion.close()


def elegir_sucursal():
    root = ctk.CTk()
    root.title("Elija una sucursal")
    root.resizable(False, False)

    altura_ventana = 300
    ancho_ventana = 500
    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()

    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))
    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    def continuar():
        sucursal_seleccionada = sucursal_combobox.get()
        id_sucursal = next((s[0] for s in sucursales if s[1] == sucursal_seleccionada), None)
        if id_sucursal:
            cambiar_sucursal(id_sucursal)
            root.withdraw()
            from gestor.menu_principal import menu_principal
            menu_principal()
        else:
            CTkMessagebox(title="Error", message="Sucursal no válida.", icon="cancel")

    def cerrar_sesion():
        root.destroy()
        from login import login
        login()

    root.configure(fg_color="#2E2E2E")

    volver_btn = ctk.CTkButton(root, text="Volver", fg_color="#4C9FC5", font=("Helvetica", 12, "bold"),
                               text_color="white", width=100, height=40, command=cerrar_sesion)
    volver_btn.grid(row=0, column=0, sticky="w", padx=20, pady=20)

    menu_principal_lbl = ctk.CTkLabel(root, text="Elija la sucursal que desea administrar",
                                      font=("Helvetica", 16, "bold"), text_color="white")
    menu_principal_lbl.grid(row=1, column=0, columnspan=3, pady=20)

    ctk.CTkLabel(root, text="Sucursal:", font=("Helvetica", 12), text_color="white").grid(row=2, column=0, padx=20, pady=10)

    sucursales = obtener_sucursales()
    sucursal_combobox = ctk.CTkComboBox(root, values=[f"{s[1]}" for s in sucursales], font=("Helvetica", 12),
                                        width=300, state="readonly")  # Hacer combo box de solo lectura
    sucursal_combobox.grid(row=2, column=1, padx=20, pady=10)

    if sucursales:
        sucursal_combobox.set(sucursales[0][1])

    gestor_stock_btn = ctk.CTkButton(root, text="Continuar", fg_color="#4C9FC5", font=("Helvetica", 12, "bold"),
                                     text_color="white", width=100, height=40, command=continuar)
    gestor_stock_btn.grid(row=3, column=1, padx=20, pady=20)

    root.mainloop()


if __name__ == "__main__":
    elegir_sucursal()
