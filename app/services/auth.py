import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Optional, Dict, Any
from datetime import datetime
from core.config import settings
from clients.dynamodb import get_dynamodb_resource


def _admins_table():
    dynamo = get_dynamodb_resource()
    return dynamo.Table(settings.ADMINS_TABLE_NAME)


def _to_dt_iso(v) -> str:
    if isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, str):
        return v
    return datetime.utcnow().isoformat()


def _normalize_admin(item: Dict[str, Any]) -> Dict[str, Any]:
    item["created_at"] = _to_dt_iso(item.get("created_at"))
    item["updated_at"] = _to_dt_iso(item.get("updated_at"))
    return item


async def get_admin_by_sub(cognito_sub: str) -> Optional[Dict[str, Any]]:
    table = _admins_table()

    try:
        resp = table.query(
            IndexName="cognito_sub-index",
            KeyConditionExpression=Key("cognito_sub").eq(cognito_sub),
            Limit=1,
        )
        items = resp.get("Items", [])
        if items:
            return _normalize_admin(items[0])
    except Exception:
        resp = table.scan(FilterExpression=Attr("cognito_sub").eq(cognito_sub))
        items = resp.get("Items", [])
        if items:
            return _normalize_admin(items[0])

    return None
