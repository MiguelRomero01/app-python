import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
import importlib.util
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config 

def actualizar_valor_slider(slider, label):
    """Actualiza la etiqueta con el valor actual del slider."""
    valor = slider.get()
    label.config(text=f"{valor:.0f}")  # Mostrar valor entero

def exit():
    try:
        ventana.destroy()
        ruta_absoluta = os.path.abspath(f'Screens/SelectOption.py')
        spec = importlib.util.spec_from_file_location("modulo_seleccion", ruta_absoluta)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
    except Exception as e:
        print(f"Error al cambiar de pantalla: {e}")

def calcular_huella():
    # Obtener valores de los controles
    horas_luces = luces_slider.get()
    dispositivos_apagados = dispositivos_combobox.get()
    frecuencia_electrodomesticos = electrodomesticos_slider.get()
    tipo_bombillas = bombillas_combobox.get().lower()
    energia_renovable = renovable_combobox.get()

    # Factores de consumo estimado
    consumo_luces = horas_luces * 0.06 * 30  # kWh por luces encendidas (30 días al mes)
    consumo_dispositivos = 10 if dispositivos_apagados == "Sí" else 20  # kWh mensuales
    consumo_electrodomesticos = frecuencia_electrodomesticos * 3  # kWh por uso semanal
    consumo_bombillas = 0 if tipo_bombillas == "led" else (15 if tipo_bombillas == "ahorradores" else 30)
    descuento_renovable = 0.8 if energia_renovable == "Sí" else 1.0  # Reducción por energía renovable

    # Calcular huella mensual
    huella_mensual = (
        consumo_luces + consumo_dispositivos + consumo_electrodomesticos + consumo_bombillas
    ) * descuento_renovable

    # Mostrar resultados
    resultado_label.config(
        text=f"Tu huella eléctrica estimada es de: {huella_mensual:.2f} kWh mensuales.\n"
             f"Recuerda que el promedio es de 35 kWh mensuales por persona."
    )


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Huella Eléctrica")
ventana.geometry("500x700")
ventana.configure(bg="#3B8C6E")

# Título
titulo = tk.Label(ventana, text="Calcula tu Huella Eléctrica", font=("Arial", 16, "bold"), bg="#3B8C6E", fg="#0B2B40")
titulo.pack(pady=10)

# Pregunta 1: Horas de luz encendidas
luces_label = tk.Label(ventana, text="¿Cuántas horas al día tienes luces encendidas?", bg="#3B8C6E", font=("Arial", 12))
luces_label.pack(anchor="w", padx=20, pady=5)
luces_slider = ttk.Scale(ventana, from_=0, to=24, orient="horizontal", length=300)
luces_slider.set(4)
luces_slider.pack(pady=5, padx=20)
luces_valor_label = tk.Label(ventana, text="4", bg="#3B8C6E", font=("Arial", 12))
luces_valor_label.pack()
luces_slider.configure(command=lambda val: actualizar_valor_slider(luces_slider, luces_valor_label))

# Pregunta 2: Apagas dispositivos
dispositivos_label = tk.Label(ventana, text="¿Apagas dispositivos cuando no los usas?", bg="#3B8C6E", font=("Arial", 12))
dispositivos_label.pack(anchor="w", padx=20, pady=5)
dispositivos_combobox = ttk.Combobox(ventana, values=["Sí", "No"], state="readonly")
dispositivos_combobox.pack(pady=5, padx=20)
dispositivos_combobox.set("Sí")  # Valor por defecto

# Pregunta 3: Frecuencia de uso de electrodomésticos
electrodomesticos_label = tk.Label(ventana, text="¿Cuántas veces usas electrodomésticos a la semana?", bg="#3B8C6E", font=("Arial", 12))
electrodomesticos_label.pack(anchor="w", padx=20, pady=5)
electrodomesticos_slider = ttk.Scale(ventana, from_=0, to=14, orient="horizontal", length=300)
electrodomesticos_slider.set(5)
electrodomesticos_slider.pack(pady=5, padx=20)
electrodomesticos_valor_label = tk.Label(ventana, text="5", bg="#3B8C6E", font=("Arial", 12))
electrodomesticos_valor_label.pack()
electrodomesticos_slider.configure(command=lambda val: actualizar_valor_slider(electrodomesticos_slider, electrodomesticos_valor_label))

# Pregunta 4: Tipo de bombillas
bombillas_label = tk.Label(ventana, text="¿Qué tipo de bombillas usas?", bg="#3B8C6E", font=("Arial", 12))
bombillas_label.pack(anchor="w", padx=20, pady=5)
bombillas_combobox = ttk.Combobox(ventana, values=["LED", "Ahorradores", "Incandescentes"], state="readonly")
bombillas_combobox.pack(pady=5, padx=20)
bombillas_combobox.set("LED")  # Valor por defecto

# Pregunta 5: Energía renovable
renovable_label = tk.Label(ventana, text="¿Usas energía renovable?", bg="#3B8C6E", font=("Arial", 12))
renovable_label.pack(anchor="w", padx=20, pady=5)
renovable_combobox = ttk.Combobox(ventana, values=["Sí", "No"], state="readonly")
renovable_combobox.pack(pady=5, padx=20)
renovable_combobox.set("No")  # Valor por defecto

# Botón para calcular
calcular_button = ttk.Button(ventana, text="Calcular Huella Eléctrica", command=calcular_huella)
calcular_button.pack(pady=20)

#Boton para salir
salir_button = ttk.Button(ventana, text="Salir", command=exit)
salir_button.pack(pady=20)

# Resultado
resultado_label = tk.Label(ventana, text="", bg="#3B8C6E", font=("Arial", 12), wraplength=450)
resultado_label.pack(pady=10)

# Iniciar ventana
ventana.mainloop()
