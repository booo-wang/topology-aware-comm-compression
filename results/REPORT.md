# Demo Report

- Source: `demo_scenarios_20260327_115734.json`
- Benchmark: `demo_scenarios`
- Number of scenarios: `96`

## Best Configuration

- Scenario: `fully_connected__novelty_topk__budget3__vis0.25__drop0.00`
- Topology: `fully_connected`
- Compressor: `novelty_topk`
- Budget: `3`
- Dropout: `0.0`
- Visibility: `0.25`
- Mean recall: `1.0`
- Efficiency: `0.011009`
- Hop trajectory: `0.897 -> 0.998 -> 1.000`

## Current Findings

- A first pass over the sweep suggests that `fully_connected` is the strongest topology for raw recovery. Its average recall is 0.896, about 0.074 higher than `ring`.
- The tradeoff picture is different from the raw-recall ranking: `star` looks best on efficiency (0.01523), even though `fully_connected` still leads on absolute recall.
- One pattern that looks fairly consistent in this synthetic setting is that novelty-oriented compression behaves better than naive retransmission. Averaged over the current runs, novelty-based variants reach 0.866 recall / 0.01595 efficiency, compared with 0.626 / 0.00695 for `full_state`.
- Looking at hop-wise behavior, the best configuration already reaches 0.998 recall by hop 2 and then saturates near 1.000. That makes the hop trajectory itself worth tracking, not just the final score.

## Top 5 Scenarios

| Scenario | Topology | Compressor | Budget | Recall | Efficiency |
| --- | --- | --- | ---: | ---: | ---: |
| fully_connected__novelty_topk__budget3__vis0.25__drop0.00 | fully_connected | novelty_topk | 3 | 1.0000 | 0.011009 |
| fully_connected__novelty_topk__budget2__vis0.25__drop0.00 | fully_connected | novelty_topk | 2 | 0.9980 | 0.011034 |
| fully_connected__novelty_topk__budget3__vis0.35__drop0.00 | fully_connected | novelty_topk | 3 | 0.9980 | 0.010458 |
| fully_connected__novelty_topk__budget3__vis0.25__drop0.10 | fully_connected | novelty_topk | 3 | 0.9980 | 0.010262 |
| fully_connected__novelty_topk__budget3__vis0.35__drop0.10 | fully_connected | novelty_topk | 3 | 0.9960 | 0.010374 |