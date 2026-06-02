from airport import *
import matplotlib.pyplot as plt
import math

# -------------------------------------------------------
# CLASE Aircraft - Version 4
# Añadimos destination y departure_time respecto a V3
# -------------------------------------------------------

class Aircraft:
    def __init__(self, aircraft, company, origin, time, destination="", departure_time=""):
        self.aircraft = aircraft          # id del avion (string)
        self.company = company            # codigo ICAO aerolinea (3 letras)
        self.origin = origin              # aeropuerto origen (4 letras ICAO)
        self.time = time                  # hora de llegada (hh:mm)

       #===VERSIÓN 4===
        self.destination = destination    # aeropuerto destino (4 letras ICAO) - NUEVO V4
        self.departure_time = departure_time  # hora de salida (hh:mm) - NUEVO V4


# -------------------------------------------------------
# FUNCIONES VERSION 2
# -------------------------------------------------------

# ===== LOAD ARRIVALS  =====
def LoadArrivals(filename):
    lista_arrivals = []
    try:
        f = open(filename, "r")
        lineas = f.readlines()
        f.close()

        i = 1
        while i < len(lineas):
            partes = lineas[i].split()
            if len(partes) == 4:
                aircraft = partes[0]
                origin = partes[1]
                time = partes[2]
                company = partes[3]
                if ':' in time:
                    nuevo = Aircraft(aircraft, company, origin, time)
                    lista_arrivals.append(nuevo)
            i = i + 1

    except FileNotFoundError:
        print("No se encontro el archivo:", filename)
        return []
    return lista_arrivals

# ===== PLOT ARRIVALS  =====
def PlotArrivals(aircrafts):

    if len(aircrafts) == 0:
        print("No existeix la llista")
        return

    Vx = range(24)  # hores
    Vy = [0] * 24  # arribades/hora
    i = 0
    while i < len(aircrafts):
        fila = aircrafts[i]
        tiempo = fila.time
        if tiempo != "":  # saltar aviones nocturnos sin hora de llegada
            partes = tiempo.split(":")
            if len(partes) == 2 and partes[0] != "":
                hlanding = int(partes[0])
                Vy[hlanding] = Vy[hlanding] + 1
        i = i + 1

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(Vx, Vy, color='skyblue', edgecolor='black')
    ax.set_title("Frecuencia de aterrizajes por hora")
    ax.set_ylabel("Número de aviones")
    ax.set_xlabel("Hora del día")
    ax.set_xticks(range(0, 24))

    return fig


# ===== SAVE FLIGHTS  =====
def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0:
        print("No existeix la llista")
        return False
    try:
        out = open(filename, 'w')
        out.write("Aircraft\tOrigin\tTime\tCompany\tDestination\tDeparture\n")
        i = 0
        while i < len(aircrafts):
            fila = aircrafts[i]

            aircraft = fila.aircraft if fila.aircraft != "" else "-"
            origin = fila.origin if fila.origin != "" else "-"
            arrival = fila.time if fila.time != "" else "-"
            airline = fila.company if fila.company != "" else "-"
            destination = fila.destination if fila.destination != "" else "-"
            departure = fila.departure_time if fila.departure_time != "" else "-"

            out.write(aircraft + "\t" + origin + "\t" + arrival + "\t" +
                      airline + "\t" + destination + "\t" + departure + "\n")
            i = i + 1

        out.close()
        return True
    except:
        print("No se pudo guardar el archivo")
        return False


# ===== PLOT AIRLINES  =====
def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("No existeix la llista")
        return

    # Primero contamos los vuelos por aerolinea (igual que antes)
    Vx = []
    Vy = []
    i = 0
    while i < len(aircrafts):
        fila = aircrafts[i]
        airline = fila.company
        if airline not in Vx:
            Vx.append(airline)
            Vy.append(1)
        else:
            encontrado = False
            x = 0
            while not encontrado and x < len(Vx):
                if Vx[x] == airline:
                    encontrado = True
                else:
                    x = x + 1
            if encontrado:
                Vy[x] = Vy[x] + 1
        i = i + 1

    # Ahora ordenamos para quedarnos solo con las 10 con mas vuelos
    # Usamos bubble sort para ordenar de mayor a menor
    n = len(Vx)
    j = 0
    while j < n - 1:
        k = 0
        while k < n - j - 1:
            if Vy[k] < Vy[k + 1]:
                # Intercambiamos vuelos
                temp_y = Vy[k]
                Vy[k] = Vy[k + 1]
                Vy[k + 1] = temp_y
                # Intercambiamos nombres
                temp_x = Vx[k]
                Vx[k] = Vx[k + 1]
                Vx[k + 1] = temp_x
            k = k + 1
        j = j + 1

    # Nos quedamos solo con las 10 primeras
    if len(Vx) > 10:
        Vx = Vx[0:10]
        Vy = Vy[0:10]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(Vx, Vy, color='orange')
    ax.set_xlabel("Aerolíneas")
    ax.set_ylabel("Número de vuelos")
    ax.set_title("Top 10 aerolíneas con más vuelos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# ===== PLOT FLIGHTS TYPE  =====
def PlotFlightsType(aircrafts):
    if len(aircrafts) > 0:
        schengen = 0
        no_schengen = 0

        schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                          'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS','GC']

        i = 0
        while i < len(aircrafts):
            fila = aircrafts[i]
            origen = fila.origin
            inicio = origen[0:2]
            encontrado = False
            j = 0
            while j < len(schengen_codes) and not encontrado:
                if schengen_codes[j] == inicio:
                    encontrado = True
                else:
                    j = j + 1

            if encontrado == True:
                schengen = schengen + 1
            else:
                no_schengen = no_schengen + 1
            i = i + 1

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['Schengen', 'No Schengen'], [schengen, no_schengen], color=['blue', 'red'])
        ax.set_title("Vuelos Schengen vs No Schengen")
        ax.set_ylabel("Cantidad de vuelos")
        return fig
    else:
        return None

