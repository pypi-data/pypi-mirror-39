"""Define a client to interact with Flu Near You."""
# pylint: disable=unused-import
import logging
from typing import Union  # noqa

from aiohttp import ClientSession, client_exceptions

from .cdc import CdcReport
from .const import DEFAULT_CACHE_SECONDS
from .errors import RequestError
from .user import UserReport

_LOGGER = logging.getLogger(__name__)

API_URL_SCAFFOLD = 'https://api.v2.flunearyou.org'

DEFAULT_HOST = 'api.v2.flunearyou.org'
DEFAULT_ORIGIN = 'https://flunearyou.org'
DEFAULT_REFERER = 'https://flunearyou.org/'
DEFAULT_USER_AGENT = 'Home Assistant (Macintosh; OS X/10.14.0) GCDHTTPRequest'


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class Client:
    """Define the client."""

    def __init__(
            self,
            websession: ClientSession,
            *,
            cache_seconds: int = DEFAULT_CACHE_SECONDS) -> None:
        """Initialize."""
        self._cache_seconds = cache_seconds
        self._websession = websession
        self.cdc_reports = CdcReport(
            self._request, self._raw_data, cache_seconds)
        self.user_reports = UserReport(
            self._request, self._raw_data, cache_seconds)

    async def _raw_data(self, endpoint: str) -> dict:
        """Return raw data from an endpoint."""
        resp = await self._request('get', endpoint)
        _LOGGER.debug('Response for "%s": %s', endpoint, resp)
        return resp

    async def _request(
            self, method: str, endpoint: str, *, headers: dict = None) -> dict:
        """Make a request against air-matters.com."""
        url = '{0}/{1}'.format(API_URL_SCAFFOLD, endpoint)

        if not headers:
            headers = {}
        headers.update({
            'Host': DEFAULT_HOST,
            'Origin': DEFAULT_ORIGIN,
            'Referer': DEFAULT_REFERER,
            'User-Agent': DEFAULT_USER_AGENT,
        })

        async with self._websession.request(
                method,
                url,
                headers=headers,
        ) as resp:
            try:
                resp.raise_for_status()
                return await resp.json(content_type=None)
            except client_exceptions.ClientError as err:
                raise RequestError(
                    'Error requesting data from {0}: {1}'.format(
                        endpoint, err)) from None
