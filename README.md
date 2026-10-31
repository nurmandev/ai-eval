# AI Evaluation Research

## Purpose

This project defines a research design for evaluating AI-generated Java solutions to **Challenge 1: The Transaction Collapse Engine**. Its current scope is limited to project organization and the five Research Quality criteria: a precise question, a defensible gap, related work, measurable hypotheses, and research neutrality.

The challenge is an abstract sequence-optimization problem. It is not a benchmark of database transactions, ACID properties, multithreaded concurrency, or distributed ledgers.

## Status

- Research question and proposed experimental design: drafted.
- Literature review: initial synthesis based on the supplied research; primary-source verification remains pending where noted.
- Empirical model evaluation: **not conducted**.
- Reference implementation, hidden tests, and challenge corrections: outside this phase.

## Structure

```text
.
├── README.md
├── research/
│   └── research-quality/
│       ├── README.md
│       ├── research-question.md
│       ├── research-gap.md
│       ├── related-work.md
│       ├── hypothesis.md
│       ├── research-bias-and-validity.md
│       ├── research-sources.md
│       └── research-quality-checklist.md
├── references/
│   └── README.md
├── challenges/
│   └── challenge-01-transaction-collapse/
│       └── README.md
└── docs/
    └── research-methodology.md
```

## Navigation

- [Research Quality guide](research/research-quality/README.md)
- [Research methodology](docs/research-methodology.md)
- [References and verification status](references/README.md)
- [Challenge research subject](challenges/challenge-01-transaction-collapse/README.md)

## Research summary from the pasted brief

The pasted research frames the problem as an AI evaluation task for Java code generation under a constrained transactional optimization setting. It argues that the benchmark should be treated as a controlled algorithmic reasoning problem, not as a test of database transactions, concurrency, or distributed ledger behavior.

The central distinction is between a general code-generation benchmark and a more specific evaluation of whether models can implement a valid optimization algorithm when a global feasibility rule is added. In the supplied formulation, the model must choose a contiguous deletion of length at most `K`, maximize the retained sum, and preserve at least one strictly positive element. This is a sequential array problem with a global constraint, and it is specifically positioned as a challenge for correctness under adversarial input conditions and hidden tests.

The brief also emphasizes that the challenge's documentation must be corrected before it is used as a research instrument: contradictory examples, invalid boundary assumptions, and inaccurate procedure descriptions can undermine the credibility of the benchmark. The research therefore treats the challenge as a useful evaluation target only once its examples, constraints, and algorithmic interpretation are reconciled against the original statement.

No empirical results are claimed here; the work remains a research-design and documentation effort, with validation explicitly pending.

No challenge specification or Java implementation is included in this research-only phase.
