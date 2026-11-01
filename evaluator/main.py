import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import sys
import subprocess
import uuid
from pathlib import Path

from adapters import ProviderError, generate
from grading import SandboxUnavailable, extract_java_source, load_test_cases, run_java
from reporting import build_report


ROOT = Path(__file__).resolve().parents[1]
TASKS = {
    "version-a-control": {
        "task_id": "version-a-control",
        "path": ROOT / "tasks" / "transaction-collapse-control",
        "reference": ROOT / "reference-solutions" / "transaction-collapse-control" / "Main.java",
    },
    "version-b-experimental": {
        "task_id": "version-b-experimental",
        "path": ROOT / "challenges" / "challenge-01-transaction-collapse",
        "reference": ROOT / "reference-solutions" / "challenge-01" / "Main.java",
    },
}
DEFAULT_OUTPUT = Path(os.environ.get("EVAL_OUTPUT_DIR", ROOT / "results"))


def load_dotenv(path=ROOT / ".env"):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def make_prompt(task_path):
    template = (ROOT / "evaluator" / "prompts" / "challenge-prompt.md").read_text(
        encoding="utf-8"
    )
    problem = (task_path / "problem.md").read_text(encoding="utf-8")
    return template.replace("{{PROBLEM_STATEMENT}}", problem)


