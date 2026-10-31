# Research Neutrality, Bias Prevention, and Validity

## Bias-prevention procedures

- Select models using a documented rule, not an expectation that they will fail.
- Freeze task versions, prompts, hidden tests, reference implementations, resource limits, acceptance criteria, failure categories, and analysis before model evaluation.
- Validate the reference oracle independently. For small inputs, compare it with exhaustive enumeration; cross-check optimized code with seeded random cases and boundary-focused tests.
- Keep prompts, tools, Java version, compiler settings, and execution limits consistent across A and B.
- Record model family, exact model/version, date, prompt, sampling settings, full first output, compilation logs, test outcomes, resource results, and provider errors.
- Keep all attempted runs, including failures, timeouts, malformed outputs, and incomplete provider responses. Apply only predefined exclusion rules and report exclusions.
- Use deterministic execution tests as the correctness judge. Do not substitute explanation quality, human intuition, or another AI model for objective testing.
- Predefine failure labels. Where subjective classification is necessary, use independent reviewers, conceal condition labels where feasible, and document disagreements and adjudication.
- Report results whether they support, contradict, or fail to resolve H1. Separate preregistered analyses from exploratory analyses.
- Analyze first-attempt code separately from later debugging or repair, since those measure different capabilities.

## Validity risks

### Construct validity

The study intends to measure the effect of a global feasibility constraint, but wording ambiguity or unequal task clarity could instead drive results. Review both task statements for equivalent clarity and ensure only the target rule differs.

### Internal validity

Model updates, random sampling, prompt variation, tool availability, test order, and feedback can confound the comparison. Freeze versions and settings where possible, pair and counterbalance runs, and document deviations.

### Test and oracle validity

An incorrect reference solution or incomplete hidden suite can produce false acceptance or rejection. Independently validate the oracle with exhaustive small cases, differential testing, independent review, boundary cases, and maximum-size performance tests before freezing.

### External validity

A single task and language do not support general conclusions about all AI-generated code. Limit claims to the tested model versions, prompts, Java environment, and task variants. Replicate on additional independently designed problems before broader claims.

### Statistical conclusion validity

Too few runs, invalid pairing, unplanned multiple tests, or model-level variation can make estimates unstable. Preregister the analysis, report uncertainty and per-model outcomes, and do not equate lack of statistical significance with equivalence.

## Domain and product framing

The financial story is illustrative. A real financial ledger should preserve posted history and use auditable reversals or compensating entries rather than deleting records to improve a balance. The proposed challenge evaluates abstract array optimization, not production financial transaction processing.
