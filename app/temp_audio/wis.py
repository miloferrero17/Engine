import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

import os
import openai
from dotenv import load_dotenv

# Cargar variables de entorno desde .env, si las usas
load_dotenv()

# Elimina las variables de entorno relacionadas con proxies
for var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "NO_PROXY", "no_proxy"]:
    os.environ.pop(var, None)

# Configura la API key
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.proxy = None  # Asegúrate de que OpenAI no use proxy

# Limpia la configuración de proxy en la sesión de requests
try:
    api_requestor = openai.api_requestor.default_api_requestor()
    api_requestor._session.proxies = {}
except Exception as e:
    print("No se pudo limpiar proxies en la sesión:", e)
    

print("Directorio actual:", os.getcwd())
# Asegúrate de tener la variable de entorno OPENAI_API_KEY configurada
#openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai  # Definimos client como referencia a openai
print("Versión de openai:", openai.__version__)

def transcribir_audio_cloud(ruta_archivo: str) -> str:
    try:
        with open(ruta_archivo, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text  # Use attribute access instead of transcription["text"]
    except Exception as e:
        return f"Error en la transcripción: {e}"

if __name__ == "__main__":
    client = openai  # Usamos client como alias de openai
    # Forzar que la sesión interna no tenga proxies:
    try:
        client.requestor._session.proxies = {}
    except Exception as e:
        print("No se pudo limpiar proxies en la sesión:", e)
    
    current_directory = os.getcwd()
    ruta = current_directory +  "/flask-lambda-hello/app/temp_audio/test2.m4a"
    text = transcribir_audio_cloud(ruta)
    print(text)