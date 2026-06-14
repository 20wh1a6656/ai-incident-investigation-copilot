# SOP-106: Handling Identity Provider (IdP) Outages

# Incident Category
Identity & Access Management

# Business Impact
Critical - Complete loss of user authorization and SSO logins across the enterprise.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Okta or Azure AD returns HTTP 503 Service Unavailable errors.
- SAML redirect requests fail with connection timed out.
- SSO portal login forms do not load on user browsers.
- LDAP authentication requests reject bind credentials.
- VPN gateway authentication drops user authorization maps.
- Duo push notifications time out due to missing IdP callback.
- Microservices log 'Identity metadata query returned null'.
- DNS lookup failures for corporate IdP domain names.
- OAuth token verification libraries throw signature validation errors.
- SMTP alert emails fail to deliver due to authentication timeout.
- Active Directory sync agent reports sync service offline.
- MFA validation responses fail to associate with user profiles.
- VPC tunnel gateways drop active directory verification routes.
- Internal corporate wikis show 'Unable to map user roles' alerts.
- API gateway returns HTTP 502 bad gateway on login paths.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- External Identity Provider (e.g. Okta, Azure AD) core system outage.
- Corporate IdP DNS zone delegation dropped.
- IdP SAML signing certificates expired or mismatched.
- Active Directory federation servers offline or database corrupt.
- TLS handshake failures between application clusters and IdP.
- Corporate firewall rules blocking outgoing IdP traffic.
- Time sync drift on corporate domain controllers.
- IdP integration configuration modified without authorization.
- OAuth token signing keys rotated without updating metadata endpoint.
- Network routing issues on corporate boundary gateway links.
- Network packet drops on critical WAN gateway links.
- Subnet routing changes dropping VPC registry entries.
- Intermediate CA validation failure on authentication trust paths.
- Local thread pool starvation under high transaction latency.
- Outdated session caches locking user authentication tables.

# Investigation Steps
## Phase 1: Ingestion & Verification
1. Gather core incident symptoms from the alert console (descriptions, alarms, logs).
2. Check network link latency metrics on boundary router interfaces.
3. Test local hostname resolution using standard lookup commands.

## Phase 2: Diagnostic Checks
1. Check external IdP (Okta/Azure) status page for global issues.
2. Run dig command to check IdP domain name resolution status.
3. Inspect SSO middleware logs for SAML signature errors.
4. Verify target federation servers service status.
5. Confirm that system clock is synchronized across clusters.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Engage failover emergency access protocols.
- Restore previous stable IdP integration config metadata.
- Rotate SAML token signing keys in corporate console.
- Flush local authentication cache lists.
- Route outbound traffic through backup gateway paths.
- Enable temporary authentication bypass policy if approved by security.

# Escalation Guidance
- **L1 Support**: Perform initial verification checks (host pings, telnet connection checks). If the issue is not resolved within 15 minutes, escalate to L2.
- **L2 Operations**: Inspect proxy server logging trails, check local configuration files, and check resource metrics on nodes. Escalate to L3 if changes require cluster alterations.
- **L3 Specialist**: Alter VPC routing tables, rotate security certificates, alter database connection pool configurations, and modify system kernel settings.
- **Vendor Support**: Open tickets with external identity, cloud, or email providers if global service outages are reported on their status pages.

# Verification Checklist
- [ ] Active authentication request timeouts return below 1% threshold limits.
- [ ] Network packet loss drops to 0% on boundary links.
- [ ] Client connections establish successfully without timeouts.
- [ ] Application thread pools and database connection counts stabilize.

# Related Systems
- Identity Providers (Okta, Azure Active Directory)
- Kubernetes Cluster DNS Resolver (CoreDNS)
- PostgreSQL Database Master Replica
- Email Delivery SMTP Gateways
- Border Gateway Firewalls & Routers

# Keywords
idp, identity, provider, okta, azure, outage, sso, saml, metadata, oauth, token, signature, verification, auth, dns, resolve, ldap, active directory, bind, vpn, gateway, mfa, duo, timeout, latency, connection, pool, firewall, tls, ssl, certificate, drift, clock, smtp, vpc, sync, federation, user, role, authorization, check, identity-provider, idp-outage, saml-signing, oauth-token, idp-metadata, idp-dns

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
