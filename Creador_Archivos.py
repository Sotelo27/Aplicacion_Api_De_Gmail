from random import randint, sample
import csv
import os
import string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_ALUMNOS = os.path.join(BASE_DIR, "alumnos.txt")
RUTA_NOTAS = os.path.join(BASE_DIR, "notas.txt")

RUTA_ALUMNOS_CSV = os.path.join(BASE_DIR, "alumnos.csv")
RUTA_NOTAS_CSV = os.path.join(BASE_DIR, "notas.csv")

MATERIAS = (
            "Física II", "Algoritmos y Programacion I", "Algoritmos y Programacion II", 
            "Algoritmos y Programacion II", "AMII", "ALGII", "Física", "Química", "Teoría de Algoritmos I",
           )

INF_PADRON = 70000
SUP_PADRON = 120000
INF_NOTA = 0
SUP_NOTA = 10
MAX_LETRAS = 6
CANTIDAD = 100

def validar_padron(alumnos: dict) -> int:
    padron = randint(INF_PADRON, SUP_PADRON)
    while padron in alumnos:
        padron = randint(INF_PADRON, SUP_PADRON)
    return str(padron)


def crear_archivo_csv_alumnos(alumnos: dict):
    
    with open(RUTA_ALUMNOS_CSV, 'w',newline='', encoding="UTF-8") as archivo_csv:
        csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(["Padron", "Nombre", "Apellido"]) #Escribimos el header

        for padron, nombre_completo in alumnos.items():
            nombre, apellido = nombre_completo
            csv_writer.writerow((padron, nombre, apellido))


def crear_archivo_alumnos(alumnos: dict) -> None:
    
    with open(RUTA_ALUMNOS, 'w', encoding="UTF-8") as archivo:
        for padron, info in alumnos.items():
            nombre, apellido = info
            archivo.write(f"{','.join((padron,nombre,apellido))}\n")

def crear_archivo_notas(notas: dict) -> None:
    
    with open(RUTA_NOTAS, 'w', encoding="UTF-8") as archivo:
        for padron, materias in notas.items():
            for materia, nota in materias:
                archivo.write(f"{','.join((padron, materia, nota))}\n")

def generar_notas(alumnos: dict) -> dict:
    notas = dict()
    for padron in alumnos:
        for materia in MATERIAS:
            nota = str(randint(INF_NOTA, SUP_NOTA))
            if padron not in notas:
                notas[padron] = [(materia, nota)]
            else:
                notas[padron].append((materia,nota))
    return notas

def generar_datos_alumnos(gen_string: str) -> dict:
    alumnos = dict()
    for i in range(CANTIDAD):
        padron = validar_padron(alumnos)
        nombre = "".join(sample(gen_string, MAX_LETRAS))
        apellido = "".join(sample(gen_string, MAX_LETRAS))
        alumnos[padron] = (nombre, apellido)
    return alumnos

def main():
    gen_string = string.ascii_letters
    alumnos = generar_datos_alumnos(gen_string)
    notas = generar_notas(alumnos)
    
    crear_archivo_alumnos(alumnos)
    crear_archivo_notas(notas)

    crear_archivo_csv_alumnos(alumnos)
    # crear_archivo_csv_notas(notas)

main()