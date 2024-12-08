import tkinter as tk
from tkinter import ttk
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
    """Realiza el cálculo de la huella eléctrica y actualiza el resultado."""
    try:
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

        config.EnergyScore = True

        # Mostrar resultados junto al promedio
        promedio_consumo = 35  # Promedio global de consumo mensual
        resultado_label.config(
            text=f"Tu huella eléctrica estimada es de: {huella_mensual:.2f} kWh mensuales.\n"
                 f"El consumo promedio global es de {promedio_consumo} kWh mensuales por persona."
        )
    except Exception as e:
        resultado_label.config(text=f"Error al calcular la huella eléctrica: {e}")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Huella Eléctrica")

# Obtener dimensiones de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

# Establecer el tamaño de la ventana
window_width = 500
window_height = 715

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

# Texto informativo resaltado
info_frame = tk.Frame(ventana, bg="#2C3E50", padx=10, pady=10, relief="groove")
info_frame.pack(fill="x", padx=20, pady=10)
info_label = tk.Label(
    info_frame,
    text="La huella eléctrica mide el consumo de energía que usas en tu hogar.",
    font=INFO_FONT,
    bg="#2C3E50",
    fg="#1ABC9C",
    wraplength=450,
    justify="center"
)
info_label.pack()

# Título
titulo = tk.Label(ventana, text="Calcula tu Huella Eléctrica", font=TITULO_FONT, bg="#3B8C6E", fg="#FFFFFF")
titulo.pack(pady=10, padx=20, anchor="w")

# Crear slider con valor al lado derecho
def crear_slider(padre, texto, desde, hasta, valor_inicial):
    frame = tk.Frame(padre, bg="#3B8C6E")
    frame.pack(fill="x", padx=20, pady=5)

    label = tk.Label(frame, text=texto, font=PREGUNTA_FONT, bg="#3B8C6E", fg="#FFFFFF")
    label.grid(row=0, column=0, sticky="w")

    slider = ttk.Scale(frame, from_=desde, to=hasta, orient="horizontal", length=300)
    slider.set(valor_inicial)
    slider.grid(row=1, column=0, sticky="w", padx=10)

    valor_label = tk.Label(frame, text=f"{valor_inicial:.0f}", font=VALOR_FONT, bg="#3B8C6E", fg="#FFFFFF")
    valor_label.grid(row=1, column=1, sticky="e", padx=10)

    slider.configure(command=lambda val: actualizar_valor_slider(slider, valor_label))
    return slider

# Preguntas
luces_slider = crear_slider(ventana, "¿Cuántas horas al día tienes luces encendidas?", 0, 24, 4)
dispositivos_label = tk.Label(ventana, text="¿Apagas dispositivos cuando no los usas?", font=PREGUNTA_FONT, bg="#3B8C6E", fg="#FFFFFF")
dispositivos_label.pack(anchor="w", padx=20, pady=5)
dispositivos_combobox = ttk.Combobox(ventana, values=["Sí", "No"], state="readonly")
dispositivos_combobox.pack(padx=20, pady=5)
dispositivos_combobox.set("Sí")

electrodomesticos_slider = crear_slider(ventana, "¿Cuántas veces usas electrodomésticos a la semana?", 0, 14, 5)
bombillas_label = tk.Label(ventana, text="¿Qué tipo de bombillas usas?", font=PREGUNTA_FONT, bg="#3B8C6E", fg="#FFFFFF")
bombillas_label.pack(anchor="w", padx=20, pady=5)
bombillas_combobox = ttk.Combobox(ventana, values=["LED", "Ahorradores", "Incandescentes"], state="readonly")
bombillas_combobox.pack(padx=20, pady=5)
bombillas_combobox.set("LED")

renovable_label = tk.Label(ventana, text="¿Usas energía renovable?", font=PREGUNTA_FONT, bg="#3B8C6E", fg="#FFFFFF")
renovable_label.pack(anchor="w", padx=20, pady=5)
renovable_combobox = ttk.Combobox(ventana, values=["Sí", "No"], state="readonly")
renovable_combobox.pack(padx=20, pady=5)
renovable_combobox.set("No")

# Botón para calcular
calcular_button = ttk.Button(ventana, text="Calcular Huella Eléctrica", command=calcular_huella)
calcular_button.pack(pady=20, padx=20, anchor="w")

# Resultado resaltado
resultado_frame = tk.Frame(ventana, bg="#2C3E50", padx=10, pady=10, relief="groove")
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
salir_button = ttk.Button(ventana, text="Salir", command=exit)
salir_button.pack(pady=20, padx=20, anchor="w")

# Iniciar ventana
ventana.mainloop()
