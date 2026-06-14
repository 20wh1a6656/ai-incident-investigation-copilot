# SOP-105: Troubleshooting Multi-Factor Authentication (MFA) Failures

# Incident Category
Identity & Access Management

# Business Impact
Critical - Users locked out of MFA verification pipelines, disabling authentication.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Users report MFA passcode input results in login timeout errors.
- MFA provider logs show 'Callback connection timeout' alerts.
- VPN gateway authentication times out waiting for Duo push response.
- SSO portal returns 'MFA provider endpoint unreachable' errors.
- LDAP bind attempts succeed but login hangs at MFA phase.
- Duo API connection metrics dashboard show extreme latency spikes.
- Active Directory sync agent reports callback connection refused.
- DNS lookup failures for api.duosecurity.com endpoints.
- Email notification alerts fail to deliver due to gateway timeout.
- Multiple services reporting authentication verification failures.
- SMS dispatch logs show MFA codes are not being delivered.
- SAML assertions reject identity metadata due to missing MFA attribute.
- Kubernetes pods reporting connectivity timeouts to external identity systems.
- API gateway returns HTTP 504 gateway timeout on login routes.
- Duo security proxy logs report thread locks under heavy load.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Duo Security or Okta MFA API endpoint network routing down.
- Duo auth proxy daemon thread starvation under load peaks.
- Firewall blocking outgoing MFA callback ports (443).
- Local DNS resolver failing to resolve api.duosecurity.com.
- MFA provider TLS certificate expired or revoked.
- Time drift on local servers causing authentication key mismatches.
- SMS gateway provider network connectivity degraded.
- MFA bypass policy misconfigured during update.
- Duo proxy credentials rotated but not updated.
- Network connection saturation peaks on corporate WAN links.
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
1. Check Duo Security or Okta service status pages.
2. Verify local DNS resolution of api.duosecurity.com.
3. Inspect Duo auth proxy logs for thread locking or connection errors.
4. Verify local system clock synchronization using NTP query.
5. Confirm outbound connection to port 443 via curl.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Restart Duo auth proxy daemon.
- Enable temporary SRE emergency bypass policy if approved.
- Route traffic through backup DNS resolvers.
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
mfa, duo, okta, authentication, verification, callback, push, passcode, timeout, latency, dns, resolve, api, proxy, vpn, gateway, sso, saml, ldap, email, sms, network, firewall, tls, ssl, certificate, drift, clock, wan, vpc, active directory, bind, port, credentials, thread, starvation, connection, pool, identity, provider, token, mfa-provider, duo-push, auth-proxy, duo-timeout, mfa-bypass, sms-gateway

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
