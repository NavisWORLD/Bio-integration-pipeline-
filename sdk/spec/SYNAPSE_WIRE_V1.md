# COSMOS Synapse Kernel / Wire Contract v1

This document freezes the cross-language deterministic state transition used by the Bio/CNS interoperability SDKs.

## Scope

The kernel is a compact computational state update. It is not a medical model, consciousness test, emotion decoder, biological nervous system, or claim about physical extra dimensions.

## Inputs

- `previous_state`: finite vector of N floating-point values, N > 0.
- `features`: ordered pairs of `(baseline_delta, quality)`.
- `quality`: finite value in `[0,1]`.
- `leak`: finite value in `[0,1)`; reference default `0.88`.
- `input_gain`: finite non-negative value; reference default `0.12`.
- `phase_step`: constant `0.61803398875`.

For feature j:

`input_j = tanh(baseline_delta_j) * quality_j`

For state dimension i, zero-based:

`source_i = input_(i mod feature_count)`

`phase_i = sin((i + 1) * 0.61803398875)`

`next_i = clamp(leak * previous_i + input_gain * source_i * phase_i, -1, 1)`

If `features` is empty, the vector is unchanged and a stateful engine still increments its revision while reporting confidence `0.0`.

## Numerical parity

`sdk/spec/golden_vector.json` is the normative parity vector. First-party implementations must match each expected element within absolute tolerance `1e-12` on IEEE-754 double precision platforms.

## Transport contract

The synaptic kernel is transport-independent. Full Bio/CNS observations continue to use the repository JSON schemas and `/v1/observe` HTTP endpoint. Languages that do not use a first-party native SDK can integrate through HTTP/JSON or the stable C ABI exported by the C++ package.

## Versioning

Changing the equation, ordering, constant, validation domain, or empty-feature behavior requires a new wire-contract version and a new golden vector. Cosmetic refactors do not.
