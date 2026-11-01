# Related Work

## Scope and evidence standard

This review covers influential and directly relevant evaluation projects. Paper titles and high-level claims below are linked to primary arXiv records or official benchmark repositories. Benchmark counts are release-specific and must not be conflated across versions. Access date for the linked sources: 2026-11-01.

This is a focused narrative review, not a systematic review. It does not establish that the proposed matched constraint experiment is novel.

## Literature

### HumanEval / Codex

**Mark Chen et al., “Evaluating Large Language Models Trained on Code” (arXiv submission 2021).** [arXiv:2107.03374](https://arxiv.org/abs/2107.03374).

The paper introduces HumanEval, a set of 164 Python function-synthesis problems specified as docstrings and checked with executable tests, and evaluates Codex and other code models. The authors report pass@k results and discuss repeated sampling. This is early evidence for execution-based functional correctness, not a result about current frontier models. HumanEval is Python-focused and short-function oriented; it does not isolate Java algorithmic constraints, adversarial operation histories, or transactional invariants.

### MBPP

**Jacob Austin et al., “Program Synthesis with Large Language Models” (arXiv submission 2021).** [arXiv:2108.07732](https://arxiv.org/abs/2108.07732).

The work introduces Mostly Basic Programming Problems (MBPP), a collection of 974 entry-level Python programming tasks, and MathQA-Python (23,914 problems), and studies few-shot and fine-tuned synthesis from natural-language descriptions. The abstract reports performance scaling with model size and analyzes the effects of feedback. The tasks are Python-focused and do not form a Java transaction/state-management benchmark or a matched test of one added global feasibility constraint.

### SWE-bench

**Carlos E. Jimenez et al., “SWE-bench: Can Language Models Resolve Real-World GitHub Issues?” (arXiv submission 2023).** [arXiv:2310.06770](https://arxiv.org/abs/2310.06770).

SWE-bench evaluates whether a model can resolve real issues in existing repositories. The paper describes 2,294 problems across 12 Python repositories, with repository context and tests, and reports that the evaluated models resolved only a small fraction of issues at publication time. It captures software-engineering work across files rather than standalone stdin/stdout algorithm challenges; it does not isolate the proposed constraint.

### LiveCodeBench

**Naman Jain et al., “LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code” (arXiv submission 2024).** [arXiv:2403.07974](https://arxiv.org/abs/2403.07974); [official repository](https://github.com/LiveCodeBench/LiveCodeBench).

The project continuously collects contest questions from LeetCode, AtCoder, and Codeforces and evaluates multiple coding capabilities. The official repository lists dated release versions and reports 400 questions in its initial release, with later releases growing substantially. It is directly relevant to competitive programming and freshness/contamination concerns. It is a broad benchmark rather than a controlled comparison of an otherwise matched problem with and without one global feasibility rule.

### BigCodeBench

**Terry Yue Zhuo et al., “BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions” (arXiv submission 2024).** [arXiv:2406.15877](https://arxiv.org/abs/2406.15877); [official repository](https://github.com/bigcode-bench/bigcodebench).

BigCodeBench targets complex instructions and diverse library/function use, with executable evaluation. Its official repository describes the benchmark and release artifacts. This offers a useful contrast: realistic instruction-following and API-use challenges differ from a standalone algorithm specification with Java stdin/stdout and explicit asymptotic constraints.

## Synthesis and project interpretation

The cited literature shows that functional correctness, programming-problem synthesis, competitive-programming performance, complex instruction following, and real repository repair are established evaluation areas. The project must not claim those fields are unstudied. Its defensible candidate is narrower: a preregistered, matched Java task comparison that measures the incremental effect of a named global constraint and classifies failures using predeclared categories.

The cited studies do not establish that AI models will fail on the proposed task. That remains an empirical question. The present review also does not verify the supplied brief’s claims about ProBench, LiveCodeBench Pro, CONCUR, or PROBE; those works require exact identification and primary-source checks before being included as evidence.

## Limitations

This review is not exhaustive, does not include a systematic search protocol, and does not provide complete author lists or venue metadata where the primary record was not inspected in detail. Before final submission, expand it with database/search terms, inclusion criteria, full citations, the applicable benchmark snapshots, and primary-source validation for every claim.
