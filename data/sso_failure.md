# SOP-102: Single Sign-On (SSO) Authentication Failures

## Overview
SSO failures occur when Okta / Active Directory credentials cannot synchronize or when SAML assertions expire.

## Diagnostics Steps
1. Verify token expiration timers in application logs (`invalid_grant` or `signature_verification_failed`).
2. Test user authentication parameters directly via AD mock endpoints.
3. Verify TLS certificates are valid and match current key pairs.

## Mitigation Action
Renew expired token signatures:
```bash
okta-admin-sync --force-renew
```
Clear user cache blocks to invalidate outdated session cookies.
