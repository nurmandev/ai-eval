# Research Methodology

## Study design

Run a matched, execution-based comparison of two standalone Java tasks. Version A is the base bounded contiguous-deletion optimization problem. Version B adds the rule that at least one strictly positive value must remain. Use identical prompting, tools, compiler/runtime, resource constraints, and evaluation criteria except where wording must express the additional rule.

## Preparation and current implementation

The original challenge statement was not available. The repository therefore contains separately labelled, newly authored matched pilot specifications rather than an asserted correction of that original. Version A and Version B share the same input domain and objective; the intended difference is the positive-preservation constraint.

The pilot includes standalone Java 17-compatible references for both variants, a Python brute-force oracle, exhaustive small-array comparisons, seeded random differential tests, and 200,000-element stress tests. Each evaluator test manifest totals 100 points and includes core, boundary, adversarial, numeric, and performance tests. A deliberate incorrect deque mutation is tested to ensure the Version B suite detects a plausible bug. These local checks validate the authored pilot pair only; they are not AI model results.

Before any model evaluation, freeze the task text and test suite (including hashes), verify the exact provider model IDs, define the run count and analysis plan, and disclose that the original challenge source was unavailable.

## Evaluation

For each selected model/version, record the exact model identifier, provider, date, prompt, settings, complete first response, compiler output, test results, runtime, and any provider or execution error. Apply the same Java 17 target and documented runtime limits to both conditions. Do not provide repair feedback before the first-attempt outcome is recorded.

Acceptance requires successful compilation and passage of every hidden correctness and resource test. Report pass@1, compilation, constraint compliance, numerical correctness, and performance separately. Classify rejected outputs using predefined categories; retain uncategorized and ambiguous cases.

## Analysis and reporting

Report counts, rates, uncertainty intervals, and per-model results. Use a paired comparison only where runs are genuinely matched and define the unit of pairing in advance. Report the null and alternative results, all exclusions and deviations, and any exploratory analysis as exploratory. Distinguish first-attempt evaluation from later debugging or repair.

## Current limitation

This remains a proposed experimental protocol, not a report of a completed model experiment. Pilot reference/oracle checks and evaluator scaffolding exist, but the original task inspection, source review completion, preregistration, model runs, and empirical analysis remain pending.
