import os
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from core.config import settings

# テーブル名
POST_SHORTLINKS_TABLE = os.getenv("POST_SHORTLINKS_TABLE_NAME", "PostShortlinks")
SHORTLINK_METRICS_DAILY_TABLE = os.getenv("SHORTLINK_METRICS_DAILY_TABLE_NAME", "ShortlinkMetricsDaily")

# # DynamoDB リソース生成
def _dynamo():
    return boto3.resource(
        "dynamodb",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.DYNAMODB_ENDPOINT or None,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

# PostShortlinks テーブルの Table オブジェクトを返す
def _tbl_shortlinks():
    return _dynamo().Table(POST_SHORTLINKS_TABLE)

# ShortlinkMetricsDaily テーブルの Table オブジェクトを返す
def _tbl_metrics():
    return _dynamo().Table(SHORTLINK_METRICS_DAILY_TABLE)

# 日付や日時、文字列を "YYYY-MM-DD" の文字列形式に変換する
def _to_ymd(v: Optional[str | date | datetime]) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, str):
        return v
    if isinstance(v, datetime):
        return v.date().isoformat()
    if isinstance(v, date):
        return v.isoformat()
    return None

# DynamoDBから全ての短縮リンクを取得し、post_id ごとにまとめて返す
async def list_shortlinks_by_post() -> Dict[str, List[Dict]]:
    table = _tbl_shortlinks()
    items: List[Dict] = []
    start_key = None
    while True:
        if start_key:
            resp = table.scan(ExclusiveStartKey=start_key)
        else:
            resp = table.scan()
        items.extend(resp.get("Items", []))
        start_key = resp.get("LastEvaluatedKey")
        if not start_key:
            break

    by_post: Dict[str, List[Dict]] = {}
    for it in items:
        pid = it.get("post_id")
        if not pid:
            continue
        by_post.setdefault(pid, []).append({
            "short_url": it.get("short_url"),
            "link_type": it.get("link_type"),
        })
    return by_post

async def _sum_clicks_for_shortlink(short_url: str, date_from: Optional[str], date_to: Optional[str]) -> int:
    table = _tbl_metrics()
    date_from = _to_ymd(date_from)
    date_to = _to_ymd(date_to)

    if date_from and date_to:
        resp = table.query(
            KeyConditionExpression=Key("short_url").eq(short_url) & Key("date").between(date_from, date_to),
        )
    elif date_from:
        resp = table.query(
            KeyConditionExpression=Key("short_url").eq(short_url) & Key("date").gte(date_from),
        )
    else:
        resp = table.query(
            KeyConditionExpression=Key("short_url").eq(short_url),
        )

    return sum(int(i.get("clicks", 0)) for i in resp.get("Items", []))

async def build_post_clicks_map(
    date_from: Optional[str | date | datetime] = None,
    date_to: Optional[str | date | datetime] = None,
) -> Dict[str, int]:
    shortlinks_by_post = await list_shortlinks_by_post()
    dfrom = _to_ymd(date_from)
    dto = _to_ymd(date_to)

    result: Dict[str, int] = {}
    for post_id, rows in shortlinks_by_post.items():
        total = 0
        for row in rows:
            su = row.get("short_url")
            if not su:
                continue
            total += await _sum_clicks_for_shortlink(su, dfrom, dto)
        result[post_id] = total
    return result

async def total_clicks_all_posts(
    date_from: Optional[str | date | datetime] = None,
    date_to: Optional[str | date | datetime] = None,
) -> int:
    m = await build_post_clicks_map(date_from=date_from, date_to=date_to)
    return sum(m.values())
