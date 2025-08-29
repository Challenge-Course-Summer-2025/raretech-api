from __future__ import annotations
from decimal import Decimal
from typing import Dict
from core.config import settings
from clients.dynamodb import get_dynamodb_resource, get_post_data
from .dashboard import _get_article_clicks_map, _sum_static_metrics


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

    # 記事リンク（Article_link_clicks）
    article_clicks_map = _get_article_clicks_map()
    clicks_article_total = sum(article_clicks_map.values())

    # 固定リンク（Static_link_clicks）
    static = _sum_static_metrics()

    # CTR（記事はビュー数が無いので 0 扱い、必要なら _sum_posts_article_metrics を呼ぶ）
    ctr_article = 0.0

    total_clicks = (
        clicks_article_total
        + static["clicks_trial_lesson_total"]
        + static["clicks_counseling_total"]
    )

    return {
        "total_posts": total_posts,
        "total_clicks": total_clicks,
        "article": {
            "clicks": clicks_article_total,
            "x_views": 0,
            "ctr": ctr_article,
        },
        "static_links": {
            "clicks_trial_lesson": static["clicks_trial_lesson_total"],
            "clicks_counseling":  static["clicks_counseling_total"],
            "tweet_views":        static["tweet_views_total"],
            "ctr_trial_lesson":   static["ctr_trial_lesson"],
            "ctr_counseling":     static["ctr_counseling"],
        },
    }
