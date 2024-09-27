import json

from templates_repository import create_template

def load_json_to_db(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        templates = json.load(file)
        
        for template in templates:
            create_template(template)

load_json_to_db('messages_templates.json')