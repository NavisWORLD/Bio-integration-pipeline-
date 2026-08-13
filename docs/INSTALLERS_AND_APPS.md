# Installers and Mobile Apps

The v0.1.0 release line has first-party packaging targets for Windows, macOS, Android, and iOS.

## Windows

GitHub Actions builds the real local CNS desktop application with PyInstaller and then wraps it in an Inno Setup installer.

Release artifacts:

- `COSMOS-Bio-CNS-Setup-Windows-x64.exe` — one-click per-user installer with Start Menu shortcut and optional desktop shortcut.
- `COSMOS-Bio-CNS-Windows-x64-portable.exe` — portable single-file executable.

The desktop application runs the repository's actual `PushBioAdapter -> BioFusionEngine -> LocalCNS -> SQLiteEventStore -> heartbeat` path locally.

## macOS

GitHub Actions builds a native Apple Silicon `.app` bundle around the same desktop runtime and packages it in a DMG.

Release artifacts:

- `COSMOS-Bio-CNS-macOS-arm64.dmg`
- `COSMOS-Bio-CNS-macOS-arm64.app.zip`

The CI build is ad-hoc signed so its bundle integrity is checked. It is not Apple-notarized. Public distribution without Gatekeeper warnings requires an Apple Developer ID certificate and notarization credentials.

## Android

`apps/android/` is a first-party Android application. It is intentionally dependency-light: one Activity, the Android platform HTTP stack, and the repository's `/v1/observe` JSON contract.

Release artifact:

- `COSMOS-Bio-CNS-Android-debug.apk`

The APK is installable for testing and local integration. The default emulator endpoint is `http://10.0.2.2:8765`. A physical device needs a reachable host address. Network-facing bridge deployments require authentication and encrypted transport; `--allow-remote` alone is not a production security layer.

## iPhone / iOS

`apps/ios/` is a first-party SwiftUI application using the same `/v1/observe` contract. CI generates the Xcode project, compiles it against the iOS Simulator SDK, and packages the resulting app bundle.

Release artifact:

- `COSMOS-Bio-CNS-iOS-Simulator.app.zip`

A simulator build proves the source compiles as an iOS application without requiring a private signing identity. A physical-device/App Store IPA cannot be universally pre-signed by an open-source repository: Apple requires the distributor's Apple team, certificates, and provisioning profile. Open `apps/ios/CosmosBioCNS.xcodeproj` after running XcodeGen, select your team, and Xcode can create the development provisioning profile for your device.

## Release automation

`.github/workflows/platform-builds.yml` builds all platform artifacts on pull requests and on `main`. When the workflow succeeds on `main`, its release job creates or refreshes GitHub Release `v0.1.0` and uploads the tested artifacts.

The release workflow does not claim medical, clinical, App Store, Microsoft Store, or notarization certification. It certifies that the corresponding CI build target completed and produced the named artifact.
