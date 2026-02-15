from __future__ import annotations

from on_air_indicator.config import DeviceConfig, KasaDeviceConfig, TuyaDeviceConfig
from on_air_indicator.devices.base import Device
from on_air_indicator.devices.kasa import KasaDevice
from on_air_indicator.devices.tuya import TuyaDevice


def create_device(config: DeviceConfig) -> Device:
    if isinstance(config, TuyaDeviceConfig):
        return TuyaDevice(config)
    if isinstance(config, KasaDeviceConfig):
        return KasaDevice(config)
    raise ValueError(f"Unknown device config type: {type(config)!r}")


__all__ = ["Device", "create_device"]
