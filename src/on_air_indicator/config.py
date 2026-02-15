from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


CONFIG_PATH = Path.home() / ".config" / "on-air-indicator" / "config.toml"


@dataclass(frozen=True)
class TuyaDeviceConfig:
    name: str
    id: str
    ip: str
    key: str
    version: float = 3.3


@dataclass(frozen=True)
class KasaDeviceConfig:
    name: str
    ip: str


DeviceConfig = TuyaDeviceConfig | KasaDeviceConfig


def load_config(path: Path = CONFIG_PATH) -> list[DeviceConfig]:
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}\n"
            "Copy config.sample.toml to this location and fill in your device details."
        )

    with path.open("rb") as f:
        raw = tomllib.load(f)

    devices_raw = raw.get("devices")
    if not devices_raw:
        raise ValueError("Config file must contain at least one [[devices]] entry.")

    devices: list[DeviceConfig] = []
    for entry in devices_raw:
        device_type = entry.get("type")
        if device_type == "tuya":
            devices.append(
                TuyaDeviceConfig(
                    name=entry["name"],
                    id=entry["id"],
                    ip=entry["ip"],
                    key=entry["key"],
                    version=entry.get("version", 3.3),
                )
            )
        elif device_type == "kasa":
            devices.append(
                KasaDeviceConfig(
                    name=entry["name"],
                    ip=entry["ip"],
                )
            )
        else:
            raise ValueError(f"Unknown device type: {device_type!r}")

    return devices
