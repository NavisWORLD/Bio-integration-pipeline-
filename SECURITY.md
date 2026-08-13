# Security Policy

## Never commit

- Azure/IoT connection strings;
- API keys or tokens;
- private keys or credentials;
- private biometric datasets;
- raw camera/audio recordings without an explicit public-data decision;
- personally identifying consent records.

## Local HTTP bridge

The reference JSON bridge is designed for loopback use and has no built-in authentication layer. By default it refuses non-loopback binds. `--allow-remote` is an explicit escape hatch for controlled development environments, not a production security feature.

Before any network-exposed deployment, place the service behind an authenticated, encrypted transport and perform a deployment-specific security/privacy review. Do not assume CORS, a private-looking hostname, or obscurity provides authorization.

## Reporting

For security issues, use GitHub's private vulnerability reporting feature when available instead of opening a public issue containing exploit details or credentials.

## Threat model priorities

- credential theft;
- unauthorized sensor activation or observation submission;
- replay/forgery of bio events;
- unit/schema confusion;
- cross-thread event-order corruption;
- event-ledger tampering;
- accidental raw-media retention;
- cloud reconciliation overwriting local lineage;
- remote exposure of the unauthenticated reference bridge.
