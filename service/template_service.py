from data import templates_repository

def get_all_templates():
    return templates_repository.get_all_templates()

def create_template(template_data):
    templates_repository.create_template(template_data)

def delete_template(template_id):
    templates_repository.delete_template(template_id)

def get_template(template_id):
    return templates_repository.read_template(template_id)

def update_template(template_id, template_data):
    templates_repository.update_template(template_id, template_data)