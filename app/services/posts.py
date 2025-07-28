from clients.dynamodb import get_post_data

async def get_posts(page: int, limit: int, search: str = None):
    # DynamoDB から全投稿を取得
    posts = get_post_data()

    # 検索条件があればフィルタリング
    if search:
        posts = [p for p in posts if search.lower() in p["title"].lower()]

    # ページング処理
    start = (page - 1) * limit
    end = start + limit
    paginated_posts = posts[start:end]

    return{
        "page": page,
        "limit": limit,
        "total": len(posts),
        "posts": paginated_posts
    }
