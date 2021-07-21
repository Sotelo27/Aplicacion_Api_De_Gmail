from servicio_gmail import obtener_servicio
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
import mimetypes
servicio = obtener_servicio()

def crear_mensaje_con_adjunto(sender, to, subject, message_text, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    (content_type, encoding) = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    (main_type, sub_type) = content_type.split('/', 1)
    if main_type == 'text':
        with open (file, 'rb') as f:
            msg = MIMEText(f.read().decode('utf-8'),_subtype = sub_type)
    elif main_type == 'image':
        with open (file, 'rb') as f:
            msg = MIMEImage(f.read(), _subtype=sub_type)
        
    elif main_type == 'audio':
        with open (file, 'rb') as f:
            msg = MIMEAudio(f.read(), _subtype=sub_type)
    else:
        with open (file,'rb') as f:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(f.read())
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    raw_msg = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
    return {'raw':raw_msg.decode('utf-8')}

def enviar_correo(service, usuario_id, message):
    try:
        message = service.users().messages().send(userId=usuario_id, body=message).execute()
        print ('Message Id: {}'.format(message['id']))
        return message
    except Exception as error:
        print('An error occurred: {}'.format(error))
        return None



