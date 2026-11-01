# Editorial: Transaction Collapse Engine

## Key observation

Maximizing the retained sum is equivalent to minimizing the sum of the removed interval, while retaining the option to remove nothing. Thus the target is the minimum sum among all valid contiguous intervals of length at most `K`, and zero.

Let `p` and `q` be the first and last indices whose values are strictly positive. A removed interval is invalid exactly when it contains both `p` and `q`: if it does, it removes every positive value; if it does not, at least one of those endpoint positives remains.

Therefore every valid interval lies either wholly before `q` (within `[0, q-1]`) or wholly after `p` (within `[p+1, N-1]`). These ranges may overlap; that is harmless. If `p == q`, the ranges cover all positions except the sole positive element.

## Algorithm

1. Build 64-bit prefix sums.
2. In each of the two allowed index ranges, find the minimum-sum non-empty subarray with length at most `K`.
3. Use a monotonic deque of prefix-sum indices. For each right endpoint, the best left prefix is the minimum prefix among indices in the valid length window.
4. Compare the minimum valid deletion sum with zero (no deletion).
5. Subtract that chosen deletion sum from the original total.

## Correctness argument

Any valid deletion cannot contain both the first and last positive array positions, because doing so would remove every positive element. Hence it must end before the last positive or start after the first positive and is considered in one of the scanned ranges.

Conversely, an interval wholly before the last positive cannot contain that last positive, and an interval wholly after the first positive cannot contain that first positive. Every considered interval is therefore valid.

The deque returns the minimum prefix sum among exactly the left boundaries that produce non-empty intervals of length at most `K`, so it finds the minimum deletion sum in each allowed range. Taking the minimum of those candidates and zero gives the best permitted action. Subtracting the removed sum from the original total maximizes the retained sum.

## Complexity

- Time: `O(N)`.
- Auxiliary memory: `O(N)` for values and prefix sums; deque size is `O(N)`.

## Common incorrect approaches

- Finding the globally minimum-sum interval without checking whether it removes every positive value.
- Checking only whether the interval contains a positive value, rather than whether any positive value remains outside it.
- Assuming the maximum-length window is always optimal.
- Using 32-bit sums.
- Forgetting the no-deletion option when every valid interval has positive sum.
