import time
from messages.message_processing import get_template_by_text, handle_template, process_message, markRead_Message
from service.whatsapp_service import enviar_Mensaje_whatsapp

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    return process_message(message)

def administrar_chatbot(text, number, messageId, name):
    text = text.lower()  # mensaje que envio el usuario
    mensajes = []  # Cambiado de 'list' a 'mensajes'
    print("mensaje del usuario: ",text)
    mark_read = markRead_Message(messageId)
    mensajes.append(mark_read)
    template_encontrado = get_template_by_text(text)
    handle_template(template_encontrado, number, messageId, mensajes)

    for item in mensajes:
        enviar_Mensaje_whatsapp(item)  # Corregido: alineación adecuada
        if 'delay' in item:
            time.sleep(item['delay'])

def replace_start(s):
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s
