from typing import Any

__all__ = ["ResponseParseContentError"]


class ResponseParseContentError(Exception):
    def __init__(self, response: Any, path: str):
        self._response = response
        self._path = path

    @property
    def response(self):
        return self._response

    @property
    def status(self) -> int:
        if hasattr(self._response, "status_code"):
            return int(self._response.status_code)
        return int(self._response.status)

    def __str__(self):
        return (
            f"Response processing error:\n"
            f"Api call: {self._path}\n"
            f"Response status: {self.status}\n"
            f"Response: <use `await e.async_str()` to see body>\n"
        )

    async def async_str(self) -> str:
        try:
            json_body = await _response_body(self._response)
        except Exception as exc:
            json_body = f"<failed to parse body: {exc}>"

        return (
            f"Response processing error:\n"
            f"Api call: {self._path}\n"
            f"Response status: {self.status}\n"
            f"Response: {json_body}\n"
        )


async def _response_body(response: Any) -> Any:
    if hasattr(response, "json"):
        try:
            body = response.json()
        except TypeError:
            body = await response.json()
        else:
            if hasattr(body, "__await__"):
                body = await body
        return body
    if hasattr(response, "text"):
        text = response.text
        if hasattr(text, "__await__"):
            text = await text
        return text
    return str(response)
