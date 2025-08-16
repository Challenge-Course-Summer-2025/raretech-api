from decimal import Decimal
import os
import boto3
from core.config import settings
from clients.dynamodb import get_post_data

# テーブル名
ARTICLE_LINK_CLICKS_TABLE = os.getenv("ARTICLE_LINK_CLICKS_TABLE_NAME", "Article_link_clicks")
STATIC_LINK_CLICKS_TABLE = os.getenv("STATIC_LINK_CLICKS_TABLE_NAME", "Static_link_clicks")


def _dynamo():
    return boto3.resource(
        "dynamodb",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.DYNAMODB_ENDPOINT or None,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def _to_int(v) -> int:
    if isinstance(v, Decimal):
        return int(v)
    if isinstance(v, (int, float)):
        return int(v)
    return 0


def _sum_article_metrics() -> dict:
    # Article_link_clicks から記事リンク用の合計メトリクスを算出
    tbl = _dynamo().Table(ARTICLE_LINK_CLICKS_TABLE)
    clicks_article_total = 0
    tweet_views_total = 0
    start_key = None
    while True:
        if start_key:
            resp = tbl.scan(
                ExclusiveStartKey=start_key,
                ProjectionExpression="clicks_article, tweet_views",
            )
        else:
            resp = tbl.scan(
                ProjectionExpression="clicks_article, tweet_views",
            )
        for item in resp.get("Items", []):
            clicks_article_total += _to_int(item.get("clicks_article"))
            tweet_views_total += _to_int(item.get("tweet_views"))
        start_key = resp.get("LastEvaluatedKey")
        if not start_key:
            break

    ctr_article = round((clicks_article_total / tweet_views_total) * 100, 2) if tweet_views_total else 0.0
    return {
        "clicks_article_total": clicks_article_total,
        "tweet_views_total": tweet_views_total,
        "ctr_article": ctr_article,
    }


def _sum_static_metrics() -> dict:
    # Static_link_clicks から固定リンク(体験授業/カウンセリング)の合計メトリクスを算出
    tbl = _dynamo().Table(STATIC_LINK_CLICKS_TABLE)
    clicks_trial_lesson_total = 0
    clicks_counseling_total = 0
    tweet_views_total = 0
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
            clicks_trial_lesson_total += _to_int(item.get("clicks_trial_lesson"))
            clicks_counseling_total += _to_int(item.get("clicks_counseling"))
            tweet_views_total += _to_int(item.get("tweet_views"))
        start_key = resp.get("LastEvaluatedKey")
        if not start_key:
            break

    ctr_trial = round((clicks_trial_lesson_total / tweet_views_total) * 100, 2) if tweet_views_total else 0.0
    ctr_counsel = round((clicks_counseling_total / tweet_views_total) * 100, 2) if tweet_views_total else 0.0

    return {
        "clicks_trial_lesson_total": clicks_trial_lesson_total,
        "clicks_counseling_total": clicks_counseling_total,
        "tweet_views_total": tweet_views_total,
        "ctr_trial_lesson": ctr_trial,
        "ctr_counseling": ctr_counsel,
    }

async def get_dashboard_data():
    # Posts　メタデータ のみを取得
    posts = get_post_data()
    total_posts = len(posts)

    # 記事リンクの集計
    article = _sum_article_metrics()

    # 固定リンク(体験授業/カウンセリング)の集計
    static = _sum_static_metrics()

    # 総クリック数 = 記事リンク + 固定リンク
    total_clicks = (
        article["clicks_article_total"]
        + static["clicks_trial_lesson_total"]
        + static["clicks_counseling_total"]
    )

    # CTR
    summary = {
        "total_posts": total_posts,
        "total_clicks": total_clicks,
        # 主要KPIを明示的に分けて返す
        "article": {
            "clicks": article["clicks_article_total"],
            "tweet_views": article["tweet_views_total"],
            "ctr": article["ctr_article"],  # 記事リンクのCTR
        },
        "static_links": {
            "clicks_trial_lesson": static["clicks_trial_lesson_total"],
            "clicks_counseling": static["clicks_counseling_total"],
            "tweet_views": static["tweet_views_total"],
            "ctr_trial_lesson": static["ctr_trial_lesson"],  # 体験授業のCTR
            "ctr_counseling": static["ctr_counseling"],      # カウンセリングのCTR
        },
        "error_count": 0,
    }

    return {
        "summary": summary,
        "latest_posts": posts,
    }
