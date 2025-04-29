
# Modulos Build-in
from datetime import datetime
import json
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+
from typing import Optional

# Modulos de 3eros
import app.services.twilio_service as twilio
from twilio.twiml.messaging_response import MessagingResponse


# Modulos propios
from app.Model.users import Users   
from app.Model.enums import Role
from app.Model.contacts import Contacts
from app.Model.engine import Engine
from app.Model.messages import Messages
from app.Model.transactions import Transactions
import app.services.brain as brain
import app.services.decisions as decs
import app.services.embedding as vector

numero_limpio = "5491133585362"
response_text = ""
last_assistant_question = Messages()
aux = last_assistant_question.get_latest_by_phone(numero_limpio)

response_text = aux.text
print(response_text)

import json
import app.services.brain as brain
import app.services.twilio_service as twilio
from app.Model.messages import Messages
from app.Model.questions import Questions
from twilio.twiml.messaging_response import MessagingResponse
import requests
import builtins
import sys

sender_number = "whatsapp:+" + numero_limpio

# 1) Cargo conversation_history
contacto = ctt.get_by_phone(numero_limpio)
conversation_str = tx.get_open_conversation_by_contact_id(contacto.contact_id)
conversation_history = json.loads(conversation_str) if conversation_str else []

mensaje_urgencia = (
            "En base únicamente a la respuesta de mi amigo, necesitas hacerle más preguntas o ya puedes concluir "
            "que tiene que hacerse alguna intervención médica. Respuestas: /0 si necesitas hacerle más preguntas/, "
            "/1 si puedes concluir que tiene que hacerse alguna intervención médica."
        )

conversation_history.append({
    "role": "assistant",
    "content": mensaje_urgencia
})
result = brain.ask_openai(conversation_history, temperature=0, model="gpt-4")
#print(result)

if result == "1":
    print("Urgente")    
    mensaje_derivacion_url = "https://mi-bucket-milito.s3.us-east-1.amazonaws.com/mensaje_derivacion.txt"
    response = requests.get(mensaje_derivacion_url)

    if response.status_code == 200:
        mensaje_derivacion = response.text
        print("✅ Archivo Mensaje de Derivacion cargado correctamente:")
        #print(mensaje_derivacion)
    else:
        print(f"❌ Error al cargar el archivo Mensaje de Derivacion: {response.status_code}")
    twilio.send_whatsapp_message("Estoy pensando, dame unos segundos...", sender_number, None)    

    conversation_history.append({
                "role": "assistant",
                "content": mensaje_derivacion
            })
    
    response_text = brain.ask_openai(conversation_history, temperature = 0, model = "gpt-4")
    result = "Cerrado"
    response_text = brain.ask_openai(conversation_history, temperature = 0, model = "gpt-4")
    nodo_destino = 3

    #receta_url = "https://mi-bucket-milito.s3.us-east-1.amazonaws.com/R01.pdf"
    
    #twilio.send_whatsapp_message("", sender_number, receta_url)

else:
    print("No Urgente")    
    grupos = qs.get_groups_by_event_id(event_id=2)

    # inicializo mi string “acumulador”
    grupos_str = ""
    derivacion = 0

    for g in grupos:
        # concateno cada línea al string, con salto de línea
        grupos_str += f"{g['group_id']} - {g['group_name']}, "

    # al finalizar, 'resultado' es un único string con todas las líneas
    #print(grupos_str)

    mensaje_def_triage = "Basado únicamente en la respuesta del paciente, cual de estas guardaias estas medianamente seguro de que corresponde derivarlo?: " + grupos_str + " En caso de que no tengas una apuesta indica el camino numero 11. Serias tan amable de responderme solamente con numeros la guardia?"

    print(mensaje_def_triage)

    conversation_history.append({
            "role": "assistant",
            "content": mensaje_def_triage
        })
    
    result = brain.ask_openai(conversation_history, temperature = 0, model = "gpt-4")
    print(result)

    if result == "11":
        result = "Cerrado"
        #print(result)
        response_text = "No te entiendo ... te recomiendo que te vayas a la guardia"
        nodo_destino = 3
    else:
        group_id = builtins.int(result)
        print("Derivacion")
        print(group_id)
        question_ids = qs.get_question_ids_by_group_id(group_id)
        print("IDs de Preguntas")
        print(question_ids)
        msj = Messages()
        mensaje = msj.get_penultimate_by_phone(numero_limpio)
        print("Objeto")  
        print(mensaje)  
        print(mensaje.question_id)
        msj_id_int = builtins.int(mensaje.question_id)
        print(msj_id_int)

        if mensaje.question_id == 0:
            pregunta_grupo = question_ids[0]
            print(f"Primera pregunta: {pregunta_grupo}")
            question_id= pregunta_grupo
            print(question_id)
            response_text = "Pregunta 1"
            nodo_destino = 5

        else:
            print ("Pregunta del medio")
            '''
            siguiente = qs.get_next_question_id(msj_id_int)
            next_qs_id_int = builtins.int(siguiente.question_id)
            print(next_qs_id_int)
            print("Aca falla")
            question_name = qs.get_question_name_by_id(next_qs_id_int)
            print(question_name)
            question_id= msj_id_int
            print(question_id)
            '''
            response_text = "Pregunta del medio"

            nodo_destino = 5
            sys.exit()

            if siguiente != "No existe":
                pregunta_grupo = siguiente
                print(f"Siguiente pregunta: {pregunta_grupo}")
                response_text = question_name
                print(response_text)
                nodo_destino = 5
            else:
                # No hay siguiente pregunta, derivamos
                twilio.send_whatsapp_message("Estoy pensando, dame unos segundos...", sender_number, None)

                conversation_history.append({
                    "role": "assistant",
                    "content": mensaje_derivacion
                })

                response_text = brain.ask_openai(conversation_history, temperature=0, model="gpt-4")
                result = "Cerrado"
                nodo_destino = 3

'''

conversation_history.append({
    "role": "user",
    "content": body  # lo que escribió la persona
})


last_assistant_question.add(
    msg_key=2,
    text=response_text,
    phone=numero_limpio    
)

msj.add(
    msg_key=2,
    text=body,
    phone=numero_limpio
)

next_node_question = "¿Tenes una cuenta bancaria?¿Es de comercio exterior?"

aux_question_fofoca = [{
    "role": "assistant",
    "content":"Sos un experto en comercio exterior del mercosur con foco en Argentina. Ante esta pregunta: "+ response_text + "El usuario contesto esto: " + body + " Razonamiento: Podrias darle al usuario breve consejo de no mas de 80 tokens con foco en el potencial de importar y el valor que le podes aportar como despachante de aduana. Adicionalmente hace que la narrativa tienda a la siguiente pregunta: " + next_node_question
}]

print(aux_question_fofoca)

conversation_history.append({
    "role": "assistant",
    "content": response_text
})


result = brain.ask_openai(aux_question_fofoca, temperature=0, model="gpt-4")

print(result)
nodo_destino = 5

msj.add(
    msg_key=nodo_destino,
    text=result,
    phone=numero_limpio
)
'''