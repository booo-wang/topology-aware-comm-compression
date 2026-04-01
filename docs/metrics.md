# Metrics and Protocol Notes

## Why This Exists

This repository is intentionally lightweight, but the evaluation should still be easy to read.
These notes define the main quantities reported in the benchmark outputs and dashboard.

## Core Metrics

### Mean Recall

`avg_mean_recall` measures how much of the global object state is recovered on average across runs.
Higher is better.

### Min / Max Recall

`avg_min_recall` and `avg_max_recall` summarize the spread across agents or runs.
They are useful for checking whether a strong average hides uneven information recovery.

### Communication Cost

`avg_total_cost` tracks the amount of information transmitted during a run.
It is useful when a topology reaches high recall by simply sending much more data.

### Total Messages

`avg_total_messages` records how many messages were exchanged.
This helps separate payload size from message frequency.

### Efficiency

`avg_efficiency` is a lightweight recovery-per-cost indicator.
It is not meant to be a final research metric, but it is useful for comparing heuristics under the same sandbox assumptions.

### Hop-Wise Recall

`avg_hop_mean_recalls` stores the average recall after each communication hop.
This is often more informative than final recall alone because it shows how quickly information spreads.

## Experimental Knobs

### Topology

The current sandbox compares `chain`, `ring`, `star`, and `fully_connected` communication graphs.

### Compressor

Current message strategies include:

- `full_state`
- `novelty_topk`
- `novelty_then_fill`
- `degree_aware_novelty`
- `random_k`

### Budget

`message_budget` limits how much content can be transmitted in a single message.
This is the main knob for bandwidth pressure.

### Visibility

`visibility_prob` controls how much of the environment each agent can observe locally before communication.

### Dropout

`message_dropout_prob` simulates unreliable communication by randomly removing messages.

## Reading Results

A strong configuration in this repository is not just the one with the highest recall.
A more convincing configuration usually combines:

- good recall
- reasonable efficiency
- stable hop-wise improvement
- acceptable behavior under tighter budgets or dropout

That is why the dashboard and Markdown report both show tradeoff-oriented summaries rather than only a single best score.
