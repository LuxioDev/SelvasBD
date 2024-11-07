import tkinter as tk
from tkinter import messagebox

def gestion_stock():
    root = tk.Tk()
    root.title("Gestor de stock")
    root.resizable(False, False)

    # Configuración de la ventana
    altura_ventana = 300
    ancho_ventana = 800

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()

    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))

    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    # Establecer fondo oscuro
    root.config(bg="#2E2E2E")

    # Función para cambiar a otras ventanas
    def volver_menu_principal():
        from gestor.menu_principal import menu_principal
        root.destroy()
        menu_principal()

    def abrir_anadir_stock():
        from gestor.añadir_stock import ventana_anadir_stock
        root.destroy()
        ventana_anadir_stock()

    def abrir_anadir_productos():
        from gestor.añadir_productos import ventana_anadir_productos
        root.destroy()
        ventana_anadir_productos()

    # Botón de volver
    volver_btn = tk.Button(root, text="Volver", bg="#3399FF", font=("Helvetica", 12, "bold"), fg="white", width=15, height=2, relief="flat", command=volver_menu_principal)
    volver_btn.grid(row=0, column=0, stick="w", padx=20, pady=20)

    # Título del menú
    menu_principal_lbl = tk.Label(root, text="Data Base OMENTECH S.A", font=("Helvetica", 16), fg="white", bg="#2E2E2E")
    menu_principal_lbl.grid(row=2, column=1, columnspan=3, pady=20)

    # Botones de opciones
    anadir_stock_btn = tk.Button(root, text="Añadir Stock", bg="#3399FF", font=("Helvetica", 12, "bold"), fg="white", width=15, height=2, relief="flat", command=abrir_anadir_stock)
    anadir_stock_btn.grid(row=4, column=1, padx=10, pady=10)

    ver_productos_btn = tk.Button(root, text="Añadir producto", bg="#3399FF", font=("Helvetica", 12, "bold"), fg="white", width=20, height=2, relief="flat", command=abrir_anadir_productos)
    ver_productos_btn.grid(row=4, column=2, padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    gestion_stock()
