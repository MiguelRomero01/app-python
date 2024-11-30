import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# Crear la base de datos y la tabla si no existen
def inicializar_base_datos():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# Guardar el usuario en la base de datos
def registrar_usuario():
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
        usuario_entry.delete(0, tk.END)
        contraseña_entry.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El usuario ya existe.")
    finally:
        conexion.close()

# Crear la ventana principal
register = tk.Tk()
register.title("Registro")
register.geometry("400x350")
register.configure(bg="#3B8C6E")  # Fondo oscuro

# Inicializar la base de datos
inicializar_base_datos()

# Estilo moderno
style = ttk.Style()
style.configure("TLabel", background="#3B8C6E", foreground="white", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))
style.configure("TButton", background="#2980b9", foreground="white", font=("Arial", 12), padding=5)

# Título
titulo = ttk.Label(register, text="Registro de Usuario", font=("Arial", 16, "bold"))
titulo.pack(pady=20)

# Marco central para organizar elementos
frame = tk.Frame(register, bg="#3B8C6E", padx=20, pady=20)
frame.pack(pady=10, fill="x", padx=50)

# Etiquetas y campos de entrada
usuario_label = ttk.Label(frame, text="Usuario:")
usuario_label.grid(row=0, column=0, sticky="w", pady=5)
usuario_entry = ttk.Entry(frame, width=25)
usuario_entry.grid(row=0, column=1, pady=5)

contraseña_label = ttk.Label(frame, text="Contraseña:")
contraseña_label.grid(row=1, column=0, sticky="w", pady=5)
contraseña_entry = ttk.Entry(frame, show="*", width=25)
contraseña_entry.grid(row=1, column=1, pady=5)

# Botón de registrar
registrar_button = ttk.Button(register, text="Registrar", command=registrar_usuario)
registrar_button.pack(pady=20)

# Footer
footer = ttk.Label(register, text="© 2024 Mi Aplicación", font=("Arial", 10, "italic"), background="#3B8C6E", foreground="white")
footer.pack(side="bottom", pady=10)

# Iniciar el loop de la aplicación
register.mainloop()
