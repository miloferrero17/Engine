import os
import base64
import pdfplumber
import openai
import logging
import warnings
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Capturar warnings silenciosos de librerías como pdfplumber
warnings.filterwarnings("always")
logging.captureWarnings(True)


def encode_image(image_path):
    """
    Convierte una imagen en base64 para enviarla a la API de OpenAI.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def describe_image(image_path):
    """
    Describe el contenido de una imagen usando GPT-4 Vision.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Imagen no encontrada en: {image_path}")

    base64_image = encode_image(image_path)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describime la imagen en 1000 caracteres."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=300
        )

        if "choices" not in response or not response["choices"]:
            print("❌ La respuesta de OpenAI no contiene 'choices' válidos:", response)
            return "❌ No se pudo procesar la imagen. Intentalo de nuevo."

        content = response["choices"][0]["message"].get("content", "").strip()
        if not content:
            print("❌ El contenido devuelto está vacío:", response)
            return "❌ No se obtuvo descripción de la imagen."

        print("🧠 Descripción generada:", content)
        return content

    except Exception as e:
        print("❌ Error en describe_image:", str(e))
        return f"❌ Error procesando imagen: {str(e)}"


def resumir_texto_largo(texto_original, max_tokens=300):
    """
    Usa OpenAI GPT para resumir un texto largo.
    """
    if not texto_original or texto_original.strip() == "":
        return "❌ No se encontró texto para resumir."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Resumí este texto en menos de {max_tokens * 4} caracteres para que se entienda fácilmente:\n\n{texto_original}"
                }
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"❌ Error al resumir el texto: {str(e)}"


def extract_text_from_pdf(pdf_path, max_chars=3000):
    """
    Extrae el texto de un PDF. Si es muy largo, lo resume automáticamente.
    """
    if not os.path.exists(pdf_path):
        return f"❌ No se encontró el archivo PDF: {pdf_path}"

    try:
        full_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    text = page.extract_text() or ""
                    print(f"📄 Página {page_num + 1} — {len(text)} caracteres extraídos.")
                    full_text += text
                except Exception as e:
                    print(f"⚠️ Error al procesar página {page_num + 1}: {e}")

        if not full_text.strip():
            return "❌ El PDF no contiene texto legible."

        if len(full_text) > max_chars:
            return resumir_texto_largo(full_text)
        else:
            return full_text.strip()

    except Exception as e:
        return f"❌ Error al procesar el PDF: {str(e)}"






