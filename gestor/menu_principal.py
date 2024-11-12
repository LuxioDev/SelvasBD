import tkinter as tk
import usuario_actual

def menu_principal():
    root = tk.Tk()
    root.title("Menu Principal")
    root.resizable(False, False)

    altura_ventana = 400
    ancho_ventana = 800

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()

    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))

    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    # Configuración de fondo oscuro
    root.config(bg="#2E2E2E")  # Fondo gris oscuro

    # Mostramos el nombre del usuario que inició sesión
    if usuario_actual.usuario_actual:
        nombre_usuario = usuario_actual.usuario_actual[1]
        bienvenida_lbl = tk.Label(root, text=f"Bienvenido {nombre_usuario}", font=("Helvetica", 14, "bold"), fg="white", bg="#2E2E2E")
        bienvenida_lbl.grid(row=0, column=1, padx=10, pady=10)
    else:
        bienvenida_lbl = tk.Label(root, text="Bienvenido", font=("Helvetica", 14, "bold"), fg="white", bg="#2E2E2E")
        bienvenida_lbl.grid(row=0, column=1, padx=10, pady=10)

    def gestionar_stock():
        root.destroy()
        from gestor.gestion_stock import gestion_stock
        gestion_stock()

    def historial_movimientos():
        root.destroy()
        from gestor.historial_movimientos import historial_movimientos
        historial_movimientos()

    def usuarios():
        root.destroy()
        from admin.usuario_crear import crear_usuario_ventana
        crear_usuario_ventana()

    # Función para cerrar sesión
    def cerrar_sesion():
        root.destroy()
        from login import login
        login()

    # Crear los botones con el efecto hover
    def on_enter(btn, color):
        btn.configure(bg=color)

    def on_leave(btn):
        btn.configure(bg="#4C9FC5")  # Color original del botón

    # Botón de cerrar sesión
    volver_btn = tk.Button(root, text="Cerrar Sesión", bg="#4C9FC5", font=("Helvetica", 12, "bold"), fg="white", width=15, height=2, relief="flat", command=cerrar_sesion)
    volver_btn.grid(row=0, column=0, stick="w", padx=20, pady=20)
    volver_btn.bind("<Enter>", lambda e: on_enter(volver_btn, "#2A7B9D"))  # Hover color
    volver_btn.bind("<Leave>", lambda e: on_leave(volver_btn))  # Revertir color

    # Título del menú
    menu_principal_lbl = tk.Label(root, text="Data Base OMENTECH S.A", font=("Helvetica", 18, "bold"), fg="white", bg="#2E2E2E")
    menu_principal_lbl.grid(row=2, column=0, columnspan=3, pady=40)

    # Botón de gestión de stock
    gestor_stock_btn = tk.Button(root, text="Gestión de stock", bg="#3399FF", font=("Helvetica", 12, "bold"), fg="white", width=18, height=2, relief="flat", command=gestionar_stock)
    gestor_stock_btn.grid(row=4, column=0, padx=30, pady=20)
    gestor_stock_btn.bind("<Enter>", lambda e: on_enter(gestor_stock_btn, "#2A7B9D"))  # Hover color
    gestor_stock_btn.bind("<Leave>", lambda e: on_leave(gestor_stock_btn))  # Revertir color

    # Botón de movimientos
    ventas_btn = tk.Button(root, text="Movimientos", bg="#3399FF", font=("Helvetica", 12, "bold"), fg="white", width=18, height=2, relief="flat", command=historial_movimientos)
    ventas_btn.grid(row=4, column=1, padx=40, pady=20)
    ventas_btn.bind("<Enter>", lambda e: on_enter(ventas_btn, "#2A7B9D"))  # Hover color
    ventas_btn.bind("<Leave>", lambda e: on_leave(ventas_btn))  # Revertir color

    # Botón de gestión de usuarios
    gestor_usuario_btn = tk.Button(root, text="Gestión de usuarios", bg="#3399FF", font=("Helvetica", 12, "bold"), fg="white", width=18, height=2, relief="flat", command=usuarios)
    gestor_usuario_btn.grid(row=4, column=2, padx=40, pady=20)
    gestor_usuario_btn.bind("<Enter>", lambda e: on_enter(gestor_usuario_btn, "#2A7B9D"))  # Hover color
    gestor_usuario_btn.bind("<Leave>", lambda e: on_leave(gestor_usuario_btn))  # Revertir color

    root.mainloop()

if __name__ == "__main__":
    menu_principal()

