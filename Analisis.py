import tkinter as tk
from tkinter import messagebox, filedialog,ttk
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit


import cv2


# Variable global para almacenar los datos importados
datos = None

# Variable global para almacenar la ruta del archivo CSV
archivo_csv = None

# Variable global para contar objetos detectados
objetos_detectados = 0

def importar_csv():
    global archivo_csv, datos
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo_csv:
        datos = pd.read_csv(archivo_csv)
        messagebox.showinfo("Éxito", f"Archivo CSV '{archivo_csv}' importado correctamente.")
        realizar_eda()
        realizar_boxplot()
        realizar_regresion_lineal()

def realizar_eda():
    if datos is not None:
        # Crear una nueva pestaña para el análisis descriptivo
        pestaña_descriptivo = ttk.Frame(notebook)
        notebook.add(pestaña_descriptivo, text="Análisis Descriptivo")

        # Mostrar estadísticas descriptivas básicas
        with pd.option_context('display.float_format', '{:.2f}'.format):
            estadisticas_descriptivas = datos.describe()
        texto_descriptivo = tk.Text(pestaña_descriptivo, wrap=tk.WORD, height=10, width=50)
        texto_descriptivo.insert(tk.END, estadisticas_descriptivas)
        texto_descriptivo.config(state=tk.DISABLED)
        texto_descriptivo.pack(padx=20, pady=20)


        # Crear un lienzo para mostrar gráficas
        figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Mostrar gráficos de dispersión para cada par de variables
        scatter_matrix(datos, alpha=0.5, ax=ax1)

        # Mostrar gráfico de caja para visualizar datos atípicos
        datos.boxplot(ax=ax2)
        ax2.set_title("Gráfico de Caja")

        # Crear un lienzo para mostrar gráficos
        canvas = FigureCanvasTkAgg(figure, master=pestaña_descriptivo)
        canvas.get_tk_widget().pack(padx=20, pady=20)

        # Actualizar la interfaz
        ventana.update_idletasks()

    else:
        messagebox.showwarning("Advertencia", "Primero importa un archivo CSV.")

def realizar_boxplot():
    if datos is not None:
        # Crear una nueva pestaña para el boxplot
        pestaña_boxplot = ttk.Frame(notebook)
        notebook.add(pestaña_boxplot, text="Boxplot")

        # Crear controles deslizantes para ajustar la escala del boxplot
        label_escala = tk.Label(pestaña_boxplot, text="Ajustar Escala:")
        label_escala.grid(row=0, column=0, padx=10, pady=10)

        escala_minima = tk.DoubleVar()
        escala_maxima = tk.DoubleVar()

        slider_min = tk.Scale(pestaña_boxplot, variable=escala_minima, from_=0, to=100, resolution=0.1, orient="horizontal", label="Mínimo")
        slider_max = tk.Scale(pestaña_boxplot, variable=escala_maxima, from_=0, to=100, resolution=0.1, orient="horizontal", label="Máximo")

        slider_min.grid(row=0, column=1, padx=10, pady=10)
        slider_max.grid(row=0, column=2, padx=10, pady=10)

        # Configurar el boxplot con la escala ajustada
        def actualizar_boxplot():
            figura, ax = plt.subplots(figsize=(12, 6))
            datos.boxplot(ax=ax)
            ax.set_title("Gráfico de Caja")
            ax.set_ylim(escala_minima.get(), escala_maxima.get())

            # Crear un lienzo para mostrar el boxplot
            canvas = FigureCanvasTkAgg(figura, master=pestaña_boxplot)
            canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, padx=20, pady=20)

        actualizar_boxplot()

        # Agregar un botón para aplicar la escala
        boton_aplicar = tk.Button(pestaña_boxplot, text="Aplicar Escala", command=actualizar_boxplot)
        boton_aplicar.grid(row=2, column=1, columnspan=2, pady=10)

        # Actualizar la interfaz
        ventana.update_idletasks()

    else:
        messagebox.showwarning("Advertencia", "Primero importa un archivo CSV.")

