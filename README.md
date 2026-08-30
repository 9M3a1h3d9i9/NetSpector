# NetSpector — Network & RAN Intelligence

> Modular network monitoring framework evolving toward **RAN KPI analytics, anomaly detection, and optimization support**.

## Vision

NetSpector starts from practical network observability and extends it toward an intelligent monitoring layer suitable for research experiments in mobile/RAN networks.

```text
Network Measurements
        ↓
RAN KPI Ingestion
        ↓
Validation & Normalization
        ↓
Cell Health Scoring
        ↓
Anomaly Detection
        ↓
Diagnosis / Alerting
        ↓
Optimization Support
```

## Current Capabilities

- Network latency, jitter, packet-loss, and speed measurements
- Structured measurement storage
- Console / GUI foundations
- Typed RAN KPI schema
- Explainable 0–100 cell-health scoring
- Statistical KPI anomaly detection baseline
- Deterministic synthetic RAN KPI generator for development and CI
- Automated unit tests for the new analytics layer

## RAN KPI Foundation

The first RAN-oriented layer works with technology-neutral KPIs including:

- RSRP
- RSRQ
- SINR
- Downlink / uplink throughput
- Drop rate
- Handover success rate
- Availability

The default thresholds are **prototype engineering assumptions**, not operator-specific thresholds. Real deployment should load calibrated thresholds from configuration or OSS/NMS data.

## Repository Structure

```text
NetSpector/
├── src/
│   └── ranopt/
│       ├── kpis.py       # KPI schema and validation
│       ├── health.py     # explainable health score
│       ├── anomaly.py    # statistical anomaly baseline
│       └── synthetic.py  # deterministic development data
├── tests/
│   └── test_ranopt.py
├── examples/
│   └── ranopt_demo.py
├── data/
├── requirements.txt
└── pyproject.toml
```

## Quick Start

```bash
python -m pip install -e .
python examples/ranopt_demo.py
pytest
```

The demo uses synthetic data only. It does **not** represent measurements from a mobile operator.

## Development Status

**Stage 1 — RAN analytics foundation**

Implemented: KPI schema, validation, health scoring, anomaly baseline, synthetic data, demo, and tests.

Not yet implemented: real LTE/5G telemetry ingestion, operator-specific KPI thresholds, production dashboards, root-cause diagnosis, and optimization policies.

## Roadmap

### Stage 2 — Monitoring
- CSV/API KPI ingestion
- Rolling-window statistics
- Threshold configuration
- Cell-level alerts
- Time-series dashboard

### Stage 3 — Diagnosis
- Correlation between KPI degradation and events
- Root-cause candidates
- Neighbor-cell analysis
- Mobility / handover analysis

### Stage 4 — Optimization
- Formulate optimization objectives
- Build a simulation environment
- Add optimization baselines
- Evaluate reinforcement-learning policies
- Connect the project conceptually with NeuroBottleneck

## Research Integrity

Synthetic measurements are used for development and automated testing. No real operator performance, benchmark, or telecom KPI improvement is claimed by this prototype.

## Portfolio Role

This project demonstrates the engineering bridge between **network monitoring** and **AI-driven telecom optimization** and is intended to support a broader research portfolio around GNNs, DRL, bottleneck detection, and resilient networks.

## Author

**Mohammad Mahdi Shafighi** — M.Sc. Artificial Intelligence
