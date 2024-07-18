import tkinter as tk
from tkinter import messagebox
import mysql.connector
import math

# Conexión a la base de datos
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",   
        password="", 
        database="cantidad_economica_de_pedido" 
    )
#     /* CREATE TABLE resultados (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     demanda_anual DECIMAL(15,2) NOT NULL,
#     costo_pedidos DECIMAL(15,2) NOT NULL,
#     costo_unidad DECIMAL(15,2) NOT NULL,
#     costo_mantenimiento DECIMAL(15,2) NOT NULL,
#     tiempo_entrega INT NOT NULL,
#     tamano_optimo_pedido INT NOT NULL,
#     num_pedidos INT NOT NULL,
#     dias_entre_ordenes INT NOT NULL,
#     punto_reorden INT NOT NULL
# */ );

# Función para calcular y guardar los resultados
def calcular_y_guardar():
    try:
        D = int(entry_D.get())
        A = int(entry_A.get())
        v = int(entry_v.get())
        r = float(entry_r.get())
        L = int(entry_L.get())

        # Calcular tamaño óptimo de pedido (Q)
        Q = math.sqrt((2 * D * A) / (v * r))
        
        # Número de pedidos al año
        num_pedidos = D / Q
        
        # Días entre órdenes
        dias_entre_ordenes = 365 / num_pedidos
        
        # Punto de reorden (R)
        R = (D * L) / 365

        Q = int(Q)
        num_peidos = int(num_pedidos)
        dias_entre_ordenes = int(dias_entre_ordenes)
        R=int(R)
        
        # Guardar en base de datos
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "INSERT INTO resultados (demanda_anual, costo_pedidos, costo_unidad, costo_mantenimiento, tiempo_entrega, tamano_optimo_pedido, num_pedidos, dias_entre_ordenes, punto_reorden) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (D, A, v, r, L, Q, num_pedidos, dias_entre_ordenes, R)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        # Mostrar resultados
        messagebox.showinfo("Resultados", f"El tamaño óptimo de pedido es: {Q:.2f}\nNúmero de pedidos al año: {num_pedidos:.2f}\nDías entre órdenes: {dias_entre_ordenes:.2f}\nPunto de reorden: {R:.2f}")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Configuración de la ventana principal
root = tk.Tk()
root.title("Administración de Proyectos")
root.geometry("600x400")


# Colores y estilo
frame = tk.Frame(root, bg="lavender", bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.8, anchor="n")

label_style = {"bg": "white", "fg": "black", "font": ("Helvetica", 12)}
entry_style = {"font": ("Helvetica", 12)}

tk.Label(frame, text="Demanda anual (D)", **label_style).grid(row=0, column=0, pady=10, padx=10, sticky="w")
entry_D = tk.Entry(frame, **entry_style)
entry_D.grid(row=0, column=1, pady=10, padx=10)

tk.Label(frame, text="Costo de hacer pedidos (A)", **label_style).grid(row=1, column=0, pady=10, padx=10, sticky="w")
entry_A = tk.Entry(frame, **entry_style)
entry_A.grid(row=1, column=1, pady=10, padx=10)

tk.Label(frame, text="Costo por unidad (v)", **label_style).grid(row=2, column=0, pady=10, padx=10, sticky="w")
entry_v = tk.Entry(frame, **entry_style)
entry_v.grid(row=2, column=1, pady=10, padx=10)

tk.Label(frame, text="Costo de mantenimiento (r)", **label_style).grid(row=3, column=0, pady=10, padx=10, sticky="w")
entry_r = tk.Entry(frame, **entry_style)
entry_r.grid(row=3, column=1, pady=10, padx=10)

tk.Label(frame, text="Tiempo de entrega (L)", **label_style).grid(row=4, column=0, pady=10, padx=10, sticky="w")
entry_L = tk.Entry(frame, **entry_style)
entry_L.grid(row=4, column=1, pady=10, padx=10)

button = tk.Button(frame, text="Calcular y Guardar", command=calcular_y_guardar, bg="white", fg="black", font=("Helvetica", 12))
button.grid(row=5, columnspan=2, pady=20)

root.mainloop()