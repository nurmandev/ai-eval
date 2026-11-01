# Challenge 02: Retry Idempotency Engine

Challenge 02 adds an ordered wallet-request simulation to the benchmark. It is algorithmically distinct from Challenge 01's contiguous interval optimization: correctness depends on composite-key identity, cached terminal outcomes, fixed TTL expiration, payload conflict precedence, and balance-state transitions.

- [Problem statement and public samples](problem.md)
- [Constraints](constraints.md)
- [Machine-readable metadata](metadata.json)
- [Verified validation and mutation results](validation-report.md)
- [Private weighted test manifest](test-cases/core.json)
- [Standalone Java 17 reference and editorial](../../reference-solutions/challenge-02/Main.java)
- [Test fixtures](tests/)

Only the problem statement and its public samples belong in the evaluated-model prompt. The weighted test manifest, expected hidden outputs, mutation tests, and editorial are grading/research materials and must not be added to that prompt.
