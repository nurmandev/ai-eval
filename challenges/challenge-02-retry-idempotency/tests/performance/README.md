# Generated maximum-size cases

The evaluator's hidden manifest contains two deterministic generators instead of checked-in multi-megabyte files:

- `idempotency_unique_max`: 200,000 accounts and 200,000 unique successful keys.
- `idempotency_reuse_max`: 200,000 requests, one repeated key, and expiration/reuse every two requests.

The Python-standard-library loader expands each descriptor to full stdin and expected stdout before grading. Generator definitions and their exact output formulas are in `test-cases/core.json` and `evaluator/grading.py`; neither is included in prompts sent to models.
