# Módulos Built-in
import flask
import os
import requests
import time
from dotenv import load_dotenv

# Módulos de terceros
from requests.auth import HTTPBasicAuth
from twilio.twiml.messaging_response import MessagingResponse
import app.services.twilio_service as twilio
import app.services.wisper as wisper
import app.services.vision as vision
import openai

# Módulos propios
from app.Model.users import Users
import app.message_p as engine

routes = flask.Blueprint("routes", __name__)

# Cargar variables de entorno
load_dotenv()
TMP_DIR = "/tmp"

@routes.route("/", methods=["GET", "POST"])
def whatsapp_reply():
    if flask.request.method == 'GET':
        return "✅ Server is running and accessible via GET request."

    sender_number = flask.request.form.get('From')
    message_body = flask.request.form.get("Body", "").strip()
    num_media = int(flask.request.form.get("NumMedia", 0))
    media_url = flask.request.form.get("MediaUrl0")
    media_type = flask.request.form.get("MediaContentType0")
    tiene_adjunto = 0
    description = ""
    transcription = ""
    pdf_text = ""

    if num_media > 0:
        # Crear carpeta temporal para el archivo recibido
        clean_sender = sender_number.replace(":", "_").replace("+", "")
        folder = os.path.join(TMP_DIR, f"{clean_sender}_media")
        os.makedirs(folder, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        extension = media_type.split("/")[-1]
        nombre_del_archivo = f"{clean_sender}_{timestamp}.{extension}"
        file_path = os.path.join(folder, nombre_del_archivo)

        try:
            reply_path = download_file(media_url, file_path)

            if media_type.startswith("audio"):
                print("🎙️ Es audio")
                twilio.send_whatsapp_message("Te estoy escuchando ...", sender_number)
                transcription = wisper.transcribir_audio_cloud(reply_path)
                print(f"📝 Transcripción: {transcription}")
                message_body = transcription
                tiene_adjunto = 1

            elif media_type.startswith("image"):
                print("🖼️ Es imagen")
                twilio.send_whatsapp_message("Dejame ver tu foto ...", sender_number)
                description = vision.describe_image(reply_path)
                print(f"🧠 Descripción generada: {description}")
                message_body = message_body + "\n📷 " + description
                tiene_adjunto = 1

            elif media_type == "application/pdf":
                print("📄 Es PDF")
                twilio.send_whatsapp_message("Dejame ver tu archivo ...", sender_number)
                pdf_text = vision.extract_text_from_pdf(reply_path)
                print(f"📄 Texto extraído del PDF:\n{pdf_text[:300]}...")  # Log parcial
                #twilio.send_whatsapp_message("Dejame ver ... ", sender_number)
                message_body = message_body + "\n📄 " + pdf_text
                tiene_adjunto = 1
            else:
                print("⚠️ Tipo de archivo no soportado:", media_type)
                twilio.send_whatsapp_message("⚠️ Tipo de archivo no soportado. Enviá audio, imagen o PDF.", sender_number)

        except Exception as e:
            print("❌ Error procesando media:", str(e))
            twilio.send_whatsapp_message("❌ Hubo un problema procesando el archivo. Intentalo de nuevo.", sender_number)
            return str(MessagingResponse())  # Twilio necesita respuesta válida

    # En todos los casos (texto, transcripción, imagen, PDF)
    try:
        engine.handle_incoming_message(message_body, sender_number, tiene_adjunto)
    except Exception as e:
        print(f"❌ Error en engine: {e}")
        twilio.send_whatsapp_message("❌ Ocurrió un error interno al procesar tu mensaje.", sender_number)

    # Siempre devolver algo válido para Twilio
    return str(MessagingResponse())


def download_file(media_url: str, file_path: str) -> str:
    """
    Descarga un archivo multimedia desde Twilio con autenticación.
    """
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")

        if not account_sid or not auth_token:
            raise ValueError("TWILIO_ACCOUNT_SID o TWILIO_AUTH_TOKEN no están definidos")

        response = requests.get(media_url, auth=HTTPBasicAuth(account_sid, auth_token), timeout=10)
        response.raise_for_status()

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"✅ Archivo descargado en: {file_path}")
        return file_path

    except Exception as e:
        print(f"❌ Error al descargar archivo desde {media_url}: {e}")
        raise


