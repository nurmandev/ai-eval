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

    static long solve(int[] values, int k) {
        long[] prefix = new long[values.length + 1];
        for (int i = 0; i < values.length; i++) {
            prefix[i + 1] = prefix[i] + values[i];
        }

        long minimumRemoval = 0;
        Deque<Integer> candidates = new ArrayDeque<>();
        for (int rightPrefix = 1; rightPrefix <= values.length && k > 0; rightPrefix++) {
            int newPrefix = rightPrefix - 1;
            while (!candidates.isEmpty()
                    && prefix[candidates.peekLast()] <= prefix[newPrefix]) {
                candidates.removeLast();
            }
            candidates.addLast(newPrefix);

            int earliestAllowed = rightPrefix - k;
            while (!candidates.isEmpty() && candidates.peekFirst() < earliestAllowed) {
                candidates.removeFirst();
            }
            minimumRemoval = Math.min(
                    minimumRemoval,
                    prefix[rightPrefix] - prefix[candidates.peekFirst()]
            );
        }

        return prefix[values.length] - minimumRemoval;
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
