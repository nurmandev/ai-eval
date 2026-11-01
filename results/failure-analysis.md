# Failure Analysis

**Status: NOT RUN.** No model responses or model failures are available to analyze.

After model evaluation, summarize all runs, not only illustrative failures. For each failure provide:

| Field | Required evidence |
|---|---|
| Model / run | Exact provider, model ID, and run ID |
| Task / test | Task version and test ID/category |
| Expected / observed | Expected output and actual output or compiler/runtime result |
| Failure type | Incorrect algorithm, invariant violation, boundary, numeric, complexity/performance, compilation, interpretation, or other |
| Explanation | Short, evidence-based causal account; distinguish observation from inference |
| Reproducibility | Whether the failure recurs on an independent run |

Keep raw responses in `raw-outputs/`. Do not infer algorithmic cause from score alone, omit successful runs, or describe a provider/API error as a model reasoning failure.
