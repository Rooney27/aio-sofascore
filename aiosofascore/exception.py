from aiohttp import ClientResponse

__all__ = ["ResponseParseContentError"]


class ResponseParseContentError(Exception):
    def __init__(self, response: ClientResponse, path: str):
        self._response = response
        self._path = path

    @property
    def response(self):
        return self._response

    def __str__(self):
        return (
            f"Response processing error:\n"
            f"Api call: {self._response.url}\n"
            f"Headers request: {self._response.request_info}\n"
            f"Response status: {self._response.status}\n"
            f"Response: <async - use `await e.async_str()` to see body>\n"
        )

    async def async_str(self) -> str:
        try:
            json_body = await self._response.json()
        except Exception as e:
            json_body = f"<failed to parse JSON: {e}>"

        return (
            f"Response processing error:\n"
            f"Api call: {self._path}\n"
            f"Response status: {self._response.status}\n"
            f"Response: {json_body}\n"
        )
