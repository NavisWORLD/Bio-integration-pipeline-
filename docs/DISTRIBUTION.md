# Distribution and Reuse Guide

## Code license

The Python source and software configuration in this repository are released under the Apache License 2.0.

You may use, modify, redistribute, and commercially deploy the code subject to the license terms. Preserve the `LICENSE` file, copyright notices, modification notices where required, and any applicable `NOTICE` material with redistributed copies.

Apache-2.0 was selected for the reusable library because it is permissive and includes an explicit patent-license framework for contributions. This guide is not legal advice; organizations should have qualified counsel review their own distribution obligations when needed.

## Documentation and companion-paper license

Unless a file states otherwise, repository-authored material under `docs/` and `paper/` is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0), as recorded in `LICENSE-DOCS.md`.

That means downstream users may share and adapt the repository-authored documentation and companion paper, including commercially, with appropriate attribution, a license reference, and an indication of changes.

Third-party publications, trademarks, datasets, quoted material, external links, and other third-party works are not relicensed by this repository.

## What downstream projects should keep

- `LICENSE` for covered software;
- `LICENSE-DOCS.md` when redistributing covered repository-authored documentation/paper material;
- applicable `NOTICE` entries;
- notices identifying modified files where the Apache-2.0 terms require them;
- provenance/citation to this repository when substantially derived from it;
- the foundational research citation where CST-specific architecture or terminology is discussed;
- safety/privacy boundaries if handling human biosignal data.

Suggested repository attribution:

> Cory Shane Davis, COSMOS Bio/CNS Integration Pipeline, https://github.com/NavisWORLD/Bio-integration-pipeline-, foundational CST DOI 10.5281/zenodo.17574447.

## PyPI-style build

```bash
python -m pip install --upgrade build
python -m build
```

Validate artifacts:

```bash
python -m pip install --upgrade twine
python -m twine check dist/*
```

Then publish only from an account or organization authorized to use the chosen package name.

## Vendoring

Downstream applications may vendor `src/cosmos_bio_cns` directly. Keep the Apache-2.0 license and applicable notices adjacent to the vendored code.

## Container/mobile/native projects

The Python package can act as a local service or reference implementation. Native iOS/Android/C++/Rust implementations should preserve the event schemas and adapter/CNS boundaries when interoperability is desired, and must not copy device permissions, user secrets, or credentials into shared source.

## Human data

Do not distribute raw biometric datasets merely because the software is open source. Dataset consent, privacy, retention, jurisdiction, institutional review requirements, and other applicable obligations are separate from the software and documentation licenses.

## Release validation

The repository includes `.github/workflows/ci.yml`, which runs supported-Python tests, source compilation, CLI smoke tests, package builds, and distribution metadata validation. See `docs/RELEASE_READINESS.md` for the release-readiness scope.
