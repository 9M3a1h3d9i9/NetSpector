"""RAN KPI data structures and validation helpers."""

from dataclasses import dataclass
from math import isfinite
from typing import Mapping


@dataclass(frozen=True)
class RANKPIs:
    """Core radio KPIs used by the first RAN analytics prototype.

    Values are intentionally technology-neutral so the same analytics layer can
    later consume LTE/5G measurements from CSV, APIs, or a network simulator.
    """

    rsrp_dbm: float
    rsrq_db: float
    sinr_db: float
    dl_throughput_mbps: float
    ul_throughput_mbps: float
    drop_rate_pct: float
    handover_success_pct: float
    availability_pct: float

    def validate(self) -> None:
        values = self.__dict__
        if not all(isfinite(float(v)) for v in values.values()):
            raise ValueError("All KPI values must be finite numbers")
        bounded = {
            "drop_rate_pct": (0.0, 100.0),
            "handover_success_pct": (0.0, 100.0),
            "availability_pct": (0.0, 100.0),
        }
        for name, (low, high) in bounded.items():
            value = float(getattr(self, name))
            if not low <= value <= high:
                raise ValueError(f"{name} must be between {low} and {high}")


def row_to_kpis(row: Mapping[str, float]) -> RANKPIs:
    """Convert a mapping with canonical KPI names into a validated record."""
    kpis = RANKPIs(**{field: float(row[field]) for field in RANKPIs.__dataclass_fields__})
    kpis.validate()
    return kpis
