'''
Usaremos estos módulos a lo largo del programa.
'''
import os
import pickle
import zipfile
import io
import csv
import base64
from base64 import urlsafe_b64decode
from email.mime.text import MIMEText
from apiclient import errors
from googleapiclient.discovery import Resource
from servicio_gmail import obtener_servicio

def crear_correo(remitente: str, destinatario: str, asunto: str, texto_mensaje: str) -> object:
    '''
    PRE: recibe al usuario que envia, como el destinatario, el asunto del mensaje,
    y el cuerpo a escribir.
    POST: crea un objeta que contiene los diferentes valores del correo.
    '''
    mensaje = MIMEText(texto_mensaje)
    mensaje['to'] = destinatario
    mensaje['from'] = remitente
    mensaje['subject'] = asunto
    raw_msg = base64.urlsafe_b64encode(mensaje.as_string().encode('utf-8'))
    return {'raw':raw_msg.decode('utf-8')}


def enviar_correo(servicio:Resource, usuario_id: str, mensaje: object) -> object:
    '''
    PRE: recibe la credenciales de gmail, como la id del usuario y el cuerpo del mensaje en objeto.
    POST: envia el mensaje con la informacion dada por el usuario, y lo retorna en objeto,
    para ser usado mas tarde.
    '''
    try:
        message = servicio.users().messages().send(userId=usuario_id, body=mensaje).execute()
        print ('Id del mensaje : {}'.format(message['id']))
    except Exception as error:
        print('Ha ocurrido un error: {}'.format(error))
    return message


def leer_archivo_alumnos(archivo: str, diccionario_datos: dict, opcion: int) -> None:
    '''
    Procedimiento que recibe el archivo de los alumnos y modifica un diccionario vacio
    a partir del mismo, sera usado para las validaciones. Dependiendo la opcion que reciba,
    la lectura y la creacion del diccionario variara.
    Dicha opcion es arbitraria decidia por el creador de la apliacion.
    '''
    if opcion == 1:
        valor_1 = 1
        valor_2 = 2
    else:
        valor_1 = 1
        valor_2 = 0
    with open(archivo, mode = 'r', newline='', encoding="UTF-8") as archivo_csv1:
        csv_reader = csv.reader(archivo_csv1, delimiter=',')
        for columna in csv_reader:
            diccionario_datos[columna[valor_1]] = columna[valor_2]
        #se le asigna a la determinada llave el valor,

def validaciones(
    email: str, asunto: str, nombre_archivo_adjunto: str,
    archivo_alumnos: str) -> bool:
    '''
    PRE: Recibe el email, el asunto, el nombre del archivo adjunto y el
    archivo del correspondiente mensaje.
    POST: A partir de las validaciones, se verifica si el correo cumple con las
    condiciones pedidas por los docentes.
    '''
    validar = True
    email_padron_asignado:dict = {}
    #Diccionario que sera utilizado para guardar padrones e emails
    numerico = asunto.isnumeric()
    #Comprobacion de que el asunto es un numero.
    leer_archivo_alumnos(archivo_alumnos,email_padron_asignado,1)
    #Se lee los archivos, y a su vez se modifica el diccionario
    if numerico is False:
        validar = False
    elif ".zip" not in nombre_archivo_adjunto:
    #Si no tiene la extension .zip el adjunto, su validacion sera falsa.
        validar = False
    elif asunto not in email_padron_asignado:
    #Aunque cumpla la condicion numerica, se verifica que se encuentra verificado dicho padron.
        validar = False
    elif email not in email_padron_asignado.values():
    #Si el email pertenece a la Facultad o es de un medio externo.
        validar = False
    elif email_padron_asignado[asunto] != email:
    #Si el email, como viceversa tambien funcionara, de que el padron e email son del mismo alumno.
        validar = False

    return validar


