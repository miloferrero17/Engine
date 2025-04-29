import os
from twilio.rest import Client
from datetime import datetime
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth


# Load variables from .env file
load_dotenv()

# Configuración de Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Validación de configuración
if not account_sid or not auth_token or not twilio_whatsapp_number:
    raise ValueError(
        "Configura las variables de entorno TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN y TWILIO_WHATSAPP_NUMBER."
    )

# Inicialización del cliente Twilio
client = Client(account_sid, auth_token)

def send_whatsapp_message(body, to, media_url = None):
    """
    Envía un mensaje de WhatsApp utilizando Twilio.

    Parámetros:
        body (str): Contenido del mensaje.
        to (str): Número de WhatsApp del destinatario, en formato internacional (e.g., 'whatsapp:+123456789').

    Retorna:
        Message: Objeto de mensaje Twilio con los detalles del envío.

    Lanza:
        RuntimeError: Si ocurre algún error al enviar el mensaje.
    """
    try:
        message = client.messages.create(
            from_=f'whatsapp:{twilio_whatsapp_number}',
            body=body,
            to=to,
            media_url=media_url if media_url else None
        )
        return message
    except Exception as e:
        raise RuntimeError(f"Error al enviar el mensaje de WhatsApp: {e}")
   
send_whatsapp_message("Dale amargo", "whatsapp:+5491133585362", media_url = None)
