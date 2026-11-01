import java.io.BufferedInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

public class Main {
    record IdempotencyKey(String clientId, String value) {}

    record Payload(int source, int destination, long amount) {}

    enum Outcome {
        SUCCESS,
        INSUFFICIENT_FUNDS
    }

    static final class IdempotencyRecord {
        final Payload payload;
        final Outcome outcome;
        final long expiresAt;
        final long generation;

        IdempotencyRecord(Payload payload, Outcome outcome, long expiresAt, long generation) {
            this.payload = payload;
            this.outcome = outcome;
            this.expiresAt = expiresAt;
            this.generation = generation;
        }
    }

    static final class ExpirationEvent implements Comparable<ExpirationEvent> {
        final IdempotencyKey key;
        final long expiresAt;
        final long generation;

        ExpirationEvent(IdempotencyKey key, long expiresAt, long generation) {
            this.key = key;
            this.expiresAt = expiresAt;
            this.generation = generation;
        }

        @Override
        public int compareTo(ExpirationEvent other) {
            return Long.compare(expiresAt, other.expiresAt);
        }
    }

    static final class Engine {
        final Map<String, Integer> accountIndexes = new HashMap<>();
        final String[] accountIds;
        final long[] balances;
        final long ttl;
        final Map<IdempotencyKey, IdempotencyRecord> activeRecords = new HashMap<>();
        final PriorityQueue<ExpirationEvent> expirations = new PriorityQueue<>();
        long nextGeneration;

        Engine(String[] accountIds, long[] balances, long ttl) {
            this.accountIds = accountIds;
            this.balances = balances;
            this.ttl = ttl;
            for (int i = 0; i < accountIds.length; i++) {
                accountIndexes.put(accountIds[i], i);
            }
        }

        void expire(long timestamp) {
            while (!expirations.isEmpty() && expirations.peek().expiresAt <= timestamp) {
                ExpirationEvent event = expirations.remove();
                IdempotencyRecord current = activeRecords.get(event.key);
                if (current != null
                        && current.generation == event.generation
                        && current.expiresAt == event.expiresAt) {
                    activeRecords.remove(event.key);
                }
            }
        }

        String process(
                long timestamp,
                String clientId,
                String keyValue,
                String sourceId,
                String destinationId,
                long amount) {
            expire(timestamp);

            IdempotencyKey key = new IdempotencyKey(clientId, keyValue);
            IdempotencyRecord existing = activeRecords.get(key);
            if (existing != null) {
                Payload incoming = payloadFor(sourceId, destinationId, amount);
                if (!existing.payload.equals(incoming)) {
                    return "KEY_CONFLICT";
                }
                return existing.outcome == Outcome.SUCCESS
                        ? "REPLAY_SUCCESS"
                        : "REPLAY_INSUFFICIENT_FUNDS";
            }

            Integer source = accountIndexes.get(sourceId);
            Integer destination = accountIndexes.get(destinationId);
            if (amount <= 0
                    || source == null
                    || destination == null
                    || source.equals(destination)) {
                return "INVALID";
            }

            Payload payload = new Payload(source, destination, amount);
            Outcome outcome;
            if (balances[source] >= amount) {
                balances[source] -= amount;
                balances[destination] += amount;
                outcome = Outcome.SUCCESS;
            } else {
                outcome = Outcome.INSUFFICIENT_FUNDS;
            }
            remember(key, payload, outcome, timestamp);
            return outcome == Outcome.SUCCESS ? "SUCCESS" : "INSUFFICIENT_FUNDS";
        }

        private Payload payloadFor(String sourceId, String destinationId, long amount) {
            Integer source = accountIndexes.get(sourceId);
            Integer destination = accountIndexes.get(destinationId);
            return new Payload(
                    source == null ? -1 : source,
                    destination == null ? -1 : destination,
                    amount);
        }

        private void remember(
                IdempotencyKey key, Payload payload, Outcome outcome, long timestamp) {
            long expiresAt = timestamp + ttl;
            long generation = nextGeneration++;
            activeRecords.put(
                    key, new IdempotencyRecord(payload, outcome, expiresAt, generation));
            expirations.add(new ExpirationEvent(key, expiresAt, generation));
        }
    }

    private static final class FastScanner {
        private final BufferedInputStream input = new BufferedInputStream(System.in);
        private final byte[] buffer = new byte[1 << 16];
        private final byte[] tokenBuffer = new byte[256];
        private int position;
        private int limit;

        private int read() throws IOException {
            if (position == limit) {
                limit = input.read(buffer);
                position = 0;
                if (limit == -1) {
                    return -1;
                }
            }
            return buffer[position++] & 0xff;
        }

        String next() throws IOException {
            int current;
            do {
                current = read();
            } while (current <= ' ' && current != -1);
            if (current == -1) {
                throw new IOException("Unexpected end of input");
            }

            int length = 0;
            while (current > ' ') {
                if (length == tokenBuffer.length) {
                    throw new IOException("Identifier token exceeds the supported length");
                }
                tokenBuffer[length++] = (byte) current;
                current = read();
            }
            return new String(tokenBuffer, 0, length, StandardCharsets.UTF_8);
        }

        long nextLong() throws IOException {
            String token = next();
            try {
                return Long.parseLong(token);
            } catch (NumberFormatException error) {
                throw new IOException("Invalid integer token", error);
            }
        }

        int nextInt() throws IOException {
            return Math.toIntExact(nextLong());
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner scanner = new FastScanner();
        int accountCount = scanner.nextInt();
        int requestCount = scanner.nextInt();
        long ttl = scanner.nextLong();

        String[] accountIds = new String[accountCount];
        long[] balances = new long[accountCount];
        for (int i = 0; i < accountCount; i++) {
            accountIds[i] = scanner.next();
            balances[i] = scanner.nextLong();
        }

        Engine engine = new Engine(accountIds, balances, ttl);
        StringBuilder output = new StringBuilder(requestCount * 24 + accountCount * 24);
        for (int i = 0; i < requestCount; i++) {
            long timestamp = scanner.nextLong();
            String clientId = scanner.next();
            String key = scanner.next();
            String source = scanner.next();
            String destination = scanner.next();
            long amount = scanner.nextLong();
            output.append(engine.process(
                    timestamp, clientId, key, source, destination, amount));
            output.append('\n');
        }

        output.append('\n');
        for (int i = 0; i < accountCount; i++) {
            output.append(accountIds[i]).append(' ').append(balances[i]).append('\n');
        }
        System.out.print(output);
    }
}
