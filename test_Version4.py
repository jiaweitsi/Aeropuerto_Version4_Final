# -------------------------------------------------------
# SECCION DE TEST
# -------------------------------------------------------
from aircraft import *

if __name__ == "__main__":
    print("=== TEST AIRCRAFT.PY - VERSION 4 ===\n")

    print("Test 1: Cargar llegadas")
    aircrafts = LoadArrivals("Arrivals.txt")
    print("Llegadas cargadas:", len(aircrafts))

    print("\nTest 2: Cargar salidas")
    departures = LoadDepartures("Departures.txt")
    print("Salidas cargadas:", len(departures))

    print("\nTest 3: Merge de movimientos")
    merged = MergeMovements(aircrafts, departures)
    print("Total movimientos fusionados:", len(merged))

    print("\nTest 4: Aviones nocturnos")
    nocturnos = NightAircraft(merged)
    print("Aviones nocturnos:", len(nocturnos))
    i = 0
    while i < len(nocturnos) and i < 5:
        print("  -", nocturnos[i].aircraft, "sale a", nocturnos[i].destination,
              "a las", nocturnos[i].departure_time)
        i = i + 1

    print("\nTest 5: Grafica llegadas")
    PlotArrivals(aircrafts)

    print("\n=== FIN TEST ===")