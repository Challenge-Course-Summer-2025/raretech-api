from clients.dynamodb import get_post_data


async def get_metrics() -> dict:
    # DynamoDB/モックから投稿データを取得
    posts = get_post_data()

    # メトリクスを計算
    total_posts = len(posts)
    total_clicks = sum(post.get("clicks_total", 0) for post in posts)
    ctr = round((total_clicks / total_posts * 100), 2) if total_posts else 0.0

    return{
        "total_posts": total_posts,
        "total_clicks": total_clicks,
        "ctr": ctr
    }
