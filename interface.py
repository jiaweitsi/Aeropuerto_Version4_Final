import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import subprocess

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from airport import *
from aircraft import *
from LEBL import *


# =====================================================================
# VARIABLES GLOBALES
# =====================================================================

lista_trabajo = []
lista_vuelos  = []
bcn           = None


# =====================================================================
# FUNCIONES - AEROPUERTOS (VERSION 1)
# =====================================================================

def btn_cargar_click():
    global lista_trabajo
    lista_trabajo = LoadAirports("Airports.txt")
    actualizar_pantalla()
    messagebox.showinfo("Cargar", "Datos cargados correctamente")

def btn_anadir_click():
    c   = entrada_cod.get().upper()
    lat = entrada_lat.get()
    lon = entrada_lon.get()
    if len(c) != 4 or not c.isalpha():
        messagebox.showerror("Error", "El código ICAO debe tener 4 LETRAS.")
        return
    try:
        lat    = float(lat)
        lon    = float(lon)
        nuevo  = Airport(c, lat, lon)
        anadido = AddAirport(lista_trabajo, nuevo)
        if anadido:
            entrada_cod.delete(0, tk.END)
            entrada_lat.delete(0, tk.END)
            entrada_lon.delete(0, tk.END)
            actualizar_pantalla()
        else:
            messagebox.showerror("Error", "El aeropuerto ya existe en la lista.")
    except ValueError:
        messagebox.showerror("Error", "Introduce números válidos en Lat y Lon.")

def btn_borrar_click():
    c = entrada_cod.get().upper()
    if c == "":
        messagebox.showwarning("Aviso", "Escribe el código ICAO a borrar.")
        return
    RemoveAirport(lista_trabajo, c)
    actualizar_pantalla()

def btn_guardar_click():
    SaveSchengenAirports(lista_trabajo, "Schengen_Only.txt")
    messagebox.showinfo("Guardar", "Archivo Schengen_Only.txt creado")

def abrir_google_earth(archivo_kml):
    archivo_kml = os.path.abspath(archivo_kml)
    if not os.path.exists(archivo_kml):
        return False
    try:
        rutas_windows = [
            "C:\\Program Files\\Google\\Google Earth Pro\\client\\googleearth.exe",
            "C:\\Program Files (x86)\\Google\\Google Earth Pro\\client\\googleearth.exe",
        ]
        encontrado = False
        i = 0
        while i < len(rutas_windows) and not encontrado:
            if os.path.exists(rutas_windows[i]):
                subprocess.Popen([rutas_windows[i], archivo_kml])
                encontrado = True
            i += 1
        if not encontrado:
            os.startfile(archivo_kml)
        return True
    except Exception as e:
        print("Error:", e)
        return False

def btn_mapa_aeropuertos_click():
    if len(lista_trabajo) == 0:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    MapAirports(lista_trabajo)
    exito = abrir_google_earth("airports_map.kml")
    if exito:
        messagebox.showinfo("Google Earth", "Archivo generado y abierto en Google Earth Pro")
    else:
        messagebox.showwarning("Aviso", "Archivo generado pero no se pudo abrir Google Earth.\nAbre manualmente airports_map.kml")

def actualizar_pantalla():
    caja.delete(1.0, tk.END)
    i = 0
    while i < len(lista_trabajo):
        a   = lista_trabajo[i]
        SetSchengen(a)
        res = "SI" if a.schengen else "NO"
        caja.insert(tk.END,
            "Cod: " + a.code +
            " | Lat: " + str(round(a.lat, 4)) +
            " | Lon: " + str(round(a.lon, 4)) +
            " | Schengen: " + res + "\n")
        i += 1


# =====================================================================
# FUNCIONES - VUELOS (VERSION 2)
# =====================================================================

def btn_cargar_vuelos_click():
    global lista_vuelos
    lista_vuelos = LoadArrivals("Arrivals.txt")
    actualizar_pantalla_vuelos()
    messagebox.showinfo("Vuelos", "Vuelos cargados correctamente")

def btn_mapa_kml_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Aviso", "Carga los vuelos primero")
        return
    if len(lista_trabajo) == 0:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    MapFlights(lista_vuelos, lista_trabajo)
    exito = abrir_google_earth("trayectorias.kml")
    if exito:
        messagebox.showinfo("Google Earth", "Archivo generado y abierto en Google Earth Pro")
    else:
        messagebox.showwarning("Aviso", "Archivo generado pero no se pudo abrir Google Earth.\nAbre manualmente trayectorias.kml")

