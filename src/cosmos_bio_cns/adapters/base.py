from __future__ import annotations

from typing import Protocol, runtime_checkable
from cosmos_bio_cns.models import BioObservation


@runtime_checkable
class BioAdapter(Protocol):
    """Minimal contract for wearable, phone, camera, microphone, or synthetic adapters."""

    name: str

    def connect(self) -> None: ...
    def read(self) -> list[BioObservation]: ...
    def disconnect(self) -> None: ...
