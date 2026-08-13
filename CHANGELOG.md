# Changelog

## 0.1.0 — 2026-08-12

Initial public extraction of the COSMOS/CST bio/CNS integration pipeline:

- adapter protocol and deterministic demo adapter;
- person-relative baseline engine;
- multimodal fusion frame;
- 12D local CNS reference state;
- seven-organ status vocabulary;
- hash-chained SQLite event store;
- heartbeat records;
- local JSONL and optional Azure IoT sink;
- CLI, tests, examples, architecture manual, teacher manual, distribution guide, and companion manuscript;
- language-neutral localhost HTTP bridge, push adapter, multimodal example, and JSON schemas;
- automated CI, explicit documentation licensing, and release-readiness record.

### Final pre-release hardening audit

- made SQLite event persistence safe for the threaded HTTP bridge and serialized bridge state transitions;
- enforced `bio_processing=False` consent at the fusion boundary;
- isolated adaptive baselines by subject, sensor, channel, and unit;
- refused unauthenticated non-loopback HTTP binds by default;
- packaged JSON schemas and `py.typed` with distributions;
- added HTTP/consent/baseline/schema regression tests;
- added quickstart, API reference, release checklist, Dependabot, and contribution templates.
