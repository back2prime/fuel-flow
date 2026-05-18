import httpx

from core import settings
from core.constants import HTTP_URL

from fastapi import HTTPException
from starlette import status

class HttpHelper:
    """Async HTTP client helper for making API requests.

    Manages a single httpx.AsyncClient instance for the lifetime of the application.
    """
    def __init__(self, url: str, apikey: str):
        self._url = url
        self._apikey = apikey
        self._client = httpx.AsyncClient()

    async def get_response(self, params: dict, api_method: str):
        params["apikey"] = self._apikey
        try:
            response = await self._client.get(self._url + api_method, params=params)
            return response.json()
        except httpx.ReadTimeout:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="API timeout")
        except httpx.RequestError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="API unavailable")
    async def close(self):
        await self._client.aclose()


http_helper = HttpHelper(url=HTTP_URL, apikey=settings.API_KEY)
