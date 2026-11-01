import unittest
from pathlib import Path
import os
import json
import tempfile
from unittest.mock import patch

from grading import extract_java_source, load_test_cases, run_java
from adapters import generate
from reporting import build_report, wilson_interval


ROOT = Path(__file__).resolve().parents[1]


class GradingUnitTests(unittest.TestCase):
    def test_wilson_interval_reports_uncertainty(self):
        interval = wilson_interval(3, 3)
        self.assertAlmostEqual(interval[0], 0.4385, places=3)
        self.assertEqual(interval[1], 1.0)
        self.assertIsNone(wilson_interval(0, 0))

    def test_report_marks_missing_runs_as_not_run(self):
        with tempfile.TemporaryDirectory() as directory:
            report = build_report(directory)
            self.assertEqual(report["status"], "NOT RUN")
            self.assertEqual(report["graded_model_runs"], 0)
            self.assertIn("NOT RUN", (Path(directory) / "final-report.md").read_text())

    def test_report_pairs_control_and_experimental_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "raw-outputs"
            output.mkdir()
            for task_id, score in (
                ("version-a-control", 100),
                ("version-b-experimental", 95),
            ):
                record = {
                    "provider": "fixture",
                    "model_id": "fixture-model",
                    "task_id": task_id,
                    "run_number": 1,
                    "grading": {"compiled": True, "passed_weight": score},
                }
                (output / f"{task_id}.json").write_text(json.dumps(record), encoding="utf-8")
            aggregate = build_report(directory)
            paired = aggregate["paired_comparison"][0]
            self.assertEqual(paired["matched_graded_runs"], 1)
            self.assertEqual(paired["mean_score_delta_b_minus_a"], -5)
            self.assertEqual(paired["control_only_accepts"], 1)

    def test_extracts_java_fence(self):
        response = "Explanation\n```java\npublic class Main {}\n```\n"
        self.assertEqual(extract_java_source(response), "public class Main {}")

    def test_accepts_plain_source(self):
        source = "public class Main { public static void main(String[] args) {} }"
        self.assertEqual(extract_java_source(source), source)

    def test_rejects_missing_java_fence(self):
        with self.assertRaises(ValueError):
            extract_java_source("```python\nprint('not Java')\n```")

    def test_loads_weighted_pilot_tests(self):
        tests = load_test_cases(
            ROOT / "challenges" / "challenge-01-transaction-collapse" / "test-cases" / "core.json"
        )
        self.assertEqual(sum(case["weight"] for case in tests), 100)
        stress = next(case for case in tests if case["category"] == "performance")
        self.assertEqual(len(stress["input"].split()), 200002)

        control_tests = load_test_cases(
            ROOT / "tasks" / "transaction-collapse-control" / "test-cases" / "core.json"
        )
        self.assertEqual(sum(case["weight"] for case in control_tests), 100)
        experimental_by_id = {case["id"]: case for case in tests}
        control_by_id = {case["id"]: case for case in control_tests}
        self.assertEqual(set(experimental_by_id), set(control_by_id))
        for test_id in experimental_by_id:
            for field in ("category", "input", "weight"):
                self.assertEqual(
                    experimental_by_id[test_id][field],
                    control_by_id[test_id][field],
                    (test_id, field),
                )
        changed_outputs = {
            test_id
            for test_id in experimental_by_id
            if experimental_by_id[test_id]["expected_output"]
            != control_by_id[test_id]["expected_output"]
        }
        self.assertEqual(
            changed_outputs,
            {
                "edge-single-positive",
                "adversarial-preserve-positive",
            },
        )

    def test_loads_challenge02_weighted_tests_and_generators(self):
        challenge = ROOT / "challenges" / "challenge-02-retry-idempotency"
        tests = load_test_cases(challenge / "test-cases" / "core.json")
        self.assertEqual(len(tests), 21)
        self.assertEqual(sum(case["weight"] for case in tests), 100)
        category_weights = {}
        for case in tests:
            category_weights[case["category"]] = (
                category_weights.get(case["category"], 0) + case["weight"]
            )
        self.assertEqual(
            category_weights,
            {
                "core": 25,
                "conflicts": 20,
                "expiration": 25,
                "adversarial": 20,
                "performance": 10,
            },
        )
        unique = next(case for case in tests if case["id"] == "max-unique-accounts-and-keys")
        self.assertEqual(len(unique["input"].splitlines()), 400001)
        self.assertTrue(unique["expected_output"].startswith("SUCCESS\n"))
        repeated = next(case for case in tests if case["id"] == "max-reused-key-expiration")
        self.assertEqual(repeated["input"].splitlines()[0], "2 200000 1")
        self.assertEqual(repeated["expected_output"].splitlines()[-2:], ["a 100000", "b 100000"])

    def test_challenge02_prompt_contains_only_public_problem(self):
        from main import make_prompt

        task_path = ROOT / "challenges" / "challenge-02-retry-idempotency"
        prompt = make_prompt(task_path)
        self.assertIn("Retry Idempotency Engine", prompt)
        self.assertNotIn("max-unique-accounts-and-keys", prompt)
        self.assertNotIn("Editorial:", prompt)

    def test_sandboxed_grader_runs_challenge02_weighted_suite(self):
        challenge = ROOT / "challenges" / "challenge-02-retry-idempotency"
        source = (ROOT / "reference-solutions" / "challenge-02" / "Main.java").read_text(
            encoding="utf-8"
        )
        tests = load_test_cases(challenge / "test-cases" / "core.json")
        result = run_java(source, tests)
        self.assertTrue(result["compiled"], result.get("compile_stderr"))
        self.assertEqual(len(result["tests"]), 21)
        self.assertEqual(result["passed_weight"], 100)

    def test_sandboxed_grader_reads_stdin_and_catches_mutation(self):
        source = (ROOT / "reference-solutions" / "challenge-01" / "Main.java").read_text(
            encoding="utf-8"
        )
        tests = load_test_cases(
            ROOT
            / "challenges"
            / "challenge-01-transaction-collapse"
            / "test-cases"
            / "core.json"
        )
        result = run_java(source, tests)
        self.assertTrue(result["compiled"], result.get("compile_stderr"))
        self.assertEqual(result["passed_weight"], 100)

        mutant = source.replace(
            "prefix[candidates.peekLast()] <= prefix[newPrefix]",
            "prefix[candidates.peekLast()] >= prefix[newPrefix]",
        )
        self.assertNotEqual(mutant, source)
        mutant_result = run_java(mutant, tests[:-1])
        self.assertTrue(mutant_result["compiled"], mutant_result.get("compile_stderr"))
        self.assertLess(mutant_result["passed_weight"], sum(case["weight"] for case in tests[:-1]))

    def test_sandbox_does_not_inherit_environment_secrets(self):
        os.environ["EVAL_SENTINEL_SECRET"] = "must-not-reach-generated-code"
        try:
            result = run_java(
                "public class Main { public static void main(String[] args) { "
                "System.out.println(System.getenv(\"EVAL_SENTINEL_SECRET\")); } }",
                [
                    {
                        "id": "secret-isolation",
                        "category": "security",
                        "input": "",
                        "expected_output": "null\n",
                        "weight": 100,
                    }
                ],
            )
        finally:
            os.environ.pop("EVAL_SENTINEL_SECRET", None)
        self.assertTrue(result["compiled"], result.get("compile_stderr"))
        self.assertEqual(result["passed_weight"], 100)

    def test_sandbox_enforces_wall_clock_timeout(self):
        result = run_java(
            "public class Main { public static void main(String[] args) { "
            "while (true) {} } }",
            [
                {
                    "id": "timeout",
                    "category": "runtime",
                    "input": "",
                    "expected_output": "done\n",
                    "weight": 100,
                }
            ],
            timeout_seconds=1,
        )
        self.assertTrue(result["compiled"], result.get("compile_stderr"))
        self.assertEqual(result["tests"][0]["status"], "timeout")

    def test_openai_adapter_uses_configured_credential_without_logging_it(self):
        response_body = (
            b'{"id":"request-test","output":[{"content":'
            b'[{"type":"output_text","text":"public class Main {}"}]}],"usage":{"total_tokens":1}}'
        )

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit):
                return response_body

        with patch.dict(os.environ, {"OPENAI_API_KEY": "unit-test-placeholder"}):
            with patch("adapters.urllib.request.urlopen", return_value=FakeResponse()) as mocked:
                text, request_id, usage = generate(
                    {
                        "provider": "openai",
                        "model_id": "test-model",
                        "temperature": 0,
                    },
                    "test prompt",
                )
        request = mocked.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer unit-test-placeholder")
        self.assertEqual(text, "public class Main {}")
        self.assertEqual(request_id, "request-test")
        self.assertEqual(usage["total_tokens"], 1)

    def test_anthropic_adapter_extracts_text(self):
        response_body = (
            b'{"id":"anthropic-request","content":[{"type":"text",'
            b'"text":"public class Main {}"}],"usage":{"input_tokens":2}}'
        )

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit):
                return response_body

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "unit-test-placeholder"}):
            with patch("adapters.urllib.request.urlopen", return_value=FakeResponse()):
                text, request_id, usage = generate(
                    {"provider": "anthropic", "model_id": "test-model"},
                    "test prompt",
                )
        self.assertEqual(text, "public class Main {}")
        self.assertEqual(request_id, "anthropic-request")
        self.assertEqual(usage["input_tokens"], 2)

    def test_google_adapter_extracts_text(self):
        response_body = (
            b'{"responseId":"google-request","candidates":[{"content":{"parts":'
            b'[{"text":"public class Main {}"}]}}],"usageMetadata":{"totalTokenCount":3}}'
        )

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit):
                return response_body

        with patch.dict(os.environ, {"GOOGLE_API_KEY": "unit-test-placeholder"}):
            with patch("adapters.urllib.request.urlopen", return_value=FakeResponse()):
                text, request_id, usage = generate(
                    {"provider": "google", "model_id": "test-model"},
                    "test prompt",
                )
        self.assertEqual(text, "public class Main {}")
        self.assertEqual(request_id, "google-request")
        self.assertEqual(usage["totalTokenCount"], 3)


if __name__ == "__main__":
    unittest.main()
