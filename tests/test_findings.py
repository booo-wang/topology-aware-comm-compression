from tacc.reporting.findings import build_findings


def test_build_findings_returns_human_sounding_observations() -> None:
    result = {
        'benchmark': 'demo',
        'experiments': [
            {
                'communication': {'topology': 'ring', 'compressor': 'novelty_topk'},
                'summary': {'avg_mean_recall': 0.92, 'avg_efficiency': 0.025, 'avg_hop_mean_recalls': [0.45, 0.78, 0.92]},
            },
            {
                'communication': {'topology': 'ring', 'compressor': 'full_state'},
                'summary': {'avg_mean_recall': 0.87, 'avg_efficiency': 0.016, 'avg_hop_mean_recalls': [0.42, 0.70, 0.87]},
            },
            {
                'communication': {'topology': 'star', 'compressor': 'novelty_topk'},
                'summary': {'avg_mean_recall': 0.95, 'avg_efficiency': 0.020, 'avg_hop_mean_recalls': [0.55, 0.84, 0.95]},
            },
            {
                'communication': {'topology': 'fully_connected', 'compressor': 'full_state'},
                'summary': {'avg_mean_recall': 0.90, 'avg_efficiency': 0.013, 'avg_hop_mean_recalls': [0.60, 0.82, 0.90]},
            },
        ],
        'top_result': {
            'summary': {'avg_hop_mean_recalls': [0.55, 0.84, 0.95]},
        },
    }

    findings = build_findings(result)

    assert findings
    assert any('A first pass over the sweep suggests' in item for item in findings)
    assert any('tradeoff picture' in item for item in findings)
    assert any('novelty-oriented compression' in item for item in findings)
    assert any('hop-wise behavior' in item for item in findings)
