import tkinter as tk
import usuario_actual

def menu_usuario():
    root = tk.Tk()
    root.title("Menu Ventas")
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

    def comprar_productos():
        root.destroy()
        from usuario.comprar_productos import ventana_comprar_productos
        ventana_comprar_productos()

    def historial_compras():
        root.destroy()
        from usuario.historial_compras import historial_compras
        historial_compras()


    # Función para cerrar sesión
    def cerrar_sesion():
        root.destroy()
        from login import login
        login()

    volver_btn = tk.Button(root, text="Cerrar Sesión", bg="White", font=("Helvetica", 12), width=15, command=cerrar_sesion)
    volver_btn.grid(row=0, column=0, stick="w", padx=10, pady=10)

    menu_principal_lbl = tk.Label(root, text="Mercado de OMENMEAT S.A", font=("Helvetica", 16))
    menu_principal_lbl.grid(row=2, column=0, columnspan=5, pady=50,padx=110)

    gestor_stock_btn = tk.Button(root, text="Lista de productos", bg="White", font=("Helvetica", 12), width=18, command=comprar_productos)
    gestor_stock_btn.grid(row=4, column=0, padx=30, pady=10)

    historial_btn= tk.Button(root, text="Historial de compras", bg="White", font=("Helvetica", 12), width=18, command=historial_compras)
    historial_btn.grid(row=4, column=1, padx=40, pady=10)

    root.mainloop()

if __name__ == "__main__":
    menu_usuario()