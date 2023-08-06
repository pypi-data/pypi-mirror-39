import aiohttp
from types import TracebackType
from typing import Union, Type, Optional
from yarl import URL

from .api import API
from .jobs import (
    Jobs,
    Image,
    JobDescription,
    JobStatus,
    JobStatusHistory,
    NetworkPortForwarding,
    Resources,
    VolumeDescriptionPayload,
)
from .models import Models, TrainResult

__all__ = (
    "Image",
    "JobDescription",
    "JobStatus",
    "JobStatusHistory",
    "NetworkPortForwarding",
    "Resources",
    "VolumeDescriptionPayload",
    "TrainResult",
    "ClientV2",
)

DEFAULT_TIMEOUT = aiohttp.ClientTimeout(None, None, 30, 30)  # type: ignore


class ClientV2:
    def __init__(
        self,
        url: Union[URL, str],
        token: str,
        *,
        timeout: aiohttp.ClientTimeout = DEFAULT_TIMEOUT,  # type: ignore
    ) -> None:
        if isinstance(url, str):
            url = URL(url)
        self._api = API(url, token, timeout)
        self._jobs = Jobs(self._api)
        self._models = Models(self._api)

    async def close(self) -> None:
        await self._api.close()

    async def __aenter__(self) -> "ClientV2":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        await self.close()

    @property
    def jobs(self) -> Jobs:
        return self._jobs

    @property
    def models(self) -> Models:
        return self._models
