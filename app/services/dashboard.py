from clients.dynamodb import get_post_data
from services.shortlinks import total_clicks_all_posts

async def get_dashboard_data():
    # Posts　メタデータ のみを取得
    posts = get_post_data()

    # クリック総数は ShortlinkMetricsDaily から集計
    total_clicks = await total_clicks_all_posts()

    # CTR
    summary = {
        "total_posts": len(posts),
        "total_clicks": total_clicks,
        "ctr": round(total_clicks / len(posts) * 100, 2) if posts else 0.0,
        "error_count": 0,
    }

    return {
        "summary": summary,
        "latest_posts": posts,
    }