# ===== MAP FLIGHTS  =====
def MapFlights(lista_arrivals, lista_airports):
    f = open("trayectorias.kml", "w")

    # Cabecera del archivo KML - comillas dobles obligatorias para Google Earth
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    f.write("<Document>\n")

    # Estilo para vuelos Schengen: linea verde
    f.write("  <Style id=\"schengen\">\n")
    f.write("    <LineStyle>\n")
    f.write("      <color>ff00ff00</color>\n")
    f.write("      <width>3</width>\n")
    f.write("    </LineStyle>\n")
    f.write("  </Style>\n")

    # Estilo para vuelos no Schengen: linea roja
    f.write("  <Style id=\"noschengen\">\n")
    f.write("    <LineStyle>\n")
    f.write("      <color>ff0000ff</color>\n")
    f.write("      <width>3</width>\n")
    f.write("    </LineStyle>\n")
    f.write("  </Style>\n")

    # Coordenadas de Barcelona El Prat (LEBL)
    lat_bcn = 41.297445
    lon_bcn = 2.0832941

    schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                      'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS','GC']

    i = 0
    while i < len(lista_arrivals):
        vuelo = lista_arrivals[i]

        # Buscamos el aeropuerto origen en la lista
        aeropuerto_encontrado = None
        j = 0
        while j < len(lista_airports):
            if lista_airports[j].code == vuelo.origin:
                aeropuerto_encontrado = lista_airports[j]
            j = j + 1

        # Solo dibujamos si encontramos el aeropuerto origen
        if aeropuerto_encontrado != None:

            # Comprobamos si es Schengen mirando las 2 primeras letras del codigo origen
            es_schengen = False
            k = 0
            while k < len(schengen_codes):
                if vuelo.origin[0:2] == schengen_codes[k]:
                    es_schengen = True
                k = k + 1

            if es_schengen:
                estilo = "schengen"
            else:
                estilo = "noschengen"

            f.write("  <Placemark>\n")
            f.write("    <name>" + vuelo.aircraft + " desde " + vuelo.origin + "</name>\n")
            f.write("    <styleUrl>#" + estilo + "</styleUrl>\n")
            f.write("    <LineString>\n")
            f.write("      <tessellate>1</tessellate>\n")
            f.write("      <coordinates>\n")
            # Origen: lon,lat del aeropuerto de salida
            f.write("        " + str(aeropuerto_encontrado.lon) + "," +
                    str(aeropuerto_encontrado.lat) + ",0\n")
            # Destino: lon,lat de Barcelona
            f.write("        " + str(lon_bcn) + "," + str(lat_bcn) + ",0\n")
            f.write("      </coordinates>\n")
            f.write("    </LineString>\n")
            f.write("  </Placemark>\n")

        i = i + 1

    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()
    print("Archivo trayectorias.kml generado.")

# ===== LONG FLIGHT ARRIVALS  =====
def LongFlightArrivals(aircrafts, lista_aeropuertos):
    vuelos_largos = []

    lat_bcn = 0
    lon_bcn = 0
    k = 0
    while k < len(lista_aeropuertos):
        if lista_aeropuertos[k].code == "LEBL":
            lat_bcn = lista_aeropuertos[k].lat
            lon_bcn = lista_aeropuertos[k].lon
        k = k + 1

    radio_tierra = 6371

    i = 0
    while i < len(aircrafts):
        vuelo = aircrafts[i]
        lat_origen = 0
        lon_origen = 0
        encontrado = False

        j = 0
        while j < len(lista_aeropuertos) and not encontrado:
            if lista_aeropuertos[j].code == vuelo.origin:
                lat_origen = lista_aeropuertos[j].lat
                lon_origen = lista_aeropuertos[j].lon
                encontrado = True
            j = j + 1

        if encontrado:
            phi1 = math.radians(lat_origen)
            phi2 = math.radians(lat_bcn)
            dphi = math.radians(lat_bcn - lat_origen)
            dlambda = math.radians(lon_bcn - lon_origen)

            a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distancia = radio_tierra * c

            if distancia > 2000:
                vuelos_largos.append(vuelo)
        i = i + 1

    return vuelos_largos


