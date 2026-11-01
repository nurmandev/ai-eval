import csv
import json
import math
from collections import defaultdict
from pathlib import Path


def wilson_interval(successes, trials, z=1.959963984540054):
    if trials == 0:
        return None
    proportion = successes / trials
    denominator = 1 + z * z / trials
    center = (proportion + z * z / (2 * trials)) / denominator
    margin = (
        z
        * math.sqrt(
            proportion * (1 - proportion) / trials + z * z / (4 * trials * trials)
        )
        / denominator
    )
    return [max(0.0, center - margin), min(1.0, center + margin)]


def format_interval(interval):
    if interval is None:
        return ""
    return f"[{interval[0]:.3f}, {interval[1]:.3f}]"


def build_report(results_dir):
    root = Path(results_dir)
    root.mkdir(parents=True, exist_ok=True)
    records = []
    for path in sorted((root / "raw-outputs").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        records.append(record)

    aggregate_path = root / "aggregate-results.json"
    csv_path = root / "model-comparison.csv"
    report_path = root / "final-report.md"
    if not records:
        aggregate = {"status": "NOT RUN", "attempted_model_runs": 0, "graded_model_runs": 0, "models": []}
        aggregate_path.write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")
        csv_path.write_text(
            "provider,model_id,task_id,attempted_runs,graded_runs,ungraded_attempts,"
            "mean_score,full_pass_rate,full_pass_wilson_95,compilation_rate,"
            "compilation_wilson_95\n",
            encoding="utf-8",
        )
        report_path.write_text(
            "# Evaluation Report\n\n"
            "**Status: NOT RUN.** No completed model evaluations were found. "
            "No scores or model findings are claimed. Configure real provider model IDs "
            "and credentials, then run `make pilot`.\n",
            encoding="utf-8",
        )
        return aggregate

    groups = defaultdict(list)
    for record in records:
        key = (record["provider"], record["model_id"], record["task_id"])
        grading = record.get("grading", {})
        groups[key].append(
            {
                "score": grading.get("passed_weight"),
                "compiled": grading.get("compiled"),
                "full_pass": (
                    grading.get("compiled", False)
                    and grading.get("passed_weight", 0) == 100
                    if grading
                    else None
                ),
                "attempt_status": record.get("attempt_status", "unknown"),
                "run_id": record.get("run_id"),
                "task_id": record.get("task_id"),
            }
        )

    paired_runs = defaultdict(dict)
    for record in records:
        if record.get("task_id") in {"version-a-control", "version-b-experimental"}:
            paired_runs[
                (record["provider"], record["model_id"], record["run_number"])
            ][record["task_id"]] = record

    paired_groups = defaultdict(list)
    for (provider, model_id, run_number), pair in paired_runs.items():
        control = pair.get("version-a-control", {}).get("grading")
        experimental = pair.get("version-b-experimental", {}).get("grading")
        if control is not None and experimental is not None:
            paired_groups[(provider, model_id)].append(
                {
                    "run_number": run_number,
                    "control_score": control["passed_weight"],
                    "experimental_score": experimental["passed_weight"],
                    "control_accept": control["compiled"] and control["passed_weight"] == 100,
                    "experimental_accept": (
                        experimental["compiled"] and experimental["passed_weight"] == 100
                    ),
                }
            )

    paired_comparison = []
    for (provider, model_id), pairs in sorted(paired_groups.items()):
        deltas = [pair["experimental_score"] - pair["control_score"] for pair in pairs]
        paired_comparison.append(
            {
                "provider": provider,
                "model_id": model_id,
                "matched_graded_runs": len(pairs),
                "mean_score_delta_b_minus_a": round(sum(deltas) / len(deltas), 3),
                "control_only_accepts": sum(
                    pair["control_accept"] and not pair["experimental_accept"] for pair in pairs
                ),
                "experimental_only_accepts": sum(
                    pair["experimental_accept"] and not pair["control_accept"] for pair in pairs
                ),
                "both_accept": sum(
                    pair["control_accept"] and pair["experimental_accept"] for pair in pairs
                ),
                "neither_accept": sum(
                    not pair["control_accept"] and not pair["experimental_accept"]
                    for pair in pairs
                ),
                "runs": pairs,
            }
        )

    aggregate = {
        "status": "COMPLETED" if any("grading" in item for item in records) else "NO_GRADED_RUNS",
        "attempted_model_runs": len(records),
        "graded_model_runs": sum("grading" in item for item in records),
        "models": [],
        "paired_comparison": paired_comparison,
    }
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "provider",
                "model_id",
                "task_id",
                "attempted_runs",
                "graded_runs",
                "ungraded_attempts",
                "mean_score",
                "full_pass_rate",
                "full_pass_wilson_95",
                "compilation_rate",
                "compilation_wilson_95",
            ],
        )
        writer.writeheader()
        for (provider, model_id, task_id), runs in sorted(groups.items()):
            graded = [item for item in runs if item["score"] is not None]
            row = {
                "provider": provider,
                "model_id": model_id,
                "task_id": task_id,
                "attempted_runs": len(runs),
                "graded_runs": len(graded),
                "ungraded_attempts": sum(item["score"] is None for item in runs),
                "mean_score": (
                    round(sum(item["score"] for item in graded) / len(graded), 3)
                    if graded
                    else ""
                ),
                "full_pass_rate": (
                    round(sum(item["full_pass"] for item in graded) / len(graded), 4)
                    if graded
                    else ""
                ),
                "compilation_rate": (
                    round(sum(item["compiled"] for item in graded) / len(graded), 4)
                    if graded
                    else ""
                ),
                "full_pass_wilson_95": wilson_interval(
                    sum(item["full_pass"] for item in graded), len(graded)
                ),
                "compilation_wilson_95": wilson_interval(
                    sum(item["compiled"] for item in graded), len(graded)
                ),
            }
            csv_row = {
                **row,
                "full_pass_wilson_95": format_interval(row["full_pass_wilson_95"]),
                "compilation_wilson_95": format_interval(row["compilation_wilson_95"]),
            }
            writer.writerow(csv_row)
            aggregate["models"].append({**row, "runs_detail": runs})

    aggregate_path.write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Evaluation Report",
        "",
        f"Attempted model runs: **{len(records)}**; graded: "
        f"**{aggregate['graded_model_runs']}**.",
        "",
        "| Provider | Model ID | Task | Attempts (graded; ungraded) | Mean weighted score | Full-pass rate (95% Wilson CI) | Compilation rate (95% Wilson CI) |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for model in aggregate["models"]:
        mean = f"{model['mean_score']:.3f}" if model["mean_score"] != "" else "—"
        full_pass = (
            f"{model['full_pass_rate']:.1%}" if model["full_pass_rate"] != "" else "—"
        )
        full_pass += " " + format_interval(model["full_pass_wilson_95"])
        compile_rate = (
            f"{model['compilation_rate']:.1%}" if model["compilation_rate"] != "" else "—"
        )
        compile_rate += " " + format_interval(model["compilation_wilson_95"])
        lines.append(
            f"| {model['provider']} | {model['model_id']} | {model['task_id']} | "
            f"{model['attempted_runs']} ({model['graded_runs']} graded; "
            f"{model['ungraded_attempts']} ungraded) | {mean} | {full_pass} | "
            f"{compile_rate} |"
        )
    lines.extend(
        [
            "",
            "## Matched A/B outcomes",
            "",
            "Pairs use the same provider/model and configured run number. These are descriptive "
            "counts; inferential tests require a preregistered analysis plan.",
            "",
            "| Provider | Model ID | Matched graded runs | Mean score delta (B-A) | A-only accepts | B-only accepts | Both accept | Neither |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for pair in paired_comparison:
        lines.append(
            f"| {pair['provider']} | {pair['model_id']} | {pair['matched_graded_runs']} | "
            f"{pair['mean_score_delta_b_minus_a']:.3f} | {pair['control_only_accepts']} | "
            f"{pair['experimental_only_accepts']} | {pair['both_accept']} | "
            f"{pair['neither_accept']} |"
        )
    lines.extend(
        [
            "",
            "Scores summarize only recorded executions for the current matched pilot pair. "
            "They do not support general claims beyond the tested models, prompt, and task.",
            "Wilson intervals assume independent Bernoulli runs; interpret cautiously, especially with few or deterministic repeats.",
            "",
            "Raw responses and run metadata are in `raw-outputs/`.",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return aggregate
