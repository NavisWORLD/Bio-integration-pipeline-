from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Sequence

PHASE_STEP = 0.61803398875
DEFAULT_DIMENSIONS = 12
DEFAULT_LEAK = 0.88
DEFAULT_INPUT_GAIN = 0.12


@dataclass(frozen=True)
class SynapticFeature:
    """Language-neutral feature used by the deterministic synaptic kernel."""

    baseline_delta: float
    quality: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.baseline_delta):
            raise ValueError("baseline_delta must be finite")
        if not math.isfinite(self.quality) or not 0.0 <= self.quality <= 1.0:
            raise ValueError("quality must be finite and in [0,1]")


def _coerce_feature(feature: SynapticFeature | tuple[float, float]) -> SynapticFeature:
    if isinstance(feature, SynapticFeature):
        return feature
    baseline_delta, quality = feature
    return SynapticFeature(float(baseline_delta), float(quality))


def synaptic_step(
    previous_state: Sequence[float],
    features: Iterable[SynapticFeature | tuple[float, float]],
    *,
    leak: float = DEFAULT_LEAK,
    input_gain: float = DEFAULT_INPUT_GAIN,
) -> tuple[float, ...]:
    """Run one deterministic COSMOS synaptic state transition.

    This is an engineering interoperability primitive. It is not a medical,
    diagnostic, biological, or consciousness model.
    """

    if not previous_state:
        raise ValueError("previous_state must not be empty")
    if not math.isfinite(leak) or not 0.0 <= leak < 1.0:
        raise ValueError("leak must be finite and in [0,1)")
    if not math.isfinite(input_gain) or input_gain < 0.0:
        raise ValueError("input_gain must be finite and non-negative")

    state = tuple(float(value) for value in previous_state)
    if not all(math.isfinite(value) for value in state):
        raise ValueError("previous_state values must be finite")

    normalized = tuple(_coerce_feature(feature) for feature in features)
    if not normalized:
        return state

    inputs = tuple(math.tanh(feature.baseline_delta) * feature.quality for feature in normalized)
    next_state: list[float] = []
    for i, previous in enumerate(state):
        source = inputs[i % len(inputs)]
        phase = math.sin((i + 1) * PHASE_STEP)
        value = leak * previous + input_gain * source * phase
        next_state.append(max(-1.0, min(1.0, value)))
    return tuple(next_state)


def cosmos_12d_step(
    previous_state: Sequence[float],
    features: Iterable[SynapticFeature | tuple[float, float]],
) -> tuple[float, ...]:
    if len(previous_state) != DEFAULT_DIMENSIONS:
        raise ValueError("cosmos_12d_step requires exactly 12 state values")
    return synaptic_step(previous_state, features)
