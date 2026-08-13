from __future__ import annotations

from dataclasses import asdict
import uuid
from cosmos_bio_cns.models import CNSState, FusionFrame, HeartbeatRecord


class HeartbeatEmitter:
    def __init__(self, cosmos_id: str = "cosmos-local") -> None:
        self.cosmos_id = cosmos_id
        self.boot_id = f"boot-{uuid.uuid4().hex[:12]}"
        self.sequence = 0

    def build(self, state: CNSState, frame: FusionFrame | None, runtime_health: dict[str, bool], *, memory_revision: int = 0, model_revision: str = "local-cns-v1") -> HeartbeatRecord:
        self.sequence += 1
        return HeartbeatRecord(
            cosmos_id=self.cosmos_id,
            boot_id=self.boot_id,
            sequence=self.sequence,
            state=state,
            bio_frame_id=frame.frame_id if frame else None,
            bio_confidence=frame.confidence if frame else 0.0,
            runtime_health=runtime_health,
            memory_revision=memory_revision,
            model_revision=model_revision,
        )

    @staticmethod
    def as_payload(record: HeartbeatRecord) -> dict:
        return asdict(record)
