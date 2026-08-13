# Language-Neutral Integration

Projects do not have to be written in Python. Run the local bridge:

```bash
cosmos-bio-cns serve --host 127.0.0.1 --port 8765
```

Then any process that can send HTTP/JSON can provide observations.

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
  "device_id": "watch-1"
}
```

The response contains the fusion frame and current CNS state.

Multiple modalities can be posted in one array:

```json
[
  {"sensor":"watch","channel":"heart_rate","value":74.2,"unit":"bpm","quality":0.97},
  {"sensor":"phone","channel":"motion_energy","value":0.31,"unit":"normalized","quality":0.94},
  {"sensor":"audio-feature-extractor","channel":"rms","value":0.18,"unit":"normalized","quality":0.90}
]
```

## GET `/v1/state`

Returns the most recent fusion frame/state.

## GET `/health`

Returns service health plus ledger-chain verification.

## GET `/v1/ledger/verify`

Returns event count, chain head, and verification status.

## Schemas

See:

- `schemas/bio_observation.schema.json`
- `schemas/heartbeat.schema.json`

Mobile/native code should keep sensor permission acquisition on the device side and send only the neutral features actually needed by the project.
