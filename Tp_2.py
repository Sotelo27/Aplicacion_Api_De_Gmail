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

def main ()->None:
    cerrar_menu = False
    while not cerrar_menu:
        print("""
        -**-
        Bienvenido al menú inicial
        -**-
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
        if opcion == 8:
            cerrar_menu = True
main()


