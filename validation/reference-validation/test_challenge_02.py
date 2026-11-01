import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "evaluator"))
from grading import load_test_cases


ROOT = Path(__file__).resolve().parents[2]
CHALLENGE = ROOT / "challenges" / "challenge-02-retry-idempotency"
SOURCE = ROOT / "reference-solutions" / "challenge-02" / "Main.java"


def oracle(account_ids, initial_balances, ttl, requests):
    balances = dict(zip(account_ids, initial_balances))
    active = {}
    statuses = []
    initial_total = sum(initial_balances)

    for timestamp, client, key, source, destination, amount in requests:
        for composite in [
            composite for composite, record in active.items()
            if record["expires_at"] <= timestamp
        ]:
            del active[composite]

        composite = (client, key)
        payload = (source, destination, amount)
        existing = active.get(composite)
        if existing is not None:
            if existing["payload"] != payload:
                statuses.append("KEY_CONFLICT")
            elif existing["outcome"] == "SUCCESS":
                statuses.append("REPLAY_SUCCESS")
            else:
                statuses.append("REPLAY_INSUFFICIENT_FUNDS")
            continue

        if (
            source not in balances
            or destination not in balances
            or source == destination
            or amount <= 0
        ):
            statuses.append("INVALID")
            continue

        if balances[source] >= amount:
            balances[source] -= amount
            balances[destination] += amount
            outcome = "SUCCESS"
        else:
            outcome = "INSUFFICIENT_FUNDS"
        active[composite] = {
            "payload": payload,
            "outcome": outcome,
            "expires_at": timestamp + ttl,
        }
        statuses.append(outcome)

    assert sum(balances.values()) == initial_total
    expected = statuses + [""]
    expected.extend(f"{account} {balances[account]}" for account in account_ids)
    return "\n".join(expected) + "\n"


def encode_input(account_ids, initial_balances, ttl, requests):
    lines = [f"{len(account_ids)} {len(requests)} {ttl}"]
    lines.extend(
        f"{account} {balance}" for account, balance in zip(account_ids, initial_balances)
    )
    lines.extend(
        f"{timestamp} {client} {key} {source} {destination} {amount}"
        for timestamp, client, key, source, destination, amount in requests
    )
    return "\n".join(lines) + "\n"


def decode_input(input_text):
    tokens = input_text.split()
    account_count, request_count, ttl = map(int, tokens[:3])
    cursor = 3
    account_ids = []
    initial_balances = []
    for _ in range(account_count):
        account_ids.append(tokens[cursor])
        initial_balances.append(int(tokens[cursor + 1]))
        cursor += 2
    requests = []
    for _ in range(request_count):
        timestamp, client, key, source, destination, amount = tokens[cursor : cursor + 6]
        requests.append(
            (int(timestamp), client, key, source, destination, int(amount))
        )
        cursor += 6
    if cursor != len(tokens):
        raise AssertionError("fixture contains trailing tokens")
    return account_ids, initial_balances, ttl, requests


