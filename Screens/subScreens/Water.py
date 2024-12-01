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
ventana.geometry("500x650")
ventana.configure(bg="#3B8C6E")

def actualizar_valor(slider, label_var):
    label_var.set(f"{slider.get():.0f}")

def calcular_huella():
    print(f"IMPORTANTEE: Usuario actual asignado en config en screen3: {config.usuario_actual}")
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
titulo = tk.Label(frame, text="Calcula tu Huella Hídrica", font=("Arial", 16, "bold"), bg="#3B8C6E", fg="#0B2B40")
titulo.pack(pady=10)

# Variables para mostrar valores
duchas_valor = tk.StringVar()
tiempo_valor = tk.StringVar()
grifo_valor = tk.StringVar()
ropa_valor = tk.StringVar()
coche_valor = tk.StringVar()
lavadora_valor = tk.StringVar()

# Pregunta 1: ¿Cuántas duchas tomas al día?
duchas_label = tk.Label(frame, text="¿Cuántas duchas tomas al día?", bg="#3B8C6E", font=("Arial", 12))
duchas_label.pack(anchor="w", padx=20, pady=5)
duchas_slider = ttk.Scale(
    frame, from_=0, to=5, orient="horizontal", length=300, command=lambda x: actualizar_valor(duchas_slider, duchas_valor)
)
duchas_slider.set(1)
duchas_slider.pack(pady=5, padx=20)
duchas_valor_label = tk.Label(frame, textvariable=duchas_valor, bg="#3B8C6E", font=("Arial", 12))
duchas_valor_label.pack()

# Pregunta 2: ¿Cuánto dura una ducha promedio (en minutos)?
tiempo_label = tk.Label(frame, text="¿Cuánto dura una ducha promedio (en minutos)?", bg="#3B8C6E", font=("Arial", 12))
tiempo_label.pack(anchor="w", padx=20, pady=5)
tiempo_slider = ttk.Scale(
    frame, from_=0, to=30, orient="horizontal", length=300, command=lambda x: actualizar_valor(tiempo_slider, tiempo_valor)
)
tiempo_slider.set(5)
tiempo_slider.pack(pady=5, padx=20)
tiempo_valor_label = tk.Label(frame, textvariable=tiempo_valor, bg="#3B8C6E", font=("Arial", 12))
tiempo_valor_label.pack()

# Pregunta 3: ¿Cuánto tiempo dejas el grifo abierto diariamente (en minutos)?
grifo_label = tk.Label(frame, text="¿Cuánto tiempo dejas el grifo abierto diariamente (en minutos)?", bg="#3B8C6E", font=("Arial", 12))
grifo_label.pack(anchor="w", padx=20, pady=5)
grifo_slider = ttk.Scale(
    frame, from_=0, to=60, orient="horizontal", length=300, command=lambda x: actualizar_valor(grifo_slider, grifo_valor)
)
grifo_slider.set(10)
grifo_slider.pack(pady=5, padx=20)
grifo_valor_label = tk.Label(frame, textvariable=grifo_valor, bg="#3B8C6E", font=("Arial", 12))
grifo_valor_label.pack()

# Pregunta 4: ¿Cuántas veces lavas ropa a la semana?
ropa_label = tk.Label(frame, text="¿Cuántas veces lavas ropa a la semana?", bg="#3B8C6E", font=("Arial", 12))
ropa_label.pack(anchor="w", padx=20, pady=5)
lavar_ropa_slider = ttk.Scale(
    frame, from_=0, to=10, orient="horizontal", length=300, command=lambda x: actualizar_valor(lavar_ropa_slider, ropa_valor)
)
lavar_ropa_slider.set(2)
lavar_ropa_slider.pack(pady=5, padx=20)
ropa_valor_label = tk.Label(frame, textvariable=ropa_valor, bg="#3B8C6E", font=("Arial", 12))
ropa_valor_label.pack()

# Pregunta 5: ¿Si tienes coche, cuántas veces lo lavas al mes?
coche_label = tk.Label(frame, text="¿Si tienes coche, cuántas veces lo lavas al mes?", bg="#3B8C6E", font=("Arial", 12))
coche_label.pack(anchor="w", padx=20, pady=5)
lavar_coche_slider = ttk.Scale(
    frame, from_=0, to=10, orient="horizontal", length=300, command=lambda x: actualizar_valor(lavar_coche_slider, coche_valor)
)
lavar_coche_slider.set(1)
lavar_coche_slider.pack(pady=5, padx=20)
coche_valor_label = tk.Label(frame, textvariable=coche_valor, bg="#3B8C6E", font=("Arial", 12))
coche_valor_label.pack()


# Pregunta 7: ¿Cómo describirías tu consumo de carne?
carne_label = tk.Label(frame, text="¿Cómo describirías tu consumo de carne?", bg="#3B8C6E", font=("Arial", 12))
carne_label.pack(anchor="w", padx=20, pady=5)
carne_combobox = ttk.Combobox(frame, values=["Alta", "Media", "Baja"], state="readonly")
carne_combobox.pack(pady=5, padx=20)
carne_combobox.set("Media")  # Valor por defecto

# Botón para calcular huella hídrica
calcular_button = ttk.Button(frame, text="Calcular Huella Hídrica", command=calcular_huella)
calcular_button.pack(pady=20)

#Boton para salir
salir_button = ttk.Button(frame, text="Salir", command=exit)
salir_button.pack(pady=20)

# Resultado
resultado_label = tk.Label(frame, text="", bg="#3B8C6E", font=("Arial", 12), wraplength=550)
resultado_label.pack(pady=10, padx=20)

# Actualizar el área visible para el canvas
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Iniciar la ventana
ventana.mainloop()
