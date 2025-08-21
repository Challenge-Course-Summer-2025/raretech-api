from __future__ import annotations
from clients.dynamodb import (
    get_templates_data,
    create_template_data,
    update_template_data,
    delete_template_data,
    activate_template_data,
)
from core.x_post_validator import validate_x_post_length, XPostLengthResult


async def get_templates():
    return get_templates_data()


async def create_template(template: dict):
    return create_template_data(template)


async def update_template(template_id: str, template: dict):
    return update_template_data(template_id, template)


async def delete_template(template_id: str):
    return delete_template_data(template_id)


async def activate_template(template_id: str):
    return activate_template_data(template_id)


def render_template(template: str, variables: Optional[Dict[str, Any]] = None) -> str:
    # テンプレート文字列に変数を埋め込み、最終的な投稿文字列を返す
    if not template:
        return ""
    variables = variables or {}
    class _SafeDict(dict):
        def __missing__(self, key):
            return "{" + key + "}"
    return template.format_map(_SafeDict(variables))


def validate_template_for_x_post(template: str, variables: Optional[Dict[str, Any]] = None) -> XPostLengthResult:
    # テンプレートと変数から実際の投稿文面を生成し、X投稿の文字数ルールでバリデーションする
    rendered = render_template(template, variables)
    return validate_x_post_length(rendered)