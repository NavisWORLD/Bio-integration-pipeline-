# Security Policy

## Never commit

- Azure/IoT connection strings;
- API keys or tokens;
- private biometric datasets;
- raw camera/audio recordings without an explicit public-data decision;
- personally identifying consent records.

## Reporting

For security issues, use GitHub's private vulnerability reporting feature when available instead of opening a public issue containing exploit details or credentials.

## Threat model priorities

- credential theft;
- unauthorized sensor activation;
- replay/forgery of bio events;
- unit/schema confusion;
- event-ledger tampering;
- accidental raw-media retention;
- cloud reconciliation overwriting local lineage.
