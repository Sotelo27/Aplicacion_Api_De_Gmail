import csv

dic = {"Docente1": "docente1@gmail.com", "Docente2": "docente2@gmail.com","Docente3": "docente3@gmail.com",
        "Docente4": "docente4@gmail.com","Docente5": "docente5@gmail.com","Docente6": "docente6@gmail.com"}

archivo = "Docentes.csv"

csv = open(archivo,"w")
Head = ["Docente | Email_Docente \n"]
csv.write(f"{','.join(Head)}\n")
for key in dic.keys():
    Nombre_Docente = key
    Email_Docente = dic[key]
    filas = Nombre_Docente +"  "+ Email_Docente + "\n"
    csv.write(f"{''.join(filas)}")
