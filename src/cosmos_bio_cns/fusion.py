from __future__ import annotations

from collections import defaultdict
from cosmos_bio_cns.baseline import RunningBaseline
from cosmos_bio_cns.models import BioFeature, BioObservation, FusionFrame


class BioFusionEngine:
    """Normalize consented observations and build a quality-gated fusion frame."""

    def __init__(self, *, min_quality: float = 0.5, alpha: float = 0.05, window_ms: int = 1000) -> None:
        self.min_quality = min_quality
        self.alpha = alpha
        self.window_ms = window_ms
        self._baselines: dict[tuple[str, str, str, str], RunningBaseline] = defaultdict(
            lambda: RunningBaseline(alpha=self.alpha)
        )

    def ingest(self, observations: list[BioObservation]) -> FusionFrame:
        features: list[BioFeature] = []
        quality_sum = 0.0
        accepted = 0

        for obs in observations:
            if obs.consent is not None and not obs.consent.bio_processing:
                continue
            if obs.quality < self.min_quality:
                continue

            # Baselines must never blend different sensors or units merely
            # because they happen to reuse the same channel label.
            baseline_key = (obs.subject_id, obs.sensor, obs.channel, obs.unit)
            baseline = self._baselines[baseline_key]
            delta = baseline.update(obs.value)
            features.append(
                BioFeature(
                    channel=obs.channel,
                    name=obs.channel,
                    value=obs.value,
                    quality=obs.quality,
                    baseline_delta=delta,
                    timestamp=obs.timestamp,
                )
            )
            quality_sum += obs.quality
            accepted += 1

        confidence = quality_sum / accepted if accepted else 0.0
        return FusionFrame(features=tuple(features), confidence=confidence, window_ms=self.window_ms)
