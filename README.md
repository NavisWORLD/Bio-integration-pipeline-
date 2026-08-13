# COSMOS Bio/CNS Integration Pipeline

[![CI](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/ci.yml/badge.svg)](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/ci.yml)

A local-first, open-source Python library for connecting human-facing sensor adapters to a compact adaptive CNS state, persistent event ledger, and optional cloud heartbeat bridge.

**Author:** Cory Shane Davis  
**Foundational CST research DOI:** https://doi.org/10.5281/zenodo.17574447  
**Code license:** Apache-2.0  
**Repository-authored docs/paper license:** CC BY 4.0

> This repository is an engineering and research toolkit. It is not a medical device, diagnostic system, consciousness detector, or proof that a biometric measurement equals an emotion.

## Release status

**v0.1.0 reference implementation — release-ready for research, education, prototyping, and integration testing.**

The repository includes automated CI across Python 3.10, 3.11, and 3.12, distribution-build validation, regression tests, CLI smoke tests, explicit software/documentation licensing, packaged schemas, examples, manuals, security guidance, dependency-update automation, and citation metadata. See `docs/RELEASE_READINESS.md` for the audit scope and the important distinction between engineering release readiness and formal medical/regulatory/security certification.

## Start here

If you are new to the project, follow these in order:

1. `docs/QUICKSTART.md` — get the local loop running in about five minutes;
2. `docs/API_REFERENCE.md` — learn the stable Python/CLI/HTTP interfaces;
3. `docs/ARCHITECTURE.md` — understand the complete pipeline;
4. `docs/ADAPTER_AUTHORING.md` — connect your own sensor or host application;
5. `docs/INTEROPERABILITY.md` — connect Swift, Kotlin, C++, Rust, JavaScript, or another process;
6. `docs/AZURE_HEARTBEAT.md` — add optional cloud continuity/reconciliation;
7. `docs/TEACHER_MANUAL.md` — teach the subsystem with labs and assignments;
8. `docs/RESEARCH_BOUNDARIES.md` — understand exactly what the system does and does not establish.

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
- explicit processing-consent enforcement;
- pluggable `BioAdapter` protocol;
- personal EWMA baselines isolated by subject, sensor, channel, and unit;
- quality-gated multimodal fusion;
- deterministic local 12D CNS reference engine;
- seven-organ CNS status vocabulary (`quantum`, `dark_matter`, `emeth`, `plasticity`, `awareness`, `daemons`, `surgeon`);
- thread-safe append-only SQLite event ledger with SHA-256 chaining;
- versioned heartbeat records;
- JSONL offline sink;
- optional Azure IoT Hub sink;
- deterministic mock cardiac adapter for demos and CI;
- language-neutral localhost JSON bridge for non-Python hosts;
- JSON schemas both in the repository and packaged in the Python distribution;
- `py.typed` marker for typed downstream Python integrations;
- CLI, examples, regression tests, engineering manual, teacher manual, distribution guide, companion publication manuscript, and release checklist.

## Install

```bash
git clone https://github.com/NavisWORLD/Bio-integration-pipeline-.git
cd Bio-integration-pipeline-
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

Optional Azure support:

```bash
python -m pip install -e ".[azure]"
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

The first accepted sample establishes that sensor stream's baseline, so its baseline delta is expected to be zero. Person-relative adaptation appears on subsequent deviations.

## Use it from any language

Start the reference bridge:

```bash
cosmos-bio-cns serve --host 127.0.0.1 --port 8765
```

Then POST neutral observations to `http://127.0.0.1:8765/v1/observe` from Swift, Kotlin, C++, Rust, JavaScript, Python, or any other HTTP client.

**Security boundary:** the reference bridge has no authentication layer and therefore refuses non-loopback binds by default. `--allow-remote` is an explicit development escape hatch, not production security. Put any network-exposed deployment behind authenticated encrypted transport and perform a deployment-specific review. See `SECURITY.md`.

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

If `ConsentScope.bio_processing` is false, the fusion layer rejects that observation from processing. Open-source code rights never override the subject's data permissions.

See `docs/ADAPTER_AUTHORING.md` for the production adapter checklist.

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
src/cosmos_bio_cns/       reusable Python library + packaged schemas
examples/                 minimal integration examples
tests/                    regression/unit suite
schemas/                  language-neutral JSON contracts
docs/QUICKSTART.md        five-minute onboarding
docs/API_REFERENCE.md     public Python/CLI/HTTP interfaces
docs/ARCHITECTURE.md      full system design
docs/AZURE_HEARTBEAT.md   storage/reconciliation pipeline
docs/INTEROPERABILITY.md  cross-language local bridge
docs/DISTRIBUTION.md      redistribution + packaging guide
docs/TEACHER_MANUAL.md    course/labs for this section
docs/RELEASE_CHECKLIST.md release procedure
docs/RELEASE_READINESS.md audit/certification scope
paper/                    companion paper + foundational citation
```

## Test

```bash
python -m unittest discover -s tests -v
python -m compileall -q src examples tests
```

GitHub Actions runs the supported Python matrix, HTTP/consent/baseline/schema regression suite, CLI smoke test, package build, and `twine check` automatically.

## Citation

Please cite the software repository and the foundational CST deposit. See `CITATION.cff` and `paper/FOUNDATIONAL_PUBLICATION.md`.

The foundational DOI is cited as research lineage; this repository does not claim that DOI was issued specifically for this software package.

## License and redistribution

Source code and software configuration are licensed under Apache License 2.0. Repository-authored documentation and companion-paper text are licensed under CC BY 4.0 unless a file states otherwise. Keep applicable license, notice, attribution, and modification information with redistributed copies.

See `LICENSE`, `LICENSE-DOCS.md`, `NOTICE`, and `docs/DISTRIBUTION.md`.

Open-source software rights do not grant permission to redistribute private human biosignal data. Consent, privacy, retention, research approval, and applicable law remain separate obligations.

## Contributing and releases

Adapters, tests, documentation, baseline studies, and reproducibility improvements are welcome. See `CONTRIBUTING.md`, the GitHub issue/PR templates, and `docs/RELEASE_CHECKLIST.md`.
