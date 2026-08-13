# Release Checklist

Use this before tagging or publishing any release.

## Code

- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] `python -m compileall -q src examples tests` passes.
- [ ] CLI demo and ledger verification pass.
- [ ] HTTP bridge regression test passes.
- [ ] Consent and baseline-isolation tests pass.
- [ ] No `TODO`/`FIXME` items block the release.

## Package

- [ ] Version is consistent in `pyproject.toml`, `src/cosmos_bio_cns/__init__.py`, `CITATION.cff`, and changelog.
- [ ] `python -m build` succeeds.
- [ ] `twine check dist/*` succeeds.
- [ ] Wheel includes `py.typed` and packaged JSON schemas.

## Documentation

- [ ] README release status matches reality.
- [ ] Quickstart works from a clean environment.
- [ ] API reference matches public behavior.
- [ ] Architecture, Azure, interoperability, distribution, teacher, and research-boundary documents remain current.
- [ ] Foundational DOI/citation metadata is unchanged unless independently verified.

## Security and privacy

- [ ] No live credentials, tokens, private keys, connection strings, or private human data are committed.
- [ ] Remote HTTP exposure is not enabled by default.
- [ ] Human-data consent/retention rules are documented.
- [ ] Dependency alerts/updates have been reviewed.

## Research claims

- [ ] Implemented/observed/measured/null/hypothesis boundaries are preserved.
- [ ] No medical, consciousness, physical-dimensionality, or quantum-advantage claim is inferred from the software mechanism alone.
- [ ] Any new benchmark identifies exact artifact, data, metric, seeds/configuration, and limitations.

## Final

- [ ] GitHub Actions is green on the exact commit being tagged.
- [ ] `docs/RELEASE_READINESS.md` still accurately describes scope.
- [ ] Release notes list user-visible changes and limitations.
