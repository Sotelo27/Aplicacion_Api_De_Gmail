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


def menu_listar_archivos() -> None:
    cerrar_menu = False
    while not cerrar_menu:
        print("""
        En este menú puede listar los archivos o navegar a través de carpetas.
        1. Mostrar los archivos locales.
        2. Mostrar los archivos en remoto.
        3. Abrir una carpeta existente.
        4. Volver una carpeta atrás.
        5. Cerrar el menú.
        """)
        opcion = validar_opcion(1, 5)
        if opcion == 1:
            listar_archivos_local()
        elif opcion == 2:
            print("Funcionalidad no implementada.")
        elif opcion == 3:
            nombre = input("Ingrese el nombre de la carpeta a abrir: ")
            try:
                os.chdir(nombre)
            except:
                print("Ha ocurrido un error.")
            else:
                print("Carpeta abierta exitosamente.")
        elif opcion == 4:
            os.chdir("..")
        elif opcion == 5:
            cerrar_menu = True


def listar_archivos_local() -> None:
    contador = 1
    print("Listado de archivos de la carpeta actual (y subcarpetas): ")
    directorio = os.getcwd()
    for ruta, subcarpetas, archivos in os.walk(directorio):
        subnivel = ruta.replace(directorio, '').count(os.sep)
        separacion_carpetas = ' ' * 8 * (subnivel)
        print(f"{separacion_carpetas}{contador} » {os.path.basename(ruta)}/")
        separacion_archivos = ' ' * 8 * (subnivel + 1)
        for nombre_archivos in archivos:
            print(f"{separacion_archivos}{nombre_archivos}")
        contador += 1


def menu_crear_archivo_y_carpeta():
    ruta_actual = os.getcwd()
    print(f"Los archivos se crearan en la carpeta actual. Ruta: {ruta_actual}")
    cerrar_menu = False
    while not cerrar_menu:
        print("""
        1. Crear un archivo.
        2. Crear una carpeta.
        3. Cerrar el menú.""")
        opcion = validar_opcion(1, 3)
        if opcion == 1:
            nombre_archivo = input("Ingrese el nombre para este archivo: ")
            extension = input("Ingrese la extensión del archivo: ")
            open(f"{nombre_archivo}.{extension}", "w")
            print(f"El archivo {nombre_archivo}.{extension} fue creado satisfactoriamente.")
        elif opcion == 2:
            nombre = input("Ingrese el nombre para esta carpeta: ")
            try:
                os.mkdir(nombre)
            except FileExistsError:
                print(f"Error, la carpeta {nombre} ya existe.")
            except:
                print("Ha ocurrido un error.")
            else:
                print(f"La carpeta {nombre} fue creada satisfactoriamente.")
        elif opcion == 3:
                cerrar_menu = True


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
            menu_listar_archivos()
        elif opcion == 2:
            menu_crear_archivo_y_carpeta()
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
main()