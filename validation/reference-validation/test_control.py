import itertools
import random
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "reference-solutions" / "transaction-collapse-control" / "Main.java"


def brute_force(values, max_length):
    total = sum(values)
    best = total
    for left in range(len(values)):
        removed = 0
        for right in range(left, min(len(values), left + max_length)):
            removed += values[right]
            best = max(best, total - removed)
    return best


class ControlReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory(prefix="control-classes-")
        compile_result = subprocess.run(
            ["javac", "--release", "17", "-d", cls.temp_dir.name, str(SOURCE)],
            text=True,
            capture_output=True,
            check=False,
        )
        if compile_result.returncode:
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
        if harness_compile.returncode:
            raise RuntimeError(f"javac harness failed:\n{harness_compile.stderr}")

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def run_batch(self, cases):
        lines = [str(len(cases))]
        for values, max_length in cases:
            lines.extend((f"{len(values)} {max_length}", " ".join(map(str, values))))
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

    def test_examples(self):
        self.assertEqual(self.run_batch([([-2, 5, -10], 3), ([3, -4, 2, 0], 0)]), [3, 1])

    def test_exhaustive_and_seeded_random_against_brute_force(self):
        cases = []
        for size in range(1, 4):
            for values in itertools.product((-2, -1, 0, 1, 2), repeat=size):
                if not any(value > 0 for value in values):
                    continue
                cases.extend((list(values), k) for k in range(size + 1))

        rng = random.Random(20261101)
        for _ in range(120):
            size = rng.randint(1, 10)
            values = [rng.randint(-12, 12) for _ in range(size)]
            values[rng.randrange(size)] = rng.randint(1, 12)
            cases.append((values, rng.randint(0, size)))

        self.assertEqual(
            self.run_batch(cases),
            [brute_force(values, k) for values, k in cases],
        )

    def test_maximum_input_size(self):
        values = [1_000_000_000, -1_000_000_000] * 100_000
        self.assertEqual(self.run_batch([(values, len(values))]), [1_000_000_000])


if __name__ == "__main__":
    unittest.main()
