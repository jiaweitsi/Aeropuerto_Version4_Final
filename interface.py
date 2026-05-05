import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from airport import *
from aircraft import *

lista_trabajo = [] # Para los aerpuertos
lista_vuelos = []  # Para aviones (Aircrafts)
lista_aeropuertos_ref = []  # Necesaria para buscar coordenadas en LongFlightArrivals

def btn_cargar_click():
    global lista_trabajo
    lista_trabajo = LoadAirports("Airports.txt")
    actualizar_pantalla()
    messagebox.showinfo("Cargar", "Datos cargados correctamente")

def btn_anadir_click():
    c = entrada_cod.get().upper()
    lat = entrada_lat.get()
    lon = entrada_lon.get()

    if len(c) != 4 or not c.isalpha():
        messagebox.showerror("Error", "El código ICAO debe tener 4 LETRAS.")
        return

    try:
        lat = float(lat)
        lon = float(lon)

        nuevo = Airport(c, lat, lon)
        anadido = AddAirport(lista_trabajo, nuevo)

        if anadido:
            actualizar_pantalla()
        else:
            messagebox.showerror("Error", "El aeropuerto ya existe en la lista.")

    except ValueError:
        messagebox.showerror("Error", "Por favor, introduzca números enteros en lat y lon.")

def btn_borrar_click():
    c = entrada_cod.get().upper()
    RemoveAirport(lista_trabajo, c)
    actualizar_pantalla()

def btn_guardar_click():
    SaveSchengenAirports(lista_trabajo, "Schengen_Only.txt")
    messagebox.showinfo("Guardar", "Archivo Schengen_Only.txt creado")

def actualizar_pantalla():
    caja.delete(1.0, tk.END)
    for a in lista_trabajo:
        SetSchengen(a)
        res = "SI" if a.schengen else "NO"
        caja.insert(tk.END, f"Cod: {a.code} | Lat: {a.lat} | Lon: {a.lon} | Schengen: {res}\n")

###########################################################################

def btn_cargar_vuelos_click():
    global lista_vuelos
    lista_vuelos = LoadArrivals("Arrivals.txt")
    actualizar_pantalla_vuelos()
    messagebox.showinfo("Vuelos", "Vuelos cargados correctamente")


def btn_mapa_kml_click():
    MapFlights(lista_vuelos, lista_trabajo)
    messagebox.showinfo("KML", "Archivo generado. Ábrelo en Google Earth")

def btn_vuelos_largos_click():
    vuelos_distantes = LongFlightArrivals(lista_vuelos, lista_trabajo)

    caja.delete(1.0, tk.END)
    caja.insert(tk.END, "--- VUELOS DE LARGA DISTANCIA (>2000km) ---\n")
    for v in vuelos_distantes:
        caja.insert(tk.END, f"Avion: {v.aircraft} | Origen: {v.origin} | Hora: {v.time}\n")


def btn_exportar_vuelos_largos_click():
    vuelos_especiales = LongFlightArrivals(lista_vuelos, lista_trabajo)

    if len(vuelos_especiales) > 0:
        nombre_fichero = "vuelos_inspeccion_especial.txt"
        exito = SaveFlights(vuelos_especiales, nombre_fichero)

        if exito:
            messagebox.showinfo("Exportar", f"Se han guardado {len(vuelos_especiales)} vuelos en {nombre_fichero}")
        else:
            messagebox.showerror("Error", "No se pudo crear el archivo de exportación")
    else:
        messagebox.showwarning("Atención", "No hay vuelos que superen los 2000km de distancia")


def actualizar_pantalla_vuelos():
    caja.delete(1.0, tk.END)
    i = 0
    while i < len(lista_vuelos):
        v = lista_vuelos[i]

        texto = "Avión: " + str(v.aircraft) + " | Origen: " + str(v.origin) + " | Hora: " + str(v.time) + "\n"

        caja.insert(tk.END, texto)
        i = i + 1


def btn_guardar_vuelos_fichero_click():
    if len(lista_vuelos) > 0:
        exito = SaveFlights(lista_vuelos, "vuelos_largos.txt")

        if exito:
            messagebox.showinfo("Guardar", "Vuelos guardados en 'vuelos_largos.txt'")
        else:
            messagebox.showerror("Error", "No se ha podido guardar el archivo")
    else:
        messagebox.showwarning("Error", "No hay vuelos cargados para guardar")

###########################GRAFICOS###############################GRÁFICOS##############################
#Codigo general para las graficas
#si ya hay un gráfico puesto, poder borrarlo
canvas_picture = None


def mostrar_grafico_en_interfaz(figura):
    global canvas_picture

    # Si ya hay un gráfico en pantalla, lo eliminamos
    if canvas_picture is not None:
        canvas_picture.get_tk_widget().destroy()

    canvas_obj = FigureCanvasTkAgg(figura, master=root)
    canvas_obj.draw()

    canvas_picture = canvas_obj
    widget = canvas_obj.get_tk_widget()
    widget.config(width=500, height=300)
    widget.grid(row=2, column=1, rowspan=5, padx=10, pady=10)

#version 1 airports:Schengen vs NoSchengen
def btn_grafica_aeropuertos_click():
    if not lista_trabajo:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return

    figura = PlotAirports(lista_trabajo)
    mostrar_grafico_en_interfaz(figura)

