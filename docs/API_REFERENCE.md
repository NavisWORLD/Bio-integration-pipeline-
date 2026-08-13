# API Reference

This is the stable v0.1.0 integration surface. Internal implementation details may change without becoming part of the public contract.

## Python objects

### `BioObservation`
Neutral measurement record. Required fields: `sensor`, `channel`, `value`, `unit`, `quality`. Optional fields include timestamp, sequence, subject/device pseudonyms, metadata, and `ConsentScope`.

### `ConsentScope`
Carries `session_id`, `bio_processing`, and `raw_retention`. `bio_processing=False` causes the fusion engine to reject the observation.

### `BioAdapter`
Protocol with `connect()`, `read() -> list[BioObservation]`, and `disconnect()`.

### `PushBioAdapter`
Thread-safe queue-style adapter for host/mobile/native code that already owns sensor acquisition.

### `RunningBaseline`
Exponentially weighted per-stream reference statistics.

### `BioFusionEngine`
Quality- and consent-gated person-relative feature fusion. Baselines are isolated by subject, sensor, channel, and unit.

### `LocalCNS`
Deterministic 12-state reference engine. `update(FusionFrame) -> CNSState`.

### `BioCNSRuntime`
Orchestrates adapters → fusion → CNS → event store/sink → heartbeat.

### `SQLiteEventStore`
Thread-safe append-only API over a SHA-256 chained SQLite event ledger.

### `load_schema(name)`
Loads packaged JSON schemas. Stable names: `bio_observation`, `heartbeat`.

## CLI

```text
cosmos-bio-cns demo [--steps N] [--db PATH]
cosmos-bio-cns verify-ledger [--db PATH]
cosmos-bio-cns serve [--host HOST] [--port PORT] [--db PATH] [--allow-remote]
```

`serve` rejects non-loopback binds unless `--allow-remote` is explicitly supplied. The reference server has no authentication layer.

## HTTP bridge

### `POST /v1/observe`
Accepts one `BioObservation` JSON object or an array of objects. Returns the resulting fusion frame and CNS state.

### `GET /v1/state`
Returns the most recent fusion frame and CNS state, or null values before the first processed request.

### `GET /health`
Returns service health and current ledger-chain verification.

### `GET /v1/ledger/verify`
Returns event count, hash-chain head, and verification result.

## Event behavior

Each successful runtime step records:

1. `cosmos.bio_cns.state`;
2. `cosmos.heartbeat`.

The heartbeat contains boot identity, sequence, current CNS state, bio confidence, runtime health, memory revision, and model revision.

## Compatibility principle

Downstream implementations may replace the local state engine or transport while preserving the observation, fusion-frame/state, and heartbeat boundaries. Do not silently reinterpret units or biometric observations inside adapters.
