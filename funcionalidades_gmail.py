from servicio_gmail import obtener_servicio
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
servicio = obtener_servicio()

def crear_correo_con_adjunto(remitente,destinatario,asunto,texto_correo,adjunto)->object:
    correo = MIMEMultipart()
    correo ['destinatario'] = destinatario
    correo ['remitente'] = remitente
    correo['asunto'] = asunto
    mensaje = MIMEText(texto_correo)
    correo.attach(mensaje)
    for archivo in adjunto:
        content_type, encoding = mimetypes.guess_type(archivo)
        main_type, sub_type = content_type.split('/', 1)
        filename = os.path.basename(archivo)
        f = open(archivo, 'rb')
        myFile = MIMEBase(main_type,sub_type)
        myFile.set_payload(f.read())
        myFile.add_header('Content-Disposition','archivo',filename=filename)
        encoders.encode_base64(myFile)

        f.close()
        correo.attach(myFile)

    return {'raw': base64.urlsafe_b64encode(correo.as_string())}


def enviar_correo(servicio,email_usuario,mensaje):
    mensaje = servicio.users().messages().send(userdId=email_usuario,body={'raw':raw_string}).execute()

archivo = ('Archivos\cadena.txt')
raw_string = crear_correo_con_adjunto('lmsotelo@fi.uba.ar','sotelomartin343@gmail.com','tenes un mensaje','hola',archivo)
enviar_correo(servicio,'lmsotelo@fi.uba.ar',raw_string)



