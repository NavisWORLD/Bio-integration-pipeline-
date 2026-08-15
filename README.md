# COSMOS Bio/CNS Integration Pipeline

[![CI](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/ci.yml/badge.svg)](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/ci.yml)
[![Cross-Language SDK](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/cross-language.yml/badge.svg)](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/cross-language.yml)

A local-first, source-available Bio/CNS integration research and engineering toolkit with a Python runtime, deterministic synaptic state kernel, cross-language SDKs, persistent event ledger, optional cloud heartbeat, desktop installers, and native mobile clients.

**Author:** Cory Shane Davis  
**Foundational CST research DOI:** https://doi.org/10.5281/zenodo.17574447  
**Current generation:** 0.3.0  
**Current rights:** Cory Davis Bio/CNS Research Source Rights Reservation v1.0  
**Historical boundary:** 0.1.x and 0.2.x software were Apache-2.0; repository-authored docs/paper were CC BY 4.0 unless otherwise stated. Those valid historical grants remain intact.

> Engineering/research toolkit only. Not a medical device, diagnostic system, consciousness detector, emotion oracle, or proof that a biometric measurement has one fixed psychological meaning.

## Rights and provenance first

This repository is public for inspection, evaluation, citation, provenance, and controlled research visibility. Public availability does **not** mean current newly authored or materially revised Cory-owned material is offered under a general reuse license.

The current rights boundary begins 2026-08-15. Newly authored or materially revised covered material is governed by `LICENSE` unless a file expressly states otherwise. Historical Apache-2.0 and CC BY 4.0 copies keep the rights those licenses granted. The chronology is recorded in `LICENSE_HISTORY.md` rather than rewritten.

The current rights notice grants no new public patent license. Commercial, enterprise, OEM, hosted-service, paid deployment, commercial research, product integration, or commercial AI/ML use of current covered material requires separate written authorization where the `LICENSE` states so.

Copyright does not itself protect abstract ideas, mathematical principles, methods, systems, or discoveries. Independent implementation of unprotected ideas may be lawful unless another right applies. The protected source code, documentation, schemas, diagrams, specifications, tests, examples, and other copyrightable expression remain subject to the rights governing the exact version or copy involved.

## Release status

**v0.3.0 rights-boundary generation.** The engineering implementation remains based on the v0.2.0 cross-language reference release while the repository now has an explicit prospective commercial and IP boundary for new material.

The repository includes Python 3.10-3.12 CI, package validation, regression tests, native cross-language parity tests, platform builds, schemas, manuals, security guidance, licensing, citation/provenance metadata, Windows/macOS packaging, Android/iOS clients, and a versioned synaptic wire contract.

See `docs/RELEASE_READINESS.md` for the engineering-certification boundary of the v0.2.0 reference implementation and `LICENSE_HISTORY.md` for the rights boundary.

## Start here

1. `LICENSE` - current rights reservation;
2. `LICENSE_HISTORY.md` - historical Apache/CC boundary;
3. `LICENSE-DOCS.md` - documentation/paper rights;
4. `COMMERCIAL_RIGHTS.md` - commercial licensing boundary;
5. `docs/QUICKSTART.md` - run the local loop;
6. `docs/API_REFERENCE.md` - Python/CLI/HTTP interfaces;
7. `docs/CROSS_LANGUAGE_SDK.md` - Rust, C++, C, Go, JS/TS, JVM, .NET, Swift, and universal binding routes;
8. `sdk/spec/SYNAPSE_WIRE_V1.md` - canonical synaptic equation and behavior;
9. `docs/ARCHITECTURE.md` - complete pipeline;
10. `docs/RESEARCH_BOUNDARIES.md` - explicit scientific claim boundaries.

## Core loop

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
local CNS / synaptic state
      ↓
persistent event + heartbeat
      ↓
project behavior / memory / optional cloud reconciliation
      ↺
```

## What is implemented

- neutral `BioObservation` schema and explicit processing-consent enforcement;
- pluggable adapters and deterministic demo sensor;
- person-relative EWMA baselines isolated by subject, sensor, channel, and unit;
- quality-gated multimodal fusion;
- deterministic local 12D CNS reference engine;
- Python synaptic kernel;
- first-party Rust, C++17/C ABI, Go, JavaScript/TypeScript, Java/JVM, C#/.NET, and Swift synaptic SDKs;
- Kotlin compatibility through the Java/JVM SDK;
- universal fallback through C FFI or loopback HTTP/JSON;
- golden cross-language parity vector with `1e-12` tolerance;
- seven-organ CNS software-role vocabulary;
- thread-safe append-only SQLite ledger with SHA-256 chaining;
- versioned heartbeat records, JSONL, optional Azure IoT sink;
- language-neutral local HTTP bridge and packaged JSON schemas;
- desktop/mobile apps, CI, examples, engineering/teacher manuals, distribution guide, companion manuscript, and release records.

## Install Python runtime

```bash
git clone https://github.com/NavisWORLD/Bio-integration-pipeline-.git
cd Bio-integration-pipeline-
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

