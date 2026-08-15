# Contributing

Thank you for helping make the bio/CNS integration layer easier to test and evaluate.

## Useful contributions

- reproducible bug reports;
- benchmark results and null results;
- security reports;
- interoperability observations;
- documentation corrections;
- proposed sensor-adapter designs with clear units and quality semantics.

## Requirements

1. Do not commit real private biometric data, credentials, API keys, or raw consent-sensitive recordings.
2. Keep sensor observation separate from interpretation.
3. Document units, sampling behavior, and failure modes.
4. Do not market a contribution as medical, diagnostic, or consciousness-detecting without independent evidence and appropriate regulatory work.
5. Do not submit third-party code or documentation unless you have the rights necessary to do so and clearly identify its source and license.

## Copyrightable code and documentation contributions

The current 0.3.x rights-reserved generation does **not** automatically accept copyrightable pull-request contributions under Apache-2.0.

No external copyrightable contribution will be incorporated into the rights-reserved core unless the contributor and Cory Shane Davis first execute a written contributor, assignment, or other rights agreement sufficient to permit incorporation and future licensing.

Opening an issue, pull request, discussion, or sending a patch does not by itself transfer copyright ownership or grant Cory Shane Davis rights beyond those independently provided by law or an applicable agreement. Likewise, repository participation does not grant the contributor additional rights in Cory-owned material.

Historical contributions and copies remain governed by the license terms applicable when they were validly distributed. See `LICENSE_HISTORY.md`.

## Development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
python -m unittest discover -s tests -v
```
