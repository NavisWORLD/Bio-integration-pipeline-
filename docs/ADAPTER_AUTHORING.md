# Adapter Authoring Guide

A sensor adapter is deliberately small. It should know how to acquire a measurement and report its reliability; it should not decide what the measurement "means" psychologically or medically.

## Contract

```python
from cosmos_bio_cns.models import BioObservation, ConsentScope

class MyAdapter:
    name = "example"

    def connect(self) -> None:
        ...

    def read(self) -> list[BioObservation]:
        return [BioObservation(
            sensor="example-device",
            channel="example_channel",
            value=1.0,
            unit="arbitrary",
            quality=0.95,
            sequence=1,
            subject_id="pseudonym",
            device_id="device-pseudonym",
            consent=ConsentScope(
                session_id="session-001",
                bio_processing=True,
                raw_retention=False,
            ),
        )]

    def disconnect(self) -> None:
        ...
```

## Consent behavior

`ConsentScope` is not decorative metadata. If `bio_processing=False`, `BioFusionEngine` rejects that observation before baseline or CNS processing.

A downstream application is still responsible for obtaining valid consent/permission and deciding what consent semantics are appropriate for its jurisdiction and use case. This software flag does not itself constitute legal consent.

## Units and baseline identity

Personal baselines are isolated by:

```text
subject_id + sensor + channel + unit
```

Use explicit stable units. Do not send one stream as `bpm` and later silently switch it to `Hz`, milliseconds, normalized values, or another representation under the same unit label.

## Recommended production additions

- permission/capability detection;
- reconnect/backoff logic;
- monotonic sequencing;
- clock drift handling;
- explicit unit conversion;
- confidence/quality calculation;
- calibration metadata;
- documented sampling cadence;
- user-controlled consent and retention policy;
- device/firmware provenance when measurements depend on it;
- tests for unavailable sensors, low-quality data, reconnects, and unit changes.

## Do not

- silently convert unknown units;
- invent a quality score when the device cannot support one;
- store raw media merely because it is available;
- declare emotions or diagnoses inside the adapter;
- treat an open-source license as permission to process or publish human data;
- commit credentials or personally identifying data.