def eliminar_caracteres(cadena_str: str) -> str:
    '''
    Esta funcion tiene como objetivo obtener solo el correo del valor que
    se obtiene de From: y eliminar así, los archivos innecesarios
    PRE: Recibe una cadena str
    POST: La divide, elimina los caracteres y se crea un nuevo str que solo contendra el
    email del usuario que envio el mensaje.
    '''
    lista = cadena_str.split()
    #Se crea una lista
    email = lista.pop()
    #Se obtiene el ultimo caracter, que sera siempre el email
    caracteres_a_eliminar = "> <"
    #Se elimina los caracteres innecesarios predeterminados el email
    for letras in range(len(caracteres_a_eliminar)):
        email = email.replace(caracteres_a_eliminar[letras],"")
    #Se lo reemplaza por solo un espacio vacio
    return email


def definir_errores(correo: object, archivo_alumnos: str) -> bool:
    '''
    PRE: Recibe el correo y sus partes, como a su vez la dirrecion del archivo que
    contiene informacion de los alumnos.
    POST: Devuelve un booleano que a partir de la funcion validaciones,
    comprobara si hay un error en el mismo.
    '''
    validar_entrega = True
    payload = correo['payload']
    encabezados = payload.get("headers")
    # Se separa el correo en sus distintas partes para utilizarlo en las validaciones.
    partes = payload.get('parts')
    for part in partes:
        nombre_archivo = part["filename"]
        #Nombre del archivo para comprobar su extension.
    for valores in encabezados:
        nombre = valores.get("name")
        valor = valores.get("value")
        if nombre.lower() == "subject":
            asunto = valor
        if nombre.lower() == "from":
            destinatario = valor
    email = eliminar_caracteres(destinatario)
    validar_entrega = validaciones(email,asunto,nombre_archivo,archivo_alumnos)

    return validar_entrega


def recepcion_de_entregas(servicio: Resource, correo: object, archivo_alumnos: str) -> str:
    '''
    Procedimiento que tiene como objetivo verificar el correo y a partir de alli,
    construir el correo que se enviara a los alumnos confirmando o no su entrega.
    '''
    validar_entrega = definir_errores(correo,archivo_alumnos) #Validacion del correo
    asunto = "Entrega evaluacion"
    payload = correo["payload"]
    encabezados = payload.get("headers")
    for valores in encabezados:
        nombre = valores.get("name")
        valor = valores.get("value")
        if nombre.lower() == "from":
            destinatario = valor #utilizado para contestarle al alumno
        elif nombre.lower() =="subject":
            padron = valor
    if validar_entrega is True:
        texto_mensaje = "Entrega valida"
        correo = crear_correo("me",destinatario,asunto,texto_mensaje)
        enviar_correo(servicio,"me",correo)
    else:
        texto_mensaje = "Entrega invalida"
        correo = crear_correo("me",destinatario,asunto,texto_mensaje)
        enviar_correo(servicio,"me",correo)
        padron = "no es valido"
    return padron


def actualizar_entregas(servicio: Resource, carpeta_evaluacion: str) -> None:
    '''
    Procedimiento que recibe solamente el archivo de alumnos y el de docente con
    su alumno respectivo, y tiene como objetivo actualizar las entregas llegadas
    por los alumnos siempre y cuando, este mismo no se haya leido.
    '''
    print("Creando carpeta en ",os.getcwd())
    mensajes_email = buscar_email(servicio,"is:unread",["INBOX"])
    #Se chequea en la bandeja de entrada del usuario los mensajes no leidos
    if mensajes_email is None:
        print("No hay mensajes para actualizar")
    else:
        os.chdir(carpeta_evaluacion)
        archivo_alumnos = "alumnos.csv"
        archivo_docente_alumnos = 'docente-alumnos.csv'
        for email in mensajes_email:
            #Se itera sobre la misma para conseguir la id del mismo y acceder a cada mensaje
            id_mensaje = email["id"]
            correo = detalles_del_email(servicio,id_mensaje)
            #se consiguen los detalles del mismo
            padron = recepcion_de_entregas(servicio, correo, archivo_alumnos)
            #se verificara si es correcta o no la entrega del mismo
        if padron != "no es valido":
            anidar_archivos_alumno(servicio, padron, archivo_alumnos,
            archivo_docente_alumnos, id_mensaje)
    os.chdir("..")
    

