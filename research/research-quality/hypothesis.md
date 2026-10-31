# Hypotheses and Measurement Plan

## Variables

- **Independent variable:** Challenge version (A or B).
- **Primary dependent variable:** First-attempt acceptance, recorded as a binary outcome for each run. Acceptance requires successful compilation and passing every pre-frozen correctness and resource test.
- **Secondary outcomes:** Compilation success; functional correctness by test category; preservation-rule violations; numerical errors; runtime and memory-limit failures; measured execution time and memory; failure category.
- **Recorded factors:** Model family and exact version, run number, prompt, generation settings, date, and any provider or environment deviations.

## Hypotheses

**H1 — Primary alternative:** AI coding models will have a lower first-attempt acceptance rate on Version B than Version A because Version B adds a global feasibility constraint.

**H0 — Null:** There will be no statistically reliable difference in first-attempt acceptance rates between Versions A and B under the preregistered comparison.

**H2 — Secondary failure-pattern hypothesis:** Among rejected Version B submissions, some failures will be attributable to invalid deletion intervals, boundary handling, or failure to meet the specified complexity or resource limits. Report observed counts and proportions; do not assume the pattern in advance.

All hypotheses are proposed and **untested**. Equal or higher acceptance on Version B is a valid result and must be reported.

## Conditions and controls

Use the same language/runtime, input-output format, base objective, numeric limits, prompting template, tool access, execution sandbox, resource limits, and scoring for both versions. The positive-preservation rule should be the only substantive difference. Freeze both statements and test suites before collecting model outputs.

Choose models by a documented rule unrelated to expected success or failure. Record exact model identifiers/versions and generation settings. Perform independent repeated runs and, where possible, pair runs by model and run index. Randomize version order or use a counterbalanced order to reduce order effects. Do not provide repair feedback before recording first-attempt outcomes.

## Measurement and acceptance

The hidden test suite should cover the specified boundaries, positive-only arrays, exactly one positive value, zeroes, intervals that would remove all positive values, ties, short and maximum deletion lengths, numerical extremes, and maximum input size. The exact tests and all input guarantees must be finalized from the original specification.

Record pass@1, compilation, functional correctness, constraint compliance, numerical correctness, runtime, memory, and failure classifications separately. Do not count passing samples or a convincing explanation as correctness.

## Statistical analysis

Before evaluation, define the run count, pairing unit, confidence-interval method, significance level, statistical test, handling of missing or invalid runs, and any multiple-comparison adjustment. For genuinely paired binary outcomes, a paired method such as McNemar's test may be appropriate; select and preregister the final method based on the actual design. Report counts, denominators, rates, uncertainty intervals, and per-model results. Do not treat a non-significant difference as proof of equivalence.

## Confounds to address

Potential confounders include inconsistent wording, model-version changes, nondeterministic sampling, prompt differences, tool access, test leakage, order effects, unclear edge cases, oracle errors, unequal task difficulty unrelated to the added constraint, and insufficient independent runs. Document deviations and avoid changing criteria after inspecting results.
