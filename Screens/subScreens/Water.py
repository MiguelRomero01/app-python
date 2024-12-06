import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
import importlib.util
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config 

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Huella Hídrica")

# Obtener dimensiones de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

# Establecer el tamaño de la ventana
window_width = 500
window_height = 800

# Calcular la posición para centrar la ventana
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Configurar la geometría para centrar la ventana
ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
ventana.configure(bg="#3B8C6E")

# Función para actualizar el valor mostrado de cada slider
def actualizar_valor(slider, label_var):
    label_var.set(f"{slider.get():.0f}")

def calcular_huella():
    print(f"IMPORTANTE: Usuario actual asignado en config en screen3: {config.usuario_actual}")
    if config.usuario_actual is None:
        resultado_label.config(text="Error: No se detectó un usuario logueado.")
        return
    
    duchas_diarias = duchas_slider.get()
    tiempo_ducha = tiempo_slider.get()
    tiempo_grifo = grifo_slider.get()
    veces_lavar_ropa = lavar_ropa_slider.get()
    veces_lavar_coche = lavar_coche_slider.get()
    consumo_carne = carne_combobox.get()

    flujo_ducha = 10  # litros/minuto
    flujo_grifo = 9  # litros/minuto
    litros_lavadora = 50  # litros por carga
    litros_coche = 150  # litros por lavado
    carne_dict = {"Alta": 500, "Media": 333, "Baja": 100}

    huella_mensual = (
        duchas_diarias * tiempo_ducha * flujo_ducha * 30 +
        tiempo_grifo * flujo_grifo * 30 +
        veces_lavar_ropa * litros_lavadora * 4 +
        veces_lavar_coche * litros_coche +
        carne_dict.get(consumo_carne, 0) * 30
    )

    # Actualizar en la base de datos
    try:
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE usuarios
            SET waterScore = ?
            WHERE usuario = ?
        """, (huella_mensual, config.usuario_actual))
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        resultado_label.config(text=f"Error al actualizar la base de datos: {e}")
        return

    resultado_label.config(
        text=f"Tu huella hídrica aproximada es de: {huella_mensual:.2f} litros mensuales."
    )
    config.waterScore = True
    print(config.waterScore)

# Función para salir y cargar una pantalla diferente
def exit():
    try:
        ventana.destroy()
        ruta_absoluta = os.path.abspath(f'Screens/SelectOption.py')
        spec = importlib.util.spec_from_file_location("modulo_seleccion", ruta_absoluta)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
    except Exception as e:
        print(f"Error al cambiar de pantalla: {e}")

# Crear estilo personalizado
style = ttk.Style()
style.theme_use("clam")
style.configure("TScrollbar", troughcolor="#3B8C6E", background="#0B2B40", arrowcolor="white")
style.configure("TScale", background="#3B8C6E")
style.configure("TButton", background="#2C3E50", foreground="white", font=("Arial", 10))
style.configure("TCombobox", fieldbackground="#3B8C6E", background="#3B8C6E")

# Crear un Canvas con scrollbar
canvas = tk.Canvas(ventana, bg="#3B8C6E", highlightthickness=0)
scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=canvas.yview, style="TScrollbar")
frame = tk.Frame(canvas, bg="#3B8C6E")

canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Título
titulo = tk.Label(frame, text="Calcula tu Huella Hídrica", font=("Arial", 16, "bold"), bg="#3B8C6E", fg="#FFFFFF")
titulo.pack(pady=10)

# Crear variables para mostrar valores
def crear_slider(frame, texto, desde, hasta, variable, color="#FFFFFF"):
    etiqueta = tk.Label(frame, text=texto, bg="#3B8C6E", fg=color, font=("Arial", 12))
    etiqueta.pack(anchor="w", padx=20, pady=5)
    slider = ttk.Scale(frame, from_=desde, to=hasta, orient="horizontal", length=300,
                       command=lambda x: actualizar_valor(slider, variable))
    slider.pack(pady=5, padx=20)
    valor_label = tk.Label(frame, textvariable=variable, bg="#3B8C6E", fg=color, font=("Arial", 12))
    valor_label.pack()
    return slider

# Variables para mostrar valores
duchas_valor = tk.StringVar()
tiempo_valor = tk.StringVar()
grifo_valor = tk.StringVar()
ropa_valor = tk.StringVar()
coche_valor = tk.StringVar()

# Pregunta 1: ¿Cuántas duchas tomas al día?
duchas_slider = crear_slider(frame, "¿Cuántas duchas tomas al día?", 0, 5, duchas_valor)

# Pregunta 2: ¿Cuánto dura una ducha promedio (en minutos)?
tiempo_slider = crear_slider(frame, "¿Cuánto dura una ducha promedio (en minutos)?", 0, 30, tiempo_valor)

# Pregunta 3: ¿Cuánto tiempo dejas el grifo abierto diariamente (en minutos)?
grifo_slider = crear_slider(frame, "¿Cuánto tiempo dejas el grifo abierto diariamente (en minutos)?", 0, 60, grifo_valor)

# Pregunta 4: ¿Cuántas veces lavas ropa a la semana?
lavar_ropa_slider = crear_slider(frame, "¿Cuántas veces lavas ropa a la semana?", 0, 10, ropa_valor)

# Pregunta 5: ¿Si tienes coche, cuántas veces lo lavas al mes?
lavar_coche_slider = crear_slider(frame, "¿Si tienes coche, cuántas veces lo lavas al mes?", 0, 10, coche_valor)

# Pregunta 6: ¿Cómo describirías tu consumo de carne?
carne_label = tk.Label(frame, text="¿Cómo describirías tu consumo de carne?", bg="#3B8C6E", font=("Arial", 12))
carne_label.pack(anchor="w", padx=20, pady=5)
carne_combobox = ttk.Combobox(frame, values=["Alta", "Media", "Baja"], state="readonly")
carne_combobox.pack(pady=5, padx=20)
carne_combobox.set("Media")  # Valor por defecto

# Botón para calcular huella hídrica
calcular_button = ttk.Button(frame, text="Calcular Huella Hídrica", command=calcular_huella)
calcular_button.pack(pady=20)

# Botón para salir
salir_button = ttk.Button(frame, text="Salir", command=exit)
salir_button.pack(pady=20)

# Resultado
resultado_label = tk.Label(frame, text="", font=("Arial", 12), wraplength=550, bg="#3B8C6E", fg="white")
resultado_label.pack(pady=10, padx=20)

# Actualizar el área visible para el canvas
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Iniciar la ventana
ventana.mainloop()
