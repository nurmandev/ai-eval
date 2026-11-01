import random
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "reference-solutions" / "challenge-01" / "Main.java"


def brute_force(values, max_length):
    if not any(value > 0 for value in values):
        raise ValueError("The task guarantees at least one positive value")

    total = sum(values)
    best = total
    for left in range(len(values)):
        removed = 0
        for right in range(left, min(len(values), left + max_length)):
            removed += values[right]
            remaining = values[:left] + values[right + 1 :]
            if any(value > 0 for value in remaining):
                best = max(best, total - removed)
    return best


class Challenge01ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory(prefix="challenge01-classes-")
        compile_result = subprocess.run(
            ["javac", "--release", "17", "-d", cls.temp_dir.name, str(SOURCE)],
            text=True,
            capture_output=True,
            check=False,
        )
        if compile_result.returncode != 0:
            raise RuntimeError(f"javac failed:\n{compile_result.stderr}")
        harness = Path(cls.temp_dir.name) / "BatchHarness.java"
        harness.write_text(
            """import java.util.Scanner;
public class BatchHarness {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int count = in.nextInt();
        for (int test = 0; test < count; test++) {
            int n = in.nextInt();
            int k = in.nextInt();
            int[] values = new int[n];
            for (int i = 0; i < n; i++) values[i] = in.nextInt();
            System.out.println(Main.solve(values, k));
        }
    }
}
""",
            encoding="utf-8",
        )
        harness_compile = subprocess.run(
            [
                "javac",
                "--release",
                "17",
                "-cp",
                cls.temp_dir.name,
                "-d",
                cls.temp_dir.name,
                str(harness),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if harness_compile.returncode != 0:
            raise RuntimeError(f"javac harness failed:\n{harness_compile.stderr}")

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def run_solution(self, values, max_length):
        input_text = (
            f"{len(values)} {max_length}\n"
            + " ".join(map(str, values))
            + "\n"
        )
        result = subprocess.run(
            ["java", "-cp", self.temp_dir.name, "Main"],
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
            timeout=3,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return int(result.stdout.strip())

    def run_batch(self, cases):
        lines = [str(len(cases))]
        for values, max_length in cases:
            lines.append(f"{len(values)} {max_length}")
            lines.append(" ".join(map(str, values)))
        result = subprocess.run(
            ["java", "-cp", self.temp_dir.name, "BatchHarness"],
            input="\n".join(lines) + "\n",
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return [int(line) for line in result.stdout.splitlines()]

    def test_published_samples(self):
        self.assertEqual(self.run_solution([4, -5, 3, -2, 6], 3), 11)
        self.assertEqual(self.run_solution([-2, 5, -10], 3), 3)
        self.assertEqual(self.run_solution([3, -4, 2, 0], 0), 1)

    def test_keeps_the_only_positive_value(self):
        self.assertEqual(self.run_solution([-100, 7, -50], 3), -43)

    def test_rejects_removing_all_positive_values(self):
        self.assertEqual(self.run_solution([-100, 1, -100], 3), -99)

    def test_uses_64_bit_sums(self):
        values = [1_000_000_000, -1_000_000_000, 1_000_000_000]
        self.assertEqual(self.run_solution(values, 3), 2_000_000_000)

    def test_maximum_input_size(self):
        values = [1_000_000_000, -1_000_000_000] * 100_000
        self.assertEqual(self.run_solution(values, len(values)), 1_000_000_000)

    def test_seeded_random_against_independent_brute_force(self):
        rng = random.Random(20261031)
        cases = []
        for _ in range(120):
            size = rng.randint(1, 10)
            values = [rng.randint(-12, 12) for _ in range(size)]
            values[rng.randrange(size)] = rng.randint(1, 12)
            max_length = rng.randint(0, size)
            cases.append((values, max_length))
        actual = self.run_batch(cases)
        expected = [brute_force(values, k) for values, k in cases]
        self.assertEqual(actual, expected)

    def test_exhaustive_small_arrays_against_independent_brute_force(self):
        # Enumerate small arrays from {-2, -1, 0, 1, 2}, requiring a positive.
        import itertools

        cases = []
        for size in range(1, 4):
            for values in itertools.product((-2, -1, 0, 1, 2), repeat=size):
                if not any(value > 0 for value in values):
                    continue
                for max_length in range(size + 1):
                    cases.append((list(values), max_length))
        actual = self.run_batch(cases)
        expected = [brute_force(values, k) for values, k in cases]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
