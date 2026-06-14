# SOP-102: Single Sign-On (SSO) Portal Authentication Failures

# Incident Category
Identity & Access Management

# Business Impact
Critical - All corporate portals and internal tools (Okta, Jira, Github) unreachable.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Okta login page returns '400 Bad Request' or SAML signature invalid error.
- SSO authentication redirect loops on user web browsers.
- Active Directory sync agent reports 'Authentication synchronization timeout'.
- Internal identity provider logs show 'SAML assertion token validation expired'.
- MFA validation responses drop at Duo callback endpoints.
- VPN gateway rejects users mapping to Active Directory profiles.
- DNS lookup failures for internal domain controller addresses.
- Okta service agent reports NXDOMAIN for critical LDAP directories.
- LDAP bind failures registered in authorization middleware logs.
- SMTP alerts show smtp.mail-provider.com refused credentials.
- Multiple microservices reporting authentication credentials validation errors.
- OAuth client libraries throwing token verification exceptions.
- Active Directory domain controllers register credential signature mismatch.
- SAML assertions reject identity metadata mismatch alerts.
- Okta API interface returns HTTP 503 service unavailable codes.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Okta SAML signing TLS certificate expired or mismatch.
- Active Directory federation services (ADFS) servers offline.
- Time drift on application servers exceeding SAML clock skew tolerances.
- Duo security API proxy server network routes dropped.
- CoreDNS resolver mapping okta.com incorrectly.
- LDAP directory schema mismatch after automated script upgrade.
- Corporate SSO portal token caching tables saturated in database.
- Firewall rules blocking SAML token exchange payloads.
- Database pool exhaustion on Identity Provider schema.
- LDAP bind user credentials expired or locked.
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
1. Inspect Okta Admin portal system log for token reject reasons.
2. Verify system clock synchronization on AD and application nodes.
3. Run openssl command to check active SAML certificate expiration date.
4. Check LDAP bind logs for 'user locked' error strings.
5. Confirm that CoreDNS is resolving external Identity Provider endpoints.
6. Verify active directory federation services status.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Force SAML certificate token key rotation.
- Restart Active Directory sync agents.
- Synchronize application nodes clocks via NTP.
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
sso, login, okta, saml, assertion, authentication, adfs, active directory, ldap, mfa, duo, token, redirect, certificate, tls, ssl, oauth, api, database, pool, exhaustion, timeout, dns, nxdomain, resolved, smtp, credential, signature, verification, auth, identity, provider, directory, clock, drift, sync, federation, user, cookie, session, cache, token, ldap-bind, saml-token, okta-auth, sso-portal, adfs-server, identity-provider

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
