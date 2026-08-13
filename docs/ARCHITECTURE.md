# Architecture Manual

## 1. Scope

This package extracts the human-signal-to-CNS portion of COSMOS into a reusable local library. It deliberately separates observation, interpretation, state, memory, and model updates.

## 2. Canonical loop

```text
READ → TIMESTAMP → QUALITY → NORMALIZE → BASELINE → FEATURE → FUSE → CNS → PERSIST → HEARTBEAT → RECONCILE → NEXT STATE
```

### Observation layer
Adapters emit `BioObservation`. The layer records what the sensor measured, with a quality score, unit, sequence number, subject/device identifiers, and optional consent metadata.

### Baseline layer
`RunningBaseline` uses exponentially weighted moving statistics. This provides person-relative deltas so projects can reason about change from a subject's own historical range instead of treating one universal threshold as meaning the same thing for everyone.

### Fusion layer
`BioFusionEngine` rejects low-quality observations, updates channel baselines, creates `BioFeature` values, and emits a `FusionFrame` with aggregate confidence.

### CNS layer
`LocalCNS` is a deterministic compact-state interoperability implementation. It exposes 12 evolving scalars and seven logical organ status flags. The implementation is intentionally small enough to audit and replace.

Projects may substitute their own CNS by maintaining the same input/output boundary.

### Persistence layer
`SQLiteEventStore` is append-only at the API level and hash-chains every record. Historical rows are not silently rewritten during normal operation.

### Heartbeat layer
Each runtime step can emit a versioned `HeartbeatRecord` containing boot ID, sequence, state revision, bio confidence, runtime health, memory revision, and model revision.

## 3. Seven-organ vocabulary

The extracted library preserves the COSMOS CNS names as engineering roles:

- `quantum`: optional entropy/provenance bridge;
- `dark_matter`: nonlinear/chaotic state source in the historical architecture;
- `emeth`: coherence/reconciliation role;
- `plasticity`: adaptive routing/trust state;
- `awareness`: introspection/status role, not a consciousness claim;
- `daemons`: worker/model processes;
- `surgeon`: health/fault/repair role.

These labels are software architecture terms.

## 4. Adapter contract

Every sensor adapter should implement:

```text
connect()
read() -> list[BioObservation]
disconnect()
```

A production adapter should additionally handle reconnects, clock behavior, permissions, device capability detection, and quality/confidence reporting.

## 5. Privacy boundary

Preferred default:

```text
raw camera/microphone/wearable data
        ↓ local processing
compact numeric features
        ↓
CNS/runtime
```

Raw media retention requires an explicit policy and appropriate user consent. The package never needs raw video/audio to represent a feature vector.

## 6. Failure behavior

- unavailable sensor: continue with remaining channels;
- low-quality sample: reject or down-weight;
- cloud offline: continue locally and queue/export events later;
- CNS absent: adapters may still emit neutral observations;
- persistence unavailable: surface an error rather than claiming durable storage;
- incompatible schema: reject explicitly rather than guessing units.

## 7. Extending to 42D/54D

The repository defaults to 12D because it is compact and easy to embed. A project can replace `LocalCNS` with 42D or 54D state implementations while preserving the `FusionFrame → CNSState` boundary. Higher dimensionality is not assumed to be better.
