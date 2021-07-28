<<<<<<< HEAD
import os

def validar_opcion(numero_min: int, numero_max: int) -> int:
    '''
    Nos permite validar para que solo se puedan ingresar ciertos números enteros.

    PRE: Recibe dos números enteros que simbolizan la cantidad de opciones.
    POST: Devuelve un número entero dentro del rango de opciones.
    '''
    decision = input("Ingrese su opción: ")
    while not decision.isnumeric() or int(decision) > numero_max or int(decision) < numero_min:
        print("La opción ingresada, no es valida.")
        decision = input("Intente nuevamente, ingrese su opción: ")
    return int(decision)

def listar_archivos() -> None:
    contador = 0
    print("Listado de archivos de la carpeta actual (y subcarpetas): ")
    directorio = os.getcwd()
    for ruta, subcarpetas, archivos in os.walk(directorio):
        for nombre in archivos:
            contador += 1
            listado = os.path.join(ruta, nombre)
            print(f"{contador}.- {listado}")



def crear_archivo():
    pass


def subir_archivo():
    pass


def descargar_archivo():
    pass


def sincronizar():
    pass


def generar_carpetas_evaluacion():
    pass


def actualizar_entregas_via_mail():
    pass


def main ()->None:
    cerrar_menu = False
    while not cerrar_menu:
        print("""
        -***************************-
        Bienvenido al menú inicial
        -***************************-
        Por favor, elija una opción.
        1. Listar archivos de la carpeta actual.
        2. Crear un archivo.
        3. Subir un archivo.
        4. Descargar un archivo.
        5. Sincronizar.
        6. Generar carpetas de una evaluación.
        7. Actualizar entregas de alumnos vía mail
        8. Salir
        """)
        opcion = validar_opcion(1, 8)
        if opcion == 1:
            listar_archivos()
        elif opcion == 2:
            pass
        elif opcion == 3:
            pass
        elif opcion == 4:
            pass
        elif opcion == 5:
            pass
        elif opcion == 6:
            pass
        elif opcion == 7:
            pass
        elif opcion == 8:
            cerrar_menu = True

=======
import os

def validar_opcion(numero_min: int, numero_max: int) -> int:
    '''
    Nos permite validar para que solo se puedan ingresar ciertos números enteros.

    PRE: Recibe dos números enteros que simbolizan la cantidad de opciones.
    POST: Devuelve un número entero dentro del rango de opciones.
    '''
    decision = input("Ingrese su opción: ")
    while not decision.isnumeric() or int(decision) > numero_max or int(decision) < numero_min:
        print("La opción ingresada, no es valida.")
        decision = input("Intente nuevamente, ingrese su opción: ")
    return int(decision)

def listar_archivos() -> None:
    contador = 0
    print("Listado de archivos de la carpeta actual (y subcarpetas): ")
    directorio = os.getcwd()
    for ruta, subcarpetas, archivos in os.walk(directorio):
        for nombre in archivos:
            contador += 1
            listado = os.path.join(ruta, nombre)
            print(f"{contador}.- {listado}")



def crear_archivo():
    pass


def subir_archivo():
    pass


def descargar_archivo():
    pass


def sincronizar():
    pass


def generar_carpetas_evaluacion():
    pass


def actualizar_entregas_via_mail():
    pass


def main ()->None:
    cerrar_menu = False
    while not cerrar_menu:
        print("""
        -***************************-
        Bienvenido al menú inicial
        -***************************-
        Por favor, elija una opción.
        1. Listar archivos de la carpeta actual.
        2. Crear un archivo.
        3. Subir un archivo.
        4. Descargar un archivo.
        5. Sincronizar.
        6. Generar carpetas de una evaluación.
        7. Actualizar entregas de alumnos vía mail
        8. Salir
        """)
        opcion = validar_opcion(1, 8)
        if opcion == 1:
            listar_archivos()
        elif opcion == 2:
            pass
        elif opcion == 3:
            pass
        elif opcion == 4:
            pass
        elif opcion == 5:
            pass
        elif opcion == 6:
            pass
        elif opcion == 7:
            pass
        elif opcion == 8:
            cerrar_menu = True

>>>>>>> b2061dfc4d8fd920d5d23befa8d03f786441a467
main()