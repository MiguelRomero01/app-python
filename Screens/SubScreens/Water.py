import tkinter as tk
from tkinter import ttk

def actualizar_valor(slider, label_var):
    """Actualiza el valor mostrado en el Label asociado al slider."""
    label_var.set(f"{slider.get():.0f}")

def calcular_huella():
    # Obtener valores de los sliders y otros widgets
    duchas_diarias = duchas_slider.get()
    tiempo_ducha = tiempo_slider.get()
    tiempo_grifo = grifo_slider.get()
    veces_lavar_ropa = lavar_ropa_slider.get()
    veces_lavar_coche = lavar_coche_slider.get()
    veces_lavadora = lavadora_slider.get()
    consumo_carne = carne_combobox.get()

    # Calcular la huella hídrica mensual (30 días por mes)
    huella_mensual = (
        duchas_diarias * tiempo_ducha * 1 * 30  # 1 litros/minuto promedio en una ducha
        + tiempo_grifo * 1 * 30  # 1 litros/minuto promedio con el grifo abierto
        + veces_lavar_coche * 150 * 4  # 150 litros por lavado de coche, 4 semanas al mes
        + veces_lavadora * 50 * 4  # 50 litros por uso de lavadora, 4 semanas al mes
        + (5 if consumo_carne == "Alta" else 10 if consumo_carne == "Media" else 15) * 30  # Consumo de carne mensual
    )

    # Mostrar resultados
    resultado_label.config(
        text=f"Tu huella hídrica aproximada es de: {huella_mensual:.2f} litros mensuales. Recuerda que una persona consume en promedio 3300L mensuales"
    )

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Huella Hídrica")
ventana.geometry("600x700")
ventana.configure(bg="#f0f8ff")

# Crear un Canvas con scrollbar
canvas = tk.Canvas(ventana)
scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Título
titulo = tk.Label(frame, text="Calcula tu Huella Hídrica", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#2c3e50")
titulo.pack(pady=10)

# Variables para mostrar valores
duchas_valor = tk.StringVar()
tiempo_valor = tk.StringVar()
grifo_valor = tk.StringVar()
ropa_valor = tk.StringVar()
coche_valor = tk.StringVar()
lavadora_valor = tk.StringVar()

# Pregunta 1: ¿Cuántas duchas tomas al día?
duchas_label = tk.Label(frame, text="¿Cuántas duchas tomas al día?", bg="#f0f8ff", font=("Arial", 12))
duchas_label.pack(anchor="w", padx=20, pady=5)
duchas_slider = ttk.Scale(frame, from_=0, to=5, orient="horizontal", length=300, command=lambda x: actualizar_valor(duchas_slider, duchas_valor))
duchas_slider.set(1)
duchas_slider.pack(pady=5, padx=20)
duchas_valor_label = tk.Label(frame, textvariable=duchas_valor, bg="#f0f8ff", font=("Arial", 12))
duchas_valor_label.pack()

# Pregunta 2: ¿Cuánto dura una ducha promedio (en minutos)?
tiempo_label = tk.Label(frame, text="¿Cuánto dura una ducha promedio (en minutos)?", bg="#f0f8ff", font=("Arial", 12))
tiempo_label.pack(anchor="w", padx=20, pady=5)
tiempo_slider = ttk.Scale(frame, from_=0, to=30, orient="horizontal", length=300, command=lambda x: actualizar_valor(tiempo_slider, tiempo_valor))
tiempo_slider.set(5)
tiempo_slider.pack(pady=5, padx=20)
tiempo_valor_label = tk.Label(frame, textvariable=tiempo_valor, bg="#f0f8ff", font=("Arial", 12))
tiempo_valor_label.pack()

# Pregunta 3: ¿Cuánto tiempo dejas el grifo abierto diariamente (en minutos)?
grifo_label = tk.Label(frame, text="¿Cuánto tiempo dejas el grifo abierto diariamente (en minutos)?", bg="#f0f8ff", font=("Arial", 12))
grifo_label.pack(anchor="w", padx=20, pady=5)
grifo_slider = ttk.Scale(frame, from_=0, to=60, orient="horizontal", length=300, command=lambda x: actualizar_valor(grifo_slider, grifo_valor))
grifo_slider.set(10)
grifo_slider.pack(pady=5, padx=20)
grifo_valor_label = tk.Label(frame, textvariable=grifo_valor, bg="#f0f8ff", font=("Arial", 12))
grifo_valor_label.pack()

# Pregunta 4: ¿Cuántas veces lavas ropa a la semana?
ropa_label = tk.Label(frame, text="¿Cuántas veces lavas ropa a la semana?", bg="#f0f8ff", font=("Arial", 12))
ropa_label.pack(anchor="w", padx=20, pady=5)
lavar_ropa_slider = ttk.Scale(frame, from_=0, to=10, orient="horizontal", length=300, command=lambda x: actualizar_valor(lavar_ropa_slider, ropa_valor))
lavar_ropa_slider.set(2)
lavar_ropa_slider.pack(pady=5, padx=20)
ropa_valor_label = tk.Label(frame, textvariable=ropa_valor, bg="#f0f8ff", font=("Arial", 12))
ropa_valor_label.pack()

# Pregunta 5: ¿Si tienes coche, cuántas veces lo lavas al mes?
coche_label = tk.Label(frame, text="¿Si tienes coche, cuántas veces lo lavas al mes?", bg="#f0f8ff", font=("Arial", 12))
coche_label.pack(anchor="w", padx=20, pady=5)
lavar_coche_slider = ttk.Scale(frame, from_=0, to=10, orient="horizontal", length=300, command=lambda x: actualizar_valor(lavar_coche_slider, coche_valor))
lavar_coche_slider.set(1)
lavar_coche_slider.pack(pady=5, padx=20)
coche_valor_label = tk.Label(frame, textvariable=coche_valor, bg="#f0f8ff", font=("Arial", 12))
coche_valor_label.pack()

# Pregunta 6: ¿Cuántas veces usas la lavadora por semana?
lavadora_label = tk.Label(frame, text="¿Cuántas veces usas la lavadora por semana?", bg="#f0f8ff", font=("Arial", 12))
lavadora_label.pack(anchor="w", padx=20, pady=5)
lavadora_slider = ttk.Scale(frame, from_=0, to=14, orient="horizontal", length=300, command=lambda x: actualizar_valor(lavadora_slider, lavadora_valor))
lavadora_slider.set(3)
lavadora_slider.pack(pady=5, padx=20)
lavadora_valor_label = tk.Label(frame, textvariable=lavadora_valor, bg="#f0f8ff", font=("Arial", 12))
lavadora_valor_label.pack()

# Pregunta 7: ¿Cómo describirías tu consumo de carne?
carne_label = tk.Label(frame, text="¿Cómo describirías tu consumo de carne?", bg="#f0f8ff", font=("Arial", 12))
carne_label.pack(anchor="w", padx=20, pady=5)
carne_combobox = ttk.Combobox(frame, values=["Alta", "Media", "Baja"], state="readonly")
carne_combobox.pack(pady=5, padx=20)
carne_combobox.set("Media")  # Valor por defecto

# Botón para calcular huella hídrica
calcular_button = ttk.Button(frame, text="Calcular Huella Hídrica", command=calcular_huella)
calcular_button.pack(pady=20)

# Resultado
resultado_label = tk.Label(frame, text="", bg="#f0f8ff", font=("Arial", 12), wraplength=550)
resultado_label.pack(pady=10, padx=20)

# Actualizar el área visible para el canvas
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Iniciar la ventana
ventana.mainloop()
