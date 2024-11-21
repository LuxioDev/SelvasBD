import customtkinter as ctk
import usuario_actual

def menu_usuario():
    # Configuración inicial de apariencia
    ctk.set_appearance_mode("dark")  # Modo oscuro
    ctk.set_default_color_theme("blue")  # Tema de color

    # Crear ventana principal
    root = ctk.CTk()
    root.title("Menú Ventas - OMENMEAT S.A")
    root.resizable(False, False)
    root.configure(fg_color="#2C2C2C")  # Fondo gris oscuro

    # Configuración de dimensiones y posición de la ventana
    altura_ventana = 500
    ancho_ventana = 700
    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    x_cordinate = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    y_cordinate = int((altura_pantalla / 2) - (altura_ventana / 2))
    root.geometry(f"{ancho_ventana}x{altura_ventana}+{x_cordinate}+{y_cordinate}")

    # Título principal
    titulo_lbl = ctk.CTkLabel(root, text="Menú Principal", font=("Verdana", 28, "bold"), text_color="#FFFFFF")
    titulo_lbl.place(relx=0.5, rely=0.15, anchor="center")

    # Marco principal
    frame = ctk.CTkFrame(root, fg_color="#333333", width=450, height=320, corner_radius=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Subtítulo: Mostrar el nombre del usuario
    if usuario_actual.usuario_actual:
        nombre_usuario = usuario_actual.usuario_actual[1]
        bienvenida_lbl = ctk.CTkLabel(frame, text=f"Bienvenido, {nombre_usuario}",
                                      font=("Arial", 16), text_color="#FFFFFF")
    else:
        bienvenida_lbl = ctk.CTkLabel(frame, text="Bienvenido, Usuario",
                                      font=("Arial", 16), text_color="#FFFFFF")
    bienvenida_lbl.grid(row=0, column=0, pady=20, padx=20)

    # Funciones para los botones
    def comprar_productos():
        from usuario.comprar_productos import ventana_comprar_productos
        root.after(50, root.withdraw(), ventana_comprar_productos())

    def historial_compras():
        from usuario.historial_compras import historial_compras
        root.after(50, root.withdraw(), historial_compras())

    def cerrar_sesion():
        from login import login
        root.after(50, root.destroy(), login())

    # Botones principales
    gestor_stock_btn = ctk.CTkButton(frame, text="Lista de productos", command=comprar_productos,
                                     fg_color="#3399FF", hover_color="#0066CC",
                                     width=330, font=("Arial", 16, "bold"), corner_radius=15)
    gestor_stock_btn.grid(row=1, column=0, pady=10, padx=20)

    historial_btn = ctk.CTkButton(frame, text="Historial de compras", command=historial_compras,
                                  fg_color="#3399FF", hover_color="#0066CC",
                                  width=330, font=("Arial", 16, "bold"), corner_radius=15)
    historial_btn.grid(row=2, column=0, pady=10, padx=20)

    cerrar_sesion_btn = ctk.CTkButton(frame, text="Cerrar Sesión", command=cerrar_sesion,
                                      fg_color="#FF4D4D", hover_color="#CC0000",
                                      width=330, font=("Arial", 16, "bold"), corner_radius=15)
    cerrar_sesion_btn.grid(row=3, column=0, pady=10, padx=20)

    # Pie de página
    footer_lbl = ctk.CTkLabel(root, text="© 2024 OMENMEAT S.A - Todos los derechos reservados.",
                              font=("Arial", 10), text_color="#888888")
    footer_lbl.place(relx=0.5, rely=0.95, anchor="center")

    root.mainloop()

if __name__ == "__main__":
    menu_usuario()
