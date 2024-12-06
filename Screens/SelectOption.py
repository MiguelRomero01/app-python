import tkinter as tk
from tkinter import ttk
import os
import sys
import importlib.util
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import config  # Importar el archivo de configuración compartida

def ChangeScreen(path):
    print(f"IMPORTANTEE: Usuario actual asignado en config pantalla2: {config.usuario_actual}")
    print(config.waterScore)
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

# Obtener el tamaño de la pantalla
screen_width = nueva_ventana.winfo_screenwidth()
screen_height = nueva_ventana.winfo_screenheight()

# Establecer el tamaño de la ventana
window_width = 650
window_height = 820

# Calcular la posición para centrar la ventana
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Configurar la geometría para centrar la ventana
nueva_ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
nueva_ventana.configure(bg="#3B8C6E")

imagen = tk.PhotoImage(file="Assets/oit17.png")

# Crear un widget Label y asignarle la imagen
etiqueta = tk.Label(nueva_ventana, image=imagen)
etiqueta.pack()

# Título
titulo = ttk.Label(nueva_ventana, text="Selecciona una Opción", font=("Arial", 16, "bold"), background="#3B8C6E", foreground="white")
titulo.pack(pady=20)

# Frame para los botones
botones_frame = tk.Frame(nueva_ventana, bg="#3B8C6E")
botones_frame.pack(pady=10)

# Botones alineados horizontalmente
energia_button = ttk.Button(botones_frame, text="Energía", command=lambda: ChangeScreen('SubScreens/Energy.py'))
energia_button.grid(row=0, column=0, padx=10)

agua_button = ttk.Button(botones_frame, text="Agua", command=lambda: ChangeScreen('SubScreens/Water.py'))
agua_button.grid(row=0, column=1, padx=10)

if(config.waterScore and config.EnergyScore):
    Analysis_button = ttk.Button(botones_frame, text='Descubre tu resultado', command=lambda: ChangeScreen('Home.py'))
    Analysis_button.grid(row=1, column=0, columnspan=2, pady=15, sticky="ew")

# Mantener la ventana activa
nueva_ventana.mainloop()
