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
ventana.geometry("400x400")
ventana.configure(bg="#3B8C6E")  # Fondo oscuro

# Obtener el tamaño de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
ancho_ventana = 400  # Ancho especificado en ventana.geometry
alto_ventana = 400  # Alto especificado en ventana.geometry

# Calcular la posición centrada
pos_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
pos_y = (alto_pantalla // 2) - (alto_ventana // 2)

# Configurar la geometría centrada
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

# Título
titulo = tk.Label(ventana, text="Bienvenido", font=("Arial", 16, "bold"), bg="#3B8C6E", fg="white")
titulo.pack(pady=20)

# Marco central para organizar elementos
frame = tk.Frame(ventana, bg="#3B8C6E")
frame.pack(pady=20)

# Texto de registro interactivo
register_label = tk.Label(
    ventana,
    text="¿No tienes cuenta? Regístrate aquí.",
    fg="#11497a",
    cursor="hand2",
    bg="#3B8C6E",
    font=("Arial", 12, "underline")
)
register_label.pack(pady=10)
register_label.bind("<Button-1>", lambda e: abrir_registro())  # Abrir ventana de registro al hacer clic

# Etiquetas y campos de entrada
usuario_label = tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#3B8C6E", fg="white")
usuario_label.grid(row=0, column=0, sticky="w", pady=5)
usuario_entry = tk.Entry(frame, width=25, font=("Arial", 12))
usuario_entry.grid(row=0, column=1, pady=5)

contraseña_label = tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#3B8C6E", fg="white")
contraseña_label.grid(row=1, column=0, sticky="w", pady=5)
contraseña_entry = tk.Entry(frame, show="*", width=25, font=("Arial", 12))
contraseña_entry.grid(row=1, column=1, pady=5)

# Cambiar el color del botón al pasar el mouse
def on_hover(event):
    login_button["bg"] = login_button["activebackground"]

def on_leave(event):
    login_button["bg"] = "#89D99D"  # Restaurar el color original

# Botón de inicio de sesión
login_button = tk.Button(
    ventana,
    text="Iniciar sesión",
    command=iniciar_sesion,
    bg="#89D99D",
    fg="black",
    font=("Arial", 12),
    relief="flat",
    activebackground="#5ebf76",  # Color activo
    width=20
)

# Asociar los eventos
login_button.bind("<Enter>", on_hover)
login_button.bind("<Leave>", on_leave)

login_button.pack(pady=20)


# Footer
footer = tk.Label(ventana, text="© 2024 Spring", font=("Arial", 10, "italic"), bg="#3B8C6E", fg="white")
footer.pack(side="bottom", pady=10)

# Iniciar el loop de la aplicación
ventana.mainloop()
