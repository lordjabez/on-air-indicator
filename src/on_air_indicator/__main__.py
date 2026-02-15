from __future__ import annotations

import logging
import sys

from on_air_indicator.config import load_config
from on_air_indicator.devices import Device, create_device
from on_air_indicator.log_stream import stream_camera_events

logger = logging.getLogger("on_air_indicator")


def _toggle_devices(devices: list[Device], *, on: bool) -> None:
    action = "on" if on else "off"
    for device in devices:
        try:
            if on:
                device.turn_on()
            else:
                device.turn_off()
            logger.info("Turned %s: %s", action, device.name)
        except Exception:
            logger.exception("Failed to turn %s: %s", action, device.name)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )

    try:
        device_configs = load_config()
    except (FileNotFoundError, ValueError) as exc:
        logger.error("%s", exc)
        sys.exit(1)

    devices = []
    for config in device_configs:
        try:
            device = create_device(config)
            devices.append(device)
            logger.info("Initialized device: %s", config.name)
        except Exception:
            logger.exception("Failed to initialize device: %s", config.name)

    if not devices:
        logger.error("No devices initialized, exiting.")
        sys.exit(1)

    logger.info("Streaming camera events...")
    for camera_on in stream_camera_events():
        _toggle_devices(devices, on=camera_on)


if __name__ == "__main__":
    main()
