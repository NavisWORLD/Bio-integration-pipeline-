# Distribution and Reuse Guide

## Code license

The Python source in this repository is released under the Apache License 2.0.

You may use, modify, redistribute, and commercially deploy the code subject to the license terms. Preserve the `LICENSE` file, copyright notices, and any `NOTICE` material that applies to redistributed copies.

Apache-2.0 was selected for the reusable library because it is permissive and includes an explicit patent-license framework for contributions. This is not legal advice; organizations should have counsel review their own distribution obligations.

## Documentation and paper text

Repository-authored documentation and companion manuscript are intended for broad educational/research redistribution with attribution to Cory Shane Davis and this repository. Third-party material is not relicensed by this project.

## What downstream projects should keep

- `LICENSE`;
- applicable `NOTICE` entries;
- provenance/citation to this repository when derived substantially from it;
- the foundational research citation where CST-specific architecture is discussed;
- safety/privacy boundaries if handling human biosignal data.

## PyPI-style build

```bash
python -m pip install --upgrade build
python -m build
```

Validate artifacts:

```bash
python -m pip install --upgrade twine
twine check dist/*
```

Then publish only from an account/organization authorized to use the chosen package name.

## Vendoring

Downstream applications may vendor `src/cosmos_bio_cns` directly. Keep license and notices adjacent to the vendored code.

## Container/mobile/native projects

The Python package can act as a local service or reference implementation. Native iOS/Android/C++/Rust implementations should preserve the event schemas and adapter/CNS boundaries, not copy device permissions or secrets into shared source.

## Human data

Do not distribute raw biometric datasets merely because the software is open source. Dataset consent, privacy, retention, jurisdiction, and research approvals are separate from the software license.
