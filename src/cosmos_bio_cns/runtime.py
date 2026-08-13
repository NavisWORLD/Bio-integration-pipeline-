from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from cosmos_bio_cns.adapters.base import BioAdapter
from cosmos_bio_cns.bridge import EventSink
from cosmos_bio_cns.cns import LocalCNS
from cosmos_bio_cns.fusion import BioFusionEngine
from cosmos_bio_cns.heartbeat import HeartbeatEmitter
from cosmos_bio_cns.models import CNSState, FusionFrame
from cosmos_bio_cns.persistence import SQLiteEventStore


class BioCNSRuntime:
    """One-call integration runtime: adapters -> fusion -> local CNS -> persistence -> heartbeat."""

    def __init__(
        self,
        adapters: Iterable[BioAdapter],
        *,
        cns: LocalCNS | None = None,
        fusion: BioFusionEngine | None = None,
        store: SQLiteEventStore | None = None,
        sink: EventSink | None = None,
        cosmos_id: str = "cosmos-local",
    ) -> None:
        self.adapters = list(adapters)
        self.cns = cns or LocalCNS()
        self.fusion = fusion or BioFusionEngine()
        self.store = store
        self.sink = sink
        self.heartbeat = HeartbeatEmitter(cosmos_id)
        self._started = False

    def start(self) -> None:
        for adapter in self.adapters:
            adapter.connect()
        self._started = True

    def step(self) -> tuple[FusionFrame, CNSState]:
        if not self._started:
            raise RuntimeError("runtime is not started")
        observations = []
        for adapter in self.adapters:
            observations.extend(adapter.read())

        frame = self.fusion.ingest(observations)
        state = self.cns.update(frame)
        payload = {
            "frame": asdict(frame),
            "state": asdict(state),
        }

        if self.store:
            self.store.append("cosmos.bio_cns.state", payload)
        if self.sink:
            self.sink.publish("cosmos.bio_cns.state", payload)

        heartbeat = self.heartbeat.build(state, frame, self.cns.status())
        heartbeat_payload = HeartbeatEmitter.as_payload(heartbeat)
        if self.store:
            self.store.append("cosmos.heartbeat", heartbeat_payload)
        if self.sink:
            self.sink.publish("cosmos.heartbeat", heartbeat_payload)
        return frame, state

    def stop(self) -> None:
        for adapter in self.adapters:
            adapter.disconnect()
        self._started = False
