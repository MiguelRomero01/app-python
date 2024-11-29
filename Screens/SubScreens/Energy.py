import tkinter as tk
from tkinter import ttk

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
ventana.geometry("500x500")
ventana.configure(bg="#f0f8ff")

# Título
titulo = tk.Label(ventana, text="Calcula tu Huella Hídrica", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#2c3e50")
titulo.pack(pady=10)

# Pregunta 1: ¿Cuántas duchas tomas al día?
duchas_label = tk.Label(ventana, text="¿Cuántas duchas tomas al día?", bg="#f0f8ff", font=("Arial", 12))
duchas_label.pack(anchor="w", padx=20, pady=5)
duchas_slider = ttk.Scale(ventana, from_=0, to=5, orient="horizontal", length=300)
duchas_slider.set(1)
duchas_slider.pack(pady=5, padx=20)

# Pregunta 2: ¿Cuánto dura una ducha promedio (en minutos)?
tiempo_label = tk.Label(ventana, text="¿Cuánto dura una ducha promedio (en minutos)?", bg="#f0f8ff", font=("Arial", 12))
tiempo_label.pack(anchor="w", padx=20, pady=5)
tiempo_slider = ttk.Scale(ventana, from_=0, to=30, orient="horizontal", length=300)
tiempo_slider.set(5)
tiempo_slider.pack(pady=5, padx=20)

# Pregunta 3: ¿Consumes agua embotellada diariamente?
botella_var = tk.IntVar()
botella_checkbox = ttk.Checkbutton(
    ventana, text="Consumo agua embotellada diariamente", variable=botella_var
)
botella_checkbox.pack(pady=5, padx=20)

# Pregunta 4: ¿Cómo describirías tu consumo de carne?
carne_label = tk.Label(ventana, text="¿Cómo describirías tu consumo de carne?", bg="#f0f8ff", font=("Arial", 12))
carne_label.pack(anchor="w", padx=20, pady=5)
carne_combobox = ttk.Combobox(ventana, values=["Alta", "Media", "Baja"], state="readonly")
carne_combobox.pack(pady=5, padx=20)
carne_combobox.set("Media")  # Valor por defecto

# Comentarios adicionales
comentarios_label = tk.Label(ventana, text="Comentarios adicionales:", bg="#f0f8ff", font=("Arial", 12))
comentarios_label.pack(anchor="w", padx=20, pady=5)
comentarios_text = tk.Text(ventana, height=4, width=40)
comentarios_text.pack(pady=5, padx=20)

# Botón para calcular huella hídrica
calcular_button = ttk.Button(ventana, text="Calcular Huella Hídrica", command=calcular_huella)
calcular_button.pack(pady=20)

# Resultado
resultado_label = tk.Label(ventana, text="", bg="#f0f8ff", font=("Arial", 12), wraplength=450)
resultado_label.pack(pady=10, padx=20)

# Iniciar loop de la ventana
ventana.mainloop()
