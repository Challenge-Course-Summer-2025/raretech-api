from __future__ import annotations
from decimal import Decimal
from typing import Dict
from core.config import settings
from clients.dynamodb import get_dynamodb_resource, get_post_data

def _dynamo():
    return get_dynamodb_resource()

def _to_int(v) -> int:
    if isinstance(v, Decimal):
        return int(v)
    if isinstance(v, (int, float)):
        return int(v)
    return 0

async def get_metrics() -> dict:
    # 投稿件数
    posts = get_post_data()
    total_posts = len(posts)

    # 記事リンク（Posts）
    tbl_posts = _dynamo().Table(settings.POSTS_TABLE_NAME)
    clicks_article_total = 0
    x_views_total = 0
    start_key = None
    while True:
        if start_key:
            resp = tbl_posts.scan(
                ExclusiveStartKey=start_key,
                ProjectionExpression="clicks_article, x_views",
            )
        else:
            resp = tbl_posts.scan(
                ProjectionExpression="clicks_article, x_views",
            )
        for item in resp.get("Items", []):
            clicks_article_total += _to_int(item.get("clicks_article"))
            x_views_total       += _to_int(item.get("x_views"))
        start_key = resp.get("LastEvaluatedKey")
        if not start_key:
            break

    ctr_article = round((clicks_article_total / x_views_total) * 100, 3) if x_views_total else 0.0

    # 固定リンク（Static_link_clicks）
    tbl_static = _dynamo().Table(settings.STATIC_LINK_CLICKS_TABLE_NAME)
    clicks_trial_total  = 0
    clicks_counsel_total = 0
    static_views_total  = 0
    start_key = None
    while True:
        if start_key:
            resp = tbl_static.scan(
                ExclusiveStartKey=start_key,
                ProjectionExpression="clicks_trial_lesson, clicks_counseling, tweet_views",
            )
        else:
            resp = tbl_static.scan(
                ProjectionExpression="clicks_trial_lesson, clicks_counseling, tweet_views",
            )
        for item in resp.get("Items", []):
            clicks_trial_total   += _to_int(item.get("clicks_trial_lesson"))
            clicks_counsel_total += _to_int(item.get("clicks_counseling"))
            static_views_total   += _to_int(item.get("tweet_views"))
        start_key = resp.get("LastEvaluatedKey")
        if not start_key:
            break

    ctr_trial  = round((clicks_trial_total / static_views_total) * 100, 3) if static_views_total else 0.0
    ctr_counsel = round((clicks_counsel_total / static_views_total) * 100, 3) if static_views_total else 0.0

    total_clicks = clicks_article_total + clicks_trial_total + clicks_counsel_total

    return {
        "total_posts": total_posts,
        "total_clicks": total_clicks,
        "article": {
            "clicks": clicks_article_total,
            "x_views": x_views_total,
            "ctr": ctr_article,
        },
        "static_links": {
            "clicks_trial_lesson": clicks_trial_total,
            "clicks_counseling":  clicks_counsel_total,
            "tweet_views":        static_views_total,
            "ctr_trial_lesson":   ctr_trial,
            "ctr_counseling":     ctr_counsel,
        },
    }
