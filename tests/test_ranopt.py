from ranopt.anomaly import detect_zscore_anomalies
from ranopt.health import compute_health_score
from ranopt.kpis import RANKPIs


def sample():
    return {
        "rsrp_dbm": -85,
        "rsrq_db": -7,
        "sinr_db": 18,
        "dl_throughput_mbps": 100,
        "ul_throughput_mbps": 30,
        "drop_rate_pct": 0.5,
        "handover_success_pct": 99,
        "availability_pct": 99.8,
    }


def test_kpi_validation():
    record = RANKPIs(**sample())
    record.validate()


def test_health_score_is_bounded():
    score = compute_health_score(sample())
    assert 0 <= score <= 100


def test_anomaly_detector_flags_extreme_value():
    flags = detect_zscore_anomalies([10, 10, 10, 10, 10, 10, 100], threshold=2)
    assert flags[-1] is True
