import json

from messages.message_creation import buttonReply_Message, listReply_Message, text_Message, sticker_Message, document_Message, get_media_id  
from data import templates_repository

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def process_message(message):
    typeMessage = message.get('type')

    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    return text


def handle_message(template, number, messageId,
                     mensajes, footer):
    print("messageId", messageId)
    message = None
    if template['type'] == 'text':
        message = text_Message(number, template['body'])
    elif template['type'] == 'sticker':
        sticker_id = get_media_id(template['sticker_name'], 'sticker')
        if sticker_id:
            message = sticker_Message(number, sticker_id)
    elif template['type'] == 'button':  
        print("template['options']", template['options'])
        message = buttonReply_Message(number, 
                                                template['options'], 
                                                template['body'], 
                                                footer,
                                                template['seed']
                                                )
    elif template['type'] == 'list':
        message = listReply_Message(number, 
                                            template['options'], 
                                            template['body'], 
                                            footer,
                                            template['seed'] 
                                            )
    elif template['type'] == 'document':
        message = document_Message(number, 
                                            template['url'], 
                                            template['text'], 
                                            template['document_name'])
    print("handle_message() - message: ", message)  
    if message:
        mensajes.append(message)

def handle_template(template, number, message_id,
                     mensajes):
    footer = "Equipo Rosbil"
    handle_message(template, number, message_id, mensajes, footer)

    for action in template['additional_actions']:
        handle_message(action, number, message_id, mensajes, footer)

def get_template_by_text(text):
    templates = templates_repository.get_all_templates()
    template_not_found = None
    for template in templates:
        if template['trigger'] in text:
            print("get_template_by_text() - template: ",template)
            return template
        elif template['trigger'] == 'not found':
            template_not_found = template

    print("get_template_by_text() - template_not_found: ", template_not_found)
    return template_not_found