# -------------------------------------------------------
# FUNCIONES VERSION 4
# -------------------------------------------------------

# ===== LOAD DEPARTURES  =====
def LoadDepartures(filename):
    # Carga el archivo de salidas y devuelve lista de Aircraft
    # Solo rellena: aircraft, company, destination, departure_time
    # Si no existe devuelve lista vacia

    lista_departures = []

    try:
        f = open(filename, "r")
        lineas = f.readlines()
        f.close()
    except FileNotFoundError:
        print("No se encontro el archivo:", filename)
        return lista_departures

    # Formato: AIRCRAFT DESTINATION DEPARTURE AIRLINE
    i = 1
    while i < len(lineas):
        partes = lineas[i].split()
        if len(partes) == 4:
            aircraft = partes[0]
            destination = partes[1]
            departure_time = partes[2]
            company = partes[3]
            if ':' in departure_time:
                # Solo rellenamos campos de salida, llegada vacia
                nuevo = Aircraft(aircraft, company, "", "", destination, departure_time)
                lista_departures.append(nuevo)
        i = i + 1

    return lista_departures

# ===== MERGE MOVEMENTS  =====
def MergeMovements(arrivals, departures):
    # Combina listas de llegadas y salidas por ID de avion
    # Si los tiempos son compatibles (llegada < salida) se fusionan
    # Aviones solo en departures = aviones nocturnos
    # Devuelve lista fusionada

    if len(arrivals) == 0 or len(departures) == 0:
        print("Error: una de las listas esta vacia")
        return []

    # Empezamos copiando todas las llegadas
    merged = []
    i = 0
    while i < len(arrivals):
        ac = arrivals[i]
        nuevo = Aircraft(ac.aircraft, ac.company, ac.origin, ac.time, ac.destination, ac.departure_time)
        merged.append(nuevo)
        i = i + 1

    # Para cada salida buscamos si hay una llegada del mismo avion compatible
    i = 0
    while i < len(departures):
        dep = departures[i]
        encontrado = False

        j = 0
        while j < len(merged) and not encontrado:
            # Mismo id de avion
            if merged[j].aircraft == dep.aircraft:
                # Comprobamos que la llegada es antes que la salida
                if merged[j].time != "" and merged[j].departure_time == "":
                    hora_arr = int(merged[j].time.split(":")[0])
                    min_arr = int(merged[j].time.split(":")[1])
                    hora_dep = int(dep.departure_time.split(":")[0])
                    min_dep = int(dep.departure_time.split(":")[1])

                    total_arr = hora_arr * 60 + min_arr
                    total_dep = hora_dep * 60 + min_dep

                    if total_dep > total_arr:
                        # Fusionamos: añadimos datos de salida al avion de llegada
                        merged[j].destination = dep.destination
                        merged[j].departure_time = dep.departure_time
                        encontrado = True
            j = j + 1

        if not encontrado:
            # Es un avion nocturno: solo tiene salida, no llegada
            nuevo = Aircraft(dep.aircraft, dep.company, "", "", dep.destination, dep.departure_time)
            merged.append(nuevo)

        i = i + 1

    return merged

# ===== NIGHT AIRCRAFT  =====
def NightAircraft(aircrafts):
    # Devuelve lista de aviones que solo tienen salida (sin llegada)
    # Son los que pasaron la noche en el aeropuerto

    if len(aircrafts) == 0:
        print("Error: la lista esta vacia")
        return []

    nocturnos = []
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        # Avion nocturno: sin hora de llegada pero con hora de salida
        if ac.time == "" and ac.departure_time != "":
            nocturnos.append(ac)
        i = i + 1

    return nocturnos

# ===== DEPARTURES AFTER HOUR =====
def DeparturesAfterHour(aircrafts, hour):
    if len(aircrafts) == 0:
        return 0
    count = 0  # contador de vuelos que salen después de la hora indicada
    i = 0

    while i < len(aircrafts):
        ac = aircrafts[i]
        # cogemos aviones que tienen hora de salida registrada
        if ac.departure_time != "":
            # cogemos la primera parte de la hora ej 11:00, pues 11
            hora_dep = int(ac.departure_time.split(":")[0])

            # si la hora de salida es mayor a la hora indicada, contamos el vuelo
            if hora_dep > hour:
                count = count + 1

        i = i + 1

    # devolver el total
    return count