def anidar_archivos_alumno(
    servicio: Resource, padron: str, archivo_alumnos: str,
    archivo_docente_alumno: str, id_mensaje: str) -> None:
    '''
    Procedimiento que tiene como objetivo acceder a las distintas carpetas del sistemas de
    carpetas, leyendo los archivos y los el padron dado para luego descomprimirlo en la
    carpeta correspondiente.
    '''
    nombre_padron: dict = {}
    # Diccionario que tiene como llave el padron y el valor su nombre
    alumno_profesor: dict = {}
    # Diccionario que tiene como llave el alumno y el valor el profesor
    leer_archivo_alumnos(archivo_alumnos,nombre_padron,2)
    nombre = nombre_padron[padron]
    leer_archivo_alumnos(archivo_docente_alumno,alumno_profesor,3)
    profesor = alumno_profesor[nombre]
    os.chdir(profesor)
    os.chdir(nombre)
    descargar_adjunto(servicio,"me",id_mensaje)


def buscar_email(servicio: Resource, cadena_string: str, etiquetas_id: str) -> object:
    '''
    PRE: Recibe las credenciales de gmail, una cadena string que sera un
    operador de busqueda, como la etiqueta tambien.
    POST: Devuelve un objeto que contiene las partes del mensaje, con los parametros
    indicados por el usuario para su busqueda.
    '''
    try:
        lista_mensaje = servicio.users().messages().list(userId = 'me',
        labelIds = etiquetas_id, q = cadena_string).execute()
        items_mensajes = lista_mensaje.get('messages')
        nextPageToken = lista_mensaje.get('nextPageToken')
        while nextPageToken:
            lista_mensaje = servicio.user().messages().list(userId = 'me',
            labelIds=etiquetas_id, q=cadena_string, pageToken=nextPageToken).execute()
            items_mensajes.extend(lista_mensaje.get('messages'))
            nextPageToken = items_mensajes.get('nextPageToken')
    except Exception as exc:
        items_mensajes = None
        print(exc)
    return items_mensajes


def detalles_del_email(
    servicio: Resource, id_mensaje: str,
    metadata_headers:list = []) -> object:
    '''
    PRE: Recibe las credenciales de gmail, la id unica del mensaje, como el formato
    de codoficacion y la metadata de los encabezados.
    POST: Se obtiene todo los datos del mensaje en un formato completo, y se los
    retorna en un objeto para su uso a posterior.
    '''
    try:
        detalles_mensaje = servicio.users().messages().get(userId = 'me',id = id_mensaje,
        format = "full", metadataHeaders = metadata_headers).execute()
    except Exception as exc:
        detalles_mensaje = None
        print(exc)
    return detalles_mensaje


def descargar_adjunto(
    servicio: Resource,usuario_id: str,
    mensaje_id: str, directorio: str = '') -> None:
    '''
    Procedimiento que recibe las credenciales de gmail, el usuario de la aplicacion, la id unica del
    mensaje y el directorio de descarga. Tiene como objetivo acceder al cuerpo del mensaje para asi
    descargar los archivos adjuntos que posea el mismo.
    '''
    try:
        mensaje = servicio.users().messages().get(userId = 'me', id = mensaje_id).execute()

        for partes in mensaje['payload']['parts']:
            newvar = partes['body']
        if 'attachmentId' in newvar:
            #Se comprueba si tiene un adjunto
            att_id = newvar['attachmentId']
            att = servicio.users().messages().attachments().get(userId = usuario_id,
            messageId = mensaje_id, id = att_id).execute()
            #Se utiliza el metodo de la api para obtener el adjunto
            data = att['data']
            informacion_archivo = base64.urlsafe_b64decode(data.encode('UTF-8'))
            #Se codifica dicha informacion a base64
            print("Cargando archivos...")
            print(partes['filename'])
            #Impresion en pantalla del nombre del archivo
            path = ''.join([directorio, partes['filename']])
            #Se crea el directorio junto al archivo dado
            base = os.path.basename(path)
            lista = os.path.splitext(base)
            archivo_bin = lista[0] + ".bin"
            #Se lo convierte a binario, asi guardarlo
            archivo = open(archivo_bin,"wb")
            pickle.dump(informacion_archivo,archivo)
            archivo.close
            descomprimir_archivo(informacion_archivo,partes)
            #se descomprime el archivo dado

    except errors.HttpError as error:
        print ('A ocurrido un error: {}'.format(error))


