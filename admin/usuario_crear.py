from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import mysql.connector
from mysql.connector import Error

# Función para conectar a la base de datos
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='bd1',
            user='root',
            password=''
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        CTkMessagebox(title="Error de conexión", message=f"No se pudo conectar a la base de datos: {e}", icon="cancel")
    return None

# Función para cargar sucursales en el combobox
def cargar_sucursales():
    cursor = conexion.cursor()
    cursor.execute("SELECT ID_SUCURSAL, DIRECCION, LOCALIDAD FROM sucursales")
    sucursales = cursor.fetchall()
    sucursales_dict = {f"{s[1]}, {s[2]}": s[0] for s in sucursales}
    sucursal_combobox.configure(values=list(sucursales_dict.keys()))
    return sucursales_dict

# Función para cargar permisos en el combobox
def cargar_permisos():
    cursor = conexion.cursor()
    cursor.execute("SELECT ID_PERMISO, DESCRIPCION FROM permisos")
    permisos = cursor.fetchall()
    permisos_dict = {p[1]: p[0] for p in permisos}
    permiso_combobox.configure(values=list(permisos_dict.keys()))
    return permisos_dict

# Función para crear un nuevo usuario
def crear_usuario():
    try:
        nombre = nombre_entry.get()
        apellido = apellido_entry.get()
        usuario = usuario_entry.get()
        contraseña = contraseña_entry.get()
        sucursal = sucursal_combobox.get()
        permiso = permiso_combobox.get()

        if not all([nombre, apellido, usuario, contraseña, sucursal, permiso]):
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return

        id_sucursal = sucursales_dict[sucursal]
        id_permiso = permisos_dict[permiso]

        cursor = conexion.cursor()
        try:
            cursor.execute("""
            INSERT INTO usuarios (NOMBRE, APELLIDO, USUARIO, CONTRASEÑA, ID_SUCURSAL, ID_PERMISO)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, usuario, contraseña, id_sucursal, id_permiso))
            conexion.commit()
            CTkMessagebox(title="Éxito", message="Usuario creado exitosamente", icon="info")
            limpiar_campos()
        except Error as e:
            CTkMessagebox(title="Error", message=f"No se pudo crear el usuario: {e}", icon="cancel")
        finally:
            cursor.close()
    except Exception as e:
        print(f"Error: {e}")

# Función para limpiar campos de entrada
def limpiar_campos():
    nombre_entry.delete(0, ctk.END)
    apellido_entry.delete(0, ctk.END)
    usuario_entry.delete(0, ctk.END)
    contraseña_entry.delete(0, ctk.END)
    sucursal_combobox.set('')  # Ajustado para CTkComboBox
    permiso_combobox.set('')  # Ajustado para CTkComboBox

# Función para volver al menú principal
def volver_menu_usuario():
    from gestor.menu_principal import menu_principal
    root.destroy()
    menu_principal()

# Configuración de la ventana principal
root = ctk.CTk()
root.title("Crear Usuario - Admin")
root.geometry("400x300")

# Conexión a la base de datos
conexion = conectar_bd()

# Creación de widgets
ctk.CTkLabel(root, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
nombre_entry = ctk.CTkEntry(root)
nombre_entry.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
apellido_entry = ctk.CTkEntry(root)
apellido_entry.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="Usuario:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
usuario_entry = ctk.CTkEntry(root)
usuario_entry.grid(row=2, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="Contraseña:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
contraseña_entry = ctk.CTkEntry(root, show="*")
contraseña_entry.grid(row=3, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="Sucursal:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
sucursal_combobox = ctk.CTkComboBox(root, state="readonly")
sucursal_combobox.grid(row=4, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="Permiso:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
permiso_combobox = ctk.CTkComboBox(root, state="readonly")
permiso_combobox.grid(row=5, column=1, padx=5, pady=5)

# Botones para crear usuario y volver
ctk.CTkButton(root, text="Crear Usuario", command=crear_usuario).grid(row=6, column=0, columnspan=2, pady=20)
ctk.CTkButton(root, text="Volver", command=volver_menu_usuario).grid(row=6, column=2, padx=5)

# Cargar datos en los combobox
sucursales_dict = cargar_sucursales()
permisos_dict = cargar_permisos()

# Iniciar el loop principal de la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos al cerrar la aplicación
if conexion.is_connected():
    conexion.close()
