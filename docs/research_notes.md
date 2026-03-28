# Research Notes

## Framing

This repository studies communication behavior in a simplified multi-agent sensor-fusion setting.

The central question is:

How do topology and compression interact when agents must reconstruct a larger state from partial local observations?

## Why This Matters

Multi-agent systems often face a three-way constraint:

- partial observability
- limited bandwidth
- nontrivial communication structure

Even before introducing a sophisticated learned communication model, it is useful to understand what simpler communication schemes already reveal about the problem.

## Current Experimental Angle

The present codebase emphasizes:

- topology comparison
- budget-aware message passing
- novelty-oriented compression
- recovery-efficiency tradeoffs
- hop-by-hop information propagation

## Current Working Observations

These are observations from the current sandbox, not final claims:

- dense communication improves recovery speed, but can be expensive
- novelty-based communication is often more efficient than blindly retransmitting known information
- final recall can hide meaningful differences in hop-wise information flow
- topology matters not only for final performance but also for how quickly information spreads

## Relationship To Future Work

This repository is intentionally method-light.

Its role is to support future, more method-centered work by clarifying:

- which communication regimes are interesting
- which baselines are worth keeping
- which metrics are actually informative
