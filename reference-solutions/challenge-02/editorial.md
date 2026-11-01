# Editorial: Retry Idempotency Engine

## Why idempotency needs stored outcomes

A client may retry after a successful operation whose response was lost. Remembering only that a key was seen is insufficient: the server must distinguish an identical retry from a conflicting payload and replay the original terminal outcome. Insufficient funds is also terminal for the active key. Rechecking the balance on a retry could turn the original rejection into an unintended later transfer.

## Data structures

- `accountIndexes`: hash map from account ID to its index in the balance array.
- `activeRecords`: hash map from `(clientId, idempotencyKey)` to the claimed payload, outcome, expiration, and generation.
- `expirations`: min-priority queue of expiration events ordered by expiration timestamp.
- Each payload stores the resolved source and destination account indices plus the amount.

Java record equality and hashing provide exact, case-sensitive composite-key and payload comparisons. Timestamps are not payload fields.

Each new valid request, including one rejected for insufficient funds, gets a unique generation value. Its queue event carries the same key, expiration, and generation. On expiry, the event removes a map entry only if both generation and expiration still match. The identity guard prevents an obsolete event from deleting a newer record if stale events exist.

With the required operation order (drain all expired events before each request), an ordinary sequential execution removes a key's old event before that same key can be reused. Thus the stale-event interleaving is defensive against stale/duplicate events, not normally reachable through the public input semantics. The validation harness injects such an event directly to verify the identity guard.

## Algorithm

For every request `(t, client, key, source, destination, amount)`:

```text
while expiration queue is not empty and queue.minimum.expiration <= t:
    event = remove queue.minimum
    current = activeRecords[event.key]
    if current exists and current.generation == event.generation
       and current.expiration == event.expiration:
        remove activeRecords[event.key]

key = (client, idempotencyKey)
if activeRecords contains key:
    if incoming (source, destination, amount) differs from stored payload:
        output KEY_CONFLICT
    else if stored outcome is success:
        output REPLAY_SUCCESS
    else:
        output REPLAY_INSUFFICIENT_FUNDS
    continue

resolve source and destination
if either is unknown, they are equal, or amount <= 0:
    output INVALID
    continue

if source balance >= amount:
    subtract amount from source and add it to destination
    outcome = SUCCESS
else:
    outcome = INSUFFICIENT_FUNDS

expiration = t + TTL
generation = next unique generation
store key, payload, outcome, expiration, generation
insert corresponding expiration event
output outcome
```

## Correctness argument

**Expiration before lookup.** Every event with expiration at most the current timestamp is removed before the key is examined. Therefore a request exactly at expiration observes no old active record and can claim the key anew. Events with later expiration remain active.

**Composite scope.** The map key contains both client ID and idempotency key, so identical key strings from different clients occupy independent records. String equality is case-sensitive.

**`KEY_CONFLICT`.** For an active composite key, the stored payload is compared before structural validation. A mismatch returns conflict without executing, overwriting, or extending the record, as required.

**`REPLAY_SUCCESS`.** If the active key and all three payload fields match a stored successful outcome, the saved outcome is returned without applying balances again or changing expiration.

**`REPLAY_INSUFFICIENT_FUNDS`.** If the matching record stores insufficient funds, that saved terminal outcome is replayed. Later balance changes do not cause the request to be re-executed.

**`INVALID`.** With no active record, unknown accounts, equal accounts, or non-positive amount are rejected before state mutation or record creation. Therefore the key remains available for a later valid request.

**`SUCCESS`.** A valid request whose source balance covers the amount subtracts and adds the same positive amount, preserving total funds. The resulting outcome and exact payload are stored before the next request can run.

**`INSUFFICIENT_FUNDS`.** A valid request whose source balance is too small changes neither balance, but its payload and rejection are stored. This makes later identical retries replay consistently.

**Stale expiration safety.** An expiration event can remove only the record with matching generation and expiration. A stale event whose key has since acquired a newer generation cannot delete that newer record.

These cases exhaust the ordered processing rules and establish that each output status matches the specified state transition.

## Complexity

Account and composite-key map operations are expected `O(1)`. Each valid new request inserts one expiration event; each event is removed at most once, with `O(log Q)` heap cost. Across all requests, expiration work is `O(Q log Q)`, so total expected time is `O(N + Q log Q)` (commonly bounded as `O((N + Q) log Q)`). Accounts, active records, and not-yet-consumed queue events use `O(N + Q)` auxiliary space.

## Common incorrect solutions

- Keying only by idempotency token and accidentally sharing state across clients.
- Including timestamp in the payload, so a legitimate retry conflicts.
- Comparing only amount and overlooking source or destination changes.
- Checking validity before checking an existing key, violating conflict precedence.
- Caching invalid requests and preventing later valid use of that key.
- Re-executing an insufficient-funds retry after the account balance changes.
- Refreshing expiration on replay or conflict (sliding rather than fixed TTL).
- Using `>` rather than `>=` at the expiration boundary.
- Deleting a map entry based only on key when handling a stale queue event.
- Using `int` for timestamps, balances, or amounts.
- Mutating one balance before determining that the transfer is valid or sufficiently funded.
