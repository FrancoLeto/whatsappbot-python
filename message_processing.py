import json

from message_creation import buttonReply_Message, listReply_Message, text_Message, sticker_Message, document_Message, get_media_id  


def process_message(message):
    typeMessage = message.get('type')
    if typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    return text


def handle_message(template, number, messageId,
                     mensajes, footer):
    message = None
    if template['type'] == 'text':
        message = text_Message(number, template['body'])
    elif template['type'] == 'sticker':
        sticker_id = get_media_id(template['sticker_name'], 'sticker')
        if sticker_id:
            message = sticker_Message(number, sticker_id)
    elif template['type'] == 'button':
        message = buttonReply_Message(number, 
                                                template['options'], 
                                                template['body'], 
                                                footer, 
                                                template['seed'], 
                                                messageId)
    elif template['type'] == 'list':
        message = listReply_Message(number, 
                                            template['options'], 
                                            template['body'], 
                                            footer, 
                                            template['seed'], 
                                            messageId)
    elif template['type'] == 'document':
        message = document_Message(number, 
                                            template['url'], 
                                            template['text'], 
                                            template['document_name'])
    if message:
        mensajes.append(message)

def handle_template(template, number, messageId,
                     mensajes):
    footer = "Equipo Rosbil"
    handle_message(template, number, messageId, mensajes, footer)

    for action in template['additional_actions']:
        handle_message(action, number, messageId, mensajes, footer)

def get_template_by_text(text):
    with open('messages_templates.json', 'r', encoding='utf-8') as file:
        templates = json.load(file)
    template_not_found = None 
    for template in templates:
        if template['trigger'] in text:
            return template
        elif template['trigger'] == 'not found':
            template_not_found = template

    return template_not_found