'''
import os
import base64
import pdfplumber
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def encode_image(image_path):
    """
    Convierte una imagen en base64 para enviarla a la API de OpenAI.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def describe_image(image_path):
    """
    Describe el contenido de una imagen usando GPT-4 Vision.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Imagen no encontrada en: {image_path}")

    base64_image = encode_image(image_path)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describime la imagen en 1000 caracteres."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=300
        )

        if "choices" not in response or not response["choices"]:
            print("❌ La respuesta de OpenAI no contiene 'choices' válidos:", response)
            return "❌ No se pudo procesar la imagen. Intentalo de nuevo."

        content = response["choices"][0]["message"].get("content", "").strip()
        if not content:
            print("❌ El contenido devuelto está vacío:", response)
            return "❌ No se obtuvo descripción de la imagen."

        print("🧠 Descripción generada:", content)
        return content

    except Exception as e:
        print("❌ Error en describe_image:", str(e))
        return f"❌ Error procesando imagen: {str(e)}"


def resumir_texto_largo(texto_original, max_tokens=300):
    """
    Usa OpenAI GPT para resumir un texto largo.
    """
    if not texto_original or texto_original.strip() == "":
        return "❌ No se encontró texto para resumir."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Resumí este texto en menos de {max_tokens * 4} caracteres para que se entienda fácilmente:\n\n{texto_original}"
                }
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"❌ Error al resumir el texto: {str(e)}"


def extract_text_from_pdf(pdf_path, max_chars=3000):
    """
    Extrae el texto de un PDF. Si es muy largo, lo resume automáticamente.
    """
    if not os.path.exists(pdf_path):
        return f"❌ No se encontró el archivo PDF: {pdf_path}"

    try:
        full_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() or ""

        if not full_text.strip():
            return "❌ El PDF no contiene texto legible."

        if len(full_text) > max_chars:
            return resumir_texto_largo(full_text)
        else:
            return full_text.strip()

    except Exception as e:
        return f"❌ Error al procesar el PDF: {str(e)}"

import os
import base64
import pdfplumber
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def encode_image(image_path):
    """
    Convierte una imagen en base64 para enviarla a la API de OpenAI.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def describe_image(image_path):
    """
    Describe el contenido de una imagen usando GPT-4 Vision.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Imagen no encontrada en: {image_path}")

    base64_image = encode_image(image_path)

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describime la imagen en 1000 caracteres."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300
    )

    return response["choices"][0]["message"]["content"].strip()


def resumir_texto_largo(texto_original, max_tokens=300):
    """
    Usa OpenAI GPT para resumir un texto largo.
    """
    if not texto_original or texto_original.strip() == "":
        return "❌ No se encontró texto para resumir."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Resumí este texto en menos de {max_tokens * 4} caracteres para que se entienda fácilmente:\n\n{texto_original}"
                }
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"❌ Error al resumir el texto: {str(e)}"


def extract_text_from_pdf(pdf_path, max_chars=3000):
    """
    Extrae el texto de un PDF. Si es muy largo, lo resume automáticamente.
    """
    if not os.path.exists(pdf_path):
        return f"❌ No se encontró el archivo PDF: {pdf_path}"

    try:
        full_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() or ""

        if not full_text.strip():
            return "❌ El PDF no contiene texto legible."

        if len(full_text) > max_chars:
            return resumir_texto_largo(full_text)
        else:
            return full_text.strip()

    except Exception as e:
        return f"❌ Error al procesar el PDF: {str(e)}"


import openai
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def encode_image(image_path):
    """
    Converts an image file to Base64 format.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def describe_image(image_path):
    """
    Uses OpenAI API to generate a description of an image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image not found at: {image_path}")

    base64_image = encode_image(image_path)

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describime la lesion o padecimiento de la imagen."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300
    )

    return response["choices"][0]["message"]["content"]






import openai
import base64
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Función para convertir imagen a base64
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Ruta de la imagen local
image_path = os.path.join("/home/runner/workspace", "received_images", "whatsapp_+5491133585362_20250318_200356.jpeg")

# Convertir imagen a base64
base64_image = encode_image(image_path)

# Llamada a la API con imagen local en base64
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "¿Qué hay en esta imagen?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",  # 🔥 Imagen en base64
                    },
                },
            ],
        }
    ],
    max_tokens=300
)

# Mostrar la respuesta
print(response["choices"][0]["message"]["content"])
'''



'''import openai
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Configurar API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verificar si la API Key está cargada
if not openai.api_key:
    raise ValueError("⚠️ Error: No se encontró la API Key. Configura OPENAI_API_KEY en .env.")

# Llamada a la API con la imagen
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",  # Modelo con visión
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "¿Qué hay en esta imagen?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                },
            ],
        }
    ],
    max_tokens=300  # Ajustar la respuesta
)

# Mostrar la respuesta
print(response["choices"][0]["message"]["content"])
'''

'''
import openai
from dotenv import load_dotenv
import os
load_dotenv()

# Cargar la imagen y procesarla
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Extrae y devuelve únicamente el texto contenido en la imagen."},
    ],
    max_tokens=500,
    temperature=0,
    images=[{
        "url": "received_images/whatsapp_+5491133585362_20250318_200356.jpeg"
    }]
)

# Mostrar el texto extraído
print(response["choices"][0]["message"]["content"])
'''