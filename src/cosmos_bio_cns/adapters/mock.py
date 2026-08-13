from __future__ import annotations

import math
from cosmos_bio_cns.models import BioObservation


class DeterministicCardiacAdapter:
    """No-hardware adapter for demos/tests. Produces deterministic heart-rate observations."""

    name = "deterministic-cardiac"

    def __init__(self, subject_id: str = "demo", device_id: str = "mock-heart") -> None:
        self.subject_id = subject_id
        self.device_id = device_id
        self._sequence = 0
        self._connected = False

    def connect(self) -> None:
        self._connected = True

    def read(self) -> list[BioObservation]:
        if not self._connected:
            raise RuntimeError("adapter is not connected")
        self._sequence += 1
        bpm = 72.0 + 4.0 * math.sin(self._sequence / 6.0)
        return [
            BioObservation(
                sensor="cardiac",
                channel="heart_rate",
                value=bpm,
                unit="bpm",
                quality=0.98,
                sequence=self._sequence,
                subject_id=self.subject_id,
                device_id=self.device_id,
            )
        ]

    def disconnect(self) -> None:
        self._connected = False
