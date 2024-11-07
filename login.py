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
        ctk.messagebox.show_error("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
        return None


# Función para iniciar sesión
def login():
    # Confirma si las credenciales coinciden con alguna del sistema
    def credenciales():
        usuario = usuario_ent.get()
        contrasena = contrasena_ent.get()

        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            try:
                # Lee la columna de usuario y contraseña de la tabla "usuarios" y busca coincidencia en las credenciales
                consulta = "SELECT ID_USUARIO, nombre, ID_PERMISO, ID_SUCURSAL, usuario, contraseña FROM usuarios WHERE BINARY  usuario = %s AND BINARY  contraseña = %s"
                cursor.execute(consulta, (usuario, contrasena))
                # intenta encontrar una coincidencia con las credenciales
                resultado = cursor.fetchone()

                # Si coinciden las credenciales se inicia el menu principal
                if resultado:
                    id_usuario = resultado[0]
                    nombre_usuario = resultado[1]
                    permiso_usuario = resultado[2]
                    sucursal_usuario = resultado[3]
                    # Almacenamos el usuario logueado en el módulo usuario_actual
                    usuario_actual.usuario_actual = (id_usuario, nombre_usuario, permiso_usuario, sucursal_usuario)
                    if permiso_usuario == 1:
                        # Inicia el menú de usuario
                        root.destroy()
                        from usuario.menu_usuario import menu_usuario
                        menu_usuario()
                    elif permiso_usuario == 2:
                        # Inicia el menú de gestor
                        root.destroy()
                        from gestor.menu_principal import menu_principal
                        menu_principal()
                    elif permiso_usuario == 3:
                        # Inicia el menú de administrador
                        root.destroy()
                        from admin.elegir_sucursal import elegir_sucursal
                        elegir_sucursal()
                    elif permiso_usuario >= 4:
                        ctk.messagebox.show_error("Error",
                                                  "Permiso invalido, llame a un administrador de bases de datos")
                else:
                    # Si no coincide, muestra error
                    ctk.messagebox.show_error("Error", "Credenciales inválidas, intente de nuevo")

            except mysql.connector.Error as err:
                ctk.messagebox.show_error("Error", f"No se pudo verificar el usuario: {err}")
            finally:
                cursor.close()
                conexion.close()
        else:
            ctk.messagebox.show_error("Error", "No se pudo conectar a la base de datos.")

    root = ctk.CTk()
    root.title("Acceso al Sistema")
    root.resizable(False, False)

    # Establecer el tamaño de la ventana (más grande)
    root.geometry("700x500")
    root.configure(bg="#1D1D1D")  # Fondo oscuro principal

    # Centrar la ventana en la pantalla
    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    x_cordinate = int((ancho_pantalla / 2) - (700 / 2))  # Centro horizontal
    y_cordinate = int((altura_pantalla / 2) - (500 / 2))  # Centro vertical
    root.geometry(f"700x500+{x_cordinate}+{y_cordinate}")

    # --- Botón Salir con sombra y borde redondeado ---
    salir_btn = ctk.CTkButton(root, text="Salir", command=root.destroy, fg_color="#3399FF", hover_color="#0066CC",
                              width=15, font=("Arial", 16, "bold"))
    salir_btn.place(x=25, y=25)  # Ubicación en la parte superior izquierda

    # --- Título centrado (Ahora con el mismo color de fondo que el marco) ---
    usuario_lbl = ctk.CTkLabel(root, text="Bienvenido al Sistema", font=("Verdana", 28, "bold"), text_color="#3399FF",)
    usuario_lbl.place(relx=0.5, rely=0.15, anchor="center")  # Centrado vertical y horizontal

    # --- Marco con bordes redondeados y sombra (centrado) ---
    frame = ctk.CTkFrame(root, fg_color="#333333", width=450, height=240, corner_radius=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Centrado en la ventana

    # --- Campos de texto con borde redondeado, sombra y cambio de color al enfocarse ---
    usuario_ent = ctk.CTkEntry(frame, placeholder_text="Usuario", fg_color="#444444", text_color="#FFFFFF",
                               font=("Arial", 16), width=330, height=40, border_width=2, border_color="#3399FF",
                               corner_radius=10)
    usuario_ent.grid(row=0, column=0, padx=20, pady=20)

    contrasena_ent = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*", fg_color="#444444",
                                  text_color="#FFFFFF", font=("Arial", 16), width=330, height=40, border_width=2,
                                  border_color="#3399FF", corner_radius=10)
    contrasena_ent.grid(row=1, column=0, padx=20, pady=20)

    # --- Efecto de fondo con gradientes y bordes ---
    fondo = ctk.CTkFrame(root, fg_color="#2C2C2C", width=400, height=75, corner_radius=25)
    fondo.place(relx=0.5, rely=0.85, anchor="center")  # Centrado en la ventana

    # --- Botón de iniciar sesión con sombra y efecto hover ---
    iniciar_btn = ctk.CTkButton(fondo, text="Iniciar sesión", command=credenciales, fg_color="#3399FF",
                                hover_color="#0066CC", width=350, font=("Arial", 16, "bold"), corner_radius=15)
    iniciar_btn.place(relx=0.5, rely=0.5, anchor="center")  # Centrado en la parte inferior del fondo

    root.mainloop()

if __name__ == "__main__":
    login()
