from __future__ import annotations

from typing import Protocol


class Device(Protocol):
    name: str

    def turn_on(self) -> None: ...
    def turn_off(self) -> None: ...
