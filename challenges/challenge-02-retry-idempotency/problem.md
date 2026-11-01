# Retry Idempotency Engine

## Problem

A client sends a wallet transfer request to a financial system. The transfer may complete even when the response is lost, causing the client to retry. Process the ordered requests so that a retry of an already accepted request does not execute the transfer twice.

Each request has a timestamp, client ID, idempotency key, source account, destination account, and amount. Requests are processed in input order. Timestamps are non-decreasing; input order breaks ties. This is a deterministic simulation and does not use concurrent threads.

The effective idempotency key is the pair `(clientId, idempotencyKey)`. Both identifiers are case-sensitive. Keys used by different clients are independent.

The payload is exactly `(source account, destination account, amount)`. Timestamp is not part of the payload.

The system has one positive global TTL. A structurally valid new request claims its key until `creation timestamp + TTL`. The record is active only while `current timestamp < expiration timestamp`; it expires at the inclusive boundary `current timestamp >= expiration timestamp`. Expiration is fixed from the original request and is not extended by retries or conflicts. Once expired, the key can be reused.

## Processing rules

For each request, apply these rules in order:

1. Expire every record whose expiration timestamp is less than or equal to this request's timestamp.
2. Look up the composite key.
3. If an active record exists, compare payloads before validating the incoming account or amount fields:
   - Identical payload: return the stored outcome as `REPLAY_SUCCESS` or `REPLAY_INSUFFICIENT_FUNDS`. Do not change balances or expiration.
   - Different payload: return `KEY_CONFLICT`. Do not change balances or the original record.
4. If there is no active record, the request is structurally valid only if both accounts exist, the accounts differ, and amount is strictly positive. Otherwise return `INVALID`; do not change balances or claim the key.
5. For a structurally valid new request:
   - If the source balance is at least the amount, transfer the amount and store a successful outcome. Return `SUCCESS`.
   - Otherwise leave balances unchanged, store the insufficient-funds outcome, and return `INSUFFICIENT_FUNDS`.

An insufficient-funds outcome is terminal for that active key. An identical retry replays the original failure even if the source account has received funds since then. After expiration, a new request with that key is evaluated against current balances.

## Input format

The first line contains `N Q TTL`: number of accounts, number of requests, and global time-to-live.

The next `N` lines each contain `accountId initialBalance`.

The next `Q` lines each contain:

```text
timestamp clientId idempotencyKey sourceAccount destinationAccount amount
```

All identifiers are whitespace-free tokens.

## Output format

Print exactly `Q` status lines, one for each request in input order. Then print a blank line followed by one line for each account in its original input order:

```text
accountId finalBalance
```

Use only the six statuses defined below. Do not print diagnostics to standard output.

| Status | Meaning |
|---|---|
| `INVALID` | Structurally invalid new request |
| `SUCCESS` | New transfer executed |
| `INSUFFICIENT_FUNDS` | New valid request rejected for insufficient funds |
| `REPLAY_SUCCESS` | Previously stored successful outcome replayed |
| `REPLAY_INSUFFICIENT_FUNDS` | Previously stored insufficient-funds outcome replayed |
| `KEY_CONFLICT` | Active key reused with a different payload |

## Public samples

### Sample A — identical retry

Input:

```text
2 2 10
wallet-a 10000
wallet-b 0
0 mobile transfer-1 wallet-a wallet-b 5000
3 mobile transfer-1 wallet-a wallet-b 5000
```

Output:

```text
SUCCESS
REPLAY_SUCCESS

wallet-a 5000
wallet-b 5000
```

### Sample B — conflicting payload

Input:

```text
2 2 10
wallet-a 10000
wallet-b 0
0 mobile transfer-2 wallet-a wallet-b 3000
1 mobile transfer-2 wallet-a wallet-b 4000
```

Output:

```text
SUCCESS
KEY_CONFLICT

wallet-a 7000
wallet-b 3000
```

### Sample C — cached insufficient funds

Input:

```text
2 3 5
wallet-a 0
wallet-b 5
0 mobile transfer-3 wallet-a wallet-b 5
2 mobile funding wallet-b wallet-a 5
4 mobile transfer-3 wallet-a wallet-b 5
```

Output:

```text
INSUFFICIENT_FUNDS
SUCCESS
REPLAY_INSUFFICIENT_FUNDS

wallet-a 5
wallet-b 0
```

### Sample D — expiration boundary

Input:

```text
2 2 5
wallet-a 100
wallet-b 0
0 mobile transfer-4 wallet-a wallet-b 40
5 mobile transfer-4 wallet-a wallet-b 40
```

Output:

```text
SUCCESS
SUCCESS

wallet-a 20
wallet-b 80
```

### Sample E — invalid requests do not reserve a key

Input:

```text
2 3 10
wallet-a 100
wallet-b 0
0 mobile transfer-5 wallet-a wallet-b 0
1 mobile transfer-5 wallet-a wallet-b -1
2 mobile transfer-5 wallet-a wallet-b 10
```

Output:

```text
INVALID
INVALID
SUCCESS

wallet-a 90
wallet-b 10
```
