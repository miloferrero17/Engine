import os
import openai
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde .env

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY"),

def ask_openai(messages, temperature=0, model="gpt-4"):
    """
    Realiza una consulta a la API de OpenAI con los parámetros dados.

    Parámetros:
        messages (list): Lista de diccionarios que representan el historial de la conversación.
        temperature (float): Configuración de temperatura para la creatividad de las respuestas.
        model (str): Nombre del modelo de OpenAI a utilizar.

    Retorna:
        str: Respuesta generada por el modelo o un mensaje predeterminado en caso de error.
    """
    # Obtener la clave de API desde las variables de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key no encontrada. Configura la variable de entorno OPENAI_API_KEY.")

    # Configurar la clave de API para OpenAI
    openai.api_key = api_key

    try:
        # Llamada a la API de OpenAI
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        # Retorna el contenido del mensaje de la primera elección
        if completion.choices and completion.choices[0].message:
            return completion.choices[0].message.content
        else:
            return "No se pudo generar una respuesta. Intenta de nuevo."
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error en la API de OpenAI: {e}")

conversation_history = [{
    "role": "system",
    "content":"Sos un asistente virtual que te ayudara a resolver cualquier duda que tengas en comercio exterior"
}]
result = ask_openai(conversation_history,0,"gpt-4")
print(result)