from airport import *

bcn = Airport("LEBL", "41.29", "2.08")
SetSchengen(bcn)
PrintAirport(bcn)


mi_lista = []
AddAirport(mi_lista, bcn)
print("Aeropuertos en lista:", len(mi_lista))


RemoveAirport(mi_lista, "LEBL")
print("Aeropuertos tras borrar:", len(mi_lista))