from flask import Flask, request, jsonify
from flasgger import Swagger
import sett 
import services
from service import template_service

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e,403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        services.administrar_chatbot(text, number,messageId,name)
        return 'enviado'

    except Exception as e:
        return 'no enviado ' + str(e)

@app.route('/templates', methods=['GET'])
def get_templates():
    """
    Get all templates
    ---
    responses:
      200:
        description: A list of templates
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              content:
                type: string
    """
    templates = template_service.get_all_templates()
    return jsonify(templates)

@app.route('/templates', methods=['POST'])
def add_template():
    """
    Add a new template
    ---
    parameters:
      - name: body
        in: body
        required: true
        description: JSON object containing the template data
        schema:
          type: object
          properties:
            name:
              type: string
            content:
              type: string
    responses:
      201:
        description: Template created successfully
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Invalid input
    """
    template_data = request.get_json()
    template_service.create_template(template_data)
    return jsonify({'message': 'Template created successfully'}), 20
@app.route('/templates/<int:template_id>', methods=['DELETE'])
def delete_template(template_id):
    """
    Delete a template
    ---
    parameters:
      - name: template_id
        in: path
        type: integer
        required: true
        description: ID of the template to delete
    responses:
      200:
        description: Template deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Template not found
    """
    template_service.delete_template(template_id)
    return jsonify({'message': 'Template deleted successfully'}), 200

@app.route('/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    """
    Get a template by ID
    ---
    parameters:
      - name: template_id
        in: path
        type: integer
        required: true
        description: ID of the template to retrieve
    responses:
      200:
        description: Template retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            content:
              type: string
      404:
        description: Template not found
    """
    template = template_service.get_template(template_id)
    return jsonify(template)

@app.route('/templates/<int:template_id>', methods=['PUT']) 
def update_template(template_id):
    """
    Update an existing template
    ---
    parameters:
      - name: template_id
        in: path
        type: integer
        required: true
        description: ID of the template to update
      - name: body
        in: body
        required: true
        description: JSON object containing the template data
        schema:
          type: object
          properties:
            name:
              type: string
            content:
              type: string
    responses:
      200:
        description: Template updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Invalid input
      404:
        description: Template not found
    """
    template_data = request.get_json()
    template_service.update_template(template_id, template_data)
    return jsonify({'message': 'Template updated successfully'}), 200

if __name__ == '__main__':
    print("Swagger UI should be available at http://localhost:5000/apidocs")
    app.run()