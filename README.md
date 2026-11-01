# Beyond the Happy Path

This project tests how well AI models solve difficult Java programming problems.
Each solution is compiled and checked against tests.

## Project status

There are two challenges:

1. **Challenge 01: Transaction Collapse Engine** — choose which part of a number sequence to remove while following a rule.
2. **Challenge 02: Retry Idempotency Engine** — process money transfers while handling retries, duplicate keys, and expiration.

Both challenges have Java reference solutions and tests. The test suites pass locally.

**No AI models have been tested yet.** There are no model scores or findings. This is still a pilot project, not a finished submission.

## Requirements

- Linux
- Python 3.12 or later
- Java 17 or later
- `make`
- Bubblewrap (`bwrap`)

No extra Python packages are needed.

## Install and test

From the project folder, run:

```bash
make setup
make test
make validate
```

- `make setup` checks that the required tools are installed.
- `make test` runs the automated tests.
- `make validate` compiles and grades each Java reference solution.

Validation checks the Java solutions. It does **not** test AI models.

## Challenges

- [Challenge 01](challenges/challenge-01-transaction-collapse/README.md)
- [Challenge 02](challenges/challenge-02-retry-idempotency/README.md)

Challenge 02 has 21 scored tests worth 100 points in total. It also has five public sample cases and tests at the maximum input size.

## Run an AI model evaluation

This step is optional. It requires an API account and key from OpenAI, Anthropic, or Google.

1. Copy `.env.example` to `.env` and add your API key.
2. Add a current model ID to `evaluator/models/model-config.json`.
3. Run:

```bash
make pilot
make report
```

To run Challenge 02 only:

```bash
python3 evaluator/main.py evaluate --task challenge-02-retry-idempotency --runs 1
```

Evaluation saves the prompt, model response, Java code, and test results under `results/`. Do not put API keys in the model configuration file or in source code.

The evaluator runs generated Java in a restricted environment. This is a practical safety measure, not a guarantee that untrusted code is fully safe. Use a disposable machine or container when testing code from models.

## Results and limitations

- Local Java tests pass; see [Challenge 02 validation results](challenges/challenge-02-retry-idempotency/validation-report.md).
- AI evaluation has not been run.
- The project has not yet been expanded into a complete 5–10 challenge benchmark.
- The original Challenge 01 source and the separate competition guide were not available during this work.
- A public video and final submission package are still needed.
- The participant must personally review and accept the competition agreement if required.

See the [submission checklist](submission-checklist.md) for remaining work.
