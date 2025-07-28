from clients.dynamodb import get_post_data
from clients.bitly import get_clicks


async def get_dashboard_data():
    # DynamoDB から投稿データを取得
    posts = get_post_data()

    # 各投稿のクリック数を取得
    total_clicks = sum([await get_clicks(post["bitly_url"]) for post in posts if post.get("bitly_url")])

    # サマリ情報を構築
    summary = {
        "total_posts": len(posts),
        "total_clicks": total_clicks,
        "ctr": round(total_clicks / len(posts) * 100, 2) if posts else 0.0,
        "error_count": 0
    }

    # 最新投稿データとサマリを返す
    return{
        "summary": summary,
        "latest_posts": posts
    }
