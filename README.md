# COSMOS Bio/CNS Integration Pipeline

[![CI](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/ci.yml/badge.svg)](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/ci.yml)
[![Cross-Language SDK](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/cross-language.yml/badge.svg)](https://github.com/NavisWORLD/Bio-integration-pipeline-/actions/workflows/cross-language.yml)

A local-first, open-source Bio/CNS integration toolkit with a Python runtime, deterministic synaptic state kernel, cross-language SDKs, persistent event ledger, optional cloud heartbeat, desktop installers, and native mobile clients.

**Author:** Cory Shane Davis  
**Foundational CST research DOI:** https://doi.org/10.5281/zenodo.17574447  
**Code license:** Apache-2.0  
**Repository-authored docs/paper license:** CC BY 4.0

> Engineering/research toolkit only. Not a medical device, diagnostic system, consciousness detector, emotion oracle, or proof that a biometric measurement has one fixed psychological meaning.

## Release status

**v0.2.0 cross-language reference implementation.**

The repository includes Python 3.10-3.12 CI, package validation, regression tests, native cross-language parity tests, platform builds, schemas, manuals, security guidance, licensing, citation/provenance metadata, Windows/macOS packaging, Android/iOS clients, and a versioned synaptic wire contract.

See `docs/RELEASE_READINESS.md` for the exact engineering-certification boundary.

## Start here

1. `docs/QUICKSTART.md` - run the local loop;
2. `docs/API_REFERENCE.md` - Python/CLI/HTTP interfaces;
3. `docs/CROSS_LANGUAGE_SDK.md` - Rust, C++, C, Go, JS/TS, JVM, .NET, Swift, and universal binding routes;
4. `sdk/spec/SYNAPSE_WIRE_V1.md` - canonical synaptic equation and behavior;
5. `docs/ARCHITECTURE.md` - complete pipeline;
6. `docs/ADAPTER_AUTHORING.md` - connect a sensor/host app;
7. `docs/INTEROPERABILITY.md` - language-neutral runtime bridge;
8. `docs/AZURE_HEARTBEAT.md` - optional cloud continuity/reconciliation;
9. `docs/TEACHER_MANUAL.md` - labs and teaching path;
10. `docs/RESEARCH_BOUNDARIES.md` - explicit claim boundaries.

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
- public dependency-free Python synaptic kernel;
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

Equivalent parity-tested implementations live under `sdk/`.

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

## Use it from any language

Choose either:

- **native kernel:** `sdk/rust`, `sdk/cpp`, `sdk/go`, `sdk/javascript`, `sdk/java`, `sdk/csharp`, `sdk/swift`;
- **C ABI:** bind `cosmos_synapse_c.h` from C, Zig, Fortran, Julia, R, Ruby, PHP, LuaJIT, Haskell, Nim, Objective-C, and similar runtimes;
- **HTTP/JSON:** start `cosmos-bio-cns serve --host 127.0.0.1 --port 8765` and POST observations to `/v1/observe`.

The HTTP reference bridge is unauthenticated and loopback-only by default. `--allow-remote` is a development escape hatch, not production security.

## Add your own sensor

```python
class MySensor:
    name = "my-sensor"
    def connect(self): ...
    def read(self): return [BioObservation(...)]
    def disconnect(self): ...
```

Adapters report observations, not diagnoses or emotional conclusions. Open-source code rights never override a human subject's data permissions.

## Local-first design

The CNS loop works without cloud services. Cloud bridges are optional sinks/reconciliation extensions. Keep credentials outside source control and prefer managed identities/secret stores where available.

## Research boundaries

- 12D/42D/54D are computational state representations in this software lineage, not literal extra spacetime claims;
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

Please cite the software repository and foundational CST deposit. The DOI is research lineage; this repository does not claim the DOI was issued specifically for this software package.

## License and data boundary

Software/configuration: Apache License 2.0. Repository-authored documentation/paper text: CC BY 4.0 unless stated otherwise. Open-source software rights do not grant permission to redistribute private human biosignal data.

See `LICENSE`, `LICENSE-DOCS.md`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, and `docs/DISTRIBUTION.md`.
