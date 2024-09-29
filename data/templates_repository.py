import os
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True)
    trigger = Column(String)
    type = Column(String)
    body = Column(Text)
    footer = Column(Text)
    options = Column(JSON)
    seed = Column(String)
    additional_actions = Column(JSON)

def get_engine():
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, 'templates.db')
    return create_engine(f'sqlite:///{db_path}')

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def create_template(template):
    session = get_session()
    new_template = Template(
        trigger=template['trigger'],
        type=template['type'],
        body=template['body'],
        footer=template['footer'],
        options=template['options'],
        seed=template['seed'],
        additional_actions=template['additional_actions']
    )
    session.add(new_template)
    session.commit()
    session.close()

def read_template(template_id):
    session = get_session()
    template = session.query(Template).filter(Template.id == template_id).one_or_none()
    session.close()
    return template.__dict__ if template else None

def update_template(template_id, updated_template):
    session = get_session()
    template = session.query(Template).filter(Template.id == template_id).one_or_none()
    if template:
        template.trigger = updated_template['trigger']
        template.type = updated_template['type']
        template.body = updated_template['body']
        template.footer = updated_template['footer']
        template.options = updated_template['options']
        template.seed = updated_template['seed']
        template.additional_actions = updated_template['additional_actions']
        session.commit()
    session.close()

def delete_template(template_id):
    session = get_session()
    template = session.query(Template).filter(Template.id == template_id).one_or_none()
    if template:
        session.delete(template)
        session.commit()
    session.close()

def get_all_templates():
    session = get_session()
    templates = session.query(Template).all()
    session.close()
    return [template.__dict__ for template in templates]