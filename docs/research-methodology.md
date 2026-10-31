# Research Methodology

## Study design

Run a matched, execution-based comparison of two standalone Java tasks. Version A is the base bounded contiguous-deletion optimization problem. Version B adds the rule that at least one strictly positive value must remain. Use identical prompting, tools, compiler/runtime, resource constraints, and evaluation criteria except where wording must express the additional rule.

## Preparation

1. Obtain and freeze the original challenge statement; resolve all examples and input-domain edge cases.
2. Write the Version A control statement and verify that the intended difference is only the global positive-preservation constraint.
3. Implement an exhaustive oracle for small inputs and an independently reviewed optimized oracle for maximum inputs.
4. Differential-test the optimized oracle against exhaustive enumeration on seeded small cases.
5. Build hidden tests for boundary, adversarial, numerical, and maximum-size behavior. Freeze the suite and acceptance criteria before any model run.
6. Preregister model-selection criteria, run count, prompts, decoding settings, pairing, missing-run handling, failure categories, and statistical analysis.

## Evaluation

For each selected model/version, record the exact model identifier, version, date, prompt, settings, complete first response, compiler output, test results, runtime, memory, and any provider or execution error. Apply the same Java 17 environment and limits to both conditions. Do not provide repair feedback before the first-attempt outcome is recorded.

Acceptance requires successful compilation and passage of every hidden correctness and resource test. Report pass@1, compilation, constraint compliance, numerical correctness, and performance separately. Classify rejected outputs using predefined categories; retain uncategorized and ambiguous cases.

## Analysis and reporting

Report counts, rates, uncertainty intervals, and per-model results. Use a paired comparison only where runs are genuinely matched and define the unit of pairing in advance. Report the null and alternative results, all exclusions and deviations, and any exploratory analysis as exploratory. Distinguish first-attempt evaluation from later debugging or repair.

## Current limitation

This document is a proposed protocol, not a report of a completed experiment. The primary-source literature verification, original challenge inspection, oracle/test construction, preregistration, and model runs remain pending.
