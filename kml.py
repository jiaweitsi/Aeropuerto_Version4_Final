<kml xmlns="http://www.opengis.net/kml/2.1">
<Document>
  <Placemark>
   <name>Route LEAM - NIKF </name>
   <LineString>
    <altitudeMode>clampToGround</altitudeMode>
    <extrude>1</extrude>
    <tessellate>1</tessellate>
     <coordinates>
      -2.3733335667,36.8422863167
      -22.6144444444,63.9869444444
     </coordinates>
  </LineString>
 </Placemark>
</Document>
</kml>


def btn_limpiar_todo_click():
 # 1. Vaciar las listas de datos (¡Cuidado! Se borra lo que no hayas guardado)
 lista_trabajo.clear()
 lista_vuelos.clear()

 # 2. Borrar el texto de la caja derecha
 caja.delete(1.0, tk.END)

 # 3. Borrar el gráfico si existe
 global canvas_picture
 if canvas_picture is not None:
  canvas_picture.get_tk_widget().destroy()
  canvas_picture = None

 messagebox.showinfo("Limpiar", "Pantalla y datos reseteados correctamente")


btn_limpiar = tk.Button(button_pictures_frame, text="BORRAR TODO",
                        fg="white", bg="red",  # ¡Color rojo para que resalte!
                        command=btn_limpiar_todo_click)

btn_limpiar.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")


################################################
def MapFlights(lista_arrivals, lista_airports):
 # 1. Creamos/Abrimos el archivo
 f = open("trayectorias.kml", "w")

 # 2. Cabecera obligatoria (Anexo A)
 f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
 f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
 f.write('<Document>\n')

 # Coordenadas fijas de Barcelona (Destino) [cite: 758]
 lat_dest = 41.297445
 lon_dest = 2.0832941

 # 3. Recorremos los vuelos con un while
 i = 0
 while i < len(lista_arrivals):
  vuelo = lista_arrivals[i]
  codigo_de_donde_viene = vuelo.origin

  # 4. Buscamos el aeropuerto de origen en la otra lista
  aeropuerto_encontrado = None
  j = 0
  while j < len(lista_airports):
   if lista_airports[j].code == codigo_de_donde_viene:
    aeropuerto_encontrado = lista_airports[j]
   j = j + 1

  # 5. Si lo encontramos, escribimos el Placemark [cite: 672]
  if aeropuerto_encontrado != None:
   # Determinamos el color segun Schengen [cite: 896]
   # KML usa colores en formato AABBGGRR (opcional para nivel basico)
   # Si no usas estilos, saldra el color por defecto (blanco/rojo)

   f.write('<Placemark>\n')
   f.write('  <name>' + vuelo.aircraft + ' desde ' + vuelo.origin + '</name>\n')
   f.write('  <LineString>\n')
   f.write('    <coordinates>\n')
   # IMPORTANTE: El formato KML es LON,LAT (al revés que lo usual) [cite: 670]
   f.write('      ' + str(aeropuerto_encontrado.lon) + ',' + str(aeropuerto_encontrado.lat) + '\n')
   f.write('      ' + str(lon_dest) + ',' + str(lat_dest) + '\n')
   f.write('    </coordinates>\n')
   f.write('  </LineString>\n')
   f.write('</Placemark>\n')

  i = i + 1

 # 6. Cierre del archivo
 f.write('</Document>\n')
 f.write('</kml>\n')
 f.close()
 print("Archivo KML generado.")