def descomprimir_archivo(archivo: bytes, nombre_archivo: str) -> None:
    '''
    Procedimiento que hace uso de la libreria zipfiles, para la descompresion de
    los archivos enviados al correo del usuario.
    '''
    if '.zip' not in nombre_archivo["filename"]:
        print("archivo erroneo")
    else:
        print("Descomprimiendo archivos...")
        archivo_a_descomprimir = zipfile.ZipFile(io.BytesIO(archivo))
        #Al estar la informacion en bytes, se utiliza la libreria io para su descompresion.
        archivo_a_descomprimir.extractall()
        print("Archivos descomprimidos")

def opciones_busqueda() -> None:
    '''
    Procedimiento que solo printea por pantalla al usuario los metodos
    de busca por filtros que tiene a disposicion.
    '''
    print('Opciones de consulta de mensaje:')
    print('\n .1 Si desea buscar por email remitente \n .2 Si desea buscar por email destinatario'
    '\n .3 Si desea buscar todos los correos que tienen un adjunto'
    '\n .4 Por nombre de archivo adjunto \n .5 Si desea buscar por asuntos'
    '\n .6 Leidos \n .7 No leidos')


def consultar_mensaje(servicio: Resource) -> None:
    '''
    Procedimiento que recibe las credenciales de gmail, como a su vez presenta al
    usuario los metodos que tendra para consultar algun mensaje especificado de
    la manera que el usuario decida.
    '''
    opciones_busqueda()
    seleccionar_via_consulta = int(input("Eliga a continuacion: " ))
    if seleccionar_via_consulta == 1:
        email_remitente = input(
            "Escriba a continuacion el email del usuario que desea consultar sus correos: ")
        cadena_string = "from:" + email_remitente
        #Al estar en formato str las partes del correo, simplemente se le suma
        # al email del determinado usuario
        print(cadena_string)
    elif seleccionar_via_consulta == 2:
        email_destinatario = input(
            "Escriba el email del usuario  por el cual desea consultar los correos: ")
        cadena_string = "to:"+ email_destinatario
    elif seleccionar_via_consulta == 3:
        cadena_string = "has:attachment"
        #Operador de busqueda que verifica si posee un adjunto
    elif seleccionar_via_consulta == 4:
        archivo = input(
            "Introduzca el nombre del archivo con su extension: ")
        cadena_string = "filename:" + archivo
    elif seleccionar_via_consulta ==5:
        asunto = input(
            "Introduzca el asunto del correo a buscar: ")
        cadena_string = "subject:" + asunto
        #Operador de busqueda que verifica segun el asunto del correo o similares
    elif seleccionar_via_consulta == 6:
        cadena_string = "is:read"
        #Operador de busqueda que verifica si estan leidos los correos
    elif seleccionar_via_consulta == 7:
        cadena_string = "is:unread"
        #Operador de busqueda que verifica si no estan leidos los correos.
    mensajes_email = buscar_email(servicio,cadena_string,['INBOX'])
    #Con el operador selecionado por el usuario se buscara todos los correos asociados.
    if mensajes_email is None:
        print("---"*5)
        print("\n #No hay mensajes del operador que busca, intentelo denuevo\n")
        seguir = input("Si desea buscar con otro operador presione 1,caso contrario 2:" )
        if seguir == "1":
            consultar_mensaje(servicio)
        print("---"*5)

    else:
        for mensajes in mensajes_email:
            #Se itera sobre el para conseguir las id de cada uno
            mensaje_id = mensajes['id']
            email = detalles_del_email(servicio,mensaje_id)
            #Se consiguen los detalles del cada mensaje
            leer_correos(servicio,email)
            #Se los leera


