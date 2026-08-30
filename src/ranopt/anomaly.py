"""Lightweight statistical anomaly detection for KPI time series."""

from statistics import mean, pstdev
from typing import Sequence


def detect_zscore_anomalies(values: Sequence[float], threshold: float = 3.0) -> list[bool]:
    """Flag observations whose absolute z-score exceeds ``threshold``.

    A robust production version can later replace this baseline with rolling
    statistics, isolation forests, autoencoders, or temporal models.
    """
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    if not values:
        return []
    mu = mean(values)
    sigma = pstdev(values)
    if sigma == 0:
        return [False] * len(values)
    return [abs((float(x) - mu) / sigma) > threshold for x in values]
