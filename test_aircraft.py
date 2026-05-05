from xml.dom.minidom import Document

from aircraft import *
# Testeo def LoadArrivals
vuelos = LoadArrivals("Arrivals.txt")

if len(vuelos) > 0:
    test = vuelos[0]

    print(test.aircraft, test.company, test.origin, test.time)
else:
    print("Error")