def dividir_cuerpo_mensaje(servicio: Resource, partes: object) -> None:
    '''
    Procedimiento que tiene como objetivo mostrar en pantalla la informacion
    del cuerpo del mensaje, si es un adjunto, si a su vez posee un adjunto entre otros.
    Recibe las partes del mismo y las credenciales de gmail para su
    decodificacion y su lectura legible.
    '''
    if partes:
        for valores in partes:
            #Se itera sobre el objeto
            archivo = valores.get("filename")
            #Se obtiene el nombre del archivo en caso de tener
            mimeType = valores.get("mimeType")
            #Se utilizara para ver el tipo de dato
            cuerpo = valores.get("body")
            #Se obtiene el cuerpo general del archivo
            informacion = cuerpo.get("data")
            #Informacion codificada del mensaje
            if valores.get("parts"):
                dividir_cuerpo_mensaje(servicio, valores.get("parts"))
            if mimeType == "text/plain": #Si es de un tipo texto
                if informacion:
                    texto_mensaje = urlsafe_b64decode(informacion).decode()
                    #Se lo decodifica para su lectura
                    print(texto_mensaje)
            elif mimeType == "text/html":
                #Si es de un tipo html
                if not archivo:
                    arc = "index.html"
                    print("Adjunto: ",arc)
            else:
                print("Adjunto: ",archivo)


def leer_correos(servicio: Resource, mensajes_email: object) -> None:
    '''
    Procedimiento que recibe los mensajes del email y se los printea en pantalla
    de una manera estetica, subdividiendo las partes del determinado objeto en nombres y valores.
    '''
    payload = mensajes_email['payload']
    encabezados = payload.get("headers")
    partes = payload.get('parts')
    for valores in encabezados:
        #Se itera sobre los valores dentro del objeto para conseguir sus distintas partes
        nombre = valores.get("name")
        valor = valores.get("value")
        if nombre.lower() == 'from':
            #Remitente
            print("De:", valor)
        elif nombre.lower() == "to":
            #Se obtiene el destinatario
            print("Para:", valor)
        elif nombre.lower() == "subject":
            #Se obtiene el asunto
            print("Asunto:", valor)
        elif nombre.lower() == "date":
            #Fecha
            print("Fecha:", valor)
    print("\n")
    dividir_cuerpo_mensaje(servicio, partes)
    print("\n")
    print("="*50)


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