class Challenge02ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory(prefix="challenge02-classes-")
        cls.class_dir = Path(cls.temp_dir.name)
        cls.compile_source(SOURCE.read_text(encoding="utf-8"), cls.class_dir)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    @staticmethod
    def compile_source(source, class_dir):
        source_file = class_dir / "Main.java"
        source_file.write_text(source, encoding="utf-8")
        result = subprocess.run(
            ["javac", "--release", "17", "-d", str(class_dir), str(source_file)],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise AssertionError(f"javac failed:\n{result.stderr}")

    def run_program(self, input_text, class_dir=None, class_name="Main"):
        result = subprocess.run(
            ["java", "-cp", str(class_dir or self.class_dir), class_name],
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_public_samples(self):
        for sample in "abcde":
            with self.subTest(sample=sample):
                input_text = (
                    CHALLENGE / "tests" / "samples" / f"sample-{sample}.in"
                ).read_text(encoding="utf-8")
                expected = (
                    CHALLENGE
                    / "tests"
                    / "expected-outputs"
                    / f"sample-{sample}.out"
                ).read_text(encoding="utf-8")
                account_ids, balances, ttl, requests = decode_input(input_text)
                self.assertEqual(expected, oracle(account_ids, balances, ttl, requests))
                self.assertEqual(self.run_program(input_text), expected)

    def test_all_weighted_small_fixtures(self):
        cases = load_test_cases(CHALLENGE / "test-cases" / "core.json")
        self.assertEqual(len(cases), 21)
        self.assertEqual(sum(case["weight"] for case in cases), 100)
        small_cases = [case for case in cases if case["category"] != "performance"]
        for case in small_cases:
            with self.subTest(test_id=case["id"]):
                account_ids, balances, ttl, requests = decode_input(case["input"])
                self.assertEqual(
                    case["expected_output"],
                    oracle(account_ids, balances, ttl, requests),
                )
                self.assertEqual(self.run_program(case["input"]), case["expected_output"])

    def test_seeded_random_sequences_against_independent_oracle(self):
        rng = random.Random(20261101)
        account_ids = [f"a{i}" for i in range(5)]
        initial = [rng.randint(0, 40) for _ in account_ids]
        ttl = 7
        requests = []
        timestamp = 0
        clients = ["Client", "client", "other"]
        keys = ["k", "K", "x", "k"]
        references = account_ids + ["missing"]
        for _ in range(500):
            timestamp += rng.randint(0, 2)
            requests.append(
                (
                    timestamp,
                    rng.choice(clients),
                    rng.choice(keys),
                    rng.choice(references),
                    rng.choice(references),
                    rng.randint(-3, 50),
                )
            )
        actual = self.run_program(encode_input(account_ids, initial, ttl, requests))
        expected = oracle(account_ids, initial, ttl, requests)
        self.assertEqual(actual, expected)

    def test_stale_expiration_event_cannot_delete_newer_record(self):
        harness_source = """public class StaleExpirationHarness {
    public static void main(String[] args) {
        Main.Engine engine = new Main.Engine(
                new String[] {"a", "b"}, new long[] {10, 0}, 5);
        Main.IdempotencyKey key = new Main.IdempotencyKey("client", "key");
        Main.Payload payload = new Main.Payload(0, 1, 1);
        Main.IdempotencyRecord current =
                new Main.IdempotencyRecord(payload, Main.Outcome.SUCCESS, 20, 2);
        engine.activeRecords.put(key, current);
        engine.expirations.add(new Main.ExpirationEvent(key, 10, 1));
        engine.expire(10);
        if (engine.activeRecords.get(key) != current) {
            throw new AssertionError("stale expiration deleted the newer record");
        }
        System.out.println("retained");
    }
}
"""
        harness = self.class_dir / "StaleExpirationHarness.java"
        harness.write_text(harness_source, encoding="utf-8")
        result = subprocess.run(
            [
                "javac",
                "--release",
                "17",
                "-cp",
                str(self.class_dir),
                "-d",
                str(self.class_dir),
                str(harness),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.run_program("", class_name="StaleExpirationHarness"), "retained\n")

    def test_mutation_suite_detects_seven_known_bugs(self):
        original = SOURCE.read_text(encoding="utf-8")
        fixtures = {
            case["id"]: case
            for case in load_test_cases(CHALLENGE / "test-cases" / "core.json")
        }
        replay_branch = (
            'return existing.outcome == Outcome.SUCCESS\n'
            '                        ? "REPLAY_SUCCESS"\n'
            '                        : "REPLAY_INSUFFICIENT_FUNDS";'
        )
        invalid_return = """return "INVALID";"""
        stale_guard = """if (current != null
                        && current.generation == event.generation
                        && current.expiresAt == event.expiresAt)"""

        mutations = {
            "refreshes TTL on retry": (
                original.replace(
                    replay_branch,
                    "remember(key, existing.payload, existing.outcome, timestamp);\n"
                    + replay_branch,
                    1,
                ),
                "retries-do-not-extend-ttl",
            ),
            "treats TTL equality as active": (
                original.replace(
                    "expirations.peek().expiresAt <= timestamp",
                    "expirations.peek().expiresAt < timestamp",
                    1,
                ),
                "fixed-boundary",
            ),
            "ignores client ID in key scope": (
                original.replace(
                    "new IdempotencyKey(clientId, keyValue)",
                    'new IdempotencyKey("", keyValue)',
                    1,
                ),
                "client-scope",
            ),
            "re-executes cached insufficient funds": (
                original.replace(
                    replay_branch,
                    """if (existing.outcome == Outcome.INSUFFICIENT_FUNDS) {
                    balances[existing.payload.source] -= existing.payload.amount;
                    balances[existing.payload.destination] += existing.payload.amount;
                }
                """ + replay_branch,
                    1,
                ),
                "cached-failure-after-funding",
            ),
            "accepts conflicting payloads": (
                original.replace(
                    "if (!existing.payload.equals(incoming))",
                    "if (false)",
                    1,
                ),
                "payload-conflicts",
            ),
            "caches invalid new requests": (
                original.replace(
                    invalid_return,
                    """remember(key, payloadFor(sourceId, destinationId, amount),
                        Outcome.INSUFFICIENT_FUNDS, timestamp);
                return "INVALID";""",
                    1,
                ),
                "invalid-does-not-reserve",
            ),
            "lets stale events delete by key only": (
                original.replace(stale_guard, "if (current != null)", 1),
                "stale-expiration-harness",
            ),
        }

        for description, (mutant, test_id) in mutations.items():
            with self.subTest(mutation=description):
                self.assertNotEqual(mutant, original, f"mutation was not applied: {description}")
                with tempfile.TemporaryDirectory(prefix="challenge02-mutant-") as directory:
                    class_dir = Path(directory)
                    self.compile_source(mutant, class_dir)
                    if test_id == "stale-expiration-harness":
                        harness = self.class_dir / "StaleExpirationHarness.java"
                        result = subprocess.run(
                            [
                                "java",
                                "-cp",
                                f"{class_dir}:{self.class_dir}",
                                "StaleExpirationHarness",
                            ],
                            text=True,
                            capture_output=True,
                            check=False,
                        )
                        self.assertNotEqual(result.returncode, 0, result.stdout)
                    else:
                        case = fixtures[test_id]
                        actual = self.run_program(case["input"], class_dir=class_dir)
                        self.assertNotEqual(
                            actual,
                            case["expected_output"],
                            f"mutation survived: {description}",
                        )


if __name__ == "__main__":
    unittest.main()
