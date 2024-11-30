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

# Verificar las credenciales del usuario
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
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
        abrir_nueva_ventana()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Función para abrir la nueva ventana
def abrir_nueva_ventana():
    ventana.destroy()  # Cierra la ventana principal
    ruta_absoluta = os.path.abspath("Screens/SelectOption.py")  # Obtiene la ruta absoluta
    os.system(f"python {ruta_absoluta}")

# Función para abrir la ventana de registro
def abrir_registro():
    os.system("python Authentication/Register.py")  # Abre la pantalla de registro

# Inicializar la base de datos
inicializar_base_datos()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("400x350")
ventana.configure(bg="#3B8C6E")  # Fondo oscuro

# Estilo moderno
style = ttk.Style()
style.configure("TLabel", background="#3B8C6E", foreground="black", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))
style.configure("TButton", background="#2980b9", foreground="black", font=("Arial", 12), padding=5)

# Título
titulo = ttk.Label(ventana, text="Bienvenido", font=("Arial", 16, "bold"))
titulo.pack(pady=20)

# Marco central para organizar elementos
frame = tk.Frame(ventana, bg="#3B8C6E", padx=20, pady=20)
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

# Botón de login
login_button = ttk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion)
login_button.pack(pady=20)

# Texto de registro interactivo
register_label = tk.Label(
    ventana,
    text="¿No tienes cuenta? Regístrate aquí.",
    fg="blue",  # Color azul para simular un enlace
    cursor="hand2",  # Cambia el cursor a una mano
    bg="#3B8C6E",  # Fondo igual al de la ventana
    font=("Arial", 12, "underline")  # Subrayado para simular enlace
)
register_label.pack(pady=10)
register_label.bind("<Button-1>", lambda e: abrir_registro())  # Vincular el clic izquierdo

# Footer
footer = ttk.Label(ventana, text="© 2024 Mi Aplicación", font=("Arial", 10, "italic"))
footer.pack(side="bottom", pady=10)

# Iniciar el loop de la aplicación
ventana.mainloop()
