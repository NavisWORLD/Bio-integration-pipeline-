from __future__ import annotations

from importlib.resources import files
import json
from typing import Any


_SCHEMA_FILES = {
    "bio_observation": "bio_observation.schema.json",
    "heartbeat": "heartbeat.schema.json",
}


def load_schema(name: str) -> dict[str, Any]:
    """Load a packaged language-neutral JSON schema by stable short name."""
    try:
        filename = _SCHEMA_FILES[name]
    except KeyError as exc:
        raise KeyError(f"unknown schema {name!r}; choose from {sorted(_SCHEMA_FILES)}") from exc
    resource = files("cosmos_bio_cns.schemas").joinpath(filename)
    return json.loads(resource.read_text(encoding="utf-8"))
