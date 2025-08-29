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


# DynamoDB に保存済みのクリック・閲覧データを集計（Posts）
def _sum_posts_article_metrics() -> Dict[str, int | float]:
    tbl = _dynamo().Table(settings.POSTS_TABLE_NAME)

    clicks_total = 0
    views_total = 0
    start_key = None
    while True:
        if start_key:
            resp = tbl.scan(
                ExclusiveStartKey=start_key,
                ProjectionExpression="clicks_article, x_views",
            )
        else:
            resp = tbl.scan(
                ProjectionExpression="clicks_article, x_views",
            )

        for item in resp.get("Items", []):
            clicks_total += _to_int(item.get("clicks_article"))
            views_total += _to_int(item.get("x_views"))

        start_key = resp.get("LastEvaluatedKey")
        if not start_key:
            break

    ctr_weighted = round((clicks_total / views_total) * 100, 3) if views_total else 0.0
    return {
        "clicks_article_total": clicks_total,
        "x_views_total": views_total,
        "ctr_article": ctr_weighted,  # 合計から再計算した加重CTR(%)
    }


# DynamoDB に保存済みのクリック・閲覧データを集計（固定リンク = Static_link_clicks）
def _sum_static_metrics() -> Dict[str, int | float]:
    tbl = _dynamo().Table(settings.STATIC_LINK_CLICKS_TABLE_NAME)

    clicks_trial_total = 0
    clicks_counsel_total = 0
    views_total = 0
    start_key = None
    while True:
        if start_key:
            resp = tbl.scan(
                ExclusiveStartKey=start_key,
                ProjectionExpression="clicks_trial_lesson, clicks_counseling, tweet_views",
            )
        else:
            resp = tbl.scan(
                ProjectionExpression="clicks_trial_lesson, clicks_counseling, tweet_views",
            )

        for item in resp.get("Items", []):
            clicks_trial_total += _to_int(item.get("clicks_trial_lesson"))
            clicks_counsel_total += _to_int(item.get("clicks_counseling"))
            views_total += _to_int(item.get("tweet_views"))

        start_key = resp.get("LastEvaluatedKey")
        if not start_key:
            break

    ctr_trial = round((clicks_trial_total / views_total) * 100, 3) if views_total else 0.0
    ctr_counsel = round((clicks_counsel_total / views_total) * 100, 3) if views_total else 0.0

    return {
        "clicks_trial_lesson_total": clicks_trial_total,
        "clicks_counseling_total": clicks_counsel_total,
        "tweet_views_total": views_total,
        "ctr_trial_lesson": ctr_trial,      # 加重CTR(%)
        "ctr_counseling": ctr_counsel,      # 加重CTR(%)
    }


# Article_link_clicksテーブルからpost_idごとの最新clicks_articleを取得
def _get_article_clicks_map() -> Dict[str, int]:
    tbl = _dynamo().Table(settings.ARTICLE_LINK_CLICKS_TABLE_NAME)
    clicks_map = {}
    start_key = None
    while True:
        if start_key:
            resp = tbl.scan(ExclusiveStartKey=start_key)
        else:
            resp = tbl.scan()
        for item in resp.get("Items", []):
            post_id = item.get("post_id")
            clicks_article = _to_int(item.get("clicks_article"))
            # 最新のchecked_atのものを優先（同じpost_idが複数ある場合）
            if post_id:
                if post_id not in clicks_map or item.get("checked_at", "") > clicks_map[post_id]["checked_at"]:
                    clicks_map[post_id] = {
                        "clicks_article": clicks_article,
                        "checked_at": item.get("checked_at", "")
                    }
        start_key = resp.get("LastEvaluatedKey")
        if not start_key:
            break
    # post_id: clicks_article のみに変換
    return {k: v["clicks_article"] for k, v in clicks_map.items()}


async def get_dashboard_data():
    # Posts メタデータのみ取得
    posts = get_post_data()
    total_posts = len(posts)

    # Article_link_clicksからクリック数を取得
    article_clicks_map = _get_article_clicks_map()

    # 各投稿にclicks_articleを付与
    for post in posts:
        post_id = post.get("id") or post.get("post_id")
        post["clicks_article"] = article_clicks_map.get(post_id, 0)

    # 記事リンク集計（Posts）
    article = _sum_posts_article_metrics()

    # 固定リンク集計（Static_link_clicks）
    static = _sum_static_metrics()

    # 総クリック数 = 記事 + 固定
    total_clicks = (
        article["clicks_article_total"]
        + static["clicks_trial_lesson_total"]
        + static["clicks_counseling_total"]
    )

    summary = {
        "total_posts": total_posts,
        "total_clicks": total_clicks,
        "article": {
            "clicks": article["clicks_article_total"],
            "x_views": article["x_views_total"],
            "ctr": article["ctr_article"],
        },
        "static_links": {
            "clicks_trial_lesson": static["clicks_trial_lesson_total"],
            "clicks_counseling_total": static["clicks_counseling_total"],
            "tweet_views": static["tweet_views_total"],
            "ctr_trial_lesson": static["ctr_trial_lesson"],
            "ctr_counseling": static["ctr_counseling"],
        },
        "error_count": 0,
    }

    return {
        "summary": summary,
        "latest_posts": posts,
    }