def realizar_regresion_lineal():
    if datos is not None:
        # Crear una nueva pestaña para la regresión lineal
        pestaña_regresion = ttk.Frame(notebook)
        notebook.add(pestaña_regresion, text="Regresión Lineal")
        # Obtener las variables x e y de tus datos
        x = datos['Temperatura'].values
        y = datos['Humedad'].values

        # Crear un modelo de regresión lineal
        modelo = LinearRegression(fit_intercept=True)
        modelo.fit(x[:, np.newaxis], y)

        # Graficar los datos y la línea de regresión
        figure, ax = plt.subplots(figsize=(8, 4))
        ax.scatter(x, y, label='Datos')
        ax.plot(x, modelo.predict(x[:, np.newaxis]), color='green', label='Regresión Lineal')
        ax.set_xlabel("Temperatura")
        ax.set_ylabel("Humedad")
        ax.set_title("Regresión Lineal")
        ax.legend()

        # Crear un lienzo para mostrar la gráfica
        canvas = FigureCanvasTkAgg(figure, master=pestaña_regresion)
        canvas.get_tk_widget().pack(padx=20, pady=20)

        # Mostrar estadísticas descriptivas básicas
        coeficiente = modelo.coef_[0]
        intercepto = modelo.intercept_
        estadisticas = {'Coeficiente': [coeficiente], 'Intercepto': [intercepto]}
        texto_estadisticas = tk.Text(pestaña_regresion, wrap=tk.WORD, height=4, width=30)
        texto_estadisticas.insert(tk.END, estadisticas)
        texto_estadisticas.config(state=tk.DISABLED)
        texto_estadisticas.pack(padx=20, pady=20)

        # Actualizar la interfaz
        ventana.update_idletasks()
    else:
        messagebox.showwarning("Advertencia", "Primero importa un archivo CSV.")



def poblacion():
    global objetos_detectados

    # Cargar el modelo de detección de objetos
    net = cv2.dnn.readNetFromCaffe('C:/Users/herna/Desktop/IOT/REto/Proyecto/deploy.prototxt',
                                   'C:/Users/herna/Desktop/IOT/REto/Proyecto/mobilenet_iter_73000.caffemodel')

    # Inicializar la cámara
    cap = cv2.VideoCapture(0)

    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        print("Error al abrir la cámara.")
        exit()

    # Configurar el tamaño de la ventana
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    objetos_detectados = 0  # Reiniciar el contador al iniciar la detección
    
     # Inicializar la grabación de video en formato MP4
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'XVID' o 'MJPG' también son opciones
    out = cv2.VideoWriter('grabacion_poblacion.mp4', fourcc, 20.0, (640, 480))

    while True:
        # Leer un fotograma de la cámara
        ret, frame = cap.read()

        # Verificar si se pudo leer el fotograma
        if not ret:
            print("Error al leer el fotograma.")
            break

        # Obtener las dimensiones del fotograma
        height, width = frame.shape[:2]

        # Preprocesar el fotograma para la detección de objetos
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

        # Pasar el blob a través de la red y obtener las detecciones
        net.setInput(blob)
        detections = net.forward()

        # Contar objetos detectados
        objetos_detectados = sum(confidence > 0.01 for confidence in detections[0, 0, :, 2])

        # Recorrer las detecciones y dibujar cuadros alrededor de los objetos detectados
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.01:  # Filtro de confianza
                idx = int(detections[0, 0, i, 1])
                label = f'Objeto: {idx}, Confianza: {confidence:.2f}'
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


        # Mostrar el fotograma en una ventana
        cv2.imshow('Detección de Objetos', frame)
        
        # Mostrar el fotograma en una ventana
        cv2.imshow('Detección de Objetos', frame)

        # Grabar el fotograma en el video
        out.write(frame)

        # Romper el bucle si se presiona la tecla 's'
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    
    # Liberar la cámara y cerrar la ventana al finalizar
    cap.release()
    out.release()  # Detener la grabación
    cv2.destroyAllWindows()
    
    # Crear una nueva pestaña para el conteo
    pestaña_conteo = ttk.Frame(notebook)
    notebook.add(pestaña_conteo, text="Conteo")
    
    # Crear un Label para mostrar el conteo en la pestaña "Conteo"
    label_conteo = tk.Label(pestaña_conteo, text=f'Población: {objetos_detectados}', font=('Arial', 18))
    label_conteo.pack(padx=20, pady=20)



def salir():
    ventana.destroy()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi Aplicación Científica")
ventana.geometry("800x600")
ventana.configure(bg="#f0f0f0")

# Configurar el menú principal
menu_principal = tk.Menu(ventana)
ventana.config(menu=menu_principal)

# Añadir una opción de "Utilizar datos CSV" al menú principal
menu_datos_csv_principal = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Datos CSV", menu=menu_datos_csv_principal)
menu_datos_csv_principal.add_command(label="Importar datos CSV", command=importar_csv)
menu_datos_csv_principal.add_command(label="Ver poblacion", command=poblacion)



# Configurar pestañas con el Notebook
notebook = ttk.Notebook(ventana)
notebook.pack(fill=tk.BOTH, expand=True)

# Añadir un botón "Salir" en la parte inferior derecha
boton_salir = tk.Button(ventana, text="Salir", command=salir, bg="red", fg="white")
boton_salir.place(relx=1, rely=1, anchor="se")

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
print(f"Objetos detectados: {objetos_detectados}")