def generar_carpetas_de_una_evaluacion(servicio: Resource) -> None:
    '''
    Procedimiento que tiene como objetivo crear las carpetas anidadaes
    en los 3 niveles especificados, con la informacion brindada por un
    correo especificado por el usuario. Dicho correo debe seguir ciertas
    condiciones, caso contrario, no creara dicha carpeta.
    '''
    correo_con_evaluacion = input(
        "Ingrese a continuacion el correo que a enviado los datos de la evaluacion: ")
    #Se busca el correo que posee la informacion para crear las carpetas.
    operador_de_busqueda_remitente = "from:" + correo_con_evaluacion
    #Los operadores que se deben cumplir, el correo ingresado por el usuario
    operador_de_busqueda_no_leidos = "is:unread"
    #Que no se haya leido ya
    operador_de_busqueda_adjunto = "has:attachment"
    #Y que posea un adjunto
    operador_de_busqueda = operador_de_busqueda_remitente + " " +\
        operador_de_busqueda_no_leidos + " " + operador_de_busqueda_adjunto
    #se los une para una condicion general
    mensaje = buscar_email(servicio,operador_de_busqueda,["INBOX"] )
    #se busca dicho mail con ciertas condiciones en la bandeja.
    if mensaje is None:
        print("No hay nuevos correos de dicho correo")
        seguir = input("Si desea reingresar un correo presione 1, caso contrario 2")
        if seguir == "1":
            generar_carpetas_de_una_evaluacion(servicio)
    else:
        for email_mensaje in mensaje:
            #Se itera sobre el para conseguir las id de cada uno
            id_mensaje = email_mensaje['id']
            email = detalles_del_email(servicio,id_mensaje)
        payload = email['payload']
        encabezados = payload.get("headers")
        for valores in encabezados:
            nombre = valores.get("name")
            valor = valores.get("value")
            if nombre.lower() == 'subject':
                #se obtiene el asunto para poder crear la carpeta
                asunto = valor
        generar_carpeta_con_asunto(servicio,asunto,id_mensaje)
        #finalmente se genera la carpeta


def generar_carpeta_con_asunto(servicio: Resource, asunto: str, id_mensaje: str) -> None:
    '''
    Procedimiento que crea la carpeta de 3 niveles con el asunto dado y los archivos
    descomprimidos, con dichos nombres de los archivos y la informacion que contienen los mismos.
    '''
    os.mkdir(asunto)
    os.chdir(asunto)
    ruta = os.getcwd()
    descargar_adjunto(servicio,"me",id_mensaje)
    #se descarga el adjunto y se crea un bin del .zip
    with open(ruta + "\\docentes.csv", mode = 'r', newline='', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter=',')
        for columna in csv_reader:
            nombre_profesores = columna[0]
            os.mkdir(nombre_profesores)
    with open(ruta + "\\docente-alumnos.csv", mode = 'r',
    newline = '', encoding="UTF-8") as archivo2_csv:
        csv_reader2 = csv.reader(archivo2_csv, delimiter=',')
        for columna in csv_reader2:
            nombre_alumnos = columna[1]
            nombre_profesores = columna[0]
            try:
                os.chdir(nombre_profesores)
            except FileNotFoundError:
                os.mkdir("Alumnos sin asignar profesor")
                os.chdir("Alumnos sin asignar profesor")
                os.mkdir(nombre_alumnos)
                os.chdir("..")
            else:
                os.mkdir(nombre_alumnos)
                os.chdir("..")
    os.chdir("..")
    

def menu_listar_archivos() -> None:
    '''
    Procedimiento que permite al usuario navegar por las carpetas y listar subcarpetas/archivos.
    '''
    print(f"La ruta actual es {os.getcwd()}")
    cerrar_menu = False
    while not cerrar_menu:
        print("""
        ¿Qué desea hacer?
        1. Mostrar los archivos locales.
        2. Abrir una carpeta existente.
        3. Volver una carpeta atrás.
        4. Cerrar el menú.
        """)
        ruta_actual = os.getcwd()
        opcion = validar_opcion(1, 4)
        if opcion == 1:
            listar_archivos_local()
        elif opcion == 2:
            nombre = input("Ingrese el nombre de la carpeta a abrir: ")
            try:
                os.chdir(nombre)
            except FileNotFoundError:
                print("Error, esa carpeta no existe o no es subcarpeta de la actual.")
            else:
                ruta_actual = os.path.join(ruta_actual, nombre)
                print("Carpeta abierta exitosamente.")
                print(f"La ruta actual es {ruta_actual}")
        elif opcion == 3:
            os.chdir("..")
            ruta_actual = os.getcwd()
            print(f"La ruta actual es {ruta_actual}")
        elif opcion == 4:
            cerrar_menu = True


