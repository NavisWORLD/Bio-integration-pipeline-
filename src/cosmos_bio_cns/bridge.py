from __future__ import annotations

from pathlib import Path
from typing import Protocol, Any
import json


class EventSink(Protocol):
    def publish(self, event_type: str, payload: dict[str, Any]) -> None: ...


class JSONLEventSink:
    """Portable offline-first event sink."""

    def __init__(self, path: str | Path = "cosmos_events.jsonl") -> None:
        self.path = Path(path)

    def publish(self, event_type: str, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"event_type": event_type, "payload": payload}, sort_keys=True) + "\n")


class AzureIoTEventSink:
    """Optional Azure IoT Hub sink.

    Install with: pip install 'cosmos-bio-cns[azure]'
    Pass an IoT Hub device connection string at runtime; never hardcode it in source control.
    """

    def __init__(self, connection_string: str) -> None:
        try:
            from azure.iot.device import IoTHubDeviceClient, Message
        except ImportError as exc:
            raise RuntimeError("Azure extras are not installed") from exc
        self._Message = Message
        self._client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        self._client.connect()

    def publish(self, event_type: str, payload: dict[str, Any]) -> None:
        body = json.dumps({"event_type": event_type, "payload": payload}, sort_keys=True)
        message = self._Message(body)
        message.custom_properties["event_type"] = event_type
        self._client.send_message(message)

    def close(self) -> None:
        self._client.shutdown()
