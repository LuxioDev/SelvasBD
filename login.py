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
        CTkMessagebox(title="Error de conexión", message=f"No se pudo conectar a la base de datos: {err}",
                      icon="cancel")
        return None


# Función para iniciar sesión
def login():
    def credenciales():
        usuario = usuario_ent.get()
        contrasena = contrasena_ent.get()

        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            try:
                consulta = "SELECT ID_USUARIO, nombre, ID_PERMISO, ID_SUCURSAL, usuario, contraseña FROM usuarios WHERE BINARY usuario = %s AND BINARY contraseña = %s"
                cursor.execute(consulta, (usuario, contrasena))
                resultado = cursor.fetchone()

                if resultado:
                    id_usuario = resultado[0]
                    nombre_usuario = resultado[1]
                    permiso_usuario = resultado[2]
                    sucursal_usuario = resultado[3]
                    usuario_actual.usuario_actual = (id_usuario, nombre_usuario, permiso_usuario, sucursal_usuario)

                    if permiso_usuario == 1:
                        from usuario.menu_usuario import menu_usuario
                        root.destroy()
                        menu_usuario()
                    elif permiso_usuario == 2:
                        from gestor.menu_principal import menu_principal
                        root.destroy()
                        menu_principal()
                    elif permiso_usuario == 3:
                        from admin.elegir_sucursal import elegir_sucursal
                        root.destroy()
                        elegir_sucursal()
                    elif permiso_usuario >= 4:
                        CTkMessagebox(title="Error",
                                      message="Permiso invalido, llame a un administrador de bases de datos",
                                      icon="cancel")
                else:
                    CTkMessagebox(title="Error", message="Credenciales inválidas, intente de nuevo", icon="cancel")

            except mysql.connector.Error as err:
                CTkMessagebox(title="Error", message=f"No se pudo verificar el usuario: {err}", icon="cancel")
            finally:
                cursor.close()
                conexion.close()
        else:
            CTkMessagebox(title="Error", message="No se pudo conectar a la base de datos.", icon="cancel")

    def confirmar_salida():
        confirmacion = CTkMessagebox(title="Confirmación", message="¿Estás seguro de que deseas salir?",
                                     icon="question", option_1="No", option_2="Sí")
        if confirmacion.get() == "Sí":
            root.destroy()

    root = ctk.CTk()
    root.title("Acceso al Sistema")
    root.resizable(False, False)
    root.geometry("700x500")
    root.configure(fg_color="#2C2C2C")  # Fondo gris oscuro

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    x_cordinate = int((ancho_pantalla / 2) - (700 / 2))
    y_cordinate = int((altura_pantalla / 2) - (500 / 2))
    root.geometry(f"700x500+{x_cordinate}+{y_cordinate}")

    salir_btn = ctk.CTkButton(root, text="Salir", command=confirmar_salida, fg_color="#FF4D4D", hover_color="#CC0000",
                              width=15, font=("Arial", 16, "bold"))
    salir_btn.place(x=25, y=25)

    usuario_lbl = ctk.CTkLabel(root, text="Bienvenido al Sistema", font=("Verdana", 28, "bold"), text_color="#FFFFFF")
    usuario_lbl.place(relx=0.5, rely=0.15, anchor="center")

    frame = ctk.CTkFrame(root, fg_color="#333333", width=450, height=320, corner_radius=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    usuario_ent = ctk.CTkEntry(frame, placeholder_text="Usuario", fg_color="#444444", text_color="#FFFFFF",
                               font=("Arial", 16), width=330, height=40, border_width=2, border_color="#3399FF",
                               corner_radius=10)
    usuario_ent.grid(row=0, column=0, padx=20, pady=20)

    contrasena_ent = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*", fg_color="#444444",
                                  text_color="#FFFFFF", font=("Arial", 16), width=330, height=40, border_width=2,
                                  border_color="#3399FF", corner_radius=10)
    contrasena_ent.grid(row=1, column=0, padx=20, pady=20)

    iniciar_btn = ctk.CTkButton(frame, text="Iniciar sesión", command=credenciales, fg_color="#3399FF",
                                hover_color="#0066CC", width=330, font=("Arial", 16, "bold"), corner_radius=15)
    iniciar_btn.grid(row=2, column=0, padx=20, pady=20)

    root.mainloop()


if __name__ == "__main__":
    login()
