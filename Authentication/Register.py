import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import importlib.util
import os

# Crear la base de datos y la tabla si no existen
def inicializar_base_datos():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            waterScore INTEGER NOT NULL,
            EnergyScore INTEGER NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# Guardar el usuario en la base de datos
def registrar_usuario(usuario_entry, contraseña_entry, register_window):
    usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()

    if not usuario or not contraseña:
        messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
        return

    try:
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        # Intentar insertar el usuario en la base de datos
        cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)", (usuario, contraseña))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
        abrir_login(register_window)  # Llamada para abrir la ventana de login

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El usuario ya existe.")
    finally:
        conexion.close()

# Función para abrir la ventana de login
def abrir_login(register_window):
    register_window.destroy()  # Cierra la ventana de registro
    ruta_absoluta = os.path.abspath("Authentication/Login.py")
    spec = importlib.util.spec_from_file_location("login", ruta_absoluta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)  # Llama al archivo de login

# Crear la ventana principal de registro
def create_register_window():
    register_window = tk.Tk()
    register_window.title("Registro")
    register_window.geometry("400x400")
    register_window.configure(bg="#3B8C6E")  # Color de fondo original

    # Inicializar la base de datos
    inicializar_base_datos()

    # Estilo personalizado
    style = ttk.Style()
    style.theme_use("clam")  # Usar un tema más moderno
    style.configure("TLabel", background="#3B8C6E", foreground="black", font=("Arial", 12))
    style.configure("TEntry", font=("Arial", 12))
    style.configure("TButton", background="#89D99D", foreground="black", font=("Arial", 12), padding=10)
    style.map("TButton", background=[("active", "#5ebf76")])

    # Título de la ventana
    titulo = ttk.Label(register_window, text="Registro de Usuario", font=("Arial", 16, "bold"))
    titulo.pack(pady=20)

    # Marco central para organizar elementos
    frame = tk.Frame(register_window, bg="#3B8C6E", padx=20, pady=20)
    frame.pack(pady=10, fill="x", padx=50)

    # Etiquetas y campos de entrada
    usuario_label = ttk.Label(frame, text="Usuario:")
    usuario_label.grid(row=0, column=0, sticky="w", pady=5)
    usuario_entry = ttk.Entry(frame, width=30, font=("Arial", 12))  # Cambiar a ttk.Entry
    usuario_entry.grid(row=0, column=1, pady=5)

    contraseña_label = ttk.Label(frame, text="Contraseña:")
    contraseña_label.grid(row=1, column=0, sticky="w", pady=5)
    contraseña_entry = ttk.Entry(frame, show="*", width=30, font=("Arial", 12))  # Cambiar a ttk.Entry
    contraseña_entry.grid(row=1, column=1, pady=5)

    # Botón para registrar
    register_button = ttk.Button(register_window, text="Registrar", command=lambda: registrar_usuario(usuario_entry, contraseña_entry, register_window), width=10)
    register_button.pack(pady=20)

    # Footer
    footer = ttk.Label(register_window, text="© 2024 Mi Aplicación", font=("Arial", 10, "italic"), foreground="white")
    footer.pack(side="bottom", pady=10)

    # Iniciar el loop de la aplicación
    register_window.mainloop()

create_register_window()
