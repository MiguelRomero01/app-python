import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys
import sqlite3  # Necesario para la conexión a la base de datos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import config  # Importar el archivo de configuración compartida

# Crear la nueva ventana como Toplevel
home_ventana = tk.Toplevel()
home_ventana.title("Opciones")
home_ventana.geometry("500x500")
home_ventana.configure(bg="#3B8C6E")

# Centrar la ventana
ancho_ventana = 500
alto_ventana = 500
ancho_pantalla = home_ventana.winfo_screenwidth()
alto_pantalla = home_ventana.winfo_screenheight()
pos_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
pos_y = (alto_pantalla // 2) - (alto_ventana // 2)
home_ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

# Título
titulo = ttk.Label(home_ventana, text="Selecciona una Opción", font=("Arial", 16, "bold"), background="#3B8C6E", foreground="white")
titulo.pack(pady=20)

# Crear variables para el precio del metro cúbico de agua, precio de electricidad y el consumo
precio_metro_cubico = tk.DoubleVar()
precio_electricidad = tk.DoubleVar()
consumo_agua = tk.DoubleVar()
consumo_electricidad = tk.DoubleVar()

# Función para calcular los gastos de agua y electricidad
def calcular_gasto():
    precio_agua = precio_metro_cubico.get()
    precio_elec = precio_electricidad.get()
    
    try:
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        
        # Obtener el consumo de agua y electricidad para el usuario actual
        cursor.execute("""SELECT waterScore, energyScore FROM usuarios WHERE usuario = ?""", (config.usuario_actual,))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado:
            consumo_agua.set(resultado[0])  # Consumo mensual en litros
            consumo_electricidad.set(resultado[1])  # Consumo mensual en kWh
        else:
            raise ValueError("No se encontró el usuario.")
        
        # Calcular los gastos
        gasto_agua = consumo_agua.get() * precio_agua / 1000  # Convertir agua a metros cúbicos
        gasto_electricidad = consumo_electricidad.get() * precio_elec  # El precio ya está en kWh
        
        # Mostrar un mensaje con los resultados
        messagebox.showinfo(
            "Gastos Mensuales",
            f"Gasto en agua: ${gasto_agua:.2f}\nGasto en electricidad: ${gasto_electricidad:.2f}"
        )
        return gasto_agua, gasto_electricidad
    except Exception as e:
        print(f"Error al calcular el gasto: {e}")
        return 0, 0

# Función para mostrar la gráfica de barras
def mostrar_grafica_barras():
    gasto_agua, gasto_electricidad = calcular_gasto()
    
    if gasto_agua == 0 and gasto_electricidad == 0:
        return  # No generar gráfica si no hay datos
    
    # Crear una nueva ventana para la gráfica de barras
    grafica_ventana = tk.Toplevel(home_ventana)
    grafica_ventana.title("Gráfica de Gastos")
    grafica_ventana.geometry("600x500")

    # Datos para la gráfica de barras
    servicios = ['Agua', 'Electricidad']
    gastos = [gasto_agua, gasto_electricidad]
    colores = ['blue', 'yellow']  # Colores para cada servicio
    
    # Crear una figura para la gráfica de barras
    fig, ax = plt.subplots(figsize=(5, 4))  # Ajustamos el tamaño de la gráfica
    
    ax.bar(servicios, gastos, color=colores)
    ax.set_xlabel('Tipo de Servicio')
    ax.set_ylabel('Gasto en Pesos')
    ax.set_title('Gasto mensual en servicios (Agua y Electricidad)')
    
    # Ajustar el límite superior del eje Y
    ax.set_ylim(0, max(gastos) * 1.2)  # Establecer el valor máximo un 20% más alto que el gasto

    # Mostrar la gráfica en la nueva ventana
    canvas = FigureCanvasTkAgg(fig, master=grafica_ventana)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Función para mostrar la gráfica de pastel
def mostrar_grafica_pie():
    gasto_agua, gasto_electricidad = calcular_gasto()
    
    if gasto_agua == 0 and gasto_electricidad == 0:
        return  # No generar gráfica si no hay datos
    
    # Crear una nueva ventana para la gráfica
    grafica_ventana = tk.Toplevel(home_ventana)
    grafica_ventana.title("Gráfica de Gastos")
    grafica_ventana.geometry("600x500")

    # Datos para la gráfica
    servicios = ['Agua', 'Electricidad']
    gastos = [gasto_agua, gasto_electricidad]
    
    # Crear una figura para la gráfica de pastel
    fig, ax = plt.subplots(figsize=(5, 4))  # Ajustamos el tamaño de la gráfica
    
    ax.pie(gastos, labels=servicios, autopct='%1.1f%%', colors=['blue', 'yellow'], startangle=90)
    ax.set_title('Distribución de gasto mensual en servicios')

    # Mostrar la gráfica en la nueva ventana
    canvas = FigureCanvasTkAgg(fig, master=grafica_ventana)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Entrada para el precio del metro cúbico de agua
precio_agua_label = ttk.Label(home_ventana, text="Precio del metro cúbico de agua (COP):", font=("Arial", 12), background="#3B8C6E", foreground="white")
precio_agua_label.pack(pady=10)

precio_agua_entry = ttk.Entry(home_ventana, textvariable=precio_metro_cubico, font=("Arial", 12))
precio_agua_entry.pack(pady=5)

# Entrada para el precio de la electricidad
precio_electricidad_label = ttk.Label(home_ventana, text="Precio de la electricidad (COP/kWh):", font=("Arial", 12), background="#3B8C6E", foreground="white")
precio_electricidad_label.pack(pady=10)

precio_electricidad_entry = ttk.Entry(home_ventana, textvariable=precio_electricidad, font=("Arial", 12))
precio_electricidad_entry.pack(pady=5)

# Botón para mostrar la gráfica de barras
grafica_barras_button = ttk.Button(home_ventana, text="Calcular y ver gráfica de barras", command=mostrar_grafica_barras)
grafica_barras_button.pack(pady=10)

# Botón para mostrar la gráfica de líneas
grafica_lineas_button = ttk.Button(home_ventana, text="Calcular y ver gráfico de pie", command=mostrar_grafica_pie)
grafica_lineas_button.pack(pady=10)



# Mantener la ventana activa
home_ventana.mainloop()
