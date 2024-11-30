import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Librería Pillow para manipular imágenes
import os

def ChangeScreen(path):
    nueva_ventana.destroy()
    ruta_absoluta = os.path.abspath(f'Screens/{path}')  # Obtiene la ruta absoluta
    os.system(f"python {ruta_absoluta}")

# Crear la nueva ventana
nueva_ventana = tk.Tk()
nueva_ventana.title("Options")
nueva_ventana.geometry("300x300")
nueva_ventana.configure(bg="#3B8C6E")  # Fondo oscuro

# Título
titulo = ttk.Label(nueva_ventana, text="Selecciona una Opcion", font=("Arial", 16, "bold"), background="#2c3e50", foreground="white")
titulo.pack(pady=20)

# Redimensionar la imagen usando Pillow
imagen_original = Image.open("Assets/oit17.png")  # Cargar la imagen original
imagen_redimensionada = imagen_original.resize((150, 150))  # Ajusta el tamaño de la imagen (ancho, alto)
imagen = ImageTk.PhotoImage(imagen_redimensionada)  # Convertir a formato compatible con Tkinter

# Mostrar la imagen redimensionada
etiqueta_imagen = ttk.Label(nueva_ventana, image=imagen)
etiqueta_imagen.pack(pady=1)

# Botones con diferentes comandos
energia_button = ttk.Button(nueva_ventana, text="Energia", command=lambda: ChangeScreen('SubScreens/Energy.py'))
energia_button.pack(pady=20)

agua_button = ttk.Button(nueva_ventana, text="Agua", command=lambda: ChangeScreen('SubScreens/Water.py'))
agua_button.pack(pady=20)

# Iniciar el loop de la nueva ventana
nueva_ventana.mainloop()
