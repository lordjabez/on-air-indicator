from __future__ import annotations

import json
import subprocess
from collections.abc import Generator

_CAMERA_PREDICATE = (
    '(subsystem == "com.apple.controlcenter"'
    ' && eventMessage contains "Cameras changed to")'
)


def stream_camera_events() -> Generator[bool, None, None]:
    """Yield True when a camera turns on, False when all cameras turn off."""
    command = (
        "/usr/bin/log",
        "stream",
        "--style",
        "ndjson",
        "--predicate",
        _CAMERA_PREDICATE,
    )
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    assert process.stdout is not None
    for line in iter(process.stdout.readline, b""):
        if not line.startswith(b"{"):
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = entry.get("eventMessage", "")
        camera_off = "appEffects: []" in message
        yield not camera_off