'''
# Modulos Build-in
import flask
import os
import requests
import time
from dotenv import load_dotenv

# Modulos de 3eros
from requests.auth import HTTPBasicAuth
import app.services.twilio_service as twilio
import app.services.wisper as wisper
import app.services.vision as vision
import openai

# Modulos propios
from app.Model.users import Users
import app.message_p as engine

routes = flask.Blueprint("routes", __name__)


# Cargar variables de entorno
load_dotenv()
TMP_DIR = "/tmp"
# Blueprint de Flask
#routes = flask.Blueprint("routes", __name__)
@routes.route("/", methods=["GET", "POST"])

def whatsapp_reply():
    if flask.request.method == 'GET':
        return "✅ Server is running and accessible via GET request."

    #print("Versión de openai:", openai.__version__)
    sender_number = flask.request.form.get('From')
    message_body = flask.request.form.get("Body", "").strip()
    num_media = int(flask.request.form.get("NumMedia", 0))
    #print(num_media)
    media_url = flask.request.form.get("MediaUrl0")
    #print(media_url)
    media_type = flask.request.form.get("MediaContentType0")
    #print(media_type)
    
    description = ""
    transcription = ""
    pdf_text = ""

    if num_media > 0:
        # Sanitizamos número y armamos ruta
        clean_sender = sender_number.replace(":", "_").replace("+", "")
        folder = os.path.join(TMP_DIR, f"{clean_sender}_media")
        os.makedirs(folder, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        extension = media_type.split("/")[-1]
        nombre_del_archivo = f"{clean_sender}_{timestamp}.{extension}"
        file_path = os.path.join(folder, nombre_del_archivo)

        #print(f"📁 Ruta del archivo: {file_path}")

        if media_type.startswith("audio"):
            print("🎙️ Es audio")

            try:
                reply_path = download_file(media_url, file_path)
                transcription = wisper.transcribir_audio_cloud(reply_path)
                print(f"📝 Transcripción: {transcription}")

                #twilio.send_whatsapp_message(transcription, sender_number, media_url=None)

            except Exception as e:
                print("❌ Error procesando audio:", str(e))
                return "Error en transcripción", 500

        elif media_type.startswith("image"):
            print("🖼️ Es imagen")

            try:
                reply_path = download_file(media_url, file_path)
                description = vision.describe_image(reply_path)
                #twilio.send_whatsapp_message(description, sender_number, media_url=None)

            except Exception as e:
                print("❌ Error procesando imagen:", str(e))
                return "Error en descripción de imagen", 500

        elif media_type == "application/pdf":
            print("📄 Es PDF")

            try:
                reply_path = download_file(media_url, file_path)
                pdf_text = vision.extract_text_from_pdf(reply_path)
                #twilio.send_whatsapp_message(pdf_text, sender_number, media_url=None)

            except Exception as e:
                print("❌ Error procesando PDF:", str(e))
                return "Error en lectura de PDF", 500

        else:
            print("⚠️ Tipo de archivo no soportado:", media_type)
            #twilio.send_whatsapp_message( "⚠️ Tipo de archivo no soportado. Envía un mensaje de voz, imagen o PDF.", sender_number)
        
        response = MessagingResponse()

        if transcription:
            message_body = transcription
        elif description:
            message_body = message_body + "\n📷 " + description
        elif pdf_text:
            message_body = message_body + "\n📄 " + pdf_text

    print(message_body)
    return engine.handle_incoming_message(message_body, sender_number, "Ruta del archivo adjunto")
        

def download_file(media_url: str, file_path: str) -> str:
    """
    Descarga un archivo multimedia desde Twilio con autenticación.
    """
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")

        if not account_sid or not auth_token:
            raise ValueError("TWILIO_ACCOUNT_SID o TWILIO_AUTH_TOKEN no están definidos")

        response = requests.get(media_url, auth=HTTPBasicAuth(account_sid, auth_token), timeout=10)
        response.raise_for_status()

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"✅ Archivo descargado en: {file_path}")
        return file_path

    except Exception as e:
        print(f"❌ Error al descargar archivo desde {media_url}: {e}")
        raise



# Modulos Build-in
import flask
import os
import requests
import time
from dotenv import load_dotenv

# Modulos de 3eros
from requests.auth import HTTPBasicAuth
from twilio.twiml.messaging_response import MessagingResponse

# Modulos propios
import app.services.twilio_service as twilio
import app.services.wisper as wisper
import app.services.vision as vision
from app.Model.users import Users
from requests.auth import HTTPBasicAuth

routes = flask.Blueprint("routes", __name__)


# Cargar variables de entorno
load_dotenv()
TMP_DIR = "/tmp"
# Blueprint de Flask
#routes = flask.Blueprint("routes", __name__)
@routes.route("/", methods=["GET", "POST"])

def whatsapp_reply():
    if flask.request.method == 'GET':
        return "✅ Server is running and accessible via GET request."

    sender_number = flask.request.form.get('From')
    message_body = flask.request.form.get("Body", "").strip()
    num_media = int(flask.request.form.get("NumMedia", 0))

    description = ""
    transcription = ""
    pdf_text = ""

    if num_media > 0:
        media_url = flask.request.form.get("MediaUrl0")
        media_type = flask.request.form.get("MediaContentType0")

        print(f"📩 Media URL: {media_url}")
        print(f"📦 Media Type: {media_type}")

        # Sanitizamos número y armamos ruta
        clean_sender = sender_number.replace(":", "_").replace("+", "")
        folder = os.path.join(TMP_DIR, f"{clean_sender}_media")
        os.makedirs(folder, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        extension = media_type.split("/")[-1]
        nombre_del_archivo = f"{clean_sender}_{timestamp}.{extension}"
        file_path = os.path.join(folder, nombre_del_archivo)

        print(f"📁 Ruta del archivo: {file_path}")

        if media_type.startswith("audio"):
            print("🎙️ Es audio")

            try:
                reply_path = download_file(media_url, file_path)
                transcription = wisper.transcribir_audio_cloud(reply_path)
                print(f"📝 Transcripción: {transcription}")

                twilio.send_whatsapp_message(transcription, sender_number, media_url=None)

            except Exception as e:
                print("❌ Error procesando audio:", str(e))
                return "Error en transcripción", 500

        elif media_type.startswith("image"):
            print("🖼️ Es imagen")

            try:
                reply_path = download_file(media_url, file_path)
                description = vision.describe_image(reply_path)
                twilio.send_whatsapp_message(description, sender_number, media_url=None)

            except Exception as e:
                print("❌ Error procesando imagen:", str(e))
                return "Error en descripción de imagen", 500

        elif media_type == "application/pdf":
            print("📄 Es PDF")

            try:
                reply_path = download_file(media_url, file_path)
                pdf_text = vision.extract_text_from_pdf(reply_path)
                twilio.send_whatsapp_message(pdf_text, sender_number, media_url=None)

            except Exception as e:
                print("❌ Error procesando PDF:", str(e))
                return "Error en lectura de PDF", 500

        else:
            print("⚠️ Tipo de archivo no soportado:", media_type)
            twilio.send_whatsapp_message(
                "⚠️ Tipo de archivo no soportado. Envía un mensaje de voz, imagen o PDF.",
                sender_number
            )



    return "✅ Procesado correctamente"

def download_file(media_url: str, file_path: str) -> str:
    """
    Descarga un archivo multimedia desde Twilio con autenticación.
    """
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")

        if not account_sid or not auth_token:
            raise ValueError("TWILIO_ACCOUNT_SID o TWILIO_AUTH_TOKEN no están definidos")

        response = requests.get(media_url, auth=HTTPBasicAuth(account_sid, auth_token), timeout=10)
        response.raise_for_status()

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"✅ Archivo descargado en: {file_path}")
        return file_path

    except Exception as e:
        print(f"❌ Error al descargar archivo desde {media_url}: {e}")
        raise

'''
'''
# Modulos Build-in
import flask
import os
import requests
import time
from dotenv import load_dotenv

# Modulos de 3eros
from requests.auth import HTTPBasicAuth
from twilio.twiml.messaging_response import MessagingResponse

# Modulos propios
import app.services.twilio_service as twilio
import app.services.wisper as wisper
import app.services.vision as vision
from app.Model.users import Users

# Cargar variables de entorno
load_dotenv()
TMP_DIR = "/tmp"

# Blueprint de Flask
routes = flask.Blueprint("routes", __name__)

from requests.auth import HTTPBasicAuth

def download_file(media_url: str, file_path: str) -> str:
    """
    Descarga un archivo multimedia desde Twilio con autenticación.
    """
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")

        if not account_sid or not auth_token:
            raise ValueError("TWILIO_ACCOUNT_SID o TWILIO_AUTH_TOKEN no están definidos")

        response = requests.get(media_url, auth=HTTPBasicAuth(account_sid, auth_token), timeout=10)
        response.raise_for_status()

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"✅ Archivo descargado en: {file_path}")
        return file_path

    except Exception as e:
        print(f"❌ Error al descargar archivo desde {media_url}: {e}")
        raise


@routes.route("/", methods=["GET", "POST"])
def whatsapp_reply():
    if flask.request.method == 'GET':
        return "✅ Server is running and accessible via GET request."

    sender_number = flask.request.form.get('From')
    message_body = flask.request.form.get("Body", "").strip()
    num_media = int(flask.request.form.get("NumMedia", 0))

    description = ""
    transcription = ""
    pdf_text = ""

    if num_media > 0:
        media_url = flask.request.form.get("MediaUrl0")
        media_type = flask.request.form.get("MediaContentType0")

        print(f"📩 Media URL: {media_url}")
        print(f"📦 Media Type: {media_type}")

        # Sanitizamos número y armamos ruta
        clean_sender = sender_number.replace(":", "_").replace("+", "")
        folder = os.path.join(TMP_DIR, f"{clean_sender}_media")
        os.makedirs(folder, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        extension = media_type.split("/")[-1]
        nombre_del_archivo = f"{clean_sender}_{timestamp}.{extension}"
        file_path = os.path.join(folder, nombre_del_archivo)

        print(f"📁 Ruta del archivo: {file_path}")

        if media_type.startswith("audio"):
            print("🎙️ Es audio")

            try:
                reply_path = download_file(media_url, file_path)
                transcription = wisper.transcribir_audio_cloud(reply_path)
                print(f"📝 Transcripción: {transcription}")

                twilio.send_whatsapp_message(transcription, sender_number, media_url=None)

            except Exception as e:
                print("❌ Error procesando audio:", str(e))
                return "Error en transcripción", 500

        elif media_type.startswith("image"):
            print("🖼️ Es imagen")

            try:
                reply_path = download_file(media_url, file_path)
                description = vision.describe_image(reply_path)
                twilio.send_whatsapp_message(description, sender_number, media_url=None)

            except Exception as e:
                print("❌ Error procesando imagen:", str(e))
                return "Error en descripción de imagen", 500

        elif media_type == "application/pdf":
            print("📄 Es PDF")

            try:
                reply_path = download_file(media_url, file_path)
                pdf_text = vision.extract_text_from_pdf(reply_path)
                twilio.send_whatsapp_message(pdf_text, sender_number, media_url=None)

            except Exception as e:
                print("❌ Error procesando PDF:", str(e))
                return "Error en lectura de PDF", 500

        else:
            print("⚠️ Tipo de archivo no soportado:", media_type)
            twilio.send_whatsapp_message(
                "⚠️ Tipo de archivo no soportado. Envía un mensaje de voz, imagen o PDF.",
                sender_number
            )

    return "✅ Procesado correctamente"
'''
'''

# Modulos Build-in
import flask
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Modulos de 3eros
from twilio.twiml.messaging_response import MessagingResponse
import app.services.twilio_service as twilio


# Modulos propios
import app.services.wisper as wisper
import app.services.vision as vision
#import app.message_p as engine
from app.Model.users import Users   


load_dotenv()  # Carga variables desde .env
TMP_DIR = "/tmp"

routes = flask.Blueprint("routes", __name__)

@routes.route("/", methods=["GET", "POST"])
def whatsapp_reply():

    if flask.request.method == 'GET':
        return "Server is running and accessible via GET request." + new 
    
    sender_number = flask.request.form.get('From')
    message_body = flask.request.form.get("Body", "").strip()
    num_media = int(flask.request.form.get("NumMedia", 0))

    description = ""
    transcription = ""
    pdf_text = ""
    
    if num_media > 0:
        # Asegurarse de que el directorio exista
        folder = os.path.join("/tmp", f"{sender_number}_media")
        os.makedirs(folder, exist_ok=True)

        # Ruta final donde querés guardar el archivo
        file_path = os.path.join(folder, nombre_del_archivo)
        media_url = flask.request.form.get("MediaUrl0", None)
        media_type = flask.request.form.get("MediaContentType0", None)

        file_path = os.path.join(TMP_DIR, f"{sender_number}_media")

        if media_type.startswith("audio"):
            print("Es audio!")
            
            try:
                reply = twilio.download_file(sender_number, media_url, media_type, file_path)
            except Exception as e:
                print("❌ Error en download_file:", str(e))
                return "Download failed", 500
            #reply = twilio.download_file(sender_number, media_url, media_type, file_path)
            
            
            reply = list(reply)[0] if isinstance(reply, set) else reply
            print(reply)

            transcription = wisper.transcribir_audio_cloud(reply)
            print(transcription)
            twilio.send_whatsapp_message(transcription, sender_number, media_url = None)
    
    return "Ok"
'''
'''
# Modulos Build-in
import flask
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

#import flask
#from flask import Blueprint, request, jsonify
#import os
#from twilio.twiml.messaging_response import MessagingResponse
#import app.services.twilio_service as twilio

# Modulos de 3eros
from twilio.twiml.messaging_response import MessagingResponse
import app.services.twilio_service as twilio


# Modulos propios
import app.services.wisper as wisper
import app.services.vision as vision
#import app.message_p as engine

load_dotenv()  # Carga variables desde .env

routes = flask.Blueprint("routes", __name__)

@routes.route("/", methods=["GET", "POST"])
def whatsapp_reply():
    if flask.request.method == 'GET':
        return "Server is running and accessible via GET request." 
    
    sender_number = flask.request.form.get('From')
    #print(sender_number)
    message_body = flask.request.form.get("Body", "").strip()
    num_media = int(flask.request.form.get("NumMedia", 0))
    #print(num_media)

    description = ""
    transcription = ""
    pdf_text = ""
    
    
    twilio.send_whatsapp_message("Dale amargo", sender_number, media_url = None)
    return "Ok"

# Modulos Build-in
import flask
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

#import flask
#from flask import Blueprint, request, jsonify
#import os
#from twilio.twiml.messaging_response import MessagingResponse
#import app.services.twilio_service as twilio

# Modulos de 3eros
from twilio.twiml.messaging_response import MessagingResponse
import app.services.twilio_service as twilio


# Modulos propios
#import app.services.wisper as wisper
#import app.services.vision as vision
#import app.message_p as engine

load_dotenv()  # Carga variables desde .env

routes = flask.Blueprint("routes", __name__)

@routes.route("/", methods=["GET", "POST"])
def whatsapp_reply():
    if flask.request.method == 'GET':
        return "Server is running and accessible via GET request." 
    
    sender_number = flask.request.form.get('From')
    #print(sender_number)
    message_body = flask.request.form.get("Body", "").strip()
    num_media = int(flask.request.form.get("NumMedia", 0))
    #print(num_media)

    description = ""
    transcription = ""
    pdf_text = ""
    
    
    twilio.send_whatsapp_message("Dale amargo", sender_number, media_url = None)
    return "Ok"
'''
'''
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde .env

routes = Blueprint("routes", __name__)

@routes.route("/", methods=["GET", "POST"])


def hello_world():
    # Recuperamos todas las claves relevantes del entorno
    env_vars = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
        "SUPABASE_URL": os.environ.get("SUPABASE_URL"),
        "SUPABASE_API_KEY": os.environ.get("SUPABASE_API_KEY"),
        "TWILIO_ACCOUNT_SID": os.environ.get("TWILIO_ACCOUNT_SID"),
        "TWILIO_AUTH_TOKEN": os.environ.get("TWILIO_AUTH_TOKEN"),
        "TWILIO_WHATSAPP_NUMBER": os.environ.get("TWILIO_WHATSAPP_NUMBER"),
        "PINECONE_API_KEY": os.environ.get("PINECONE_API_KEY")
    }

    if request.method == "GET":
        # Devolverlo como texto plano (opcionalmente podés formatearlo mejor)
        return "\n".join([f"{k}: {v}" for k, v in env_vars.items()])

    if request.method == "POST":
        return jsonify({
            "message": "POST recibido correctamente",
            "env_vars": env_vars
        })
'''
'''
from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

@app.route("/", methods=["POST"])
def ask_openai():
    """
    Endpoint que recibe un JSON con contexto y llama a OpenAI.
    Espera: {"context": "Un chiste", "temperature": 0.7, "model": "gpt-4"}
    """
    try:
        data = request.get_json()

        context = data.get("context", "Hola")
        temperature = data.get("temperature", 0)
        model = data.get("model", "gpt-4")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return jsonify({"error": "API key no encontrada"}), 500

        openai.api_key = api_key

        messages = [{"role": "system", "content": context}]

        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        content = completion.choices[0].message.content
        return jsonify({"response": content})

    except openai.error.OpenAIError as e:
        return jsonify({"error": f"Error en la API de OpenAI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
'''
'''
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    openai_key = os.environ.get("OPENAI_API_KEY")
    return openai_key
'''
'''
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde .env

routes = Blueprint("routes", __name__)

@routes.route("/", methods=["GET", "POST"])
def hello_world():
    openai_key = os.environ.get("OPENAI_API_KEY")

    if request.method == "GET":
        return f"OPENAI_API_KEY: {openai_key}"

    if request.method == "POST":
        return jsonify({
            "message": "POST recibido correctamente",
            "openai_key": openai_key
        })  
'''