def btn_vuelos_largos_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Aviso", "Carga los vuelos primero")
        return
    if len(lista_trabajo) == 0:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    vuelos_distantes = LongFlightArrivals(lista_vuelos, lista_trabajo)
    caja.delete(1.0, tk.END)
    caja.insert(tk.END, "--- VUELOS LARGA DISTANCIA (>2000km) ---\n")
    i = 0
    while i < len(vuelos_distantes):
        v = vuelos_distantes[i]
        caja.insert(tk.END,
            "Avión: " + str(v.aircraft) +
            " | Origen: " + str(v.origin) +
            " | Hora: " + str(v.time) + "\n")
        i += 1

def btn_exportar_vuelos_largos_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Aviso", "Carga los vuelos primero")
        return
    if len(lista_trabajo) == 0:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    vuelos_especiales = LongFlightArrivals(lista_vuelos, lista_trabajo)
    if len(vuelos_especiales) > 0:
        exito = SaveFlights(vuelos_especiales, "vuelos_largos.txt")
        if exito:
            messagebox.showinfo("Exportar",
                "Guardados " + str(len(vuelos_especiales)) + " vuelos.")
        else:
            messagebox.showerror("Error", "No se ha podido guardar el archivo")
    else:
        messagebox.showwarning("Atención", "No hay vuelos de más de 2000km")

def actualizar_pantalla_vuelos():
    caja.delete(1.0, tk.END)
    i = 0
    while i < len(lista_vuelos):
        v = lista_vuelos[i]
        caja.insert(tk.END,
            "Avión: " + str(v.aircraft) +
            " | Origen: " + str(v.origin) +
            " | Hora: " + str(v.time) +
            " | Compañía: " + str(v.company) + "\n")
        i += 1

def btn_guardar_vuelos_fichero_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Error", "No hay vuelos cargados")
        return
    exito = SaveFlights(lista_vuelos, "vuelos_guardados.txt")
    if exito:
        messagebox.showinfo("Guardar", "Vuelos guardados en 'vuelos_guardados.txt'")
    else:
        messagebox.showerror("Error", "No se ha podido guardar el archivo")


# =====================================================================
# FUNCIONES - GATES (VERSION 3)
# =====================================================================

def btn_cargar_estructura_click():
    global bcn
    resultado = LoadAirportStructure("Terminals.txt")
    if resultado is None:
        messagebox.showerror("Error", "No se pudo cargar Terminals.txt")
        return
    bcn = resultado
    actualizar_pantalla_gates()
    messagebox.showinfo("Estructura", "Aeropuerto " + bcn.code + " cargado correctamente")

def btn_asignar_gates_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura (Terminals.txt)")
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror("Error", "Primero carga los vuelos")
        return
    asignados    = 0
    no_asignados = 0
    i = 0
    while i < len(lista_vuelos):
        vuelo = lista_vuelos[i]
        # Ignorar aviones nocturnos (sin origen), tienen su propio botón
        if vuelo.origin != "":
            resultado = AssignGate(bcn, vuelo)
            if resultado == 0:
                asignados += 1
            else:
                no_asignados += 1
        i += 1
    actualizar_pantalla_gates()
    messagebox.showinfo("Gates",
        "Asignados: " + str(asignados) +
        "\nNo asignados: " + str(no_asignados))

def btn_ver_ocupacion_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura del aeropuerto")
        return
    caja.delete(1.0, tk.END)
    ocupacion      = GateOccupancy(bcn)
    total_gates    = 0
    gates_libres   = 0
    gates_ocupados = 0
    i = 0
    while i < len(ocupacion):
        gate = ocupacion[i]
        total_gates += 1
        if gate[3] == "Ocupado":
            gates_ocupados += 1
        else:
            gates_libres += 1
        i += 1
    caja.insert(tk.END, "Total gates: "    + str(total_gates)    + "\n")
    caja.insert(tk.END, "Gates libres: "   + str(gates_libres)   + "\n")
    caja.insert(tk.END, "Gates ocupados: " + str(gates_ocupados) + "\n")

