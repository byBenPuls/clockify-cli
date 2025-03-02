from __future__ import annotations

from httpx import Client


class ClockifyMethod:
    def __init__(self, http_client: ClockifyHttpClient) -> None:
        self._client = http_client


class ClockifyHttpClient(Client):
    def __init__(self, token: str, *args, **kwargs):
        base_url = "https://api.clockify.me/api/v1/"
        header_auth = {"x-api-key": token}

        super().__init__(*args, base_url=base_url, headers=header_auth, **kwargs)


class Clockify:
    def __init__(self, token: str) -> None:
        self._client = ClockifyHttpClient(token)

    @property
    def http(self) -> Client:
        return self._client