# Boton grafica arrivals
def btn_grafica_llegadas_click():
    if lista_vuelos:
        fig = PlotArrivals(lista_vuelos)
        mostrar_grafico_en_interfaz(fig)
    else:
        messagebox.showwarning("Error", "Carga los vuelos primero")

#boton grafica de compañias
def btn_grafica_airlines_click():
    if lista_vuelos:
        fig = PlotAirlines(lista_vuelos)
        mostrar_grafico_en_interfaz(fig)
    else:
        messagebox.showwarning("Error", "Carga los vuelos primero")

#flight type (Schengen vs NoSchengen)
def btn_grafica_schengen_click():
    if lista_trabajo:
        fig = PlotFlightsType(lista_vuelos)
        mostrar_grafico_en_interfaz(fig)
    else:
        messagebox.showwarning("Error", "Carga los vuelos primero")

#######################DISEÑO INTERFAZ##########################DISEÑO INTERFAZ###################
root = tk.Tk()
root.title('Airport')
root.geometry("1000x800")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=10)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=10)

############################################################
button_pictures_frame = tk.LabelFrame(root, text='Acciones')
button_pictures_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

button_pictures_frame.columnconfigure(0, weight=1)
button_pictures_frame.rowconfigure(0, weight=1)
button_pictures_frame.rowconfigure(1, weight=1)

btn_cargar = tk.Button(button_pictures_frame, text="Cargar Aeropuertos", command=btn_cargar_click)
btn_cargar.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

btn_guardar = tk.Button(button_pictures_frame, text="Guardar Schengen", command=btn_guardar_click)
btn_guardar.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

#######################################################################

input_frame = tk.LabelFrame(root, text='Datos Aeropuerto')
input_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

tk.Label(input_frame, text="ICAO:").pack()
entrada_cod = tk.Entry(input_frame)
entrada_cod.pack(fill="x", padx=5)

tk.Label(input_frame, text="Lat:").pack()
entrada_lat = tk.Entry(input_frame)
entrada_lat.pack(fill="x", padx=5)

tk.Label(input_frame, text="Lon:").pack()
entrada_lon = tk.Entry(input_frame)
entrada_lon.pack(fill="x", padx=5)

btn_add = tk.Button(input_frame, text="Añadir", command=btn_anadir_click)
btn_add.pack(pady=5)

btn_borrar = tk.Button(input_frame, text="Borrar", command=btn_borrar_click)
btn_borrar.pack(pady=5)

caja = tk.Text(root, height=5)
caja.grid(row=0, column=1, rowspan=1, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

#############################SECCION GRAFICAS##########################

grafico_frame = tk.LabelFrame(root, text='Gráficas') #en root tenemos un frame que se llama graficas
grafico_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)
#El frame de graficas se posiciona en fila 2 y columna 0

btn_ver_grafico = tk.Button(grafico_frame, text="Schengen vs NoSchengen",
                            command= btn_grafica_aeropuertos_click)
btn_ver_grafico.grid(row=0, column=0, pady=5, padx=5, sticky=tk.N+tk.S+tk.E+tk.W)
#####
btn_ver_grafico= tk.Button(grafico_frame, text="Gráfico Llegadas",
                              command=btn_grafica_llegadas_click)
btn_ver_grafico.grid(row=0, column=1, pady=5, padx=5, sticky=tk.N+tk.S+tk.E+tk.W)
#####
btn_ver_grafico= tk.Button(grafico_frame, text="Gráfico por Aerolínea",
                              command=btn_grafica_airlines_click)
btn_ver_grafico.grid(row=0, column=2, pady=5, padx=5, sticky=tk.N+tk.S+tk.E+tk.W)
#####
btn_ver_grafico= tk.Button(grafico_frame, text="Vuelos Schengen vs NoSchengen",
                          command=btn_grafica_schengen_click)
btn_ver_grafico.grid(row=0, column=3, pady=5, padx=5, sticky=tk.N+tk.S+tk.E+tk.W)


############### SECCIÓN DE VUELOS ##########################
vuelos_frame = tk.LabelFrame(root, text='Gestión de Vuelos (Aircrafts)')
vuelos_frame.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

btn_vuelos = tk.Button(vuelos_frame, text="Cargar Vuelos", command=btn_cargar_vuelos_click)
btn_vuelos.pack(fill="x", padx=5, pady=2)

btn_kml = tk.Button(vuelos_frame, text="Generar KML", command=btn_mapa_kml_click)
btn_kml.pack(fill="x", padx=5, pady=2)

btn_distancia = tk.Button(vuelos_frame, text="Filtrar Vuelos Largos", command=btn_vuelos_largos_click)
btn_distancia.pack(fill="x", padx=5, pady=2)

btn_save_flights = tk.Button(vuelos_frame, text="Guardar Vuelos en Fichero",
                             command=btn_guardar_vuelos_fichero_click)
btn_save_flights.pack(fill="x", padx=5, pady=2)

btn_vuelos_largos= tk.Button(vuelos_frame, text="Guardar Vuelos Largos en Fichero",
                             command=btn_exportar_vuelos_largos_click)
btn_vuelos_largos.pack(fill="x", padx=5, pady=2)


root.mainloop()
