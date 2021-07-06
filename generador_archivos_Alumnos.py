import csv

dic = {"Alumno1": ["451254" ,"alumno1@gmail.com"], "Alumno2": ["777465", "alumno2@gmail.com"],"Alumno3": ["565645" , "alumno3@gmail.com"],
        "Alumno4": ["465321", "alumno4@gmail.com"],"Alumno5": ["454123", "alumno5@gmail.com"],"Alumno6": ["564546", "alumno6@gmail.com"]}

archivo = "Alumnos.csv"

csv = open(archivo,"w")
Head = ["Alumno | Padron | Email \n"]
csv.write(f"{','.join(Head)}\n")
for key in dic.keys():
    Nombre_alumno = key
    Email_alumno,Padron_Alumno = dic[key]
    filas = [Nombre_alumno +"  "+ Email_alumno+" "+Padron_Alumno +" " "\n"]
    csv.write(f"{''.join(filas)}")
