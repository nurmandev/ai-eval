# Challenge 02 validation report

## Status

The Java 17 reference compiled and passed the complete 21-case weighted suite at **100/100**. The five public samples also matched their expected output and an independent Python state-machine oracle. This is reference validation only; no AI model was called and no model result is claimed.

The validation uses OpenJDK 21.0.12.1 with `javac --release 17` and the repository's Bubblewrap runner. The test suite also compares one seeded sequence of 500 mixed requests against the independent oracle and checks all 19 non-performance manifest fixtures against it.

## Maximum-size performance

| Test | Size | Result | Elapsed | Peak RSS |
|---|---|---:|---:|---:|
| `max-unique-accounts-and-keys` | 200,000 accounts and 200,000 distinct successful keys | Passed | 4,860.529 ms | 160,612 KB |
| `max-reused-key-expiration` | 200,000 requests with fixed-TTL key expiration and reuse | Passed | 3,164.175 ms | 60,012 KB |

Elapsed time and peak resident memory are measured for the sandbox command, including JVM and sandbox startup. The generated Java heap cap is 128 MiB; the observed total process RSS motivates a 256 MiB task memory target. The first large test ran close to the former five-second wall limit, so Challenge 02 uses a ten-second per-test evaluator timeout.

## Mutation checks

Each intentionally faulty Java variant was compiled and failed its targeted fixture/harness:

| Deliberate bug | Test that detected it |
|---|---|
| Refreshes TTL on retry | `retries-do-not-extend-ttl` |
| Treats expiration equality as active | `fixed-boundary` |
| Omits client ID from the key | `client-scope` |
| Re-executes a cached insufficient-funds operation | `cached-failure-after-funding` |
| Accepts a changed payload on an active key | `payload-conflicts` |
| Caches an invalid new request | `invalid-does-not-reserve` |
| Deletes an active record using a stale key-only expiration event | Synthetic `StaleExpirationHarness` injection |

The stale-event injection is necessary because, under the public rules, draining every expired queue event before each request removes the old event before the same key can be reused. It verifies the defensive generation/expiration identity check; it is not claimed to be a reachable public-input sequence. These seven mutations are the variants tested, not a claim that the suite detects all incorrect algorithms.

## Evaluator integration

Challenge 02 is registered as `challenge-02-retry-idempotency`. The evaluator constructs the prompt from `problem.md` and the shared public prompt template; the weighted manifest, expected hidden outputs, editorial, and mutation harness are not passed to the provider. The reference-only validation writes 100/100 for all 21 cases. Live provider evaluation remains unexecuted.
