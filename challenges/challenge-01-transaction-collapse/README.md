# Challenge 01: Transaction Collapse Engine

This directory contains a **newly authored pilot problem**, not the original `Challenge_1_Transaction_Collapse_Engine.txt`. The original file was unavailable in the inspected repository, so the pilot does not claim to verify or correct the reported examples 2 and 4 (reported answers `21` and `4` remain unverified).

- [Complete task statement and authored samples](problem.md)
- [Machine-readable metadata](metadata.json)
- [Weighted grader test manifest](test-cases/core.json)
- [Standalone Java 17 reference and editorial](../../reference-solutions/challenge-01/editorial.md)

The pilot asks for the maximum retained array sum after optionally removing one non-empty contiguous block of length at most `K`, subject to at least one strictly positive value remaining. The input guarantees at least one positive element. It is an abstract sequential array-optimization problem, not database transaction processing, ACID behavior, or concurrency.

The [matched control, Version A](../../tasks/transaction-collapse-control/problem.md), uses the same input domain and objective without the positive-preservation rule. For example, both receive `3 3` and `-100 1 -100`; Version A returns `0` by removing the entire sequence, while Version B must retain a positive value and returns `-99`.

The problem's algorithmic reduction uses prefix sums and a monotonic deque. Both references were checked against exhaustive enumeration on small inputs, seeded random inputs, and maximum-size stress cases. The weighted grader was also tested against a deliberate deque mutation. These checks validate this repository's pilot pair only and say nothing about AI model performance.

The research design proposes a paired Version A without the preservation rule. That control task has not yet been authored or validated, so the empirical hypothesis cannot be tested yet.
