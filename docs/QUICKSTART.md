# Five-Minute Quickstart

This path is for someone who has never seen COSMOS before.

## 1. Clone and install

```bash
git clone https://github.com/NavisWORLD/Bio-integration-pipeline-.git
cd Bio-integration-pipeline-
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

## 2. Prove the local loop works

```bash
cosmos-bio-cns demo --steps 3
cosmos-bio-cns verify-ledger
```

You should see fusion/CNS state JSON and a valid event-ledger hash chain.

## 3. Understand the first sample

The first accepted value for a subject/sensor/channel/unit establishes that stream's personal baseline. Its baseline delta is therefore zero. Adaptation becomes visible on later deviations. This is intentional and prevents the first observation from being treated as an anomalous event simply because no history existed yet.

## 4. Use your own sensor in Python

Create a class with `connect()`, `read()`, and `disconnect()`. Return neutral `BioObservation` objects from `read()`. See `docs/ADAPTER_AUTHORING.md`.

## 5. Use it from another language

```bash
cosmos-bio-cns serve --host 127.0.0.1 --port 8765
```

POST JSON to `/v1/observe`. The reference bridge is deliberately localhost-only unless `--allow-remote` is supplied. It has no built-in authentication, so remote exposure requires a separate authenticated transport/proxy and deployment security review.

## 6. Consent rule

If an observation contains a consent object with `bio_processing: false`, the fusion engine rejects that observation from processing. Open-source code rights never override the human subject's data/processing permissions.

## 7. Where to go next

- `docs/API_REFERENCE.md` — public interfaces and HTTP routes;
- `docs/ARCHITECTURE.md` — system design;
- `docs/INTEROPERABILITY.md` — JSON bridge;
- `docs/AZURE_HEARTBEAT.md` — optional cloud continuity;
- `docs/TEACHER_MANUAL.md` — lessons and labs;
- `docs/RESEARCH_BOUNDARIES.md` — what the system does and does not establish.
