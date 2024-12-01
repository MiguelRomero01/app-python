import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import importlib.util
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import config  # Importar el archivo de configuración compartida

def ChangeScreen(path):
    print(f"IMPORTANTEE: Usuario actual asignado en config pantalla2: {config.usuario_actual}")
    try:
        nueva_ventana.withdraw()  # Oculta la ventana actual después de cargar el nuevo módulo
        ruta_absoluta = os.path.abspath(f'Screens/{path}')
        spec = importlib.util.spec_from_file_location("modulo_seleccion", ruta_absoluta)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
    except Exception as e:
        print(f"Error al cambiar de pantalla: {e}")

# Crear la nueva ventana como Toplevel
nueva_ventana = tk.Toplevel()
nueva_ventana.title("Options")
nueva_ventana.geometry("500x500")
nueva_ventana.configure(bg="#3B8C6E")

# Título
titulo = ttk.Label(nueva_ventana, text="Selecciona una Opción", font=("Arial", 16, "bold"), background="#3B8C6E", foreground="white")
titulo.pack(pady=20)

# Redimensionar la imagen usando Pillow
try:
    imagen_original = Image.open("Assets/oit17.png")
    imagen_redimensionada = imagen_original.resize((300, 300))
    imagen = ImageTk.PhotoImage(imagen_redimensionada)  # Crear referencia global

    etiqueta_imagen = ttk.Label(nueva_ventana)
    etiqueta_imagen.image = imagen  # Guardar referencia
    etiqueta_imagen.config(image=imagen)
    etiqueta_imagen.pack(pady=10)
except FileNotFoundError:
    print("Error: La imagen 'oit17.png' no se encuentra en la carpeta 'Assets'.")

# Frame para los botones
botones_frame = tk.Frame(nueva_ventana, bg="#3B8C6E")
botones_frame.pack(pady=10)

# Botones alineados horizontalmente
energia_button = ttk.Button(botones_frame, text="Energía", command=lambda: ChangeScreen('Energy.py'))
energia_button.grid(row=0, column=0, padx=10)

agua_button = ttk.Button(botones_frame, text="Agua", command=lambda: ChangeScreen('Water.py'))
agua_button.grid(row=0, column=1, padx=10)

# Mantener la ventana activa
nueva_ventana.mainloop()
