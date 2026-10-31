# Research Sources and Verification Status

## Status

The supplied research brief names the works below and reports several benchmark statistics. The previous research session could not retrieve relevant publisher or arXiv pages because of network/DNS and HTTP access errors. The citations and statistics therefore remain **leads**, not independently verified facts. The literature review must be updated after primary-source inspection.

## Source leads

| Work | Source lead | Verification still required |
|---|---|---|
| LiveCodeBench | [arXiv record 2403.07974](https://arxiv.org/abs/2403.07974); [official repository](https://github.com/LiveCodeBench/LiveCodeBench) | Confirm exact title, full authorship, venue, dataset version/size, evaluation protocol, and conclusions from paper and repository. |
| ProBench | [arXiv search](https://arxiv.org/search/?query=ProBench+competitive+programming&searchtype=all) | Identify the exact work; verify authors, title, venue/year, reported 790-task count, methods, and findings. Replace search result with direct primary citations. |
| LiveCodeBench Pro | [NeurIPS proceedings](https://proceedings.neurips.cc/); [arXiv search](https://arxiv.org/search/?query=LiveCodeBench+Pro&searchtype=all) | Identify exact paper and verify authors, venue, dataset size, expert-annotation process, and results. Replace search links with direct citations. |
| CONCUR | [ACM Digital Library search](https://dl.acm.org/action/doSearch?AllField=CONCUR+benchmark+LLM+concurrent+code+generation) | Verify exact title/authors/DOI and ISSTA 2026 record; check the reported 43 base problems and 72 variants against paper/artifact. |
| PROBE | [SpringerLink search](https://link.springer.com/search?query=PROBE+code+generation+functional+correctness+similarity) | Identify the exact publication and verify DOI, authors, year/venue, methodology, dimensions, and reported results. |

## Citation protocol

1. Prefer the primary paper, proceedings record, DOI landing page, and official benchmark repository.
2. Record access date and version. Benchmark sizes may differ across releases.
3. Cite every factual publication or benchmark claim in [related-work.md](related-work.md) directly to the source that supports it.
4. Mark inaccessible or unconfirmed claims as pending; do not infer bibliographic details from search snippets.
5. Separate published findings from this project's interpretation.
6. Do not treat the supplied research summary as independent verification of its own claims.

## Challenge-source verification

The original `Challenge_1_Transaction_Collapse_Engine.txt` was not present in the inspected project tree. The claims that Examples 2 and 4 should output `21` and `4`, respectively, and the reported input bounds and algorithmic properties have not been independently checked against the original statement in this workspace. They must be verified before use.

## Access note

The prior research session recorded failed retrieval attempts due to temporary DNS resolution and HTTP 403/406 responses. These failures are access limitations only; they do not confirm or refute any publication claim.
