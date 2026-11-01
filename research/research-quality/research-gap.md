# Research Gap

## What prior work establishes

Existing benchmarks already measure functional code correctness, natural-language-to-code synthesis, fresh competitive-programming tasks, complex instruction following, and multi-file software engineering. These establish that neither “AI coding has not been evaluated” nor “AI fails at hard programming” is a defensible gap. See the [related-work review](related-work.md) and [source log](research-sources.md).

## Narrow, testable candidate gap

This project will first pilot a matched Java algorithmic comparison:

- **Version A:** bounded contiguous-subarray deletion to maximize the retained sum.
- **Version B:** the same task with the additional rule that at least one strictly positive array element must remain.

The candidate research question is whether adding this global feasibility constraint changes first-attempt functional acceptance under identical prompts, runtimes, and a frozen hidden test suite. A second outcome is the distribution of objectively classifiable failure types.

This is a proposed evaluation dimension, not a claim that no prior benchmark contains similar problems. Before asserting novelty, inspect the task inventories and methods of relevant benchmarks and search specifically for matched-variant studies of algorithmic feasibility constraints. If close prior art is found, the contribution must be narrowed or the task replaced.

## Relationship to the wider project proposal

The project prompt proposes ten transaction/state-management themes, including retry handling, ledger invariants, lifecycle reconstruction, outbox semantics, graph dependencies, isolation histories, crash recovery, exact arithmetic, and reconciliation. These are candidate directions only. They are not yet ten validated tasks, and several have substantial overlap or can become ambiguous or intractable unless reduced to precisely defined deterministic algorithms.

The initial pilot is intentionally narrower than claims about real-world transaction systems or concurrency. A sequential array task does not demonstrate database correctness, concurrent execution, distributed exactly-once delivery, or state-machine reliability. Later tasks should be added only when literature review, deterministic specifications, oracle validation, and pilot evidence justify them.

## Practical significance

Incorrect algorithmic handling of invariants, numeric limits, ordering, and worst-case complexity can cause incorrect outputs or resource failures in software that processes transactional data. This benchmark can demonstrate performance on its own defined tasks; it cannot establish that a model is generally unsafe for banking or production systems.

## Novelty and validity risks

- One task cannot support broad conclusions about Java or transaction processing.
- A poorly matched Version A/Version B pair could measure statement clarity rather than the added constraint.
- Existing benchmark contamination and task exposure can influence results; new tasks and frozen prompts/tests help but do not prove that no training contamination exists.
- Benchmark statistics from mutable releases must be tied to a specific release and access date.
- The original Transaction Collapse Engine statement is absent from the repository. Any reported sample corrections and exact limits remain unverified until that source is obtained.
