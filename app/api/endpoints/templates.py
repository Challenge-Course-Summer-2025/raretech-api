from fastapi import APIRouter, Depends
from core.security_cognito import verify_admin as verify_admin_dep
from services.templates import (
    get_templates,
    create_template,
    update_template,
    delete_template,
    activate_template,
    get_template_by_id_service,
)

router = APIRouter()

@router.get("/templates")
async def fetch_templates(_: dict = Depends(verify_admin_dep)):
    return await get_templates()

@router.get("/templates/{template_id}")
async def fetch_template_by_id(template_id: str, _: dict = Depends(verify_admin_dep)):
    return await get_template_by_id_service(template_id)

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

@router.patch("/templates/{template_id}/activate")
async def activate_template_api(
    template_id: str,
    _: dict = Depends(verify_admin_dep),
):
    return await activate_template(template_id)

@router.delete("/templates/{template_id}")
async def remove_template(
    template_id: str,
    _: dict = Depends(verify_admin_dep),
):
    return await delete_template(template_id)
