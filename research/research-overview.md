# Research Overview

## Project title

**Beyond the Happy Path: Evaluating AI-Generated Java Solutions for Adversarial Algorithmic Constraints**

The title is intentionally narrower than the initial proposal's broad claims about transaction processing and concurrency. The current tasks are deterministic Java algorithm simulations: bounded array optimization and ordered idempotency-state processing. They do not measure real database or concurrent-system behavior.

## Domain and expertise

The project sits at the intersection of software engineering and computer science: Java programming, algorithms and data structures, competitive programming, mathematical reasoning, invariant checking, test design, and AI code-generation evaluation.

## Research question

The matched Challenge 01 pilot asks whether adding a global positive-element preservation constraint to bounded contiguous-deletion optimization changes first-attempt acceptance. Challenge 02 is a distinct Retry Idempotency Engine task testing state transitions, key scoping, cached outcomes, and fixed TTL boundaries. See the [formal research question](research-quality/research-question.md) and [hypothesis plan](research-quality/hypothesis.md).

## Why the question matters

Sample-only checks can miss globally invalid choices, boundary errors, numeric errors, and poor worst-case complexity. Execution-based hidden tests and an independently validated oracle provide measurable evidence on the defined task. Results would apply to the tested tasks and conditions—not prove that a model is generally unsafe for banking, concurrency, or production software.

## Current status

- **Research design:** initial matched-variant design documented.
- **Literature:** five primary benchmark/paper leads retrieved; review is focused, not systematic, and several proposed sources remain unresolved.
- **Original task:** original challenge source is missing; no task correction has been verified against it.
- **Task suite:** one matched pilot pair (Version A control and Version B experimental) and one distinct Challenge 02 task have Java references, weighted tests, and local validation; there is no complete set of 5–10 independent tasks.
- **Evaluator and Java references:** all three registered task variants have standalone Java references and are supported by the multi-provider grading runner; the runner has not been audited for hostile-code production use.
- **Model pilot/final experiment:** not run; required API credentials are not present in the environment.
- **Results/video/ZIP/agreement:** no actual results, hosted video, submission ZIP, or participant-agreement confirmation yet.

Challenge 02 adds task coverage but does not expand the empirical evidence; no task has been evaluated on AI models. Further tasks must be original, unambiguous, algorithmically feasible, and independently testable. See [task specification plan](task-specifications.md) and [limitations](research-limitations.md).
