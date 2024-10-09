import tkinter as tk
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
                        messagebox.showerror("Error", "Permiso invalido, llame a un administrador de bases de datos")
                else:
                    # Si no coincide, muestra error
                    messagebox.showerror("Error", "Credenciales inválidas, intente de nuevo")

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo verificar el usuario: {err}")
            finally:
                cursor.close()
                conexion.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    root = tk.Tk()
    root.title("Login")
    root.resizable(False, False)

    altura_ventana = 300
    ancho_ventana = 450

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()

    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))

    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    salir_btn = tk.Button(root, text="Salir", command=root.destroy)
    salir_btn.grid(row=0, column=0, padx=10, pady=10)

    usuario_lbl = tk.Label(root, text="Login")
    usuario_lbl.grid(row=0, column=2, padx=10, pady=10)
    usuario_lbl = tk.Label(root, text="Usuario :")
    usuario_lbl.grid(row=1, column=1, padx=10, pady=10)
    usuario_ent = tk.Entry(root)
    usuario_ent.grid(row=1, column=2, padx=10, pady=10)

    contrasena_lbl = tk.Label(root, text="Contraseña :")
    contrasena_lbl.grid(row=2, column=1, padx=10, pady=10)
    contrasena_ent = tk.Entry(root, show='*')
    contrasena_ent.grid(row=2, column=2, padx=10, pady=10)

    iniciar_btn = tk.Button(root, text="Iniciar sesión", command=credenciales)
    iniciar_btn.grid(row=3, column=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    login()
