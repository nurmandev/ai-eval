# Related Work

## Review status

This is an initial synthesis of the research leads provided for this project, not a completed systematic literature review. The supplied summary gives benchmark names and selected counts or conclusions but not complete citations for every work. Attempts to retrieve publisher and arXiv pages were unsuccessful in the prior research session. Accordingly, all facts not checked against primary sources are identified as **unverified leads** and must not be presented as confirmed publication findings.

## Identified benchmark leads

| Work | Supplied description | Relevance to this project | Verification needed |
|---|---|---|---|
| LiveCodeBench | Described as a contamination-aware code benchmark using recent programming problems from online platforms; the supplied summary attributes it to ICLR 2025. | Supports fresh tasks and execution-based evaluation; does not by itself establish the novelty of this particular matched constraint comparison. | Confirm exact title, authors, venue, dataset version and size, task sources, evaluation procedure, and findings from the paper and official repository. |
| ProBench | Described as competitive-programming evaluation with online-judge submissions, resource measurements, and failure analysis; the summary reports 790 tasks and a 2025 date. | Relevant to competitive-programming evaluation and failure categorization. | Confirm paper identity, authors, venue, dataset count/version, methodology, and reported results. |
| LiveCodeBench Pro | Described as an expert-annotated, Olympiad-level programming benchmark; the supplied summary attributes it to NeurIPS 2025. | Relevant to expert task annotation and analysis of nuanced algorithmic failures. | Confirm exact paper identity, authors, venue, task count, annotation process, and findings. |
| CONCUR | Described as an LLM concurrent-code-generation benchmark; the summary attributes it to ISSTA 2026 and reports 43 base problems plus 72 variants. | Important scope contrast: concurrency is not the same as the proposed sequential optimization task. | Confirm publication identity and all counts from the proceedings paper and official artifacts. |
| PROBE | Described as evaluating functional correctness, similarity to valid solutions, and code quality; the supplied summary refers to Springer Nature and 2026. | Suggests that evaluation can report quality dimensions beyond compilation and test success. | Establish exact title, authors, venue, DOI, methodology, and findings; confirm that the described dimensions are accurate. |

## Interpretation

If verified, these works demonstrate that code-generation correctness, competitive programming, concurrency, expert task evaluation, and broader code-quality measures already have research precedents. They should therefore be acknowledged rather than framed as untouched areas. The narrower proposed contribution is a controlled comparison of one sequential optimization task with and without a single global feasibility constraint.

The reported counts and venue labels above originate from the supplied research summary and are not independently confirmed here. They are not adequate evidence for a literature claim until the source log is completed.

## Required review for each paper

For every confirmed work, add the full paper title, complete author list, publication year and venue, primary paper URL or DOI, research objective, methodology, dataset or benchmark version and size, main findings, limitations, and relationship to this study. Distinguish the paper's reported results from this project's interpretation. Prefer primary papers and official benchmark repositories over secondary descriptions.

See [research-sources.md](research-sources.md) for source leads and the outstanding verification steps.
