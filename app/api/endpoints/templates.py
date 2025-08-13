from fastapi import APIRouter, Depends
from core.security_cognito import verify_admin as verify_admin_dep
from services.templates import (get_templates, create_template, update_template, delete_template)

router = APIRouter()

@router.get("/templates")
async def fetch_templates(_: dict = Depends(verify_admin_dep)):
    return await get_templates()

@router.post("/templates")
async def add_template(template_data: dict, _: dict = Depends(verify_admin_dep)):
    return await create_template(template_data)

@router.put("/templates/{template_id}")
async def edit_template(
    template_id: str,
    template_data: dict,
    _: dict = Depends(verify_admin_dep),
):
    return await update_template(template_id, template_data)

@router.delete("/templates/{template_id}")
async def remove_template(
    template_id: str,
    _: dict = Depends(verify_admin_dep),
):
    return await delete_template(template_id)
