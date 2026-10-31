# Research Quality Checklist

## Research design

- [x] Research question identifies the model-generated artifact, Java format, algorithmic task, additional constraint, and measurable outcome.
- [x] Proposed gap is narrow, measurable, and explicitly not claimed as proven novelty.
- [x] Matched control and experimental variants are described.
- [x] Primary alternative, null, and secondary failure-pattern hypotheses are stated.
- [x] Neutrality procedures, validity risks, and oracle-validation expectations are documented.
- [x] Empirical model evaluation is explicitly marked as not conducted.

## Literature status

- [ ] Verify LiveCodeBench bibliographic metadata, benchmark details, and claims against primary sources.
- [ ] Identify and verify ProBench title, authors, venue, dataset count, and claims.
- [ ] Identify and verify LiveCodeBench Pro publication and reported details.
- [ ] Verify CONCUR publication details and reported benchmark counts.
- [ ] Identify and verify the cited PROBE publication and its stated measures.
- [ ] Search for adjacent work on global feasibility constraints and matched programming-task variants before asserting novelty.

## Technical and empirical work pending

- [ ] Obtain and inspect the original challenge statement and confirm all input guarantees, numeric bounds, complexity limits, and samples.
- [ ] Resolve the reported Example 2 and Example 4 inconsistencies against that original statement; `21` and `4` are currently unverified reports.
- [ ] Confirm the positive-preservation rule, including behavior when no positive element exists in the input.
- [ ] Define edge semantics such as `N = 1`, `K = 0`, `K = N`, and whether no deletion is permitted.
- [ ] Finalize Version A and Version B with only the intended constraint differing.
- [ ] Implement and independently validate exhaustive and optimized correctness oracles.
- [ ] Freeze and hash the hidden tests and acceptance criteria before any model runs.
- [ ] Preregister model-selection rules, versions, run count, prompts/settings, pairing, missing-run policy, failure taxonomy, and statistical analysis.
- [ ] Conduct the model evaluation and report actual results with uncertainty; do not represent the study as empirically complete beforehand.

## Open questions

- Is the proposed constraint-specific contribution distinct from problems already in existing benchmark datasets?
- Are A and B matched closely enough to attribute an observed difference to the positive-preservation rule?
- How many independent runs will provide informative uncertainty estimates?
- Can failure categories be applied consistently by independent reviewers?
- Would results replicate across model families and additional problem instances?