def actualizar_pantalla_gates():
    caja.delete(1.0, tk.END)
    if bcn is None:
        return
    ocupacion       = GateOccupancy(bcn)
    terminal_actual = ""
    area_actual     = ""
    caja.insert(tk.END, "=== OCUPACION DE GATES - " + bcn.code + " ===\n\n")
    i = 0
    while i < len(ocupacion):
        g = ocupacion[i]
        if g[0] != terminal_actual:
            terminal_actual = g[0]
            area_actual     = ""
            caja.insert(tk.END, "\nTERMINAL " + terminal_actual + "\n")
        if g[1] != area_actual:
            area_actual = g[1]
            caja.insert(tk.END, "  Area " + area_actual + ":\n")
        caja.insert(tk.END, "    " + g[2] + " -> " + g[3])
        if g[3] == "Ocupado":
            caja.insert(tk.END, " (" + g[4] + ")")
        caja.insert(tk.END, "\n")
        i += 1


def btn_liberar_gate_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura del aeropuerto")
        return
    aircraft_id = entrada_liberar.get().strip().upper()
    if aircraft_id == "":
        messagebox.showwarning("Aviso", "Introduce el ID del avión a liberar.")
        return
    resultado = FreeGate(bcn, aircraft_id)
    if resultado == 0:
        entrada_liberar.delete(0, tk.END)
        actualizar_pantalla_gates()
        messagebox.showinfo("Liberar Gate", "Gate liberado correctamente para el avión: " + aircraft_id)
    else:
        messagebox.showerror("Error", "No se encontró el avión en ningún gate: " + aircraft_id)


def btn_reasignar_gate_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura del aeropuerto")
        return

    aircraft_id       = entrada_reasignar_avion.get().strip().upper()
    nuevo_gate_nombre = entrada_reasignar_gate.get().strip().upper()

    if aircraft_id == "" or nuevo_gate_nombre == "":
        messagebox.showwarning("Aviso", "Rellena el ID del avión y el nombre del gate.")
        return

    gate_destino = None
    i = 0
    while i < len(bcn.terminals) and gate_destino is None:
        terminal = bcn.terminals[i]
        j = 0
        while j < len(terminal.boarding_areas) and gate_destino is None:
            area = terminal.boarding_areas[j]
            k = 0
            while k < len(area.gates) and gate_destino is None:
                if area.gates[k].name == nuevo_gate_nombre:
                    gate_destino = area.gates[k]
                k += 1
            j += 1
        i += 1

    if gate_destino is None:
        messagebox.showerror("Error", "Gate no encontrado: " + nuevo_gate_nombre)
        return

    if gate_destino.occupied and gate_destino.aircraft_id != aircraft_id:
        messagebox.showerror("Error", "Ese gate ya está ocupado por otro avión.")
        return

    resultado_liberar = FreeGate(bcn, aircraft_id)
    if resultado_liberar != 0:
        messagebox.showinfo("Info", "El avión no está asignado a ningún gate actualmente.\nSe asignará directamente al nuevo gate.")

    gate_destino.occupied   = True
    gate_destino.aircraft_id = aircraft_id

    entrada_reasignar_avion.delete(0, tk.END)
    entrada_reasignar_gate.delete(0, tk.END)

    actualizar_pantalla_gates()
    messagebox.showinfo("Reasignar Gate",
        "Gate reasignado correctamente.\nAvión: " + aircraft_id +
        "\nNuevo Gate: " + nuevo_gate_nombre)


# =====================================================================
# FUNCIONES - SALIDAS Y DINÁMICA (VERSION 4)
# =====================================================================

def btn_cargar_salidas_click():
    global lista_vuelos
    salidas = LoadDepartures("Departures.txt")
    if len(salidas) == 0:
        messagebox.showwarning("Aviso", "No se encontró Departures.txt o está vacío")
        return
    fusionados = MergeMovements(lista_vuelos, salidas)
    if len(fusionados) == 0:
        messagebox.showwarning("Aviso", "Error al fusionar llegadas y salidas")
        return
    lista_vuelos = fusionados
    actualizar_pantalla_vuelos_v4()
    messagebox.showinfo("Salidas", "Salidas cargadas y fusionadas correctamente")

