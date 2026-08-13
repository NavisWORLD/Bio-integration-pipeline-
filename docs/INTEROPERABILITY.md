# Language-Neutral Integration

COSMOS Bio/CNS v0.2.0 supports two interoperability layers:

1. **native synaptic SDKs** for deterministic local state transitions; and
2. **HTTP/JSON** for the complete observation/fusion/persistence/heartbeat runtime.

See `docs/CROSS_LANGUAGE_SDK.md` for the SDK matrix and `sdk/spec/SYNAPSE_WIRE_V1.md` for the normative kernel contract.

## Native SDKs

First-party parity-tested implementations live in:

- Python: `src/cosmos_bio_cns/synapse.py`
- Rust: `sdk/rust/`
- C++17 + stable C ABI: `sdk/cpp/`
- Go: `sdk/go/`
- JavaScript / TypeScript: `sdk/javascript/`
- Java / JVM: `sdk/java/`
- Kotlin: reuse the Java/JVM package directly
- C# / .NET: `sdk/csharp/`
- Swift: `sdk/swift/`

Languages without a dedicated package can use the C ABI or the HTTP bridge. This avoids maintaining dozens of independently drifting copies of the same equation.

## Full runtime bridge

Run:

```bash
cosmos-bio-cns serve --host 127.0.0.1 --port 8765
```

Then any process that can send HTTP/JSON can provide observations.

### Security boundary

The reference bridge has no authentication layer. It is intended for loopback/local integration and refuses a non-loopback bind by default. `--allow-remote` is for controlled development only and does not add authentication, encryption, authorization, rate limiting, or production hardening.

## POST `/v1/observe`

```json
{
  "sensor": "watch",
  "channel": "heart_rate",
  "value": 74.2,
  "unit": "bpm",
  "quality": 0.97,
  "sequence": 42,
  "subject_id": "pseudonymous-user",
  "device_id": "watch-1",
  "consent": {
    "session_id": "session-001",
    "bio_processing": true,
    "raw_retention": false
  }
}
```

The response contains the fusion frame and current CNS state. If `consent.bio_processing` is `false`, the observation is rejected before baseline/CNS processing. Baselines remain isolated by subject, sensor, channel, and unit.

## Read endpoints

- `GET /v1/state` — most recent fusion frame/state.
- `GET /health` — service health plus ledger-chain verification.
- `GET /v1/ledger/verify` — event count, chain head, verification status.

## Schemas

- `schemas/bio_observation.schema.json`
- `schemas/heartbeat.schema.json`

Python can load packaged copies with `load_schema()`. Mobile/native code should keep sensor permission acquisition on-device and send only neutral features needed by the project.
