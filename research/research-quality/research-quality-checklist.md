# Research Quality Checklist

## Research design

- [x] Research question identifies the model-generated artifact, Java format, algorithmic task, additional constraint, and measurable outcome.
- [x] Proposed gap is narrow, measurable, and explicitly not claimed as proven novelty.
- [x] Matched control and experimental variants are described.
- [x] Primary alternative, null, and secondary failure-pattern hypotheses are stated.
- [x] Neutrality procedures, validity risks, and oracle-validation expectations are documented.
- [x] Empirical model evaluation is explicitly marked as not conducted.
- [x] One pilot has an authored statement, Java reference, independent exhaustive/seeded validation, and weighted test manifest.
- [x] A known incorrect deque mutation is detected by the pilot tests.
- [x] Model/API results are not fabricated; provider credentials are absent and the model configuration is empty.

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
- [x] For the newly authored pilot, define the positive-preservation guarantee (input contains at least one positive), `N = 1` domain, `K = 0`, `K = N`, and no-removal option.
- [x] Implement the pilot reference and a separate brute-force oracle; exhaustive small, seeded random, and maximum-size checks pass.
- [x] Add a weighted test manifest and verify the grader detects a known deque-ordering mutation.
- [ ] Author and validate Version A with only the intended constraint differing.
- [ ] Freeze and hash both hidden test suites and acceptance criteria before model runs.
- [ ] Preregister model-selection rules, versions, run count, prompts/settings, pairing, missing-run policy, failure taxonomy, and statistical analysis.
- [ ] Conduct the model evaluation and report actual results with uncertainty; do not represent the study as empirically complete beforehand.
- [ ] Complete 5–10 high-quality tasks only if they pass originality, ambiguity, algorithmic feasibility, and independent validation gates.
- [ ] Independently audit sandboxing and resource limits for the actual submission environment.
- [ ] Complete a systematic or sufficiently documented literature search before asserting a novel research gap.
- [ ] Produce a hosted public video and a submission ZIP below 50 MB after empirical results exist.

## Open questions

- Is the proposed constraint-specific contribution distinct from problems already in existing benchmark datasets?
- Are A and B matched closely enough to attribute an observed difference to the positive-preservation rule?
- How many independent runs will provide informative uncertainty estimates?
- Can failure categories be applied consistently by independent reviewers?
- Would results replicate across model families and additional problem instances?
- Has the human participant accepted the micro1 Participant Agreement manually?
