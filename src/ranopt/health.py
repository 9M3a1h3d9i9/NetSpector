"""Explainable health scoring for radio cells."""

from typing import Mapping


DEFAULT_WEIGHTS = {
    "rsrp_dbm": 0.15,
    "rsrq_db": 0.10,
    "sinr_db": 0.10,
    "dl_throughput_mbps": 0.15,
    "ul_throughput_mbps": 0.05,
    "drop_rate_pct": 0.15,
    "handover_success_pct": 0.15,
    "availability_pct": 0.15,
}


def _clip(value: float) -> float:
    return max(0.0, min(1.0, value))


def _normalize(name: str, value: float) -> float:
    """Map a KPI to a simple 0..1 health contribution.

    These are engineering defaults for a prototype, not operator-specific
    thresholds. Production deployment should load thresholds from configuration.
    """
    ranges = {
        "rsrp_dbm": (-120.0, -70.0, True),
        "rsrq_db": (-20.0, -3.0, True),
        "sinr_db": (-5.0, 30.0, True),
        "dl_throughput_mbps": (0.0, 200.0, True),
        "ul_throughput_mbps": (0.0, 80.0, True),
        "drop_rate_pct": (0.0, 10.0, False),
        "handover_success_pct": (80.0, 100.0, True),
        "availability_pct": (95.0, 100.0, True),
    }
    low, high, higher_is_better = ranges[name]
    x = _clip((value - low) / (high - low))
    return x if higher_is_better else 1.0 - x


def compute_health_score(kpis: Mapping[str, float], weights: Mapping[str, float] | None = None) -> float:
    """Return an interpretable 0..100 cell-health score."""
    weights = dict(weights or DEFAULT_WEIGHTS)
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("Weights must sum to a positive value")
    missing = set(weights) - set(kpis)
    if missing:
        raise KeyError(f"Missing KPI(s): {sorted(missing)}")
    score = sum(_normalize(name, float(kpis[name])) * weight for name, weight in weights.items())
    return round(100.0 * score / total_weight, 2)
