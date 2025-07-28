import httpx
from core.config import settings


async def get_clicks(bitlink: str) -> int:
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    headers = {"Authorization": f"Bearer {settings.BITLY_API_TOKEN}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json().get("total_clicks", 0)
