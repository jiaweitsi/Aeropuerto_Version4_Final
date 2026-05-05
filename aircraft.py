from matplotlib.pyplot import plot
from airport import *

class Aircraft:
    def __init__(self, aircraft, company, origin, time):
        self.aircraft= aircraft #string
        self.company= company #3 letras ICAO code
        self.origin= origin #4 letras ICAO code
        self.time= time #formato hh:mm

def LoadArrivals(filename):
    lista_arrivals= []
    try:
        f= open(filename,"r")
        lineas = f.readlines()
        f.close()

        i=1
        while i < len(lineas):
            partes = lineas[i].split()
            if len(partes)==4:
                aircraft = partes[0]
                origin = partes[1]
                time = partes[2]
                company = partes[3]
                if ':' in time:
                    nuevo= Aircraft(aircraft, company, origin, time)
                    lista_arrivals.append(nuevo)
            i=i+1

    except FileNotFoundError:
        print("No se encontro el archivo:", filename)
        return []
    return lista_arrivals

#mis_vuelos = LoadArrivals("arrivals.txt")??

def PlotArrivals (aircrafts):

    if len(aircrafts) == 0:
        print("No existeix la llista")
        return

    import matplotlib.pyplot as pyplot
    Vx = range(24)  # hores
    Vy = [0] * 24  # arribades/hora
    i = 0
    while i < len(aircrafts): #el while para formar la función
        fila = aircrafts[i] #cojo una fila
        tiempo= fila.time #al definirlo como clase el aircraft, cojo solo el atributo de time, con el fila.time
        partes = tiempo.split(":") #parto el time, pero con el : diviendolo

        hlanding = int(partes[0]) #aqui ya defino lo que seria la hora de aterrizaje

        Vy[hlanding] = Vy[hlanding] + 1 #ponemos la hroa en su casila
        i = i + 1
    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(Vx, Vy, color='skyblue', edgecolor='black')
    ax.set_title("Frecuencia de aterrizajes por hora")
    ax.set_ylabel("Número de aviones")
    ax.set_xlabel("Hora del día")
    ax.set_xticks(range(0, 24))  # Para que se vean todas las horas en el eje X

    return fig

def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0:
        print("No existeix la llista")
        return False
    try:
        out = open(filename, 'w')
        out.write("Aircraft\tOrigin\tTime\tCompany\n") #la cabecera del txt
        i = 0
        while i < len(aircrafts):
            fila = aircrafts[i]

            aircraft = fila.aircraft
            origin = fila.origin
            arrival = fila.time
            airline = fila.company

            if aircraft == "":
                aircraft = "-"
            if origin == "":
                origin = "-"
            if arrival == "":
                arrival = "-"
            if airline == "":
                airline = "-"
            out.write(aircraft + "\t" + origin + "\t" + arrival + "\t" + airline + "\n")

            i = i + 1

        out.close()
        return True
    except FileNotFoundError:
        print("No existeix la llista")


def PlotAirlines (aircrafts):
        if len(aircrafts) == 0:
            print("No existeix la llista")
            return

        Vx = []  # aerolinies
        Vy = []  # nº vols
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
            i=i+1

                    # també es podría fer amb pos=airlines.index("airline") (??)

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(Vx, Vy, color='orange')
        ax.set_xlabel("Aerolíneas")
        ax.set_ylabel("Número de vuelos")
        ax.set_title("Vuelos por Compañía")

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig


def PlotFlightsType(aircrafts):

    if len(aircrafts)>0:
        schengen = 0 #contadores schengen vs no schengen
        no_schengen = 0

        schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                    'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

        i = 0
        while i < len(aircrafts):
            fila=aircrafts[i] #selecciono una fila
            origen = fila.origin  #cojo el icao ej: LEBL
            inicio= origen[0:2]  #lo mismo que V1, cogiendo LE
            encontrado = False
            j = 0
            while j < len(schengen_codes) and not encontrado: #misma busqueda que version 1
                if schengen_codes[j] == inicio:
                    encontrado = True
                else:
                    j = j + 1

            if schengen == True:
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
        return []


from airport import *
import math


def MapFlights(lista_arrivals, lista_airports):
    #abrimos el archivo
    f = open("trayectorias.kml", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')

    #coordenadas LEBL
    lat_dest = 41.297445
    lon_dest = 2.0832941

    i = 0
    while i < len(lista_arrivals):
        vuelo = lista_arrivals[i]
        codigo_de_donde_viene = vuelo.origin

        #buscamos el aeropuerto de origen en la otra lista
        aeropuerto_encontrado = None
        j = 0
        while j < len(lista_airports):
            if lista_airports[j].code == codigo_de_donde_viene:
                aeropuerto_encontrado = lista_airports[j]
            j = j + 1

        #Si encontrado escribir Placemark
        if aeropuerto_encontrado != None:

            f.write('<Placemark>\n')
            f.write('  <name>' + vuelo.aircraft + ' desde ' + vuelo.origin + '</name>\n')
            f.write('  <LineString>\n')
            f.write('    <coordinates>\n')

            f.write('      ' + str(aeropuerto_encontrado.lon) + ',' + str(aeropuerto_encontrado.lat) + '\n')
            f.write('      ' + str(lon_dest) + ',' + str(lat_dest) + '\n')
            f.write('    </coordinates>\n')
            f.write('  </LineString>\n')
            f.write('</Placemark>\n')

        i = i + 1

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    print("Archivo KML generado.")


def LongFlightArrivals(aircrafts, lista_aeropuertos):
    vuelos_largos = []

    #Buscamos LEBL en la lista de aeropuertos
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

        #buscamos las coordenadas del origen
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

        #calculamos la distancia
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