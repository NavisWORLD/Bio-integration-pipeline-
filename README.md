# COSMOS Bio/CNS Integration Pipeline

A local-first, open-source Python library for connecting human-facing sensor adapters to a compact adaptive CNS state, persistent event ledger, and optional cloud heartbeat bridge.

**Author:** Cory Shane Davis  
**Foundational CST research DOI:** https://doi.org/10.5281/zenodo.17574447  
**Code license:** Apache-2.0

> This repository is an engineering toolkit. It is not a medical device, diagnostic system, consciousness detector, or proof that a biometric measurement equals an emotion.

## Why this exists

The COSMOS/CST project developed a recurring systems pattern:

```text
human / environment
      ↓
sensor adapter
      ↓
quality + timestamp + consent
      ↓
personal baseline
      ↓
normalized bio features
      ↓
multimodal fusion
      ↓
local CNS state
      ↓
persistent event + heartbeat
      ↓
project behavior / memory / optional cloud reconciliation
      ↺
```

This repository extracts that pattern into a library that other projects can import without needing the full COSMOS runtime.

## What is implemented

- neutral `BioObservation` schema;
- pluggable `BioAdapter` protocol;
- per-subject/channel EWMA baseline adaptation;
- quality-gated multimodal fusion;
- deterministic local 12D CNS reference engine;
- seven-organ CNS status vocabulary (`quantum`, `dark_matter`, `emeth`, `plasticity`, `awareness`, `daemons`, `surgeon`);
- append-only SQLite event ledger with SHA-256 chaining;
- versioned heartbeat records;
- JSONL offline sink;
- optional Azure IoT Hub sink;
- deterministic mock cardiac adapter for demos and CI;
- CLI, examples, tests, engineering manual, teacher manual, distribution guide, and companion publication manuscript.

## Install

From a clone:

```bash
git clone https://github.com/NavisWORLD/Bio-integration-pipeline-.git
cd Bio-integration-pipeline-
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
```

Optional Azure support:

```bash
pip install -e ".[azure]"
```

## 30-second local demo

```bash
cosmos-bio-cns demo --steps 5
cosmos-bio-cns verify-ledger
```

Or from Python:

```python
from cosmos_bio_cns import BioCNSRuntime, SQLiteEventStore
from cosmos_bio_cns.adapters import DeterministicCardiacAdapter

store = SQLiteEventStore("bio.sqlite3")
runtime = BioCNSRuntime([DeterministicCardiacAdapter()], store=store)
runtime.start()
try:
    frame, state = runtime.step()
    print(frame.confidence)
    print(state.vector)
finally:
    runtime.stop()
    store.close()
```

## Add your own sensor

Implement three methods:

```python
class MySensor:
    name = "my-sensor"

    def connect(self): ...
    def read(self):
        return [BioObservation(...)]
    def disconnect(self): ...
```

The adapter should report observations, not interpretations. A heart-rate adapter reports heart rate and quality; it should not declare a user's emotion or diagnosis.

## Local-first design

The CNS loop works with no cloud service. Cloud bridges are sinks and reconciliation extensions, not prerequisites for local operation.

When Azure is used, keep secrets outside source control. Prefer workload/device identities and secret stores over hard-coded keys. See `docs/AZURE_HEARTBEAT.md`.

## Research boundaries

The project lineage distinguishes implemented mechanisms from hypotheses. In particular:

- 12D/42D/54D are computational state representations in this software lineage, not claims of extra physical spacetime dimensions;
- raw camera/audio data should not be retained by default merely because features can be extracted;
- a heartbeat is a software maintenance/continuity mechanism, not a biological heartbeat;
- sensory conditioning has produced bounded/null results in some historical tests, so this library exposes the mechanism without claiming universal performance benefit;
- nothing here establishes machine consciousness.

See `docs/RESEARCH_BOUNDARIES.md`.

## Repository map

```text
src/cosmos_bio_cns/       reusable Python library
examples/                 minimal integration examples
tests/                    stdlib unittest suite
docs/ARCHITECTURE.md      full system design
docs/AZURE_HEARTBEAT.md   storage/reconciliation pipeline
docs/DISTRIBUTION.md      redistribution + packaging guide
docs/TEACHER_MANUAL.md    course/labs for this section
paper/                    companion paper + foundational citation
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Citation

Please cite the software repository and the foundational CST deposit. See `CITATION.cff` and `paper/FOUNDATIONAL_PUBLICATION.md`.

## License and redistribution

Code is licensed under Apache License 2.0. Keep the license and notices with redistributed copies. Documentation and paper text in this repository may be redistributed with attribution under the terms stated in each document. See `docs/DISTRIBUTION.md`.

## Contributing

Adapters, tests, documentation, baseline studies, and reproducibility improvements are welcome. See `CONTRIBUTING.md`.
