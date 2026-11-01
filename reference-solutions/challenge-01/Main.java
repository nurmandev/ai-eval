import java.io.BufferedInputStream;
import java.io.IOException;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    private static final class FastScanner {
        private final BufferedInputStream in = new BufferedInputStream(System.in);

        private int nextInt() throws IOException {
            int c;
            do {
                c = in.read();
            } while (c <= ' ' && c != -1);
            if (c == -1) {
                throw new IOException("Unexpected end of input");
            }

            int sign = 1;
            if (c == '-') {
                sign = -1;
                c = in.read();
            }

            int value = 0;
            while (c > ' ') {
                if (c < '0' || c > '9') {
                    throw new IOException("Invalid integer input");
                }
                value = value * 10 + c - '0';
                c = in.read();
            }
            return value * sign;
        }
    }

    private static long minimumSubarraySum(long[] prefix, int start, int end, int maxLength) {
        if (start > end || maxLength == 0) {
            return Long.MAX_VALUE;
        }

        Deque<Integer> candidates = new ArrayDeque<>();
        long minimum = Long.MAX_VALUE;
        for (int rightPrefix = start + 1; rightPrefix <= end + 1; rightPrefix++) {
            int newPrefix = rightPrefix - 1;
            while (!candidates.isEmpty()
                    && prefix[candidates.peekLast()] <= prefix[newPrefix]) {
                candidates.removeLast();
            }
            candidates.addLast(newPrefix);

            int earliestAllowed = rightPrefix - maxLength;
            while (!candidates.isEmpty() && candidates.peekFirst() < earliestAllowed) {
                candidates.removeFirst();
            }
            minimum = Math.min(minimum, prefix[rightPrefix] - prefix[candidates.peekFirst()]);
        }
        return minimum;
    }

    static long solve(int[] values, int k) {
        int n = values.length;
        long[] prefix = new long[n + 1];
        int firstPositive = -1;
        int lastPositive = -1;

        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + values[i];
            if (values[i] > 0) {
                if (firstPositive == -1) {
                    firstPositive = i;
                }
                lastPositive = i;
            }
        }

        if (firstPositive == -1) {
            throw new IllegalArgumentException("At least one positive value is required");
        }

        long total = prefix[n];
        long bestRemoval = 0;
        if (k > 0) {
            // A valid interval cannot contain both the first and last positive values.
            long prefixRemoval = minimumSubarraySum(prefix, 0, lastPositive - 1, k);
            long suffixRemoval = minimumSubarraySum(prefix, firstPositive + 1, n - 1, k);
            bestRemoval = Math.min(bestRemoval, Math.min(prefixRemoval, suffixRemoval));
        }

        return total - bestRemoval;
    }

    public static void main(String[] args) throws Exception {
        FastScanner scanner = new FastScanner();
        int n = scanner.nextInt();
        int k = scanner.nextInt();
        int[] values = new int[n];
        for (int i = 0; i < n; i++) {
            values[i] = scanner.nextInt();
        }
        System.out.println(solve(values, k));
    }
}
