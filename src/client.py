from aiohttp import ClientSession, ClientTimeout

import asyncio
from enum import StrEnum
import logging
from typing import Any
from urllib.parse import urljoin as join

from .choices import UserRestrictionType
from .models import APIResponse

log = logging.getLogger(__name__)

API_VERSION: str = "0.1.0"


class RequestType(StrEnum):
    GET = "get"
    POST = "post"


class NetbanClient:
    def __init__(self, host_url: str, auth_token: str, timeout: int = 30):
        self._host_url = host_url
        self._s = ClientSession(
            timeout=ClientTimeout(timeout),
        )
        self._s.headers.update(
            {
                "Netban-Api-Key": auth_token,
                "Netban-Api-Version": API_VERSION,
            },
        )

    def _process_response(self, data: Any) -> APIResponse:
        return APIResponse(**data)

    async def _api_request(
        self,
        url: str,
        r_type: RequestType,
        params: dict | None = None,
        json_body: dict | None = None,
    ) -> APIResponse:
        async with getattr(self._s, r_type.value)(
            url=url,
            params=params,
            json=json_body,
        ) as response:
            data = await response.json()

            return self._process_response(data)

    @property
    def host_url(self) -> str:
        return self._host_url

    async def get_restrictions_for_user(
        self, user: str, group: str | None = None
    ) -> list[dict[str, Any]]:
        url = join(self.host_url, "api/restrictions")
        params = {
            "user": user,
        }

        if group is not None:
            params["group"] = group

        return await self._api_request(
            url=url,
            r_type=RequestType.GET,
            params=params,
        )

    async def restrict_user(
        self,
        user: str,
        restricted_by: str,
        group: str | None = None,
        restriction_type: UserRestrictionType = UserRestrictionType.BAN,
        restriction_reason: str = "",
        restriction_length: str | None = None,
    ) -> dict[str, Any]:
        url = join(self.host_url, "api/restrictions/restrict/")
        json_body = {
            "user": user,
            "restricted_by": restricted_by,
            "restriction_type": restriction_type.value,
            "restriction_reason": restriction_reason,
        }
        if group is not None:
            json_body["group"] = group
        if restriction_length is not None:
            json_body["restriction_length"] = restriction_length

        return await self._api_request(
            url=url,
            r_type=RequestType.POST,
            json_body=json_body,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self._s.close()

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self._s.close())
            else:
                loop.run_until_complete(self._s.close())
        except Exception:
            pass
