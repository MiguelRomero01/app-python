import tkinter as tk
from tkinter import ttk
import os



# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("400x350")
ventana.configure(bg="#3B8C6E")  # Fondo oscuro


def abrir_nueva_ventana():
     ventana.destroy()  # Cierra la ventana principal
     ruta_absoluta = os.path.abspath("Screens/SelectOption.py")  # Obtiene la ruta absoluta
     os.system(f"python {ruta_absoluta}")
     
# Estilo moderno
style = ttk.Style()
style.configure("TLabel", background="#3B8C6E", foreground="white", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))
style.configure("TButton", background="#2980b9", foreground="white", font=("Arial", 12), padding=5)

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
login_button = ttk.Button(ventana, text="Iniciar sesión", command= lambda: abrir_nueva_ventana())
login_button.pack(pady=20)

# Footer
footer = ttk.Label(ventana, text="© 2024 Mi Aplicación", font=("Arial", 10, "italic"))
footer.pack(side="bottom", pady=10)

# Iniciar el loop de la aplicación
ventana.mainloop()
