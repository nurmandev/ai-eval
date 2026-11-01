# Constraints and limits

| Parameter | Limit |
|---|---:|
| Accounts `N` | `1 <= N <= 200,000` |
| Requests `Q` | `1 <= Q <= 200,000` |
| Global TTL | `1 <= TTL <= 10^18` |
| Timestamp | `0 <= timestamp <= 10^18` |
| Initial balance | `0 <= balance <= 10^15` |
| Transfer amount | `-10^15 <= amount <= 10^15` |
| Account ID length | 1 to 32 characters |
| Client ID length | 1 to 32 characters |
| Idempotency key length | 1 to 64 characters |

Additional guarantees:

- Account identifiers are unique.
- The sum of all initial balances is at most `10^15`.
- Request timestamps are non-decreasing.
- All numeric tokens are valid decimal integers representable as signed Java `long`.
- No floating-point arithmetic is needed.
- Identifiers contain no whitespace.
- There are no limits on how often a key may be retried or reused after expiration.

The maximum possible expiration time is `10^18 + 10^18 = 2 * 10^18`, below `Long.MAX_VALUE`. The sum of all balances is conserved by successful transfers and remains at most `10^15`, so individual balance updates cannot overflow a signed `long`.

## Evaluation limits

The reference and generated implementations target Java 17. The local evaluator compiles with `javac --release 17`, allows ten seconds for each test case, caps generated Java heap at 128 MiB, and uses the existing Bubblewrap execution isolation. The total-process memory target is 256 MiB; the measured reference peak includes JVM and sandbox overhead. These are evaluator settings, not additional input constraints.
