from servicio_gmail import obtener_servicio
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors
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
        

