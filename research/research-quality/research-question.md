# Research Question

## Primary question

Under identical prompting and execution conditions, how does adding the global feasibility constraint that at least one strictly positive array element must remain affect AI coding models' first-attempt acceptance rate on standalone Java 17 solutions to a bounded contiguous-subarray deletion optimization problem, when acceptance is measured against a hidden test suite frozen before model evaluation?

## Research scope

- **Subject:** AI-generated source code, evaluated on the first attempt.
- **Capability:** Translating a written algorithmic specification into a correct, deterministic, resource-compliant implementation.
- **Language and format:** Java 17 or later; standalone `Main.java`; standard input and standard output; no external dependencies.
- **Algorithmic problem:** Remove at most one contiguous interval of length at most `K` to maximize the sum of retained array values.
- **Experimental constraint:** At least one strictly positive value must remain after the optional deletion.
- **Primary outcome:** Binary first-attempt acceptance: compilation succeeds and the solution passes every pre-frozen hidden correctness and resource test.
- **Secondary outcomes:** Compilation success, functional correctness by test category, preservation-constraint compliance, numerical correctness, runtime, memory use, and categorized failure reasons.
- **Maximum input size:** The supplied brief states `N = 200,000`; the original challenge statement must confirm all input and resource limits before the study.

## Operational distinction

The Version A control is the same bounded deletion objective without the positive-element preservation constraint. Version B adds that constraint. The intended independent variable is therefore task version; the principal dependent variable is first-attempt acceptance rate.

## Interpretation boundary

Although the scenario uses transaction language, the task as described is a sequential array-optimization problem. It does not evaluate database transactions, ACID properties, concurrency, thread synchronization, or financial ledger correctness. The financial scenario is illustrative.

## Reproducibility

An independent researcher should be able to reproduce the experiment from archived copies of both task statements, prompts, model/version identifiers, generation settings, compiler/runtime, resource limits, hidden-test version or hash, oracle validation, acceptance rule, run count, and analysis plan.
