from __future__ import annotations

from collections import deque
from threading import Lock
from cosmos_bio_cns.models import BioObservation


class PushBioAdapter:
    """Thread-safe adapter for host applications that push already-acquired observations.

    Useful for mobile/native/web bridges: the host owns device permissions and acquisition;
    this adapter only accepts neutral BioObservation objects and drains them into the CNS loop.
    """

    name = "push"

    def __init__(self) -> None:
        self._queue: deque[BioObservation] = deque()
        self._lock = Lock()
        self._connected = False

    def connect(self) -> None:
        self._connected = True

    def push(self, observation: BioObservation) -> None:
        if not self._connected:
            raise RuntimeError("adapter is not connected")
        with self._lock:
            self._queue.append(observation)

    def extend(self, observations: list[BioObservation]) -> None:
        if not self._connected:
            raise RuntimeError("adapter is not connected")
        with self._lock:
            self._queue.extend(observations)

    def read(self) -> list[BioObservation]:
        if not self._connected:
            raise RuntimeError("adapter is not connected")
        with self._lock:
            items = list(self._queue)
            self._queue.clear()
        return items

    def disconnect(self) -> None:
        with self._lock:
            self._queue.clear()
        self._connected = False
