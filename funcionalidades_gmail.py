from servicio_gmail import obtener_servicio
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors
import pickle,os
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
        message = servicio.users().messages().send(userId=usuario_id, body=mensaje).execute()
        print ('Message Id: {}'.format(message['id']))
        return message
    except Exception as error:
        print('An error occurred: {}'.format(error))
        return None

def definir_errores():
    pass

def buscar_email_con_adjunto(servicio,cadena_string,etiquetas_id):
    try:
        lista_mensaje= servicio.users().messages().list(userId='me',labelIds=etiquetas_id,q=cadena_string).execute()
        items_mensajes = lista_mensaje.get('messages')
        nextPageToken = lista_mensaje.get('nextPageToken')
        while nextPageToken:
            lista_mensaje = servicio.user().messages().list(userId = 'me',labelIds=etiquetas_id,q=cadena_string,pageToken=nextPageToken).execute()
            items_mensajes.extend(lista_mensaje.get('messages'))
            nextPageToken = items_mensajes.get('nextPageToken')
        return items_mensajes
    except Exception as e:
        return None
def detalles_del_email(servicio,id_mensaje,format='metadata',metadata_headers=[]):
    try:
        detalles_mensaje = servicio.users().messages().get(userId='me',id=id_mensaje,format=format,metadataHeaders=metadata_headers).execute()
        return detalles_mensaje
    except Exception as e:
        print(e)
        return None
def descargar_adjunto(service,user_id,msg_id,store_dir=''):
    try:
        message = service.users().messages().get(userId='me', id=msg_id).execute()

        for part in message['payload']['parts']:
            newvar = part['body']
        if 'attachmentId' in newvar:
            att_id = newvar['attachmentId']
            att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id, id=att_id).execute()
            data = att['data']
            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
            print(part['filename'])
            path = ''.join([store_dir, part['filename']])
            f = open(path, 'wb')
            f.write(file_data)
            f.close()
    except errors.HttpError as error:
        print ('An error occurred: {%s}'.format(error))

def crear_filtro(servicio,usuario_id,cuerpo):
    filtro = servicio.users().settings().filters().create(userId = usuario_id,body = cuerpo).execute()
    print('Filtro creado {}'.format(filtro.get('id')))
    return filtro

def obtener_hilos_de_consulta(servicio,usuario_id,etiqueta_id,consulta):
    respuesta = servicio.users().threads().list(userId = usuario_id,labelIds = etiqueta_id,q = consulta).execute()
    threads = []
    if 'threads' in respuesta:
        threads.extend(respuesta['threads'])

    while 'nextPageToken' in respuesta:
        pageToken = respuesta['nextPageToken']
        respuesta = servicio.users().threads().list(userId = usuario_id,labelIds = etiqueta_id,q = consulta,pageToken = pageToken).execute()
        threads.extend(respuesta['threads'])

    return threads

def crear_busqueda_consulta(criterio_busqueda):
    lista_de_consulta = []
    llaves_mensaje = ["from","to","subject"]
    for llaves in llaves_mensaje:
        valores = criterio_busqueda.get(llaves)
        if valores is not None:
            lista_de_consulta.append("("+llaves+":"+valores+")")
    valores = criterio_busqueda.get("query")
    if valores is not None:
        lista_de_consulta.append("("+valores+")")

    return " AND ".join(lista_de_consulta)
def aplicar_filtro_a_busqueda(servicio,usuarioId,filtro_objeto):
    consulta = crear_busqueda_consulta(filtro_objeto["criteria"])
    hilos = obtener_hilos_de_consulta(servicio,usuarioId,[],consulta)
    aniadir_etiquetas = filtro_objeto["action"]["addLabelIds"]
    print("Etiquetas aniadidas {} a {} hilos".format(aniadir_etiquetas,len(hilos)))
    for contenido in hilos:
        cuerpo = {"addLabelIds":aniadir_etiquetas,"removeLabelIds":[]}
        servicio.users().threads().modify(userId=usuarioId,id=contenido["id"],body=cuerpo).execute()
        
def busqueda_filtros(servicio):
    consulta = input('Introduzca un filtro de busqueda: ')
    filtro_deseado = [{"criteria": {"subject": "[JIRA]",},"action": {"addLabelIds": [me["jira"]],}},]
    for contenido in filtro_deseado:
        crear_filtro(servicio,"me",contenido)
        aplicar_filtro_a_busqueda(servicio,"me",contenido)

def main():
    remitente ='lmsotelo@fi.uba.ar'
    destinatario = ''
    texto_mensaje = 'Su entrega ha sido correcta'
    texto_mensaje_error = 'Su entrega no a sido enviada correctamente'
    asunto = 'Entrega evaluacion'
    correo = crear_correo(remitente,destinatario,asunto,texto_mensaje)
    directorio = input('Ingrese el directorio en el que desee descargar el archivo')

