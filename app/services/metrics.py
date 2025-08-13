from clients.dynamodb import get_post_data
from services.shortlinks import build_post_clicks_map

async def get_metrics() -> dict:
    posts = get_post_data()
    total_posts = len(posts)

    # post_id -> clicks のマップを日次集計から作成
    post_clicks_map = await build_post_clicks_map()
    total_clicks = sum(post_clicks_map.values())

    ctr = round((total_clicks / total_posts * 100), 2) if total_posts else 0.0

    return {
        "total_posts": total_posts,
        "total_clicks": total_clicks,
        "ctr": ctr,
    }
