# Azure Heartbeat and Storage/Reconciliation Guide

The local runtime does not require Azure. Azure is an optional continuity, ingestion, and reconciliation layer.

## Recommended topology

```text
local sensors
  → Bio/CNS runtime
  → heartbeat/event sink
  → Azure IoT Hub
  → Event Hubs
  → immutable archive / Data Lake
  → normalization worker
  → live state database
  → change/reconciliation worker
  → cloud-to-device desired state or command
  → local runtime
```

## Storage rule

Keep two different concepts:

1. immutable/raw event history: what arrived;
2. materialized current state: what the system currently believes.

Do not overwrite history just because the current state changed.

## Event identity

Use a stable idempotency tuple such as:

```text
cosmos_id + boot_id + stream + sequence
```

This makes retransmission safe after offline operation.

## Device-to-cloud

`AzureIoTEventSink` is intentionally a thin transport. It publishes the event type and JSON payload to IoT Hub. Production deployments should use device-specific credentials/identity and rotate/revoke credentials independently.

## Cloud-to-device

Use persistent desired configuration for settings that must survive reconnects, and explicit commands for immediate actions. The local project remains authoritative over irreversible operations; cloud reconciliation should propose/version updates rather than silently rewriting local lineage.

## Offline-first loop

```text
if cloud available:
    publish event
else:
    append durable local queue

on reconnect:
    replay unacknowledged events
    deduplicate by event identity
    reconcile versions
```

## Security

Never commit IoT Hub connection strings or Azure keys. Use environment injection, platform identity, or a secret manager. Separate ingestion, processing, training, and administrator permissions.
