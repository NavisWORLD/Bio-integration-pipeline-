# Cross-Language Synapse SDK

The Bio/CNS subsystem now has one canonical deterministic synaptic contract and several first-party native implementations.

## First-party implementations

| Ecosystem | Path | Native parity test |
|---|---|---|
| Python | `src/cosmos_bio_cns/synapse.py` | yes |
| Rust | `sdk/rust/` | `cargo test` |
| C++17 | `sdk/cpp/` | CMake + CTest |
| C ABI | `sdk/cpp/include/cosmos_synapse/cosmos_synapse_c.h` | exercised by C++ test |
| Go | `sdk/go/` | `go test ./...` |
| JavaScript / TypeScript | `sdk/javascript/` | `npm test` / Node |
| Java | `sdk/java/` | `javac` + golden runner |
| Kotlin / Android | JVM Java SDK + Android bridge | Java parity + Android build |
| C# / .NET | `sdk/csharp/` | `dotnet run` golden runner |
| Swift | `sdk/swift/` | `swift test` |

All native math implementations target the same `sdk/spec/golden_vector.json` and absolute tolerance `1e-12`.

## Languages without a dedicated folder

The project intentionally does **not** maintain dozens of independently copied equations. Any language with either HTTP/JSON or C FFI can use the same system:

- Objective-C, Zig, D, Nim, Fortran, Julia, R, Ruby, PHP, Lua/LuaJIT, Haskell, OCaml, Crystal and similar native runtimes can bind the C ABI;
- Dart/Flutter, Elixir/Erlang, Scala, Groovy, Perl and browser/server languages can use the loopback HTTP/JSON bridge;
- Kotlin uses the Java/JVM implementation directly;
- mobile applications may also use the existing native Android and SwiftUI clients.

This design gives broad compatibility while keeping the equation versioned in one specification rather than allowing silent language drift.

## Python

```python
from cosmos_bio_cns import SynapticFeature, cosmos_12d_step

state = (0.0,) * 12
state = cosmos_12d_step(state, [SynapticFeature(0.5, 0.9), SynapticFeature(-0.25, 0.8)])
```

## Rust

```rust
use cosmos_synapse::{Feature, SynapseState};
let mut state = SynapseState::cosmos_12d();
let update = state.update(&[Feature::new(0.5,0.9)?, Feature::new(-0.25,0.8)?], 0.85)?;
```

## C++

```cpp
cosmos::synapse::State state;
auto update = state.update({{0.5,0.9},{-0.25,0.8}}, 0.85);
```

## C ABI

Use `cosmos_synapse_create`, `cosmos_synapse_update`, and `cosmos_synapse_destroy`. The ABI uses only C-compatible primitive arrays and an opaque handle, making it suitable for FFI generators and foreign runtimes.

## Full Bio/CNS transport

The synaptic SDK handles the deterministic compact state transition. Full observations, consent, timestamps, persistence, heartbeat and runtime orchestration remain available from the Python runtime and `/v1/observe` bridge. This separation keeps tiny embedded/native integrations possible without pretending every language needs to duplicate the entire host runtime.
