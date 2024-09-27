import json
import sett

def text_Message(number, text):
    return  create_message(number, "text", text)

def buttonReply_Message(number, options, body, footer, sedd):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )
    content = {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
    return create_message(number, "interactive", content)

def listReply_Message(number, options, body, footer, sedd):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )
    content = {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
    return create_message(number, "interactive", content)

def document_Message(number, url, caption, filename):
    content = {
                "link": url,
                "caption": caption,
                "filename": filename        
            }   
    
    return create_message(number, "document", content)

def create_message(number, message_type, content):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": message_type,
            message_type: content
        }
    )
    return data

def sticker_Message(number, sticker_id):
    content = {"id": sticker_id}
    return create_message(number, "sticker", content)

def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    content = {
        "id": messageId,
        "reaction": {
            "emoji": emoji
        }
    }
    return create_message(number, "reaction", content)

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data
