# Language-Neutral Integration

Projects do not have to be written in Python. Run the local bridge:

```bash
cosmos-bio-cns serve --host 127.0.0.1 --port 8765
```

Then any process that can send HTTP/JSON can provide observations.

## Security boundary

The reference bridge has no authentication layer. It is intended for loopback/local integration and refuses a non-loopback bind by default.

`--allow-remote` explicitly disables that bind guard for controlled development use. It does **not** add authentication, encryption, authorization, rate limiting, or production hardening. Any network-exposed deployment should sit behind an authenticated encrypted transport/proxy and receive a deployment-specific security/privacy review.

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

The response contains the fusion frame and current CNS state.

If `consent.bio_processing` is `false`, that observation is rejected by the fusion layer and does not update the personal baseline or CNS state.

Multiple modalities can be posted in one array:

```json
[
  {"sensor":"watch","channel":"heart_rate","value":74.2,"unit":"bpm","quality":0.97},
  {"sensor":"phone","channel":"motion_energy","value":0.31,"unit":"normalized","quality":0.94},
  {"sensor":"audio-feature-extractor","channel":"rms","value":0.18,"unit":"normalized","quality":0.90}
]
```

Baselines are isolated by subject, sensor, channel, and unit. Two devices using the same channel name but different units do not share one adaptive baseline.

## GET `/v1/state`

Returns the most recent fusion frame/state.

## GET `/health`

Returns service health plus ledger-chain verification.

## GET `/v1/ledger/verify`

Returns event count, chain head, and verification status.

## Schemas

Repository copies:

- `schemas/bio_observation.schema.json`
- `schemas/heartbeat.schema.json`

The same schemas are packaged inside the Python distribution and can be loaded with:

```python
from cosmos_bio_cns import load_schema

observation_schema = load_schema("bio_observation")
heartbeat_schema = load_schema("heartbeat")
```

Mobile/native code should keep sensor permission acquisition on the device side and send only the neutral features actually needed by the project.
