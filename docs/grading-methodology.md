# Grading Methodology

## Status

This scoring plan is implemented for the current single pilot task. Weights and task semantics are frozen in the committed test manifest before model evaluation. This document describes the local pilot grader, not results from an AI experiment.

## Scoring

Each test has a unique ID, category, expected output, and integer point weight. The 12 cases sum to 100 points.

| Category | Weight | Coverage |
|---|---:|---|
| Core | 15 | Mixed values and the retained-sum objective |
| Edge | 30 | `K=0`, positive-only, one positive, short deletion, and zeroes |
| Adversarial | 30 | Preserve a positive, tied optima, and monotonic-deque ordering |
| Numeric | 10 | Values and sums beyond 32-bit range |
| Performance | 15 | `N=200,000` generated input |
| **Total** | **100** | |

The scorer adds the weights of passed cases. Full task acceptance requires compilation and 100/100. A compile failure scores zero. A timeout, runtime failure, sandbox error, or wrong answer fails that case's weight. The expected output is compared exactly after removing trailing whitespace at each line and leading/trailing whitespace overall; other output differences are not ignored.

## Execution controls

- Compile using the configured JDK's `javac --release 17`, with annotation processing disabled and no external classpath.
- Compile and execution commands run in Bubblewrap namespaces with network disabled and a minimal environment. Source is capped at 256 KB; provider response at 2 MB; each testcase input at 4 MB; output/temporary file size at 1 MB.
- The Java runtime uses `-Xmx128m`, one active processor, a 4/5 second CPU soft/hard limit, and a 5-second per-test wall-clock timeout by default.
- Where GNU `time` is available, peak resident memory for the sandbox command is recorded in KB. This includes JVM/sandbox startup, not only the algorithm.
- The heap setting is not a hard total-process memory quota, and the runner does not impose a cgroup process-count limit.
- These controls are practical safeguards, not a formal security certification or complete hostile-code containment system. Run untrusted generated code only in an appropriately disposable environment.

## Validation evidence

The Java reference is checked against an independent Python exhaustive oracle for all positive-containing arrays of lengths 1–3 over `{-2,-1,0,1,2}` and every `K`. It is also compared on 120 deterministic seeded random arrays, tested against authored samples and boundary cases, and run at maximum `N`. A deliberately incorrect monotonic-deque comparison is required to lose points.

The grader's own integration test runs the reference under the same sandbox and verifies secret-environment isolation, stdin, timeout behavior, and mutation detection. These are engineering validation checks, not model-evaluation runs.

## Outcome reporting

For each real run, retain the provider, exact model ID, run ID, timestamp, prompt, generation settings, API request ID and usage when provided, raw response, compilation result, per-test status, score, elapsed time, memory estimate, and any request/execution error. The report generator includes attempts that failed before grading; it does not treat provider/setup failures as zero-scored model answers.

No subjective style bonus is awarded. Root-cause failure labels should only be assigned after inspecting the raw answer and test evidence. Token counts are recorded when returned; API cost is not computed until the provider, billing arrangement, and dated pricing source are verified.
