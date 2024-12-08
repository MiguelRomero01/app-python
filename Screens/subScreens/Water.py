import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
import importlib.util

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Huella Hídrica")

# Obtener dimensiones de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

# Establecer el tamaño de la ventana
window_width = 550
window_height = 600

# Calcular la posición para centrar la ventana
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Configurar la geometría para centrar la ventana
ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
ventana.configure(bg="#3B8C6E")

# Configuración de fuentes
TITULO_FONT = ("Arial", 18, "bold")
PREGUNTA_FONT = ("Arial", 12)
VALOR_FONT = ("Arial", 12, "bold")
RESULTADO_FONT = ("Arial", 14, "bold")
INFO_FONT = ("Arial", 13, "bold italic")

# Crear un Canvas con scrollbar
canvas = tk.Canvas(ventana, bg="#3B8C6E", highlightthickness=0)
scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas, bg="#3B8C6E")

canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Texto informativo resaltado
info_frame = tk.Frame(frame, bg="#2C3E50", padx=10, pady=10, relief="groove")
info_frame.pack(fill="x", padx=20, pady=10)
info_label = tk.Label(
    info_frame,
    text=(
        "La huella hídrica mide el uso de agua directo e indirecto.\n"
        "El consumo promedio global es de 3000 litros diarios por persona."
    ),
    font=INFO_FONT,
    bg="#2C3E50",
    fg="#1ABC9C",
    wraplength=450,
    justify="center"
)
info_label.pack()

# Título
titulo = tk.Label(frame, 
                  text="Calcula tu Huella Hídrica", 
                  font=TITULO_FONT, 
                  bg="#3B8C6E", 
                  fg="#FFFFFF")
titulo.pack(pady=10, padx=20, anchor="w")

# Función para actualizar el valor mostrado de cada slider
def actualizar_valor(slider, label_var, valor_label):
    valor_actual = slider.get()
    label_var.set(f"{valor_actual:.0f}")
    valor_label.config(text=f"{valor_actual:.0f}")

def crear_slider(frame, texto, desde, hasta, variable, color="#FFFFFF"):
    contenedor = tk.Frame(frame, bg="#3B8C6E")
    contenedor.pack(pady=10, fill="x", padx=20)
    
    etiqueta = tk.Label(contenedor, text=texto, bg="#3B8C6E", fg=color, font=PREGUNTA_FONT)
    etiqueta.grid(row=0, column=0, sticky="w")
    
    slider = ttk.Scale(contenedor, from_=desde, to=hasta, orient="horizontal", length=300,
                       command=lambda x: actualizar_valor(slider, variable, valor_label))
    slider.grid(row=1, column=0, pady=5)
    
    valor_label = tk.Label(contenedor, text="0", bg="#3B8C6E", fg=color, font=VALOR_FONT)
    valor_label.grid(row=1, column=1, padx=10)
    
    return slider

# Variables para sliders
duchas_valor = tk.StringVar()
tiempo_valor = tk.StringVar()
grifo_valor = tk.StringVar()
ropa_valor = tk.StringVar()
coche_valor = tk.StringVar()

# Sliders
duchas_slider = crear_slider(frame, "¿Cuántas duchas tomas al día?", 0, 5, duchas_valor)
tiempo_slider = crear_slider(frame, "¿Cuánto dura una ducha promedio (en minutos)?", 0, 30, tiempo_valor)
grifo_slider = crear_slider(frame, "¿Cuánto tiempo dejas el grifo abierto diariamente (en minutos)?", 0, 60, grifo_valor)
lavar_ropa_slider = crear_slider(frame, "¿Cuántas veces lavas ropa a la semana?", 0, 10, ropa_valor)
lavar_coche_slider = crear_slider(frame, "¿Si tienes coche, cuántas veces lo lavas al mes?", 0, 10, coche_valor)

# Combobox
carne_label = tk.Label(frame, text="¿Cómo describirías tu consumo de carne?", bg="#3B8C6E", fg="#FFFFFF", font=PREGUNTA_FONT)
carne_label.pack(anchor="w", padx=20, pady=5)
carne_combobox = ttk.Combobox(frame, values=["Alta", "Media", "Baja"], state="readonly")
carne_combobox.pack(pady=5, padx=20, anchor="w")
carne_combobox.set("Media")  # Valor por defecto

# Función para calcular huella hídrica
def calcular_huella():
    # Recupera las respuestas del usuario
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

    # Cálculo de huella hídrica
    huella_mensual = (
        duchas_diarias * tiempo_ducha * flujo_ducha * 30 +
        tiempo_grifo * flujo_grifo * 30 +
        veces_lavar_ropa * litros_lavadora * 4 +
        veces_lavar_coche * litros_coche +
        carne_dict.get(consumo_carne, 0) * 30
    )

    # Muestra el resultado con comparación promedio
    resultado = f"Tu huella hídrica aproximada es de {huella_mensual:.2f} litros mensuales.\n"
    promedio = "El consumo promedio global es de 3000 litros diarios por persona."
    resultado_label.config(text=resultado + promedio)

# Botón para calcular huella hídrica
calcular_button = ttk.Button(frame, text="Calcular Huella Hídrica", command=calcular_huella)
calcular_button.pack(pady=20, anchor="w", padx=20)

# Resultado resaltado
resultado_frame = tk.Frame(frame, bg="#2C3E50", padx=10, pady=10, relief="groove")
resultado_frame.pack(fill="x", padx=20, pady=10)
resultado_label = tk.Label(
    resultado_frame,
    text="",
    font=RESULTADO_FONT,
    bg="#2C3E50",
    fg="#1ABC9C",
    wraplength=450,
    justify="center"
)
resultado_label.pack()

# Botón para salir
salir_button = ttk.Button(frame, text="Salir", command=ventana.destroy)
salir_button.pack(pady=20, anchor="w", padx=20)

# Actualizar área del canvas
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Iniciar ventana
ventana.mainloop()
