# Adapter Authoring Guide

A sensor adapter is deliberately small. It should know how to acquire a measurement and report its reliability; it should not decide what the measurement "means" psychologically or medically.

## Contract

```python
from cosmos_bio_cns.models import BioObservation

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
        )]

    def disconnect(self) -> None:
        ...
```

## Recommended production additions

- permission/capability detection;
- reconnect/backoff logic;
- monotonic sequencing;
- clock drift handling;
- explicit unit conversion;
- confidence/quality calculation;
- calibration metadata;
- documented sampling cadence;
- user-controlled consent and retention policy.

## Do not

- silently convert unknown units;
- invent a quality score when the device cannot support one;
- store raw media merely because it is available;
- declare emotions or diagnoses inside the adapter;
- commit credentials or personally identifying data.
