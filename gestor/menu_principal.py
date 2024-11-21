import customtkinter as ctk
import usuario_actual

def menu_principal():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Menu Principal")
    root.resizable(False, False)

    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    x_cordinate = int((ancho_pantalla / 2) - (800 / 2))
    y_cordinate = int((altura_pantalla / 2) - (500 / 2))
    root.geometry(f"800x400+{x_cordinate}+{y_cordinate}")

    root.configure(fg_color="#2C2C2C")  # Fondo gris oscuro

    def cerrar_sesion():
        from login import login
        root.after(50, root.destroy(), login())

    salir_btn = ctk.CTkButton(root, text="Cerrar Sesión", command=cerrar_sesion, fg_color="#FF4D4D",
                              hover_color="#CC0000", font=("Arial", 16, "bold"), corner_radius=10)
    salir_btn.place(x=25, y=25)

    titulo_lbl = ctk.CTkLabel(root, text="Data Base OMENTECH S.A", font=("Verdana", 28, "bold"), text_color="#FFFFFF")
    titulo_lbl.place(relx=0.5, rely=0.1, anchor="center")

    if usuario_actual.usuario_actual:
        nombre_usuario = usuario_actual.usuario_actual[1]
        bienvenida_lbl = ctk.CTkLabel(root, text=f"Bienvenido, {nombre_usuario}", font=("Verdana", 20),
                                      text_color="#FFFFFF")
        bienvenida_lbl.place(relx=0.5, rely=0.2, anchor="center")

    frame = ctk.CTkFrame(root, fg_color="#333333", width=600, height=300, corner_radius=20)
    frame.place(relx=0.5, rely=0.55, anchor="center")

    def gestionar_stock():
        from gestor.gestion_stock import gestion_stock
        root.after(50, root.withdraw(), gestion_stock())

    def historial_movimientos():
        from gestor.historial_movimientos import historial_movimientos
        root.after(50, root.withdraw(), historial_movimientos())

    def usuarios():
        from admin.usuario_crear import crear_usuario_ventana
        root.after(50, root.withdraw(), crear_usuario_ventana())

    stock_btn = ctk.CTkButton(frame, text="Gestión de Stock", command=gestionar_stock, fg_color="#3399FF",
                              hover_color="#0066CC", font=("Arial", 16, "bold"), width=200, height=50, corner_radius=15)
    stock_btn.grid(row=0, column=0, padx=20, pady=20)

    usuarios_btn = ctk.CTkButton(frame, text="Gestión de Usuarios", command=usuarios, fg_color="#3399FF",
                                 hover_color="#0066CC", font=("Arial", 16, "bold"), width=200, height=50,
                                 corner_radius=15)
    usuarios_btn.grid(row=0, column=1, padx=20, pady=20)

    movimientos_btn = ctk.CTkButton(frame, text="Movimientos", command=historial_movimientos, fg_color="#3399FF",
                                    hover_color="#0066CC", font=("Arial", 16, "bold"), width=200, height=50,
                                    corner_radius=15)
    movimientos_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    menu_principal()
