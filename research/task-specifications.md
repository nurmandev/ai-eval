# Task Specifications Plan

## Status

The themes below are candidates from the project brief, not completed tasks. A theme becomes a benchmark task only after it has a deterministic problem statement, feasible constraints, a validated standalone Java reference, independent expected answers, adversarial tests, and a nonredundancy/originality review.

## Candidate portfolio and risks

| Candidate | Potential algorithmic core | Design risk to resolve |
|---|---|---|
| 01 Transaction Collapse Engine | Matched bounded-subarray optimization with a global positive-preservation invariant. | Original specification and samples are missing; confirm exact semantics before adopting. |
| 02 Retry Idempotency | Deterministic processing of request identifiers, payload conflicts, and bounded deduplication. | Define key lifetime, ordering, conflicts, and exact output. |
| 03 Double-Entry Ledger | Validate and aggregate debit/credit postings with exact integer arithmetic. | Avoid trivial aggregation; define invalid-entry and account constraints. |
| 04 Phantom Success | Reconstruct valid operation lifecycle state from event histories. | Define legal transitions, duplicate/out-of-order events, and final-state precedence. |
| 05 Transactional Outbox | Analyze ordered events, retries, acknowledgements, and duplicates under explicit semantics. | Do not claim distributed exactly-once delivery; model a finite deterministic log only. |
| 06 Deadlock Resolution | Detect cycles and produce deterministic dependency diagnostics/policy output. | Avoid underspecified resolution or accidentally intractable optimization. |
| 07 Isolation Anomalies | Build a precedence graph and test conflict serializability for a defined history. | Specify operation grammar, conflict definition, graph output, and edge cases. |
| 08 Crash Recovery | Reconstruct state from a specified log/checkpoint format. | Specify commit records, incomplete transactions, ordering, and durability assumptions. |
| 09 Monetary Precision | Perform exact arithmetic and explicit rounding under large values. | Ensure rounding mode, scale, overflow, and input format are unambiguous. |
| 10 Ledger Repair | Detect consistency defects and choose a deterministic repair when possible. | Unique repair may not exist; define objective/tie-breaking or restrict to detection. |

## Selection gates

1. State the task in original wording and perform a similarity review; disclose inspirations without copying protected statements.
2. Give exact stdin/stdout semantics, bounds, ordering, duplicate behavior, and error handling.
3. Prove a feasible algorithm under the proposed limits. Reject tasks whose intended solution is intractable unless complexity itself is the explicitly defined subject.
4. Implement independent brute-force and optimized oracles when feasible; compare on exhaustive small cases and seeded random inputs.
5. Use mutation testing to show the suite catches plausible incorrect algorithms.
6. Pilot prompt clarity and correctness before allocating model-evaluation runs.
7. Drop overlapping or weak candidates instead of filling a ten-task quota.

## Current deliverable

No candidate in this table is represented as implemented or validated. The first recommended step is to recover and verify the original Challenge 1 statement; if it is unavailable, create a clearly versioned original pilot specification rather than claiming to have corrected the missing source.
