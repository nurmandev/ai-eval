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

No challenge specification or Java implementation is included in this research-only phase.
