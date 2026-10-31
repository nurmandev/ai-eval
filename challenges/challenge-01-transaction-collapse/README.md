# Challenge 1: The Transaction Collapse Engine

This folder identifies the subject of the research evaluation only. The original challenge statement was not available in the workspace during this phase, so no specification or sample has been recreated or modified.

The supplied research describes a Java 17 standalone solution for removing at most one contiguous block of length at most `K` from an array, maximizing the remaining sum, while preserving at least one strictly positive element. It reports `N <= 200,000`; all exact input guarantees, value bounds, output rules, examples, and resource limits must be checked against the original statement before evaluation.

The challenge is an abstract sequential array-optimization task, not database transaction processing or concurrent programming. The research summary reports possible inconsistencies in Examples 2 and 4, but those outputs have not been independently checked here. See [the checklist](../../research/research-quality/research-quality-checklist.md).

## Research summary from the supplied brief

The supplied research argues that this should be treated as a software-engineering and AI-evaluation problem rather than as a general concurrency benchmark. The central question is whether AI coding models can independently generate functionally correct, deterministic, and constraint-compliant Java implementations when transaction outcomes depend on ordering, conflicts, numerical boundaries, and feasibility constraints.

The research distinguishes the challenge from true database transactions or multithreaded concurrent execution: it is a sequential optimization problem disguised as a financial scenario. The algorithmic core is not a concurrency challenge; it is a bounded contiguous-deletion optimization problem that requires array reasoning, prefix sums, sliding-window logic, and a validity check that prevents the deletion from removing all positive values.

The brief also notes that, in the current document set, the challenge's actual requirements appear to be:

- choose at most one contiguous deletion window
- limit the deletion length to `K`
- maximize the sum of retained values
- preserve at least one strictly positive value
- use `long` arithmetic for numerical correctness
- maintain `O(N)` or `O(N log N)` complexity

It further argues that the challenge's sample explanations contain contradictions and that the outputs for Example 2 and Example 4 may be incorrect. The research urges that these examples and their explanations be corrected before the challenge is used in a benchmark or submission pipeline, because benchmark reliability depends on consistent and independently validated examples.

The brief proposes a matched design that compares:

- Version A: the base contiguous-subarray deletion problem without the positive-preservation rule
- Version B: the same optimization with the added global constraint that at least one strictly positive element remains after deletion

The key hypothesis is that AI models will perform worse on Version B because the extra feasibility rule creates a global validity condition that can make an otherwise optimal deletion invalid. The null hypothesis is that no statistically reliable difference exists in first-attempt acceptance rates between the two versions.

The methodology emphasizes a precise, reproducible evaluation protocol with hidden tests, reference validation, and a failure taxonomy. It explicitly states that no experiments are considered complete until they have actually been run and documented. The supplied brief therefore frames this project as a research design and a research-quality section, not as a completed empirical study.
