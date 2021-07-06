import csv
with open("alumnos.csv", 'w', newline='', encoding="UTF-8") as archivo_csv:
    csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
    csv_writer.writerow(["Padron", "Nombre", "Apellido"]) #Escribimos el header
    alumnos = {}
    padron = 0
    nombre = 1
    apellido = 2
    alumnos[padron] = (nombre,apellido)
    for padron, nombre_completo in alumnos.items():
        nombre, apellido = nombre_completo
        csv_writer.writerow((padron, nombre, apellido))