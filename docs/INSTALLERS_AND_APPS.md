# Installers and Mobile Apps

The v0.2.0 release line has first-party packaging targets for Windows, macOS, Android, iOS, Python, and the cross-language SDK source bundle.

## Windows

- `COSMOS-Bio-CNS-Setup-Windows-x64.exe` — one-click per-user installer.
- `COSMOS-Bio-CNS-Windows-x64-portable.exe` — portable executable.

The desktop application runs the real `PushBioAdapter -> BioFusionEngine -> LocalCNS -> SQLiteEventStore -> heartbeat` path locally.

## macOS

- `COSMOS-Bio-CNS-macOS-arm64.dmg`
- `COSMOS-Bio-CNS-macOS-arm64.app.zip`

The CI build is ad-hoc signed for bundle-integrity verification. Apple notarization requires distributor credentials.

## Android

`apps/android/` is a first-party Android application using the `/v1/observe` contract. Release artifact: `COSMOS-Bio-CNS-Android-debug.apk`.

## iPhone / iOS

`apps/ios/` is a first-party SwiftUI application using the same `/v1/observe` contract. Release artifact: `COSMOS-Bio-CNS-iOS-Simulator.app.zip`.

A physical-device/App Store IPA requires the distributor's Apple team, certificate, and provisioning profile.

## Cross-language SDKs

The source release includes `sdk/` with Rust, C++, C ABI, Go, JavaScript/TypeScript, Java/JVM, C#/.NET, Swift, Kotlin interoperability guidance, the kernel specification and the golden parity vector.

## Release automation

`.github/workflows/platform-builds.yml` validates application/package targets before release publication. `.github/workflows/cross-language.yml` independently compiles/tests the SDK matrix.

These workflows certify engineering build targets, not medical, clinical, App Store, Microsoft Store, or notarization certification.
