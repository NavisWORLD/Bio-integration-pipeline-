# Teacher Manual — Bio/CNS Integration Section

**Author/Project:** Cory Shane Davis — COSMOS/CST Bio Integration Pipeline  
**Audience:** advanced high-school, undergraduate, maker-lab, AI/embedded systems, and independent research learners  
**Format:** 8 sessions, 60–120 minutes each

## Teaching objective

Students should leave able to build a sensor adapter, distinguish raw observation from interpretation, normalize a signal against an individual baseline, fuse multiple channels, update a compact computational state, preserve event lineage, and explain privacy/research boundaries.

## Session 1 — Observation is not interpretation

Teach `BioObservation`, timestamps, units, quality, device identity, and consent metadata.

**Lab:** modify the deterministic cardiac adapter to emit a second neutral channel.  
**Check:** students must explain why "heart rate = anxiety" is not a valid adapter rule.

## Session 2 — Personal baselines

Introduce EWMA mean/variance and person-relative normalization.

**Lab:** feed two synthetic subjects with different resting values and show that baseline deltas can be comparable even when absolute values differ.

## Session 3 — Signal quality and missing data

Teach confidence, artifact rejection, freshness, and partial operation.

**Lab:** inject low-quality observations and verify `BioFusionEngine` rejects them without crashing the whole runtime.

## Session 4 — Multimodal fusion

Map cardiac, audio, visual, and movement features into one `FusionFrame`.

**Lab:** implement a synthetic movement adapter and compare confidence with one versus two active sensors.

## Session 5 — Local CNS state

Teach the 12D state as computational state. Introduce leak/integration, bounded state, determinism, and why dimensionality is not a physics claim.

**Lab:** run the same feature sequence through two `LocalCNS` instances and prove identical output.

## Session 6 — Persistence and heartbeat

Teach append-only event history, revisions, boot IDs, sequence numbers, hashes, and current-state versus event-history separation.

**Lab:** run the CLI, inspect the SQLite ledger, and verify the hash chain.

## Session 7 — Cloud reconciliation

Teach local-first operation and the Azure pattern: edge → IoT ingestion → event stream → archive/live state → reconciliation.

**Lab:** use the JSONL sink as a fake cloud boundary, disconnect it, continue locally, then design an idempotent replay strategy on paper.

## Session 8 — Reproducible research and ethics

Teach claim taxonomy: implemented, observed, measured, null, hypothesis, metaphor/model.

**Final project:** add a new adapter and produce a two-page lab report containing:

1. sensor/data source;
2. observation schema;
3. quality rule;
4. baseline method;
5. CNS integration path;
6. privacy/consent policy;
7. expected failure modes;
8. one falsifiable hypothesis;
9. one result the project must *not* claim from the available evidence.

## Assessment rubric

- 25% engineering correctness;
- 20% signal/data discipline;
- 20% reproducibility;
- 20% privacy and claim discipline;
- 15% explanation and documentation.

## Teacher answer key — core ideas

- Sensors report observations; interpretation belongs downstream.
- Personal baselines reduce inappropriate universal thresholds.
- Missing sensors should reduce confidence, not necessarily stop the system.
- State dimension labels describe software representation unless separately validated as something else.
- Event history and current state are different data products.
- Open-source software licensing does not grant permission to share private human biosignal datasets.
- Persistence/autonomy do not prove consciousness.
