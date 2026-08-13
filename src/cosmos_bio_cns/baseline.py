from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass
class RunningBaseline:
    """EWMA mean/variance tracker for person-relative normalization."""

    alpha: float = 0.05
    epsilon: float = 1e-8
    mean: float | None = None
    variance: float = 0.0
    count: int = 0

    def update(self, value: float) -> float:
        if not 0.0 < self.alpha <= 1.0:
            raise ValueError("alpha must be in (0, 1]")
        if self.mean is None:
            self.mean = value
            self.variance = 0.0
            self.count = 1
            return 0.0

        previous_mean = self.mean
        self.mean = (1.0 - self.alpha) * self.mean + self.alpha * value
        residual = value - previous_mean
        self.variance = (1.0 - self.alpha) * self.variance + self.alpha * residual * residual
        self.count += 1
        return self.z_score(value)

    def z_score(self, value: float) -> float:
        if self.mean is None or self.count < 2:
            return 0.0
        return (value - self.mean) / max(math.sqrt(self.variance), self.epsilon)
