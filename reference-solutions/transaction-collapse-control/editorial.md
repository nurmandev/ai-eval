# Editorial: Control Version A

## Key observation

The retained sum equals the original sum minus the removed interval sum. Maximizing the retained sum is therefore equivalent to choosing a minimum-sum contiguous interval of length at most `K`, or choosing not to remove anything. No positive-preservation check is applied in the control.

## Algorithm

Build 64-bit prefix sums. For each right prefix index `r`, consider left prefix indices `l` satisfying `max(0, r-K) <= l < r`. The smallest interval sum ending at `r` is obtained by subtracting the largest prefix sum in that window from `prefix[r]`.

A monotonic deque maintains candidate prefix indices in decreasing prefix-sum order. Expire indices outside the length window, then compare the front candidate. Initialize the best removal sum to zero to represent no deletion.

## Correctness

Every non-empty contiguous interval of length at most `K` corresponds to one pair of prefix indices in the stated window. The deque front is the maximum prefix sum among those valid left endpoints, so its difference from `prefix[r]` is the minimum interval sum ending at `r`. Scanning all right endpoints finds the minimum permitted deletion; including zero accounts for leaving the array unchanged. Subtracting the minimum removal sum maximizes the retained sum.

## Complexity

- Time: `O(N)`.
- Auxiliary memory: `O(N)`.

## Contrast with Version B

Version B restricts intervals that would remove every positive element. Version A deliberately allows such removals. For input `-100 1 -100` with `K=3`, Version A may remove all values and return `0`; Version B must retain a positive value and returns `-99`.
