# Challenge 01: Transaction Collapse Engine

## Status and provenance

This is a **new pilot specification** written for this repository from the research summary. It is not a recovered copy or verified correction of the original `Challenge_1_Transaction_Collapse_Engine.txt`, which was not present in the inspected project. The samples and limits below are authored for this pilot and must not be attributed to the missing source.

## Problem

An unposted batch is represented by an array of signed integer adjustments. You may either leave the batch unchanged or remove exactly one non-empty contiguous block containing at most `K` adjustments.

Choose the action that maximizes the sum of the adjustments that remain. A removal is valid only if at least one strictly positive adjustment remains in the array after removal.

The input is guaranteed to contain at least one strictly positive adjustment.

## Input format

- The first line contains integers `N` and `K`.
- The second line contains exactly `N` integers `a1, a2, ..., aN`.

## Output format

Print one integer: the maximum possible sum after either keeping the entire array or performing one valid removal.

## Constraints

- `1 <= N <= 200000`
- `0 <= K <= N`
- `-1000000000 <= ai <= 1000000000`
- At least one `ai` is strictly positive.
- The result and all intermediate sums fit in a signed 64-bit integer.
- Target complexity: `O(N)` time and `O(N)` auxiliary memory.

## Sample 1

Input:

```text
5 3
4 -5 3 -2 6
```

Output:

```text
11
```

Explanation: Removing the single value `-5` leaves `4 + 3 - 2 + 6 = 11`, and positive values remain. No valid removal can produce a larger remaining sum.

## Sample 2

Input:

```text
3 3
-100 1 -100
```

Output:

```text
-99
```

Explanation: Removing either `-100` leaves the positive value and gives a retained sum of `-99`. Removing the whole array is invalid because no positive value would remain.

## Sample 3

Input:

```text
4 0
3 -4 2 0
```

Output:

```text
1
```

Explanation: `K = 0` permits no non-empty deletion, so the original sum is returned.

## Edge-case requirements

The implementation must handle, at minimum:

- `N = 1` with the guaranteed positive value.
- `K = 0` and `K = N`.
- Exactly one positive value.
- Positive-only arrays and arrays containing zeroes.
- Negative values at either end and between positive values.
- A tempting deletion that would remove every positive value.
- Best valid intervals of length one, length `K`, and less than `K`.
- Sums beyond 32-bit integer range.
- Maximum-size input.

## Notes

This is a deterministic sequential array problem. “Transaction” is contextual language only. The task does not model database transactions, ACID guarantees, concurrent schedules, or financial ledger operations.
