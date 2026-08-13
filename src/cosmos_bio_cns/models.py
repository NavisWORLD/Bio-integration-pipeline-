from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ConsentScope:
    session_id: str
    bio_processing: bool = True
    raw_retention: bool = False


@dataclass(frozen=True)
class BioObservation:
    sensor: str
    channel: str
    value: float
    unit: str
    quality: float
    timestamp: str = field(default_factory=utc_now_iso)
    sequence: int = 0
    subject_id: str = "anonymous"
    device_id: str = "local"
    metadata: Mapping[str, Any] = field(default_factory=dict)
    consent: ConsentScope | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.quality <= 1.0:
            raise ValueError("quality must be between 0 and 1")


@dataclass(frozen=True)
class BioFeature:
    channel: str
    name: str
    value: float
    quality: float
    baseline_delta: float = 0.0
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True)
class FusionFrame:
    features: tuple[BioFeature, ...]
    confidence: float
    window_ms: int
    frame_id: str = field(default_factory=lambda: f"bf-{uuid.uuid4().hex[:12]}")
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True)
class CNSState:
    vector: tuple[float, ...]
    dimensions: int = 12
    revision: int = 0
    confidence: float = 0.0
    timestamp: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if len(self.vector) != self.dimensions:
            raise ValueError("vector length must equal dimensions")


@dataclass(frozen=True)
class HeartbeatRecord:
    cosmos_id: str
    boot_id: str
    sequence: int
    state: CNSState
    bio_frame_id: str | None
    bio_confidence: float
    runtime_health: Mapping[str, bool]
    memory_revision: int = 0
    model_revision: str = "local-cns-v1"
    timestamp: str = field(default_factory=utc_now_iso)
    schema: str = "cosmos.heartbeat.v1"


def to_json(value: Any, *, indent: int | None = None) -> str:
    return json.dumps(asdict(value), indent=indent, sort_keys=True, separators=None if indent else (",", ":"))