def load_models(config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    models = config.get("models")
    if not isinstance(models, list) or not models:
        raise ValueError(
            f"No models configured in {config_path}; add actual provider model IDs before evaluation"
        )
    names = set()
    for model in models:
        if not isinstance(model, dict):
            raise ValueError("Each model configuration must be a JSON object")
        if not re.fullmatch(r"[A-Za-z0-9._:-]+", str(model.get("name", ""))):
            raise ValueError("Each model requires a simple unique name")
        if model["name"] in names:
            raise ValueError(f"Duplicate model name: {model['name']}")
        names.add(model["name"])
        if model.get("provider") not in {"openai", "anthropic", "google"}:
            raise ValueError(f"Unsupported provider in model entry {model.get('name')!r}")
        if not isinstance(model.get("model_id"), str) or not model["model_id"].strip():
            raise ValueError(f"Missing exact model_id for {model.get('name')!r}")
        token_limit = model.get("max_output_tokens", 8192)
        if not isinstance(token_limit, int) or token_limit < 1:
            raise ValueError(f"Invalid max_output_tokens for {model['name']!r}")
        temperature = model.get("temperature", 0)
        if temperature is not None and (
            not isinstance(temperature, (int, float)) or not 0 <= temperature <= 2
        ):
            raise ValueError(f"Invalid temperature for {model['name']!r}")
    return models


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command_version(command):
    try:
        result = subprocess.run(
            [command, "--version"],
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8"},
        )
        return (result.stdout or result.stderr).splitlines()[0]
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable"


def java_commands():
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        return str(Path(java_home) / "bin" / "java"), str(Path(java_home) / "bin" / "javac")
    return shutil.which("java") or "java", shutil.which("javac") or "javac"


def command_validate(args):
    java, javac = java_commands()
    names = list(TASKS) if args.task == "all" else [args.task]
    results = {}
    for name in names:
        task = TASKS[name]
        source = task["reference"].read_text(encoding="utf-8")
        tests = load_test_cases(task["path"] / "test-cases" / "core.json")
        results[name] = run_java(source, tests, java=java, javac=javac)
    validation_record = {
        "status": "REFERENCE_VALIDATION_ONLY",
        "is_model_evaluation": False,
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "java_runtime": command_version(java),
        "java_compiler": command_version(javac),
        "sandbox": command_version(shutil.which("bwrap") or "bwrap"),
        "tasks": {
            name: {
                "reference_sha256": sha256_file(TASKS[name]["reference"]),
                "specification_sha256": sha256_file(TASKS[name]["path"] / "problem.md"),
                "test_manifest_sha256": sha256_file(
                    TASKS[name]["path"] / "test-cases" / "core.json"
                ),
                **result,
            }
            for name, result in results.items()
        },
    }
    write_json(ROOT / "results" / "reference-validation.json", validation_record)
    print(json.dumps(results, indent=2))
    return 0 if all(
        result["compiled"] and result["passed_weight"] == 100 for result in results.values()
    ) else 1


def command_evaluate(args):
    load_dotenv()
    models = load_models(args.config)
    task_names = list(TASKS) if args.task == "all" else [args.task]
    output_root = Path(args.output)
    java, javac = java_commands()
    runs = (
        args.runs
        if args.runs is not None
        else int(os.environ.get("MODEL_RUNS_PER_TASK", "3"))
    )
    if runs < 1:
        raise ValueError("runs must be at least one")

    for model in models:
        for run_number in range(1, runs + 1):
            ordered_tasks = task_names if run_number % 2 else list(reversed(task_names))
            for task_name in ordered_tasks:
                task = TASKS[task_name]
                task_path = task["path"]
                prompt = make_prompt(task_path)
                tests = load_test_cases(task_path / "test-cases" / "core.json")
                run_id = str(uuid.uuid4())
                record = {
                    "run_id": run_id,
                    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "task_id": task["task_id"],
                    "provider": model["provider"],
                    "model_name": model["name"],
                    "model_id": model["model_id"],
                    "temperature": model.get("temperature", 0),
                    "max_output_tokens": model.get("max_output_tokens", 8192),
                    "run_number": run_number,
                    "task_order_index": ordered_tasks.index(task_name),
                    "prompt": prompt,
                    "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
                    "task_sha256": sha256_file(task_path / "problem.md"),
                    "test_manifest_sha256": sha256_file(task_path / "test-cases" / "core.json"),
                    "java_runtime": command_version(java),
                    "java_compiler": command_version(javac),
                    "sandbox": command_version(shutil.which("bwrap") or "bwrap"),
                    "api_timeout_seconds": 120,
                    "test_timeout_seconds": 5,
                }
                try:
                    raw, request_id, usage = generate(model, prompt)
                    record.update({"request_id": request_id, "usage": usage, "raw_response": raw})
                    source = extract_java_source(raw)
                    record["source_extraction"] = "code-block-or-plain-source"
                    record["extracted_java_source"] = source
                    record["grading"] = run_java(source, tests, java=java, javac=javac)
                    record["attempt_status"] = "graded"
                except (ProviderError, SandboxUnavailable, ValueError, OSError) as error:
                    record["error"] = str(error)
                    record["attempt_status"] = "error"
                safe_name = f"{model['name']}-{task_name}-{run_number}-{run_id}.json"
                write_json(output_root / "raw-outputs" / safe_name, record)
                summary = record.get("grading", {})
                if "error" in record:
                    print(
                        f"{model['name']} {task_name} run {run_number}: ERROR - "
                        f"{record['error']} (saved {safe_name})",
                        file=sys.stderr,
                    )
                else:
                    print(
                        f"{model['name']} {task_name} run {run_number}: "
                        f"{summary.get('passed_weight', 0)}/100 "
                        f"(saved {safe_name})"
                    )
    return 0


def command_report(args):
    aggregate = build_report(args.output)
    print(json.dumps(aggregate, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(description="Java algorithm challenge evaluation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Grade the local Java reference")
    validate.add_argument("--task", choices=["all", *TASKS], default="all")
    validate.set_defaults(function=command_validate)

    evaluate = subparsers.add_parser("evaluate", help="Run configured model evaluations")
    evaluate.add_argument(
        "--config",
        default=str(ROOT / "evaluator" / "models" / "model-config.json"),
    )
    evaluate.add_argument("--output", default=str(DEFAULT_OUTPUT))
    evaluate.add_argument("--runs", type=int)
    evaluate.add_argument("--task", choices=["all", *TASKS], default="all")
    evaluate.set_defaults(function=command_evaluate)

    report = subparsers.add_parser("report", help="Summarize saved model run records")
    report.add_argument("--output", default=str(DEFAULT_OUTPUT))
    report.set_defaults(function=command_report)

    args = parser.parse_args()
    try:
        return args.function(args)
    except (ValueError, OSError, json.JSONDecodeError, SandboxUnavailable) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
