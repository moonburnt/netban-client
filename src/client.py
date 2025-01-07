import logging

from typing import Any
from urllib.parse import urljoin as join

from aiohttp import ClientSession, ClientTimeout

from .errors import AuthorizationError
from .choices import UserRestrictionType

log = logging.getLogger(__name__)

API_VERSION: str = "0.1.0"


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

        async with self._s.get(
            url=url,
            params=params,
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data

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

        async with self._s.post(
            url=url,
            json=json_body,
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data
