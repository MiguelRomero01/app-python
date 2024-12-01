import tkinter as tk
from tkinter import ttk
import os
import sys
import importlib.util
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import config  # Importar el archivo de configuración compartida

# Crear la nueva ventana como Toplevel
home_ventana = tk.Toplevel()
home_ventana.title("Options")
home_ventana.geometry("500x500")
home_ventana.configure(bg="#3B8C6E")

# Título
titulo = ttk.Label(home_ventana, text="Selecciona una Opción", font=("Arial", 16, "bold"), background="#3B8C6E", foreground="white")
titulo.pack(pady=20)

# Mantener la ventana activa
home_ventana.mainloop()
