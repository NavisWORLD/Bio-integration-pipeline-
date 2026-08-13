# Changelog

## 0.2.0 — 2026-08-13

Cross-language synaptic interoperability release:

- extracted the deterministic CNS transition into public Python `synaptic_step` / `cosmos_12d_step` APIs;
- refactored `LocalCNS` to call the canonical kernel;
- froze `sdk/spec/SYNAPSE_WIRE_V1.md` and a normative `1e-12` golden vector;
- added Rust and C++17/CMake libraries plus a stable C ABI;
- added Go, JavaScript/TypeScript, Java/JVM, C#/.NET and Swift implementations;
- documented direct Kotlin/JVM reuse rather than duplicating the kernel;
- documented C-ABI and HTTP compatibility for additional runtimes;
- added automated cross-language compilation/parity validation;
- advanced package and citation metadata to v0.2.0.

## 0.1.0 — 2026-08-12

Initial public extraction of the COSMOS/CST bio/CNS integration pipeline:

- adapter protocol and deterministic demo adapter;
- person-relative baseline engine and multimodal fusion;
- deterministic 12D local CNS reference state and seven-organ software-role vocabulary;
- hash-chained SQLite event store and heartbeat records;
- local JSONL and optional Azure IoT sink;
- language-neutral localhost HTTP bridge, push adapter and JSON schemas;
- automated CI, explicit documentation licensing and release-readiness record;
- threaded persistence hardening, consent enforcement, baseline isolation and remote-bind guard;
- quickstart, API reference, release checklist, Dependabot and contribution templates.
