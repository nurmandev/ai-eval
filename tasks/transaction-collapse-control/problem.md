# Transaction Collapse Engine — Control Version A

## Status

This is the matched control task for the pilot experiment. It is original wording authored in this repository. It shares the input domain and objective with [Version B](../../challenges/challenge-01-transaction-collapse/problem.md); the intended substantive difference is that Version A does **not** require a positive value to remain after removal.

## Problem

An unposted batch is represented by an array of signed integer adjustments. You may either leave the batch unchanged or remove exactly one non-empty contiguous block containing at most `K` adjustments.

Choose the action that maximizes the sum of the adjustments that remain. The input is guaranteed to contain at least one strictly positive adjustment. There is no requirement that a positive adjustment remain after removal.

## Input format

- The first line contains integers `N` and `K`.
- The second line contains exactly `N` integers `a1, a2, ..., aN`.

## Output format

Print one integer: the maximum possible sum after either keeping the entire array or performing one permitted removal.

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

Explanation: Removing `-5` leaves a sum of `11`, which is better than keeping the original sum of `6`.

## Sample 2

Input:

```text
3 3
-100 1 -100
```

Output:

```text
0
```

Explanation: Removing the whole array is permitted and leaves an empty sequence with sum zero. In Version B, that removal is forbidden; the best valid answer is `-99`.

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

## Notes

“Transaction” is contextual language only. This is a deterministic sequential array problem, not database transaction processing or concurrent execution.
