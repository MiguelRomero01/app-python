import tkinter as tk
from tkinter import ttk
import os

def ChangeScreen(path):
     nueva_ventana.destroy()
     ruta_absoluta = os.path.abspath(f'Screens/{path}')  # Obtiene la ruta absoluta
     os.system(f"python {ruta_absoluta}")

# Crear la nueva ventana
nueva_ventana = tk.Tk()
nueva_ventana.title("Options")
nueva_ventana.geometry("400x300")
nueva_ventana.configure(bg="#2c3e50")  # Fondo oscuro

     
# Título
titulo = ttk.Label(nueva_ventana, text="Selecciona una Opcion", font=("Arial", 16, "bold"), background="#2c3e50", foreground="white")
titulo.pack(pady=20)

# Botones con diferentes comandos
energia_button = ttk.Button(nueva_ventana, text="Energia", command=lambda: ChangeScreen('SubScreens/Energy.py'))
energia_button.pack(pady=20)

agua_button = ttk.Button(nueva_ventana, text="Agua", command=lambda: ChangeScreen('SubScreens/Water.py'))
agua_button.pack(pady=20)

# Iniciar el loop de la nueva ventana
nueva_ventana.mainloop()
