from servicio_gmail import obtener_servicio
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
servicio = obtener_servicio()

def crear_correo_con_adjunto(remitente,destinatario,asunto,texto_correo,archivo)->object:
    correo = MIMEMultipart()
    correo ['destinatario'] = destinatario
    correo ['remitente'] = remitente
    correo['asunto'] = asunto
    mensaje = MIMEText(texto_correo)
    correo.attach(mensaje)
    content_type, encoding = mimetypes.guess_type(archivo)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(archivo, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(archivo, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(archivo)
    msg.add_header('Content-Disposition', 'attachment', filename = filename)
    correo.attach(mensaje)

    return {'raw': base64.urlsafe_b64encode(correo.as_string())}


def enviar_correo(servicio,email_usuario,mensaje):
    mensaje = servicio.users().messages().send(userdId=email_usuario,body={'raw':raw_string}).execute()

archivo = ('Archivos\cadena.txt')

raw_string = crear_correo_con_adjunto('sotelomartin343@gmail.com','lmsotelo@gmail.fi.uba.ar','tenes un mensaje','hola',archivo)
enviar_correo(servicio,'lmsotelo@fi.uba.ar',raw_string)


