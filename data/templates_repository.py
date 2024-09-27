import sqlite3
import json

def create_template(template):
    conn = sqlite3.connect('templates.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO templates (trigger, type, body, footer, options, seed, additional_actions)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (template['trigger'], template['type'], template['body'], template['footer'], 
          json.dumps(template['options']), template['seed'], json.dumps(template['additional_actions'])))
    
    conn.commit()
    conn.close()

def read_template(template_id):
    conn = sqlite3.connect('templates.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM templates WHERE id = ?', (template_id,))
    template = cursor.fetchone()
    
    conn.close()
    return template

def update_template(template_id, updated_template):
    conn = sqlite3.connect('templates.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE templates
    SET trigger = ?, type = ?, body = ?, footer = ?, options = ?, seed = ?, additional_actions = ?
    WHERE id = ?
    ''', (updated_template['trigger'], updated_template['type'], updated_template['body'], updated_template['footer'], 
          json.dumps(updated_template['options']), updated_template['seed'], json.dumps(updated_template['additional_actions']), template_id))
    
    conn.commit()
    conn.close()

def delete_template(template_id):
    conn = sqlite3.connect('templates.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM templates WHERE id = ?', (template_id,))
    
    conn.commit()
    conn.close()

def get_all_templates():
    conn = sqlite3.connect('templates.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM templates')
    templates = cursor.fetchall()
    
    conn.close()
    return templates