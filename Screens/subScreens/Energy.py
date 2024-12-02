import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
import importlib.util
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config 

def actualizar_valor(slider, label_var):
    """Actualiza el valor mostrado en el Label asociado al slider."""
    label_var.set(f"{slider.get():.0f}")
def calcular_huella():
    horas_diarias = horas_slider.get()
    aire_acondicionado = aire_var.get()
    luz_artificial = luz_slider.get()
    veces_electro = electro_slider.get()
    horas_dispositivos = dispositivos_slider.get()

    huella = (
        horas_diarias * 0.5
        + luz_artificial * 0.3
        + veces_electro * 0.2
        + horas_dispositivos * 0.4
        + (3 if aire_acondicionado else 0)
    )

    try:
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE usuarios
            SET EnergyScore = ?
            WHERE usuario = ?
        """, (huella, config.usuario_actual))
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        resultado_label.config(text=f"Error al actualizar la base de datos: {e}")
        return

    resultado_label.config(
        text=f"Tu huella energética aproximada es de: {huella:.2f} kWh diarios."
    )
    config.EnergyScore = True
    print(config.EnergyScore)

def exit():
    try:
        ventana.destroy()
        ruta_absoluta = os.path.abspath(f'Screens/SelectOption.py')
        spec = importlib.util.spec_from_file_location("modulo_seleccion", ruta_absoluta)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
    except Exception as e:
        print(f"Error al cambiar de pantalla: {e}")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Huella Energética")
ventana.geometry("500x670")
ventana.configure(bg="#3B8C6E")

# Crear estilo personalizado
style = ttk.Style()
style.theme_use("clam")
style.configure("TScale", background="#3B8C6E", foreground="#0B2B40")
style.configure("TButton", background="#0B2B40", foreground="white", font=("Arial", 10))

# Título
titulo = tk.Label(ventana, text="Calcula tu Huella Energética", font=("Arial", 16, "bold"), bg="#3B8C6E", fg="#0B2B40")
titulo.pack(pady=10)

# Variables para los valores de los sliders
electrodomesticos_valor = tk.StringVar()
horas_valor = tk.StringVar()

# Pregunta 2: ¿Cuántas horas al día utilizas electricidad?
horas_label = tk.Label(ventana, text="¿Cuántas horas al día utilizas electricidad?", bg="#3B8C6E", font=("Arial", 12))
horas_label.pack(anchor="w", padx=20, pady=5)
horas_slider = ttk.Scale(
    ventana, from_=0, to=24, orient="horizontal", length=300,
    command=lambda x: actualizar_valor(horas_slider, horas_valor)
)
horas_slider.set(8)
horas_slider.pack(pady=5, padx=20)
horas_valor_label = tk.Label(ventana, textvariable=horas_valor, bg="#3B8C6E", font=("Arial", 12))
horas_valor_label.pack()

# Pregunta 3: ¿Utilizas aire acondicionado?
aire_var = tk.IntVar()
aire_checkbox = ttk.Checkbutton(
    ventana, text="Uso aire acondicionado", variable=aire_var
)
aire_checkbox.pack(pady=5, padx=20)

# Pregunta 4: ¿Cuántas horas al día utilizas luz artificial?
luz_valor = tk.StringVar(value="8")
luz_label = tk.Label(ventana, text="¿Cuántas horas al día utilizas luz artificial?", bg="#3B8C6E", font=("Arial", 12))
luz_label.pack(anchor="w", padx=20, pady=5)
luz_slider = ttk.Scale(
    ventana, from_=0, to=24, orient="horizontal", length=300,
    command=lambda x: luz_valor.set(f"{int(float(x))}")
)
luz_slider.set(8)
luz_slider.pack(pady=5, padx=20)
luz_valor_label = tk.Label(ventana, textvariable=luz_valor, bg="#3B8C6E", font=("Arial", 12))
luz_valor_label.pack()


# Pregunta 5: ¿Cuántas veces usas electrodomésticos al día?
electro_valor = tk.StringVar(value="5")
electro_label = tk.Label(ventana, text="¿Cuántas veces usas electrodomésticos al día?", bg="#3B8C6E", font=("Arial", 12))
electro_label.pack(anchor="w", padx=20, pady=5)
electro_slider = ttk.Scale(
    ventana, from_=0, to=20, orient="horizontal", length=300,
    command=lambda x: electro_valor.set(f"{int(float(x))}")
)
electro_slider.set(5)
electro_slider.pack(pady=5, padx=20)
electro_valor_label = tk.Label(ventana, textvariable=electro_valor, bg="#3B8C6E", font=("Arial", 12))
electro_valor_label.pack()


# Pregunta 6: ¿Usas dispositivos electrónicos (como TV, computadora, etc.) diariamente? ¿Cuánto tiempo?
dispositivos_valor = tk.StringVar(value="4")
dispositivos_label = tk.Label(ventana, text="¿Cuántas horas al día usas dispositivos electrónicos?", bg="#3B8C6E", font=("Arial", 12))
dispositivos_label.pack(anchor="w", padx=20, pady=5)
dispositivos_slider = ttk.Scale(
    ventana, from_=0, to=16, orient="horizontal", length=300,
    command=lambda x: dispositivos_valor.set(f"{int(float(x))}")
)
dispositivos_slider.set(4)
dispositivos_slider.pack(pady=5, padx=20)
dispositivos_valor_label = tk.Label(ventana, textvariable=dispositivos_valor, bg="#3B8C6E", font=("Arial", 12))
dispositivos_valor_label.pack()


# Botón para calcular huella energética
calcular_button = ttk.Button(ventana, text="Calcular Huella Energética", command=calcular_huella)
calcular_button.pack(pady=20)

exit_button = ttk.Button(ventana, text="Salir", command=exit)
exit_button.pack(pady=20)

# Resultado
resultado_label = tk.Label(ventana, text="", bg="#3B8C6E", font=("Arial", 12), wraplength=550)
resultado_label.pack(pady=10, padx=20)

# Iniciar loop de la ventana
ventana.mainloop()
