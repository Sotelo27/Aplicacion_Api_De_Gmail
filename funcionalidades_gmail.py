from servicio_gmail import obtener_servicio
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors
from base64 import urlsafe_b64decode
import pickle
import io
import zipfile
servicio = obtener_servicio()
def crear_correo(remitente:str, destinatario:str, asunto:str, texto_mensaje:str)->object:
    mensaje = MIMEText(texto_mensaje)
    mensaje['to'] = destinatario
    mensaje['from'] = remitente
    mensaje['subject'] = asunto
    raw_msg = base64.urlsafe_b64encode(mensaje.as_string().encode('utf-8'))
    return {'raw':raw_msg.decode('utf-8')}

def enviar_correo(servicio:object, usuario_id:str, mensaje:object):
    try:
        message = servicio.users().messages().send(userId = usuario_id, body = mensaje).execute()
        print ('Message Id: {}'.format(message['id']))
        return message
    except Exception as error:
        print('An error occurred: {}'.format(error))
        return None

def definir_errores():
    pass

def buscar_email(servicio,cadena_string,etiquetas_id):
    try:
        lista_mensaje = servicio.users().messages().list(userId = 'me',labelIds = etiquetas_id,q = cadena_string).execute()
        items_mensajes = lista_mensaje.get('messages')
        nextPageToken = lista_mensaje.get('nextPageToken')
        while nextPageToken:
            lista_mensaje = servicio.user().messages().list(userId = 'me',labelIds = etiquetas_id,q = cadena_string,pageToken = nextPageToken).execute()
            items_mensajes.extend(lista_mensaje.get('messages'))
            nextPageToken = items_mensajes.get('nextPageToken')
        return items_mensajes
    except Exception as e:
        return None
def detalles_del_email(servicio,id_mensaje,format = 'metadata',metadata_headers = []):
    try:
        detalles_mensaje = servicio.users().messages().get(userId = 'me',id = id_mensaje,format = "full",metadataHeaders = metadata_headers).execute()
        return detalles_mensaje
    except Exception as e:
        print(e)
        return None
def descargar_adjunto(service,user_id,msg_id,store_dir = ''):
    try:
        message = service.users().messages().get(userId = 'me', id = msg_id).execute()

        for part in message['payload']['parts']:
            newvar = part['body']
        if 'attachmentId' in newvar:
            att_id = newvar['attachmentId']
            att = service.users().messages().attachments().get(userId = user_id, messageId = msg_id, id = att_id).execute()
            data = att['data']
            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
            print("Cargando archivos...")
            print(part['filename'])
            path = ''.join([store_dir, part['filename']])   
            archivo = open(path+".bin","wb")
            pickle.dump(file_data,archivo)
            archivo.close
            convertir_a_binario(file_data,part)
            
    except errors.HttpError as error:
        print ('An error occurred: {%s}'.format(error))

def convertir_a_binario(archivo,nombre_archivo):
    if '.zip' not in nombre_archivo["filename"]:
        print("archivo erroneo")
    else:    
        z = zipfile.ZipFile(io.BytesIO(archivo))
        z.extractall()

def opciones_busqueda():
    print('Opciones de consulta de mensaje:')
    print('\n .1 Si desea buscar por email remitente \n .2 Si desea buscar por email destinatario'
    '\n .3 Si desea buscar todos los correos que tienen un adjunto'
    '\n .4 Por nombre de archivo adjunto \n .5 Si desea buscar por asuntos \n .6 Leidos \n .7 No leidos')

def consultar_mensaje(servicio):
    opciones_busqueda()
    seleccionar_via_consulta = int(input("Eliga a continuacion: " ))
    if seleccionar_via_consulta == 1:
        email_remitente = input("Escriba a continuacion el email del usuario que desea consultar sus correos: ")
        cadena_string = "from:" + email_remitente
        print(cadena_string)
    elif seleccionar_via_consulta == 2:
        email_destinatario = input("Escriba el email del usuario  por el cual desea consultar los correos: ")
        cadena_string = "to:"+ email_destinatario
    elif seleccionar_via_consulta == 3:
        cadena_string = "has:attachment"
    elif seleccionar_via_consulta == 4:
        archivo = input("Introduzca el nombre del archivo con su extension: ")
        cadena_string = "filename:" + archivo
    elif seleccionar_via_consulta ==5:
        asunto = input("Introduzca el asunto del correo a buscar: ")
        cadena_string = "subject:" + asunto
    elif seleccionar_via_consulta == 6:
        cadena_string = "is:read"
    elif seleccionar_via_consulta == 7:
        cadena_string = "is:unread"
    mensajes_email = buscar_email(servicio,cadena_string,['INBOX'])
    for email_message in mensajes_email:
        messageId = email_message['id']
        email = detalles_del_email(servicio,messageId,)
        leer_correos(email)

def dividir_cuerpo_mensaje(servicio, partes):
    if partes:
        for valores in partes:
            archivo = valores.get("filename")
            mimeType = valores.get("mimeType")
            cuerpo = valores.get("body")
            informacion = cuerpo.get("data")
            if valores.get("parts"):
                dividir_cuerpo_mensaje(servicio, valores.get("parts"))
            if mimeType == "text/plain":
                if informacion:
                    texto_mensaje = urlsafe_b64decode(informacion).decode()
                    print(texto_mensaje)
            elif mimeType == "text/html":
                if not archivo:
                    arc = "index.html"
                    print("Adjunto: ",arc)
            else:
                print("Adjunto: ",archivo)
                
def leer_correos(mensajes_email):
    payload = mensajes_email['payload']
    encabezados = payload.get("headers")
    partes = payload.get('parts')
    for valores in encabezados:
        nombre = valores.get("name")
        valor = valores.get("value")
        if nombre.lower() == 'from':
            print("De:", valor)
        elif nombre.lower() == "to":
            print("Para:", valor)
        elif nombre.lower() == "subject":
            print("Asunto:", valor)
        elif nombre.lower() == "date":
            print("Fecha:", valor)
        elif nombre.lower() == "":
            print("Cuerpo del mensaje:",valor)
    print("\n")
    dividir_cuerpo_mensaje(servicio, partes)
    print("\n")
    print("="*50)

def main():
    remitente ='lmsotelo@fi.uba.ar'
    destinatario = ''
    texto_mensaje = 'Su entrega ha sido correcta'
    texto_mensaje_error = 'Su entrega no a sido enviada correctamente'
    asunto = 'Entrega evaluacion'
    correo = crear_correo(remitente,destinatario,asunto,texto_mensaje)
    directorio = input('Ingrese el directorio en el que desee descargar el archivo')
