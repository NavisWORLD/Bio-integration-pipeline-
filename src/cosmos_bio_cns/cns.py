from __future__ import annotations

from dataclasses import dataclass, field
import math
from cosmos_bio_cns.models import CNSState, FusionFrame


@dataclass
class OrganStatus:
    quantum: bool = False
    dark_matter: bool = True
    emeth: bool = True
    plasticity: bool = True
    awareness: bool = True
    daemons: bool = False
    surgeon: bool = True


@dataclass
class LocalCNS:
    """Small deterministic 12D state engine for embedding the bio/CNS loop in other projects.

    This is an interoperability reference implementation, not a medical or consciousness model.
    """

    dimensions: int = 12
    leak: float = 0.88
    input_gain: float = 0.12
    state: tuple[float, ...] = field(default_factory=lambda: (0.0,) * 12)
    revision: int = 0
    organs: OrganStatus = field(default_factory=OrganStatus)

    def __post_init__(self) -> None:
        if self.dimensions <= 0:
            raise ValueError("dimensions must be positive")
        if len(self.state) != self.dimensions:
            self.state = (0.0,) * self.dimensions
        if not 0.0 <= self.leak < 1.0:
            raise ValueError("leak must be in [0,1)")

    def update(self, frame: FusionFrame) -> CNSState:
        if not frame.features:
            self.revision += 1
            return CNSState(
                vector=self.state,
                dimensions=self.dimensions,
                revision=self.revision,
                confidence=0.0,
            )

        inputs = [math.tanh(f.baseline_delta) * f.quality for f in frame.features]
        new_state: list[float] = []
        for i in range(self.dimensions):
            source = inputs[i % len(inputs)]
            phase = math.sin((i + 1) * 0.61803398875)
            drive = source * phase
            value = self.leak * self.state[i] + self.input_gain * drive
            new_state.append(max(-1.0, min(1.0, value)))

        self.state = tuple(new_state)
        self.revision += 1
        return CNSState(
            vector=self.state,
            dimensions=self.dimensions,
            revision=self.revision,
            confidence=frame.confidence,
        )

    def status(self) -> dict[str, bool]:
        return {
            "cns": True,
            "quantum": self.organs.quantum,
            "dark_matter": self.organs.dark_matter,
            "emeth": self.organs.emeth,
            "plasticity": self.organs.plasticity,
            "awareness": self.organs.awareness,
            "daemons": self.organs.daemons,
            "surgeon": self.organs.surgeon,
        }
