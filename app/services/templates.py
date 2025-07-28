from clients.dynamodb import (get_templates_data, create_template_data, update_template_data, delete_template_data)

async def get_templates():
    return get_templates_data()

async def create_template(template: dict):
    return create_template_data(template)

async def update_template(template_id: str, template: dict):
    return update_template_data(template_id, template)

async def delete_template(template_id: str):
    return delete_template_data(template_id)
