"""Run the RAN analytics foundation on deterministic synthetic cells."""

from ranopt.health import compute_health_score
from ranopt.synthetic import generate_cells

KPI_FIELDS = [
    "rsrp_dbm", "rsrq_db", "sinr_db", "dl_throughput_mbps",
    "ul_throughput_mbps", "drop_rate_pct", "handover_success_pct", "availability_pct",
]


def main() -> None:
    for row in generate_cells(n=10, seed=7):
        score = compute_health_score({k: row[k] for k in KPI_FIELDS})
        state = "DEGRADED" if score < 60 else "HEALTHY" if score >= 80 else "WATCH"
        print(f"{row['cell_id']}: health={score:6.2f}  state={state}")


if __name__ == "__main__":
    main()
