class BaseRepository:
    def __init__(self, http: "HttpSessionManager"):
        self.http = http

    async def _get(self, url: str, model_cls, params: dict = None):
        resp = await self.http.get(url, params=params)
        return model_cls(**resp)

    async def _get_json(self, url: str, params: dict = None) -> dict:
        return await self.http.get(url, params=params)
