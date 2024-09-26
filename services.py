import json
import time
from message_processing import get_template_by_text, handle_template, process_message
from whatsapp_service import enviar_Mensaje_whatsapp

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    return process_message(message)

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text, number, messageId, name):
    text = text.lower()  # mensaje que envio el usuario
    mensajes = []  # Cambiado de 'list' a 'mensajes'
    print("mensaje del usuario: ",text)

    mark_read = markRead_Message(messageId)
    mensajes.append(mark_read)
    time.sleep(2)

    template_encontrado = get_template_by_text(text)
    handle_template(template_encontrado, number, messageId, mensajes)

    for item in mensajes:
        enviar_Mensaje_whatsapp(item)  # Corregido: alineación adecuada
        time.sleep(item.get('delay', 0))

def replace_start(s):
    """
    Reemplaza el prefijo del número de WhatsApp si comienza con '521' o '549'.
    
    Args:
        s (str): El número de teléfono a modificar.
    
    Returns:
        str: El número de teléfono modificado.
    """
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s

