"""Synthetic RAN KPI generation for local development and CI."""

from __future__ import annotations

import random


def generate_cells(n: int = 20, seed: int = 42) -> list[dict[str, float | str]]:
    """Generate deterministic, plausible KPI rows without real operator data."""
    if n <= 0:
        raise ValueError("n must be positive")
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        degraded = i % 7 == 0
        row = {
            "cell_id": f"CELL-{i+1:03d}",
            "rsrp_dbm": rng.uniform(-112, -75) - (8 if degraded else 0),
            "rsrq_db": rng.uniform(-17, -5) - (3 if degraded else 0),
            "sinr_db": rng.uniform(0, 25) - (5 if degraded else 0),
            "dl_throughput_mbps": rng.uniform(20, 180) * (0.45 if degraded else 1),
            "ul_throughput_mbps": rng.uniform(5, 60) * (0.55 if degraded else 1),
            "drop_rate_pct": rng.uniform(0.1, 2.0) + (4 if degraded else 0),
            "handover_success_pct": rng.uniform(94, 99.9) - (5 if degraded else 0),
            "availability_pct": rng.uniform(98.5, 100) - (2 if degraded else 0),
        }
        rows.append(row)
    return rows
