# Research Sources and Verification Log

Access date for sources marked retrieved: 2026-11-01.

## Primary-source records retrieved

| Source | Primary URL | Why it matters | Verification note |
|---|---|---|---|
| Mark Chen et al., *Evaluating Large Language Models Trained on Code* (arXiv submission 2021-07-07) | https://arxiv.org/abs/2107.03374 | HumanEval and executable functional-correctness evaluation. | Exact title, submission date, authors, and abstract retrieved through the arXiv API on 2026-11-01. |
| Jacob Austin et al., *Program Synthesis with Large Language Models* (arXiv submission 2021-08-16) | https://arxiv.org/abs/2108.07732 | MBPP and natural-language program synthesis. | Exact title, submission date, authors, and abstract retrieved through the arXiv API on 2026-11-01. |
| Carlos E. Jimenez et al., *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* (arXiv submission 2023-10-10) | https://arxiv.org/abs/2310.06770 | Repository-level issue resolution benchmark. | Exact title, submission date, authors, and abstract retrieved; paper reports 2,294 issues across 12 Python repositories. |
| Naman Jain et al., *LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code* (arXiv submission 2024-03-12) | https://arxiv.org/abs/2403.07974 | Fresh competitive-programming tasks and broader code capability evaluation. | Exact title, submission date, authors, abstract, and [official repository](https://github.com/LiveCodeBench/LiveCodeBench) retrieved. Repository counts vary by release; initial release lists 400 problems. |
| Terry Yue Zhuo et al., *BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions* (arXiv submission 2024-06-22) | https://arxiv.org/abs/2406.15877 | Complex instruction and API/function-use code generation. | Exact title, submission date, authors, abstract, and [official repository](https://github.com/bigcode-bench/bigcodebench) retrieved; dataset size must be tied to a specific release before citing. |

## Additional work requiring verification

The supplied research mentions ProBench, LiveCodeBench Pro, CONCUR, and PROBE. The provided labels alone are insufficient to establish exact papers or claims. Locate each paper using author/title/DOI and verify it directly before adding it as a cited result. The prior research notes retrieval errors for some publisher pages; those errors are not evidence for or against the work.

The broader project literature review should also search for Java-specific code-generation evaluation, competitive-programming benchmarks, adversarial test generation, numerical correctness, transaction histories, serializability, recovery algorithms, and deterministic evaluation of concurrency abstractions. Record search databases, exact queries, date, and inclusion/exclusion criteria if presenting a systematic claim.

## Citation and integrity rules

1. Prefer the paper, proceedings record, DOI landing page, and official benchmark repository.
2. Cite the benchmark version/release and access date for mutable datasets.
3. Distinguish paper claims from project interpretations.
4. Do not copy benchmark problem statements or protected task content into this project.
5. Do not infer publication metadata from search snippets.
6. Treat all result claims in this project as unverified until reproduced or directly supported by the source.

## Challenge-source verification

The original `Challenge_1_Transaction_Collapse_Engine.txt` and participant guide were not found in the repository or the inspected Desktop search. Therefore the original task’s exact constraints and the reported corrected outputs for Examples 2 and 4 remain unverified.