Building or running the current public source for evaluation does not expand the rights granted by `LICENSE`.

Optional Azure support:

```bash
python -m pip install -e ".[azure]"
```

## Use the synaptic kernel

```python
from cosmos_bio_cns import SynapticFeature, cosmos_12d_step

state = (0.0,) * 12
state = cosmos_12d_step(
    state,
    [SynapticFeature(0.5, 0.9), SynapticFeature(-0.25, 0.8)],
)
print(state)
```

Equivalent implementations live under `sdk/`. Rights to copy, port, redistribute, or commercialize an SDK depend on the exact version and license history applicable to that copy.

## 30-second runtime demo

```bash
cosmos-bio-cns demo --steps 5
cosmos-bio-cns verify-ledger
```

```python
from cosmos_bio_cns import BioCNSRuntime, SQLiteEventStore
from cosmos_bio_cns.adapters import DeterministicCardiacAdapter

store = SQLiteEventStore("bio.sqlite3")
runtime = BioCNSRuntime([DeterministicCardiacAdapter()], store=store)
runtime.start()
try:
    frame, state = runtime.step()
    print(frame.confidence, state.vector)
finally:
    runtime.stop()
    store.close()
```

The first accepted sample establishes that stream's baseline, so baseline delta is expected to be zero until subsequent deviation.

## Cross-language architecture

The repository contains implementation surfaces for Python, Rust, C++/C, Go, JavaScript/TypeScript, Java/JVM, C#/.NET, and Swift, plus HTTP/JSON and C-ABI interoperability paths.

These technical interfaces describe interoperability. They do not create licensing permission beyond the rights governing the exact source material involved.

## Add your own sensor

```python
class MySensor:
    name = "my-sensor"
    def connect(self): ...
    def read(self): return [BioObservation(...)]
    def disconnect(self): ...
```

Adapters report observations, not diagnoses or emotional conclusions. Software rights never override a human subject's data permissions.

## Local-first design

The CNS loop works without cloud services. Cloud bridges are optional sinks/reconciliation extensions. Keep credentials outside source control and prefer managed identities or secret stores where available.

## Research boundaries

- 12D/42D/54D are computational state representations in this software lineage, not literal extra-spacetime claims;
- raw camera/audio retention should be minimized;
- a software heartbeat is a continuity/scheduling mechanism, not biological life;
- historical sensory-conditioning results include bounded/null findings, so no universal performance benefit is claimed;
- nothing here establishes machine consciousness.

## Repository map

```text
src/cosmos_bio_cns/        Python runtime + canonical synaptic kernel
sdk/spec/                   versioned wire contract + golden vector
sdk/rust/                   Rust crate
sdk/cpp/                    C++17 library + stable C ABI
sdk/go/                     Go package
sdk/javascript/             JavaScript runtime + TypeScript declarations
sdk/java/                   Java/JVM implementation (Kotlin-compatible)
sdk/csharp/                 C#/.NET implementation
sdk/swift/                  Swift Package Manager implementation
apps/                       desktop, Android, iOS applications
examples/                   Python integration examples
tests/                      Python regression/parity suite
schemas/                    language-neutral JSON contracts
docs/                       manuals, API, interoperability, release records
paper/                      companion paper + foundational citation
```

## Test

```bash
python -m unittest discover -s tests -v
python -m compileall -q src examples tests
cargo test --manifest-path sdk/rust/Cargo.toml
cmake -S sdk/cpp -B build/cpp && cmake --build build/cpp && ctest --test-dir build/cpp
(cd sdk/go && go test ./...)
(cd sdk/javascript && npm test)
swift test --package-path sdk/swift
```

GitHub Actions additionally compiles the JVM and .NET implementations and validates platform packages.

## Citation

Please cite the software repository and foundational CST deposit when discussing this lineage. Citation establishes provenance and attribution. Citation does not substitute for permission when permission is required.

## License and data boundary

**Current newly authored/materially revised Cory-owned material:** governed by `LICENSE`, the Cory Davis Bio/CNS Research Source Rights Reservation v1.0, unless a file states otherwise.

**Historical software copies:** 0.1.x and 0.2.x were distributed under Apache-2.0. Their valid historical grants remain intact.

**Historical repository-authored documentation/paper copies:** 0.1.x and 0.2.x were offered under CC BY 4.0 unless a file stated otherwise. Their valid historical grants remain intact.

**Human data:** no code or documentation license grants rights to private biometric, physiological, medical, audio, image, or other consent-sensitive data.

See `LICENSE`, `LICENSE_HISTORY.md`, `LICENSE-DOCS.md`, `COMMERCIAL_RIGHTS.md`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, and `docs/DISTRIBUTION.md`.
