# message_p.py actualizado

# Módulos Build-in
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+
from typing import Optional
import json
from dateutil.parser import isoparse
import requests

# Módulos de 3eros
import app.services.twilio_service as twilio
from twilio.twiml.messaging_response import MessagingResponse

# Módulos propios
from app.Model.users import Users   
from app.Model.enums import Role
from app.Model.contacts import Contacts
from app.Model.engine import Engine
from app.Model.messages import Messages
from app.Model.transactions import Transactions
from app.Model.questions import Questions
from app.Model.events import Events
from app.Utils.table_cleaner import TableCleaner


import app.services.brain as brain
import app.services.decisions as decs
import app.services.embedding as vector
from app.services.decisions import next_node_fofoca_sin_logica, limpiar_numero, calcular_diferencia_en_minutos,ejecutar_codigo_guardado
import app.services.brain as brain


def handle_incoming_message(body, to, media_url):
    print(body)
    msj = Messages()
    tx = Transactions()
    ev = Events()
    numero_limpio = limpiar_numero(to)
    ctt = Contacts()    

    # Obtener el timestamp actual en UTC
    now_utc = datetime.now(timezone.utc)
    formatted_now = now_utc.strftime("%Y-%m-%d %H:%M:%S.%f")

    #event_id = msj.get_last_event_id_by_phone(numero_limpio)
    #print(event_id)

    ### 1) Inicializo las variables
    event_id = 0
    msg_key = 0
    tiempo_sesion = 5
    nodo_destino = 0
    ultimo_mensaje = ""
    response_text = ""
    next_node_question = ""
    registro = 0
    max_preguntas= 0
    #ev.get_cant_preguntas_by_event_id(event_id)
    #print(max_preguntas)
    contexto = ""
    #ev.get_description_by_event_id(event_id)
    #print(contexto)
    eng = Engine()
    aux = Messages()
    qs = Questions()
    last_assistant_question = Messages()
    group_id = 0
    question_id = 0
    question_name =""
    contacto = ""
    result = ""
    subsiguiente = 0
    conversation_str = ""
    conversation_history = [{"role": "system", "content": ""}]
    aux_question_fofoca = [{"role": "system", "content": ""}]
    variables = {
        "body": body,
        "max_preguntas":max_preguntas,
        "nodo_destino": nodo_destino,
        "numero_limpio": numero_limpio,
        "msg_key": msg_key,
        "ctt": ctt,
        "msj": msj,
        "qs":qs,
        "last_assistant_question": last_assistant_question,
        "eng": eng,
        "tx": tx,
        "ev":ev,
        "response_text": response_text,
        "conversation_str": conversation_str,
        "aux_question_fofoca": aux_question_fofoca,
        "ultimo_mensaje": ultimo_mensaje,
        "next_node_question": next_node_question,
        "aux": aux,
        "contacto": contacto,
        "result": result,
        "conversation_history": conversation_history,
        "question_name": question_name,
        "question_id": question_id,
        "group_id":group_id,
        "event_id":event_id,
        "subsuguientes": subsiguiente
    }


    contacto = ctt.get_by_phone(numero_limpio)

    #### 1) Reseteo
    if body in ("1", "2", "3", "4", "5"):
        event_id = int(body)
        msg_key = ev.get_nodo_inicio_by_event_id(event_id)

        try: 
            if contacto is None:
                # creás el contacto y recuperás sólo el ID
                _new_id = ctt.add(
                    event_id=event_id,
                    name="Juan",
                    phone=numero_limpio
                )
                # ahora sí traés el objeto completo con su contact_id, nombre, etc.
                contacto = ctt.get_by_phone(numero_limpio)
                print("1.1) Contacto creado")
            else:
                ctt.update(
                    contact_id=contacto.contact_id,
                    event_id=event_id
                )

        except Exception as e:
            print(f"Ocurrió un error: {e}")
        
            
        msj.add(
            msg_key=msg_key,
            text="Cambio a " + body,
            phone=numero_limpio,
            event_id=event_id
        )
        
        try:
            ultima_tx = tx.get_last_timestamp_by_phone(numero_limpio)
            print(ultima_tx)
            
            if ultima_tx is not None:
                # Cierro la transacción anterior
                tx.update(
                    id=ultima_tx["id"],
                    contact_id=contacto.contact_id,
                    phone=numero_limpio,
                    name="Cerrada",
                    timestamp=formatted_now,
                    event_id=event_id

                )
                print("2.1.) Cierro la tx vieja")                
                
                # Abro la nueva transacción
                #print(event_id)
                contexto_agente = ev.get_description_by_event_id(event_id)
                conversation_history = [{
                    "role": "system",
                    "content":contexto_agente
                }]
                #print(conversation_history)
                conversation_str = json.dumps(conversation_history)                
                
                
                tx.add(
                    contact_id=contacto.contact_id,
                    phone=numero_limpio,
                    event_id=event_id,
                    name="Abierta",
                    conversation = conversation_str,
                    timestamp=formatted_now,
                    data_created=formatted_now
                )
                print(tx)

                print("2.2.) Creo la tx")                

            else:
                # No había transacción previa: abro la primera
                contexto_agente = ev.get_description_by_event_id(event_id)
                conversation_history = [{
                    "role": "system",
                    "content":contexto_agente
                }]
                #print(conversation_history)
                conversation_str = json.dumps(conversation_history)                
                #print(conversation_str)
                tx.add(
                    contact_id=contacto.contact_id,
                    phone=numero_limpio,
                    name="Abierta",
                    event_id=event_id,
                    conversation = conversation_str,
                    timestamp=formatted_now,
                    data_created=formatted_now
                )

                print("2.3.) Creo la tx")                

        except (TypeError, KeyError) as e:
            print(f"❌ Error manejando transacciones: {e}")
            # acá podrías decidir si vuelves a lanzar la excepción o manejarla de otro modo

        
        except Exception as e:
            print(f"Ocurrió un error: {e}")

        twilio.send_whatsapp_message("Cambio de proyecto con éxito.", to, None)    
        return "Ok"        





    #### 2) Alta de contacto   
    if contacto is None:        
        ctt.add(
            event_id=0, 
            name="Juan",
            phone=numero_limpio
        )
        print("1) Contacto creado")
        twilio.send_whatsapp_message("¡Bienvenido! Estás a punto de iniciar una prueba con nuestro motor conversacional. Elegí el proyecto con el que querés comenzar. 1) Hunitro; 2) PX - Recepcion; 3) PX - Guardia; 4) PX - WA; 5) Growcast - Sales. Ingresa solo un numero.", to, None)    
        return "Ok"




    #### 3) Gestión de sesiones   
    if contacto is not None:        
        event_id = ctt.get_event_id_by_phone(numero_limpio)
        if event_id == 0:    ### Primera sesion de todas
            twilio.send_whatsapp_message("Por favor contesta un numero para comenzar.", to, None)   
            print("Por favor contesta un numero para comenzar.")
            return "Ok"        

        contexto_agente = ev.get_description_by_event_id(event_id)
        conversation_history = [{
            "role": "system",
            "content":contexto_agente
        }]
        #print(conversation_history)
        conversation_str = json.dumps(conversation_history)

        #print(conversation_str)   
        try: #### Creacion y update de sesiones
            ultima_tx = tx.get_last_timestamp_by_phone(numero_limpio)
            if ultima_tx is None:
                tx.add(
                    contact_id=contacto.contact_id,
                    phone=numero_limpio,
                    name="Abierta",
                    event_id=event_id,
                    conversation = conversation_str,
                    timestamp=formatted_now,
                    data_created=formatted_now
                )
                print("2.4) Creo la tx")
            
            
            elif tx.is_last_transaction_closed(numero_limpio) == 1: ### Esta cerrada
                print("2.8) Sesion cerrada sin hacer nada")
                tx.add(
                    contact_id=contacto.contact_id,
                    phone=numero_limpio,
                    name="Abierta",
                    event_id=event_id,
                    conversation = conversation_str,
                    timestamp=formatted_now,
                    data_created=formatted_now
                )
                
                msg_key = ev.get_nodo_inicio_by_event_id(event_id)
                msj.add(
                    msg_key=msg_key, 
                    text=body, 
                    phone=numero_limpio,
                    event_id=event_id
                )    
                print("2.6) Sesion nueva")
                    
            elif calcular_diferencia_en_minutos(tx, numero_limpio) > tiempo_sesion:
                                
                tx.update(
                    id=ultima_tx["id"],
                    contact_id=contacto.contact_id,
                    phone=numero_limpio,
                    name="Cerrada",
                    timestamp=formatted_now,
                    event_id=event_id
                )
                #print(tx)
                print("2.5) Sesion vencida")
            
                tx.add(
                    contact_id=contacto.contact_id,
                    phone=numero_limpio,
                    name="Abierta",
                    event_id=event_id,
                    conversation = conversation_str,
                    timestamp=formatted_now,
                    data_created=formatted_now
                )

                msg_key = ev.get_nodo_inicio_by_event_id(event_id)
                msj.add(
                    msg_key=msg_key, 
                    text=body, 
                    phone=numero_limpio,
                    event_id=event_id
                )    
                print("2.6) Sesion nueva")
            
            else:
                ### 3) Trabajo sobre la sesión vigente/recien creada 
                print("2.7) Sesion vigente") 
        
            
            ultimo_mensaje = msj.get_latest_by_phone(numero_limpio)
            if ultimo_mensaje:
                msg_key = ultimo_mensaje.msg_key
                print(ultimo_mensaje)
                print(msg_key)
                msj.add(
                    msg_key=msg_key, 
                    text=body, 
                    phone=numero_limpio,
                    event_id=event_id
                )


            # Bloque de update de sesión
            conversation_str = tx.get_open_conversation_by_contact_id(contacto.contact_id)
            conversation_history = json.loads(conversation_str) if conversation_str else []
            conversation_history.append({
                "role": "user",
                "content": body
            })
            conversation_str = json.dumps(conversation_history)

            '''
            open_tx_id = tx.get_open_transaction_id_by_contact_id(contacto.contact_id)
            print(open_tx_id)
            tx.update(
                id=open_tx_id,
                contact_id=contacto.contact_id,
                phone=numero_limpio,
                name="Abierta",
                conversation=conversation_str,
                timestamp=formatted_now,
                event_id=event_id
            )
            print(tx)
            '''
            nodo_destino = msg_key
            print(nodo_destino)
            while subsiguiente == 0:
                # Bloque de engine
                registro = eng.get_by_id(nodo_destino)
                print("Usted está entrando a: " + str(nodo_destino))
                #print(registro.Python_Code)
                codigo_crudo = registro.Python_Code
                contexto = {"__builtins__": {}, "print": print}
                contexto.update(variables)
                contexto_actualizado = ejecutar_codigo_guardado(codigo_crudo, variables)
                nodo_destino = contexto_actualizado.get("nodo_destino")  
                msg_key = nodo_destino
                subsiguiente = contexto_actualizado.get("subsiguiente")
                conversation_str = contexto_actualizado.get("conversation_str")
                response_text =  contexto_actualizado.get("response_text")
                group_id =  contexto_actualizado.get("group_id")
                question_id=contexto_actualizado.get("question_id")
                result=contexto_actualizado.get("result")


            print(result)
            #print(conversation_history)
            conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            conversation_str = json.dumps(conversation_history)
            print(conversation_str)

            #mensaje = msj.get_latest_by_phone(numero_limpio)
            mensaje_a_enviar = contexto_actualizado.get("response_text") or "Hubo un problema interno. Por favor intentá más tarde."
            twilio.send_whatsapp_message(mensaje_a_enviar, to, None)

            open_tx_id = tx.get_open_transaction_id_by_contact_id(contacto.contact_id)
            #print(open_tx_id)
            if result == "Cerrada": 
                tx.update(
                    id=open_tx_id,
                    contact_id=contacto.contact_id,
                    phone=numero_limpio,
                    name="Cerrada",
                    conversation=conversation_str,
                    timestamp=formatted_now,
                    event_id=event_id
                )
                twilio.send_whatsapp_message("Fin de la consulta, gracias!", to, None)
            else:
                tx.update(
                    id=open_tx_id,
                    contact_id=contacto.contact_id,
                    phone=numero_limpio,
                    name="Abierta",
                    conversation=conversation_str,
                    timestamp=formatted_now,
                    event_id=event_id

                )

            # Cargo la ultima pregunta
            last_assistant_question.add(
                msg_key=nodo_destino,
                text=response_text,
                phone=numero_limpio,
                group_id=group_id,
                question_id=question_id,
                event_id=event_id         
            )
            return "Ok"

        except (TypeError, KeyError) as e:
            print(f"❌ Error accediendo a 'name': {e}")

if __name__ == "__main__":
    handle_incoming_message("me duele la panza", "whatsapp:+5491133585362", "")