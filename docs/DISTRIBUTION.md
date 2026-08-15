# Distribution and Reuse Guide

## Current rights boundary

Beginning with the 0.3.x rights-boundary generation on 2026-08-15, newly authored or materially revised Cory Shane Davis / NavisWORLD material distributed under the repository `LICENSE` is rights reserved unless a file expressly states different terms.

Public source visibility is not a general permission to copy, modify, port, translate, distribute, sublicense, commercialize, host, or incorporate covered current material into another product. Additional rights require a separate written agreement where the `LICENSE` says so.

## Historical software license

The 0.1.x and 0.2.x software/configuration releases were distributed under Apache License 2.0. Copies validly obtained under Apache-2.0 retain the rights granted by Apache-2.0, including the historical copyright and patent permissions applicable to those copies.

Those grants are not revoked by the 0.3.x rights boundary. See `LICENSE_HISTORY.md` for the pre-boundary commit record.

## Historical documentation and companion-paper license

Repository-authored documentation and companion-paper material in the 0.1.x and 0.2.x generations was offered under Creative Commons Attribution 4.0 International (CC BY 4.0), unless a file stated otherwise.

Valid historical CC BY 4.0 grants remain in force for those copies. Newly authored or materially revised documentation distributed under the current rights notice is governed by `LICENSE-DOCS.md` unless a file states different terms.

## Commercial distribution of current covered material

Commercial, enterprise, OEM, hosted-service, paid deployment, commercial research, product integration, or commercial AI/ML use of current covered material requires separate written authorization from Cory Shane Davis unless applicable law independently permits the specific use.

The current `LICENSE` grants no new public patent license.

## Third-party material

Third-party code, SDKs, cloud services, models, datasets, publications, trademarks, and dependencies retain their own licenses and terms. The current rights reservation does not relicense them.

## Human data

No software or documentation license grants permission to collect, process, retain, redistribute, sell, or disclose private biometric or physiological data. Consent, privacy, security, medical, research, and jurisdiction-specific obligations are separate.

## Package and application builds

The repository remains buildable as an engineering reference. Building a package or application for local evaluation does not expand the rights granted by the current `LICENSE`.

Python build:

```bash
python -m pip install --upgrade build
python -m build
python -m twine check dist/*
```

Before publishing a package, installer, mobile app, hosted service, fork, translated SDK, or derivative distribution, determine which historical or current license governs the exact material involved and obtain any additional authorization required.

## Provenance

Suggested citation for factual provenance:

> Cory Shane Davis, COSMOS Bio/CNS Integration Pipeline, https://github.com/NavisWORLD/Bio-integration-pipeline-, foundational CST DOI 10.5281/zenodo.17574447.

Citation is not a substitute for permission when permission is required.
