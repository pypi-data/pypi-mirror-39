"""Define endpoints related to user reports."""
import logging
from typing import Callable, Coroutine

from aiocache import cached

from .report import Report
from .util import get_nearest_by_coordinates

_LOGGER = logging.getLogger(__name__)


class UserReport(Report):
    """Define a single class to handle these endpoints."""

    def __init__(
            self, request: Callable[..., Coroutine],
            get_raw_data: Callable[..., Coroutine],
            cache_seconds: int) -> None:
        """Initialize."""
        super().__init__(request, get_raw_data, cache_seconds)
        self.raw_local_data = cached(ttl=self._cache_seconds)(
            self._raw_local_data)

    async def _raw_local_data(self) -> dict:
        """Return the raw user data."""
        return await self._get_raw_data('map/markers')

    async def status_by_coordinates(
            self, latitude: float, longitude: float) -> dict:
        """Get symptom data for the location nearest to the user's lat/lon."""
        data = {}

        local_data = [
            location for location in await self.raw_local_data()
            if location['latitude'] and location['longitude']
        ]
        data['local'] = get_nearest_by_coordinates(
            local_data, 'latitude', 'longitude', latitude, longitude)

        state_data = [
            location for location in await self.raw_state_data()
            if location['name'] != 'United States'
        ]
        data['state'] = get_nearest_by_coordinates(
            state_data, 'lat', 'lon', latitude, longitude)

        return data

    async def status_by_zip(self, zip_code: str) -> dict:
        """Get symptom data for the provided ZIP code."""
        try:
            location = next((
                d for d in await self.raw_local_data()
                if d['zip'] == zip_code))
        except StopIteration:
            return {}

        return await self.status_by_coordinates(
            float(location['latitude']), float(location['longitude']))
