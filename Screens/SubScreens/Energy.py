import tkinter as tk
from tkinter import ttk

def actualizar_valor(slider, label_var):
    """Actualiza el valor mostrado en el Label asociado al slider."""
    label_var.set(f"{slider.get():.0f}")

def calcular_huella():
    # Obtener valores de los widgets
    duchas_diarias = duchas_slider.get()
    tiempo_ducha = tiempo_slider.get()
    agua_en_botella = botella_var.get()
    consumo_carne = carne_combobox.get()
    comentarios = comentarios_text.get("1.0", tk.END).strip()

    # Calcular una estimación sencilla de huella hídrica (en litros)
    huella = (
        duchas_diarias * tiempo_ducha * 9  # 9 litros/minuto promedio en una ducha
        + (1 if agua_en_botella else 0) * 5  # 5 litros por botella diaria
        + (500 if consumo_carne == "Alta" else 300 if consumo_carne == "Media" else 100)
    )

    # Mostrar resultados
    resultado_label.config(
        text=f"Tu huella hídrica aproximada es de: {huella:.2f} litros diarios.\nComentarios: {comentarios}"
    )

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Huella Hídrica")
ventana.geometry("500x600")
ventana.configure(bg="#3B8C6E")

# Crear estilo personalizado
style = ttk.Style()
style.theme_use("clam")
style.configure("TScale", background="#3B8C6E", foreground="#0B2B40")
style.configure("TButton", background="#0B2B40", foreground="white", font=("Arial", 10))

# Título
titulo = tk.Label(ventana, text="Calcula tu Huella Hídrica", font=("Arial", 16, "bold"), bg="#3B8C6E", fg="#0B2B40")
titulo.pack(pady=10)

# Variables para los valores de los sliders
duchas_valor = tk.StringVar()
tiempo_valor = tk.StringVar()

# Pregunta 1: ¿Cuántas duchas tomas al día?
duchas_label = tk.Label(ventana, text="¿Cuántas duchas tomas al día?", bg="#3B8C6E", font=("Arial", 12))
duchas_label.pack(anchor="w", padx=20, pady=5)
duchas_slider = ttk.Scale(
    ventana, from_=0, to=5, orient="horizontal", length=300,
    command=lambda x: actualizar_valor(duchas_slider, duchas_valor)
)
duchas_slider.set(1)
duchas_slider.pack(pady=5, padx=20)
duchas_valor_label = tk.Label(ventana, textvariable=duchas_valor, bg="#3B8C6E", font=("Arial", 12))
duchas_valor_label.pack()

# Pregunta 2: ¿Cuánto dura una ducha promedio (en minutos)?
tiempo_label = tk.Label(ventana, text="¿Cuánto dura una ducha promedio (en minutos)?", bg="#3B8C6E", font=("Arial", 12))
tiempo_label.pack(anchor="w", padx=20, pady=5)
tiempo_slider = ttk.Scale(
    ventana, from_=0, to=30, orient="horizontal", length=300,
    command=lambda x: actualizar_valor(tiempo_slider, tiempo_valor)
)
tiempo_slider.set(5)
tiempo_slider.pack(pady=5, padx=20)
tiempo_valor_label = tk.Label(ventana, textvariable=tiempo_valor, bg="#3B8C6E", font=("Arial", 12))
tiempo_valor_label.pack()

# Pregunta 3: ¿Consumes agua embotellada diariamente?
botella_var = tk.IntVar()
botella_checkbox = ttk.Checkbutton(
    ventana, text="Consumo agua embotellada diariamente", variable=botella_var
)
botella_checkbox.pack(pady=5, padx=20)

# Pregunta 4: ¿Cómo describirías tu consumo de carne?
carne_label = tk.Label(ventana, text="¿Cómo describirías tu consumo de carne?", bg="#3B8C6E", font=("Arial", 12))
carne_label.pack(anchor="w", padx=20, pady=5)
carne_combobox = ttk.Combobox(ventana, values=["Alta", "Media", "Baja"], state="readonly")
carne_combobox.pack(pady=5, padx=20)
carne_combobox.set("Media")  # Valor por defecto

# Comentarios adicionales
comentarios_label = tk.Label(ventana, text="Comentarios adicionales:", bg="#3B8C6E", font=("Arial", 12))
comentarios_label.pack(anchor="w", padx=20, pady=5)
comentarios_text = tk.Text(ventana, height=4, width=40)
comentarios_text.pack(pady=5, padx=20)

# Botón para calcular huella hídrica
calcular_button = ttk.Button(ventana, text="Calcular Huella Hídrica", command=calcular_huella)
calcular_button.pack(pady=20)

# Resultado
resultado_label = tk.Label(ventana, text="", bg="#3B8C6E", font=("Arial", 12), wraplength=450)
resultado_label.pack(pady=10, padx=20)

# Iniciar loop de la ventana
ventana.mainloop()
