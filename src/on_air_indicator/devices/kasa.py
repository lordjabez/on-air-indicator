from __future__ import annotations

import asyncio

from kasa import Discover

from on_air_indicator.config import KasaDeviceConfig


class KasaDevice:
    def __init__(self, config: KasaDeviceConfig) -> None:
        self.name = config.name
        self._ip = config.ip
        self._device = asyncio.run(Discover.discover_single(config.ip))

    def turn_on(self) -> None:
        asyncio.run(self._device.turn_on())

    def turn_off(self) -> None:
        asyncio.run(self._device.turn_off())
