import tkinter as tk
import usuario_actual

def menu_principal():
    root = tk.Tk()
    root.title("Menu Principal")
    root.resizable(False, False)

    altura_ventana = 300
    ancho_ventana = 500

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()

    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))

    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    # Mostramos el nombre del usuario que inició sesión
    if usuario_actual.usuario_actual:
        nombre_usuario = usuario_actual.usuario_actual[1]
        bienvenida_lbl = tk.Label(root, text=f"Bienvenido {nombre_usuario}", font=("Helvetica", 12))
        bienvenida_lbl.grid(row=0, column=1, padx=10, pady=10)
    else:
        bienvenida_lbl = tk.Label(root, text="Bienvenido", font=("Helvetica", 12))
        bienvenida_lbl.grid(row=0, column=1, padx=10, pady=10)

    def gestionar_stock():
        root.destroy()
        from gestor.gestion_stock import gestion_stock
        gestion_stock()

    def historial_movimientos():
        root.destroy()
        from gestor.historial_movimientos import historial_movimientos
        historial_movimientos()

    # Función para cerrar sesión
    def cerrar_sesion():
        root.destroy()
        from login import login
        login()

    volver_btn = tk.Button(root, text="Cerrar Sesión", bg="White", font=("Helvetica", 12), width=15, command=cerrar_sesion)
    volver_btn.grid(row=0, column=0, stick="w", padx=10, pady=10)

    menu_principal_lbl = tk.Label(root, text="Data Base OMENTECH S.A", font=("Helvetica", 16))
    menu_principal_lbl.grid(row=2, column=0, columnspan=3, pady=20)

    gestor_stock_btn = tk.Button(root, text="Gestion de stock", bg="White", font=("Helvetica", 12), width=15, command=gestionar_stock)
    gestor_stock_btn.grid(row=4, column=0, padx=10, pady=10)

    ventas_btn = tk.Button(root, text="Historial de movimientos", bg="White", font=("Helvetica", 12), width=15, command=historial_movimientos)
    ventas_btn.grid(row=4, column=1, padx=10, pady=10)

    gestor_usuario_btn = tk.Button(root, text="Gestion de usuarios", bg="White", font=("Helvetica", 12), width=15)
    gestor_usuario_btn.grid(row=4, column=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    menu_principal()