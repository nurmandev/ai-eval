# Research Overview

## Project title

**Beyond the Happy Path: Evaluating AI-Generated Java Solutions for Adversarial Algorithmic Constraints**

The title is intentionally narrower than the initial proposal's broad claims about transaction processing and concurrency. The current research subject is a deterministic Java optimization problem; database and concurrency topics remain candidate extensions, not capabilities already measured.

## Domain and expertise

The project sits at the intersection of software engineering and computer science: Java programming, algorithms and data structures, competitive programming, mathematical reasoning, invariant checking, test design, and AI code-generation evaluation.

## Research question

The first pilot asks whether adding a global positive-element preservation constraint to a bounded contiguous-deletion optimization problem changes first-attempt acceptance for AI-generated Java 17 solutions under a frozen hidden test suite. See the [formal research question](research-quality/research-question.md) and [hypothesis plan](research-quality/hypothesis.md).

## Why the question matters

Sample-only checks can miss globally invalid choices, boundary errors, numeric errors, and poor worst-case complexity. Execution-based hidden tests and an independently validated oracle provide measurable evidence on the defined task. Results would apply to the tested tasks and conditions—not prove that a model is generally unsafe for banking, concurrency, or production software.

## Current status

- **Research design:** initial matched-variant design documented.
- **Literature:** five primary benchmark/paper leads retrieved; review is focused, not systematic, and several proposed sources remain unresolved.
- **Original task:** original challenge source is missing; no task correction has been verified against it.
- **Task suite:** one matched pilot pair (Version A control and Version B experimental) exists; there is no complete set of 5–10 independent validated tasks.
- **Evaluator and Java references:** both pilot references and an initial multi-provider grading runner are implemented and locally tested; the runner has not been audited for hostile-code production use.
- **Model pilot/final experiment:** not run; required API credentials are not present in the environment.
- **Results/video/ZIP/agreement:** no actual results, hosted video, submission ZIP, or participant-agreement confirmation yet.

The project must move from the pilot to additional tasks only after each task is original, unambiguous, algorithmically feasible, and independently testable. See [task specification plan](task-specifications.md) and [limitations](research-limitations.md).