def listar_archivos_local() -> None:
    '''
    Procedimiento que muestra los archivos y subcarpetas en el directorio actual.
    '''
    contador = 1
    print("Listado de archivos de la carpeta actual (y subcarpetas): ")
    directorio = os.getcwd()
    for ruta, _, archivos in os.walk(directorio):
        subnivel = ruta.replace(directorio, '').count(os.sep)
        separacion_carpetas = ' ' * 8 * (subnivel)
        print(f"{separacion_carpetas}{contador} » {os.path.basename(ruta)}/")
        separacion_archivos = ' ' * 8 * (subnivel + 1)
        for nombre_archivos in archivos:
            print(f"{separacion_archivos}{nombre_archivos}")
        contador += 1


def menu_crear_archivo_y_carpeta() -> None:
    '''
    Procedimiento que permite al usuario crear subcarpetas/archivos en determinado directorio.
    '''
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
            with open(f"{nombre_archivo}.{extension}", "w"):
                print(f"El archivo {nombre_archivo}.{extension} fue creado satisfactoriamente.")
        elif opcion == 2:
            nombre = input("Ingrese el nombre para esta carpeta: ")
            try:
                os.mkdir(nombre)
            except FileExistsError:
                print(f"Error, la carpeta {nombre} ya existe.")
            else:
                print(f"La carpeta {nombre} fue creada satisfactoriamente.")
        elif opcion == 3:
            cerrar_menu = True


def validar_ruta(ruta: str, carpeta: str) -> bool:
    '''
    PRE: recibe la ruta de inicio, junto a la carpeta que se busca.
    POST: se verifica si dicha ruta existe y se lo informa al usuario,
    devuelve un bool para continuar el programa.
    '''
    ruta_nueva = ruta + "\\" + carpeta
    validacion = False
    
    if len(carpeta) == 0:
        print('La carpeta no existe.')
        validacion = False
    elif os.path.isdir(ruta_nueva):
        print('La carpeta existe')
        validacion = True
    else:
        print('La carpeta no existe.')
        validacion = False
    if validacion == False:
        continuar = input("Si desea reingresar presione 1, caso contrario 2: ")
        if continuar == "1":
            validacion = False
        else:
            print("\nVolviendo al menu principal...\n")
            validacion = None
    return validacion


def main () -> None:
    '''
    Ahi estara el menu general del programa, teniendo acceso a sus distintas funcionalidades
    como accesos.
    '''
    servicio = obtener_servicio()
    cerrar_menu = False
    while not cerrar_menu:
        validacion_ruta = False
        ruta = os.getcwd()
        print("""
        -***************************-
        Bienvenido al menú inicial
        -***************************-
        Por favor, elija una opción.
        1. Listar archivos de la carpeta actual.
        2. Crear un archivo.
        3. Consultar correos.
        4. Generar carpetas de una evaluación.
        5. Actualizar entregas de alumnos vía mail
        6. Salir
        """)
        # Hipotesis, al no usar la aplicacion drive decidimos por cambiar una
        # de las opciones a una opcion (concretamente la .3).
        # Esta opción permite visualizar dependiendo el operador de busqueda
        # indicado por el usuario, correos asociados.
        opcion = validar_opcion(1, 6)
        if opcion == 1:
            menu_listar_archivos()
        elif opcion == 2:
            menu_crear_archivo_y_carpeta()
        elif opcion == 3:
            consultar_mensaje(servicio)
        elif opcion == 4:
            generar_carpetas_de_una_evaluacion(servicio)
        elif opcion == 5:
            carpeta_evaluacion = ''
            while not (validacion_ruta == True) :
                carpeta_evaluacion = input("Ingrese el nombre de la carpeta de la evaluacion: ")
                validacion_ruta = validar_ruta(ruta,carpeta_evaluacion)
            if validacion_ruta is True:
                actualizar_entregas(servicio,carpeta_evaluacion)
        elif opcion == 6:
            cerrar_menu = True

main()
