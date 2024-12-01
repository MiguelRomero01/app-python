import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import importlib.util
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import config  # Importar el archivo de configuración compartida

# Crear la base de datos y la tabla si no existen
def inicializar_base_datos():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            waterScore INTEGER NOT NULL DEFAULT 0,
            EnergyScore INTEGER NOT NULL DEFAULT 0
        )
    """)
    conexion.commit()
    conexion.close()

def iniciar_sesion():
    usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()

    if not usuario or not contraseña:
        messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
        return

    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        config.usuario_actual = usuario  # Asignar el usuario a config
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
        print(f"IMPORTANTEE: Usuario actual asignado en config: {config.usuario_actual}")
        abrir_nueva_ventana()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Función para abrir la nueva ventana
def abrir_nueva_ventana():
    ventana.withdraw()  # Oculta la ventana principal
    print(f"IMPORTANTEE: Usuario actual asignado en config: {config.usuario_actual}")
    ruta_absoluta = os.path.abspath("Screens/SelectOption.py")
    spec = importlib.util.spec_from_file_location("modulo_seleccion", ruta_absoluta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)

# Función para abrir la ventana de registro
def abrir_registro():
    ventana.destroy()  # Oculta la ventana principal
    ruta_absoluta = os.path.abspath("Authentication/Register.py")
    spec = importlib.util.spec_from_file_location("registro", ruta_absoluta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)

# Inicializar la base de datos
inicializar_base_datos()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("400x350")
ventana.configure(bg="#3B8C6E")  # Fondo oscuro

# Estilo moderno
style = ttk.Style()
style.theme_use("clam")  # Usar un tema más moderno
style.configure("TLabel", background="#3B8C6E", foreground="black", font=("Arial", 12))
style.configure("TButton", background="#89D99D", foreground="black", font=("Arial", 12), padding=5)
style.map("TButton", background=[("active", "#3498db")])

# Estilo personalizado para los campos de entrada
style.configure("TEntry", font=("Arial", 12), fieldbackground="#FFFFFF", foreground="black")  # Establecer el fondo blanco por defecto

# Función para cambiar el fondo del campo de entrada al pasar el mouse
def on_enter(event):
    event.widget.configure(style="TEntryHover")  # Cambiar a estilo hover

def on_leave(event):
    event.widget.configure(style="TEntry")  # Volver al estilo original

# Definir el estilo hover para el campo de entrada
style.configure("TEntryHover", font=("Arial", 12), fieldbackground="#D3D3D3", foreground="black")  # Fondo gris claro

# Título
titulo = ttk.Label(ventana, text="Bienvenido", font=("Arial", 16, "bold"))
titulo.pack(pady=20)

# Marco central para organizar elementos
frame = tk.Frame(ventana, bg="#3B8C6E", padx=20, pady=20)
frame.pack(pady=10, fill="x", padx=50)

# Texto de registro interactivo (colocado arriba de los campos)
register_label = tk.Label(
    ventana,
    text="¿No tienes cuenta? Regístrate aquí.",
    fg="#11497a",  # Color azul que resalta
    cursor="hand2",  # Cambia el cursor a una mano
    bg="#3B8C6E",  # Fondo igual al de la ventana
    font=("Arial", 12, "underline")  # Subrayado para simular enlace
)
register_label.pack(pady=10)
register_label.bind("<Button-1>", lambda e: abrir_registro())  # Abrir ventana de registro al hacer clic

# Etiquetas y campos de entrada
usuario_label = ttk.Label(frame, text="Usuario:")
usuario_label.grid(row=0, column=0, sticky="w", pady=5)
usuario_entry = ttk.Entry(frame, width=30, font=("Arial", 12))  # Cambiar a ttk.Entry
usuario_entry.grid(row=0, column=1, pady=5)
usuario_entry.bind("<Enter>", on_enter)  # Asocia el evento de mouse al campo
usuario_entry.bind("<Leave>", on_leave)  # Asocia el evento de salida del mouse

contraseña_label = ttk.Label(frame, text="Contraseña:")
contraseña_label.grid(row=1, column=0, sticky="w", pady=5)
contraseña_entry = ttk.Entry(frame, show="*", width=30, font=("Arial", 12))  # Cambiar a ttk.Entry
contraseña_entry.grid(row=1, column=1, pady=5)
contraseña_entry.bind("<Enter>", on_enter)  # Asocia el evento de mouse al campo
contraseña_entry.bind("<Leave>", on_leave)  # Asocia el evento de salida del mouse

# Botón de login con bordes redondeados y color verde
login_button = ttk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion, width=20, style="TButton")
login_button.pack(pady=20)

# Footer
footer = ttk.Label(ventana, text="© 2024 Mi Aplicación", font=("Arial", 10, "italic"))
footer.pack(side="bottom", pady=10)

# Iniciar el loop de la aplicación
ventana.mainloop()
