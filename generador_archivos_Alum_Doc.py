
import csv

dic = {"Docente1": "Alumno1", "Docente2": "Alumno2","Docente3": "Alumno3",
        "Docente4": "Alumno4","Docente5": "Alumno5","Docente6": "Alumno6"}

archivo = "Docentes-Alumnos.csv"

csv = open(archivo,"w")
Head = ["Docente | Alumno \n"]
csv.write(f"{','.join(Head)}\n")
for key in dic.keys():
    nombre_Docente = key
    nombre_alumno = dic[key]
    filas = nombre_Docente +"  "+ nombre_alumno + "\n"
    csv.write(f"{''.join(filas)}")