def btn_aviones_nocturnos_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Aviso", "Carga los vuelos primero")
        return
    nocturnos = NightAircraft(lista_vuelos)
    caja.delete(1.0, tk.END)
    caja.insert(tk.END, "--- AVIONES NOCTURNOS ---\n")
    i = 0
    while i < len(nocturnos):
        ac = nocturnos[i]
        caja.insert(tk.END,
            "Avión: " + str(ac.aircraft) +
            " | Destino: " + str(ac.destination) +
            " | Salida: " + str(ac.departure_time) + "\n")
        i += 1
    if len(nocturnos) == 0:
        caja.insert(tk.END, "No hay aviones nocturnos\n")

def btn_asignar_nocturnos_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura del aeropuerto")
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror("Error", "Primero carga los vuelos")
        return
    nocturnos = NightAircraft(lista_vuelos)
    if len(nocturnos) == 0:
        messagebox.showinfo("Info", "No hay aviones nocturnos")
        return
    AssignNightGates(bcn, nocturnos)
    actualizar_pantalla_gates()
    messagebox.showinfo("Nocturnos", "Gates asignados a aviones nocturnos")

def btn_asignar_por_hora_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura del aeropuerto")
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror("Error", "Primero carga los vuelos")
        return
    hora   = entrada_hora.get()
    partes = hora.split(":")
    if len(partes) != 2:
        messagebox.showerror("Error", "Formato incorrecto. Usa hh:mm (ej: 08:00)")
        return
    try:
        h = int(partes[0])
        m = int(partes[1])
        if h < 0 or h > 23 or m < 0 or m > 59:
            messagebox.showerror("Error", "Hora fuera de rango (00:00 - 23:59)")
            return
    except ValueError:
        messagebox.showerror("Error", "Introduce números válidos en la hora")
        return
    no_asig = AssignGatesAtTime(bcn, lista_vuelos, hora)
    actualizar_pantalla_gates()
    messagebox.showinfo("Asignación por hora",
        "Periodo a partir de " + hora + " procesado.\nAviones no asignados: " + str(no_asig))

def actualizar_pantalla_vuelos_v4():
    caja.delete(1.0, tk.END)
    i = 0
    while i < len(lista_vuelos):
        v     = lista_vuelos[i]
        linea = "Avión: " + str(v.aircraft)
        if v.origin != "":
            linea += " | Origen: " + str(v.origin) + " | Llegada: " + str(v.time)
        if v.destination != "":
            linea += " | Destino: " + str(v.destination) + " | Salida: " + str(v.departure_time)
        caja.insert(tk.END, linea + "\n")
        i += 1


# =====================================================================
# GRÁFICOS
# =====================================================================

canvas_picture = None


def mostrar_grafico_en_interfaz(figura):
    global canvas_picture
    if canvas_picture is not None:
        canvas_picture.get_tk_widget().destroy()
    figura.set_size_inches(8, 6)
    canvas_obj = FigureCanvasTkAgg(figura, master=panel_graficas)
    canvas_obj.draw()
    canvas_picture = canvas_obj
    widget = canvas_obj.get_tk_widget()
    widget.grid(row=0, column=0, padx=5, pady=5)

def btn_borrar_grafica_click():
    global canvas_picture
    if canvas_picture is not None:
        canvas_picture.get_tk_widget().destroy()
        canvas_picture = None

    # Colapsa la fila de visualización para que la consola recupere el espacio
    root.rowconfigure(1, weight=0, minsize=0)
    panel_graficas.configure(height=1)
    panel_graficas.grid_propagate(True)
    root.update_idletasks()


def btn_grafica_aeropuertos_click():
    if not lista_trabajo:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    figura = PlotAirports(lista_trabajo)
    mostrar_grafico_en_interfaz(figura)

