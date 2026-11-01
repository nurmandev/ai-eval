# Beyond the Happy Path

**Evaluating AI-generated Java solutions for adversarial algorithmic constraints**

> **Status: pilot implementation, not a completed competition submission.** One matched task pair (control A and experimental B), standalone Java references, independent oracle tests, weighted grading, and API adapters are present. No AI model evaluation has been run. This is not yet a 5–10-task benchmark or submission-ready package.

## Short description

This project pilots execution-based evaluation of standalone Java solutions to deterministic algorithmic tasks with adversarial constraints. The paired research design compares bounded contiguous-deletion optimization with and without a global positive-element preservation rule while keeping input domain and objective matched. This is a candidate contribution, not a proven gap or conclusion about current AI models.

**Key experimental finding:** Not available — no AI model runs have been performed.

**Video demonstration:** `[INSERT PUBLIC VIDEO URL — not recorded or hosted]`

Submission-form description and video URL must be copied into the competition form after actual results and an accessible video exist.

## Domain and expertise

Software engineering and computer science: Java 17-compatible programming, algorithms and data structures, competitive programming, mathematical reasoning, invariant checking, exact arithmetic, testing, and AI code-generation evaluation. The pilot measures sequential array optimization. It does **not** evaluate real database ACID behavior, distributed systems, multithreaded concurrency, or banking correctness.

## What the pilot measures and why it matters

The pilot measures whether a model returns a correct, efficient `Main.java` solution under a defined global feasibility constraint, hidden weighted tests, and an adversarial maximum-size case. It measures executable behavior, not persuasive explanations. Incorrect algorithms can cause wrong outputs or resource failures in software that processes transactional data; this single matched pair cannot establish general production-system reliability.

## Repository structure

```text
.
├── challenges/challenge-01-transaction-collapse/  # Experimental Version B
├── tasks/transaction-collapse-control/           # Matched Control Version A
├── reference-solutions/                           # Standalone Java references/editorials
├── evaluator/                                      # API adapters, prompt, sandbox, grading
├── validation/reference-validation/                # Exhaustive, seeded, stress, mutation tests
├── research/                                       # Research design, sources, task plan, limits
├── results/                                        # Explicit NOT RUN status and report templates
├── docs/                                           # Study and scoring methodology
└── scripts/                                        # Setup, validation, evaluation, packaging
```

## Setup

Requirements: Linux/POSIX, Python 3.12 or later, Java/JDK 17 or later, `make`, and Bubblewrap (`bwrap`). The reference compiler targets Java 17 with `javac --release 17`. Local verification in this environment used OpenJDK 21.0.12.1; the final experiment must record its exact Java runtime/compiler versions. No third-party Python packages are currently required.

```bash
git clone <repository-url>
cd ai-eval
make setup
make test
make validate
```

`make test` includes exhaustive small-array comparisons against a separate Python brute-force oracle, seeded random comparisons, maximum-size reference execution, evaluator unit tests, sandbox checks, and a known-bug mutation check. `make validate` runs both weighted test suites against the local Java references in the same restricted execution runner used for generated Java, then writes `results/reference-validation.json`. This file is explicitly marked as reference-only, not an AI model result.

## Run a model pilot

Model calls require a real provider account and credentials. Only OpenAI, Anthropic, and Google adapters are currently implemented. Model IDs are not guessed or hardcoded; verify current API model IDs and enter the exact IDs in `evaluator/models/model-config.json`.

```bash
cp .env.example .env
# Edit .env and enter only the provider key you intend to use.
# Edit evaluator/models/model-config.json with one or more exact current model IDs.
make pilot       # one run per configured model and task variant
make evaluate    # MODEL_RUNS_PER_TASK runs (default 3) per model and variant
make report
make package     # creates a clearly labelled draft ZIP under dist/
```

The pilot runs both matched task versions per model and repetition, alternating task order by run number. One side can be run alone:

```bash
python3 evaluator/main.py evaluate --task version-a-control --runs 1
python3 evaluator/main.py evaluate --task version-b-experimental --runs 1
```

Example model configuration shape (replace the illustrative value with a verified current ID):

```json
{
  "models": [
    {
      "name": "provider-model",
      "provider": "openai",
      "model_id": "REPLACE_WITH_VERIFIED_MODEL_ID",
      "temperature": 0,
      "max_output_tokens": 8192
    }
  ]
}
```

Supported `provider` values: `openai`, `anthropic`, `google`; matching keys are in `.env.example`. The exact prompt, response, extracted source, request ID, usage metadata, settings, and grading evidence are saved under `results/raw-outputs/`; credentials are not intentionally serialized. Provider pricing is not embedded because account terms and current pricing have not been verified. Token usage is retained when returned; no API-cost result is claimed.

Generated Java is compiled with annotation processing disabled and run with Bubblewrap network/PID namespace isolation, a minimal environment, temporary filesystem, Java heap cap, CPU/file-size limits, and wall-clock timeouts. This is a practical local sandbox, not a formally audited hostile-code containment system. Use a disposable machine/container for evaluation of untrusted code.

## Scores and failure analysis

Each task version has 12 weighted test cases totaling 100 points, including core behavior, boundaries, the global invariant, ties, long-sum behavior, and `N=200,000` performance. Each test has a documented ID, category, expected output, and weight in its version's test manifest. Scoring is strict except for trailing whitespace. Compilation and per-test execution outcomes are retained. The [grading methodology](docs/grading-methodology.md) defines scoring and execution limits.

No model failure evidence currently exists. Automatic evidence is per-test status and raw output; algorithmic root-cause labels require careful review against that evidence. See the [failure-analysis template](results/failure-analysis.md). No model leaderboard or cost estimate is supplied before real runs.

## Research, prior work, and originality

The [research review](research/research-quality/related-work.md) discusses HumanEval, MBPP, SWE-bench, LiveCodeBench, and BigCodeBench. The paired task statements, references, editorials, and tests were authored for this repository; the standard prefix-sum/deque algorithm is established prior art and is not claimed as novel. The original Challenge 1 source was unavailable, so Version B is a new specification and does not claim to correct the missing source's examples.

The review is focused, not systematic. Additional proposed sources (including ProBench, LiveCodeBench Pro, CONCUR, and PROBE) are not treated as verified evidence until their exact primary publications are identified.

## Limitations and submission status

One matched task pair cannot establish a general weakness in AI coding. No model IDs, scores, outputs, failure rates, actual costs, or empirical findings are available. No complete 5–10-task evaluation exists. The separate micro1 Participant Guide was not found in the inspected project locations.

The competition brief gives a deadline of **November 9, 2026 at 05:15 GMT**. The final public video, result-backed report, clean-environment reproduction, and ZIP still require completion. The packaging script enforces the 50 MB limit, but a package created now is only a draft and is not submission-ready. See the [submission checklist](submission-checklist.md).

**Manual participant requirement:** The human participant must personally review and accept the micro1 Participant Agreement if required. It has not been accepted on the participant’s behalf.

See the [research limitations](research/research-limitations.md), [task-quality plan](research/task-specifications.md), and [video checklist](video-demo.txt).
