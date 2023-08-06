"""Define endpoints related to CDC reports."""
# pylint: disable=unused-import
import logging
from copy import deepcopy
from typing import Callable, Coroutine, Dict  # noqa

from aiocache import cached

from .report import Report
from .util import get_nearest_by_coordinates

_LOGGER = logging.getLogger(__name__)

STATUS_MAP = {
    1: 'No Data',
    2: 'Minimal',
    3: 'Low',
    4: 'Moderate',
    5: 'High',
    99: 'None',
}


def adjust_status(info: dict) -> dict:
    """Apply status mapping to a raw API result."""
    modified_info = deepcopy(info)
    modified_info.update({
        'level':
            STATUS_MAP[int(info['level'])],
        'level2':
            STATUS_MAP[int(99 if info['level2'] is None else info['level2'])],
    })

    return modified_info


class CdcReport(Report):
    """Define a single class to handle these endpoints."""

    def __init__(
            self, request: Callable[..., Coroutine],
            get_raw_data: Callable[..., Coroutine],
            cache_seconds: int) -> None:
        """Initialize."""
        super().__init__(request, get_raw_data, cache_seconds)
        self.raw_cdc_data = cached(ttl=self._cache_seconds)(self._raw_cdc_data)

    async def _raw_cdc_data(self) -> dict:
        """Return the raw CDC data."""
        return await self._get_raw_data('map/cdc')

    async def status_by_coordinates(
            self, latitude: float, longitude: float) -> dict:
        """Return the CDC status for the provided latitude/longitude."""
        cdc_data = await self.raw_cdc_data()
        state_data = [
            location for location in await self.raw_state_data()
            if location['name'] != 'United States'
        ]

        closest = get_nearest_by_coordinates(
            state_data, 'lat', 'lon', latitude, longitude)

        return adjust_status(cdc_data[closest['name']])

    async def status_by_state(self, state: str) -> dict:
        """Return the CDC status for the specified state."""
        data = await self.raw_cdc_data()

        try:
            info = next((v for k, v in data.items() if state in k))
        except StopIteration:
            return {}

        return adjust_status(info)