def btn_grafica_llegadas_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Error", "Carga los vuelos primero")
        return
    fig = PlotArrivals(lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_airlines_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Error", "Carga los vuelos primero")
        return
    fig = PlotAirlines(lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_schengen_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Error", "Carga los vuelos primero")
        return
    fig = PlotFlightsType(lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_gates_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura del aeropuerto")
        return
    fig = PlotGates(bcn)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_ocupacion_dia_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura del aeropuerto")
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror("Error", "Primero carga los vuelos")
        return
    fig = PlotDayOccupancy(bcn, lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)


# =====================================================================
# PALETA PASTEL
# =====================================================================

BG_APP      = "#F5F0FB"
BG_PANEL    = "#EDE6F7"
BG_CONSOLA  = "#FDFBFF"
C_TEXT_DARK = "#3D2B5A"
C_LABEL_FG  = "#5C4080"

C_AP_BG  = "#DFF0FF"; C_AP_FG  = "#1E4E7C"; C_AP_HOVER  = "#C5E3F8"
C_VU_BG  = "#FFE6EF"; C_VU_FG  = "#7A1E40"; C_VU_HOVER  = "#FFD0E2"
C_GA_BG  = "#EAE0FF"; C_GA_FG  = "#4A2878"; C_GA_HOVER  = "#D9C8FA"
C_V4_BG  = "#FFF3DC"; C_V4_FG  = "#7A4A10"; C_V4_HOVER  = "#FFE8BE"
C_GR_BG  = "#D8F5E8"; C_GR_FG  = "#1A5E3C"; C_GR_HOVER  = "#BEF0D4"
C_MN_BG  = "#FFE8D8"; C_MN_FG  = "#7A3010"; C_MN_HOVER  = "#FFD5B8"
C_DEL_BG = "#FFD8D8"; C_DEL_FG = "#8A1A1A"; C_DEL_HOVER = "#FFC0C0"
C_ADD_BG = "#D8EEFF"; C_ADD_FG = "#1A4E7A"; C_ADD_HOVER = "#BEE0F8"


# =====================================================================
# INICIO - VENTANA PRINCIPAL
# =====================================================================

root = tk.Tk()
root.title("Airport Manager")
root.geometry("1000x650")
root.configure(bg=BG_APP)

# ---- ESTILOS ----
style = ttk.Style()
style.theme_use("clam")

style.configure("Panel.TLabelframe",
    background=BG_PANEL, padding=4, relief="flat", borderwidth=1)
style.configure("Panel.TLabelframe.Label",
    font=("Segoe UI", 8, "bold"), foreground=C_LABEL_FG, background=BG_PANEL)

style.configure("Light.TLabelframe",
    background=BG_APP, padding=4, relief="flat", borderwidth=1)
style.configure("Light.TLabelframe.Label",
    font=("Segoe UI", 8, "bold"), foreground=C_LABEL_FG, background=BG_APP)

style.configure("TFrame",  background=BG_APP)
style.configure("TLabel",  font=("Segoe UI", 8), background=BG_PANEL, foreground=C_LABEL_FG)
style.configure("TEntry",  font=("Segoe UI", 8), fieldbackground="#FFFFFF")

def mk(name, bg, fg, hov):
    style.configure(name, background=bg, foreground=fg,
        font=("Segoe UI", 8), padding=4, relief="flat", borderwidth=0)
    style.map(name, background=[("active", hov)], foreground=[("active", fg)])

mk("AP.TButton",  C_AP_BG,  C_AP_FG,  C_AP_HOVER)
mk("VU.TButton",  C_VU_BG,  C_VU_FG,  C_VU_HOVER)
mk("GA.TButton",  C_GA_BG,  C_GA_FG,  C_GA_HOVER)
mk("V4.TButton",  C_V4_BG,  C_V4_FG,  C_V4_HOVER)
mk("GR.TButton",  C_GR_BG,  C_GR_FG,  C_GR_HOVER)
mk("MN.TButton",  C_MN_BG,  C_MN_FG,  C_MN_HOVER)
mk("ADD.TButton", C_ADD_BG, C_ADD_FG, C_ADD_HOVER)
style.configure("DEL.TButton",
    background=C_DEL_BG, foreground=C_DEL_FG,
    font=("Segoe UI", 8, "bold"), padding=4, relief="flat", borderwidth=0)
style.map("DEL.TButton",
    background=[("active", C_DEL_HOVER)], foreground=[("active", C_DEL_FG)])

# ---- GRID PRINCIPAL ----
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=2)
root.rowconfigure(1, weight=5)


# =====================================================================
# PANEL IZQUIERDO CON SCROLL
# =====================================================================

outer_left = tk.Frame(root, bg=BG_APP, width=220)
outer_left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=8, pady=8)
outer_left.grid_propagate(False)
outer_left.rowconfigure(0, weight=1)
outer_left.columnconfigure(0, weight=1)

left_canvas   = tk.Canvas(outer_left, bg=BG_PANEL, highlightthickness=0, bd=0)
left_scrollbar = tk.Scrollbar(outer_left, orient="vertical", command=left_canvas.yview)
left_canvas.configure(yscrollcommand=left_scrollbar.set)

left_scrollbar.grid(row=0, column=1, sticky="ns")
left_canvas.grid(row=0, column=0, sticky="nsew")

left_panel        = tk.Frame(left_canvas, bg=BG_PANEL)
left_panel_window = left_canvas.create_window((0, 0), window=left_panel, anchor="nw")

def _on_left_panel_configure(event):
    left_canvas.configure(scrollregion=left_canvas.bbox("all"))

def _on_left_canvas_configure(event):
    left_canvas.itemconfig(left_panel_window, width=event.width)

left_panel.bind("<Configure>",  _on_left_panel_configure)
left_canvas.bind("<Configure>", _on_left_canvas_configure)

def _on_mousewheel(event):
    left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

left_canvas.bind_all("<MouseWheel>", _on_mousewheel)
left_canvas.bind_all("<Button-4>", lambda e: left_canvas.yview_scroll(-1, "units"))
left_canvas.bind_all("<Button-5>", lambda e: left_canvas.yview_scroll(1,  "units"))

left_panel.columnconfigure(0, weight=1)

# ---- Helpers ----
def make_section(parent, text, row):
    lf = tk.LabelFrame(parent, text=text,
        bg=BG_PANEL, fg=C_LABEL_FG,
        font=("Segoe UI", 8, "bold"),
        relief="flat", bd=1, padx=4, pady=4)
    lf.grid(row=row, column=0, sticky="ew", pady=3, padx=2)
    lf.columnconfigure(0, weight=1)
    return lf

def make_btn(parent, text, style_name, command):
    color_map = {
        "AP.TButton":  (C_AP_BG,  C_AP_FG,  C_AP_HOVER),
        "VU.TButton":  (C_VU_BG,  C_VU_FG,  C_VU_HOVER),
        "GA.TButton":  (C_GA_BG,  C_GA_FG,  C_GA_HOVER),
        "V4.TButton":  (C_V4_BG,  C_V4_FG,  C_V4_HOVER),
        "MN.TButton":  (C_MN_BG,  C_MN_FG,  C_MN_HOVER),
        "ADD.TButton": (C_ADD_BG, C_ADD_FG, C_ADD_HOVER),
        "DEL.TButton": (C_DEL_BG, C_DEL_FG, C_DEL_HOVER),
        "GR.TButton":  (C_GR_BG,  C_GR_FG,  C_GR_HOVER),
    }
    bg, fg, hov = color_map.get(style_name, (BG_PANEL, C_TEXT_DARK, BG_APP))
    btn = tk.Button(parent, text=text, bg=bg, fg=fg,
        activebackground=hov, activeforeground=fg,
        font=("Segoe UI", 8), relief="flat", bd=0,
        padx=4, pady=4, cursor="hand2", command=command)
    btn.grid(sticky="ew", pady=2, padx=4)
    btn.bind("<Enter>", lambda e, b=btn, h=hov: b.configure(bg=h))
    btn.bind("<Leave>", lambda e, b=btn, n=bg:  b.configure(bg=n))
    return btn


# ---- Secciones del panel izquierdo ----
row_idx = 0

# AEROPUERTOS
acciones = make_section(left_panel, "  ✈  Aeropuertos", row_idx); row_idx += 1
for txt, cmd, sty in [
    ("Cargar Aeropuertos",   btn_cargar_click,          "AP.TButton"),
    ("Guardar Schengen",     btn_guardar_click,          "AP.TButton"),
    ("Ver en Google Earth",  btn_mapa_aeropuertos_click, "AP.TButton"),
]:
    make_btn(acciones, txt, sty, cmd)

# AÑADIR / BORRAR
datos = make_section(left_panel, "  +/-  Añadir / Borrar Aeropuerto", row_idx); row_idx += 1

entrada_cod = entrada_lat = entrada_lon = None
fields = [("ICAO (ej: LEBL):", 14), ("Latitud:", 14), ("Longitud:", 14)]
for fila_num, (label_txt, w) in enumerate(fields):
    fila = tk.Frame(datos, bg=BG_PANEL)
    fila.grid(row=fila_num, column=0, sticky="ew", pady=2, padx=4)
    tk.Label(fila, text=label_txt, width=14, anchor="w",
             bg=BG_PANEL, fg=C_LABEL_FG, font=("Segoe UI", 8)).pack(side=tk.LEFT)
    e = ttk.Entry(fila, width=w)
    e.pack(side=tk.LEFT, padx=3)
    if fila_num == 0:   entrada_cod = e
    elif fila_num == 1: entrada_lat = e
    else:               entrada_lon = e

fila_btns = tk.Frame(datos, bg=BG_PANEL)
fila_btns.grid(row=3, column=0, sticky="ew", pady=4, padx=4)
tk.Button(fila_btns, text="Añadir", bg=C_ADD_BG, fg=C_ADD_FG,
    activebackground=C_ADD_HOVER, font=("Segoe UI", 10),
    relief="flat", bd=0, padx=4, pady=4, cursor="hand2",
    command=btn_anadir_click).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
tk.Button(fila_btns, text="Borrar", bg=C_DEL_BG, fg=C_DEL_FG,
    activebackground=C_DEL_HOVER, font=("Segoe UI", 10, "bold"),
    relief="flat", bd=0, padx=4, pady=4, cursor="hand2",
    command=btn_borrar_click).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

# VUELOS
vuelos_frame = make_section(left_panel, "  🛬  Gestión de Vuelos", row_idx); row_idx += 1
for txt, cmd, sty in [
    ("Cargar Vuelos",              btn_cargar_vuelos_click,         "VU.TButton"),
    ("Trayectorias Google Earth",  btn_mapa_kml_click,              "VU.TButton"),
    ("Filtrar Vuelos Largos",      btn_vuelos_largos_click,         "VU.TButton"),
    ("Guardar Vuelos",             btn_guardar_vuelos_fichero_click, "VU.TButton"),
    ("Exportar Vuelos Largos",     btn_exportar_vuelos_largos_click, "VU.TButton"),

]:
    make_btn(vuelos_frame, txt, sty, cmd)

# GATES
gates_frame = make_section(left_panel, "  🚪  Gestión de Gates", row_idx); row_idx += 1
for txt, cmd, sty in [
    ("Cargar Estructura", btn_cargar_estructura_click, "GA.TButton"),
    ("Asignar Gates",     btn_asignar_gates_click,     "GA.TButton"),
    ("Ver Ocupación",     btn_ver_ocupacion_click,     "GA.TButton"),
]:
    make_btn(gates_frame, txt, sty, cmd)

# SALIDAS Y DINÁMICA
v4_frame = make_section(left_panel, "  🌙  Salidas y Dinámica", row_idx); row_idx += 1
make_btn(v4_frame, "Cargar Salidas",     "V4.TButton", btn_cargar_salidas_click)
make_btn(v4_frame, "Ver Aviones Nocturnos",   "V4.TButton", btn_aviones_nocturnos_click)
make_btn(v4_frame, "Asignar Gates Nocturnos", "V4.TButton", btn_asignar_nocturnos_click)

fila_hora = tk.Frame(v4_frame, bg=BG_PANEL)
fila_hora.grid(sticky="ew", pady=2, padx=4)
tk.Label(fila_hora, text="Hora (hh:mm):", bg=BG_PANEL, fg=C_LABEL_FG,
         font=("Segoe UI", 8)).pack(side=tk.LEFT)
entrada_hora = ttk.Entry(fila_hora, width=7)
entrada_hora.pack(side=tk.LEFT, padx=4)
entrada_hora.insert(0, "08:00")
make_btn(v4_frame, "Asignar Gates por Hora", "V4.TButton", btn_asignar_por_hora_click)

# GESTIÓN MANUAL DE GATES
manual_frame = make_section(left_panel, "  ✏️  Gestión Manual de Gates", row_idx); row_idx += 1

# Liberar Gate
sep_lib = tk.Frame(manual_frame, bg=BG_PANEL)
sep_lib.grid(sticky="ew", pady=(4, 2), padx=4)
tk.Label(sep_lib, text="🔓 ID Avión a liberar:",
         bg=BG_PANEL, fg=C_LABEL_FG,
         font=("Segoe UI", 8, "bold")).pack(anchor="w")

fila_lib = tk.Frame(manual_frame, bg=BG_PANEL)
fila_lib.grid(sticky="ew", pady=2, padx=4)
entrada_liberar = ttk.Entry(fila_lib, width=14)
entrada_liberar.pack(side=tk.LEFT, padx=(0, 4))
tk.Button(fila_lib, text="🔓 Liberar Gate",
    bg=C_MN_BG, fg=C_MN_FG, activebackground=C_MN_HOVER,
    font=("Segoe UI", 8), relief="flat", bd=0, padx=4, pady=3,
    cursor="hand2", command=btn_liberar_gate_click).pack(side=tk.LEFT, fill=tk.X, expand=True)

tk.Frame(manual_frame, height=1, bg="#D4C5E8").grid(sticky="ew", pady=6, padx=6)

# Reasignar Gate
sep_rea = tk.Frame(manual_frame, bg=BG_PANEL)
sep_rea.grid(sticky="ew", pady=(2, 2), padx=4)
tk.Label(sep_rea, text="🔄 Reasignar Gate Manualmente",
         bg=BG_PANEL, fg=C_LABEL_FG,
         font=("Segoe UI", 8, "bold")).pack(anchor="w")

fila_rea1 = tk.Frame(manual_frame, bg=BG_PANEL)
fila_rea1.grid(sticky="ew", pady=2, padx=4)
tk.Label(fila_rea1, text="ID Avión:", width=12, anchor="w",
         bg=BG_PANEL, fg=C_LABEL_FG, font=("Segoe UI", 8)).pack(side=tk.LEFT)
entrada_reasignar_avion = ttk.Entry(fila_rea1, width=14)
entrada_reasignar_avion.pack(side=tk.LEFT, padx=3)

fila_rea2 = tk.Frame(manual_frame, bg=BG_PANEL)
fila_rea2.grid(sticky="ew", pady=2, padx=4)
tk.Label(fila_rea2, text="Nuevo Gate:", width=12, anchor="w",
         bg=BG_PANEL, fg=C_LABEL_FG, font=("Segoe UI", 8)).pack(side=tk.LEFT)
entrada_reasignar_gate = ttk.Entry(fila_rea2, width=14)
entrada_reasignar_gate.pack(side=tk.LEFT, padx=3)

make_btn(manual_frame, "🔄 Reasignar Gate", "MN.TButton", btn_reasignar_gate_click)


# =====================================================================
# CONSOLA
# =====================================================================

consola = ttk.LabelFrame(root,
    text="  📋  Consola / Resultados", style="Panel.TLabelframe")
consola.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

scrollbar_caja = tk.Scrollbar(consola, bg=BG_PANEL, troughcolor=BG_APP)
scrollbar_caja.pack(side=tk.RIGHT, fill=tk.Y)

caja = tk.Text(consola,
    font=("Consolas", 9),
    bg=BG_CONSOLA, fg=C_TEXT_DARK,
    insertbackground=C_TEXT_DARK,
    selectbackground="#D8C8F0", selectforeground=C_TEXT_DARK,
    relief="flat", bd=0, padx=8, pady=6,
    yscrollcommand=scrollbar_caja.set)
caja.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
scrollbar_caja.config(command=caja.yview)


# =====================================================================
# PANEL GRÁFICAS
# =====================================================================

panel_graficas = ttk.LabelFrame(root,
    text="  📊  Visualización de Gráficas", style="Panel.TLabelframe")
panel_graficas.grid(row=1, column=1, padx=8, pady=4, sticky="nsew")
panel_graficas.rowconfigure(0, weight=1)
panel_graficas.columnconfigure(0, weight=1)


# =====================================================================
# BARRA BOTONES GRÁFICAS
# =====================================================================

graficas = ttk.LabelFrame(root,
    text="  Gráficas", style="Light.TLabelframe")
graficas.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=4)
graficas.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

botones_graficas = [
    ("Aeropuertos Schengen",    btn_grafica_aeropuertos_click,   "GR.TButton"),
    ("Llegadas por hora",       btn_grafica_llegadas_click,      "GR.TButton"),
    ("Vuelos por Aerolínea",    btn_grafica_airlines_click,      "GR.TButton"),
    ("Vuelos Schengen vs No Schengen", btn_grafica_schengen_click,      "GR.TButton"),
    ("Mapa de Gates",           btn_grafica_gates_click,         "GR.TButton"),
    ("Ocupación del Día",       btn_grafica_ocupacion_dia_click, "GR.TButton"),
    ("Borrar Gráfica",          btn_borrar_grafica_click,        "DEL.TButton"),
]

for i, (txt, cmd, est) in enumerate(botones_graficas):
    ttk.Button(graficas, text=txt, style=est,
               command=cmd).grid(row=0, column=i, sticky="ew", padx=3, pady=4)

#===control===



root.mainloop()

