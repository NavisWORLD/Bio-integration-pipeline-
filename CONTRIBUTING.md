# Contributing

Thank you for helping make the bio/CNS integration layer easier to test and reuse.

## Good contributions

- new sensor adapters with clear units and quality semantics;
- tests for baseline/fusion/CNS behavior;
- privacy-preserving feature extraction;
- offline/replay/reconciliation tooling;
- benchmark harnesses and null-result reporting;
- documentation and teaching examples.

## Requirements

1. Do not commit real private biometric data, credentials, API keys, or raw consent-sensitive recordings.
2. Keep sensor observation separate from interpretation.
3. Add tests for behavior changes.
4. Document units, sampling behavior, and failure modes.
5. Do not market a contribution as medical/diagnostic or consciousness-detecting without independent evidence and appropriate regulatory work.

## Development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
python -m unittest discover -s tests -v
```

By contributing, you agree that your contribution is provided under the repository's Apache-2.0 license.
