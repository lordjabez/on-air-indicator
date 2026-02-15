from __future__ import annotations

import tinytuya

from on_air_indicator.config import TuyaDeviceConfig


class TuyaDevice:
    def __init__(self, config: TuyaDeviceConfig) -> None:
        self.name = config.name
        self._device = tinytuya.OutletDevice(config.id, config.ip, config.key)
        self._device.set_version(config.version)

    def turn_on(self) -> None:
        self._device.turn_on()

    def turn_off(self) -> None:
        self._device.turn_off()
