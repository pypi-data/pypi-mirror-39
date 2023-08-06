"""Define a generic report object."""
from typing import Callable, Coroutine

from aiocache import cached


class Report:  # pylint: disable=too-few-public-methods
    """Define a generic report object."""

    def __init__(
            self, request: Callable[..., Coroutine],
            get_raw_data: Callable[..., Coroutine],
            cache_seconds: int) -> None:
        """Initialize."""
        self._cache_seconds = cache_seconds
        self._get_raw_data = get_raw_data
        self._request = request

        self.raw_state_data = cached(
            ttl=self._cache_seconds, key='state_data')(
                self._raw_state_data)

    async def _raw_state_data(self) -> dict:
        """Return the raw state data."""
        return await self._get_raw_data('states')
