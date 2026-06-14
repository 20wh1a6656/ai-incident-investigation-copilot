# SOP-101: Troubleshooting VPN Gateway Connection and Authentication Failures

# Incident Category
Network / Identity & Access Management

# Business Impact
High - Blocked external access for remote SRE teams, developers, and corporate operations.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Client connection timeout at IPSEC phase-2 handshake.
- AnyConnect reports 'Authentication failed due to host timeout' codes.
- VPN gateway controller logs show 'Tunnel authentication rejected: LDAP search timeout'.
- Radius server reports Packet Drop on VPN authentication ports.
- Duo MFA callback timeouts registered for remote connections.
- Boundary routers show high traffic saturation peaks.
- Active Directory domain controllers report high LDAP queue backlogs.
- Okta SSO integration registers authentication signature verification exceptions.
- User login attempts hang indefinitely during tunnel authorization checks.
- DNS resolver requests to internal boundary hostnames time out.
- DNS queries for external identity provider okta.com fail NXDOMAIN.
- Packet loss peaks above 5% on external WAN gateway links.
- SMTP alert emails fail to deliver due to gateway timeout.
- Kubernetes pods reporting connectivity timeouts during remote cluster access.
- SAML token signature validation fails on VPN controller interfaces.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- LDAP directory service controller connection pools exhausted.
- Active Directory primary node failing DNS lookups.
- Okta SAML encryption key certificate expired or revoked.
- VPN gateway routing tables corrupted during automated reload.
- Duo API endpoint latency spike causing client callback timeout.
- Radius daemon threads locked under heavy auth load peak.
- Boundary firewall rules blocking LDAP TLS ports (636).
- CoreDNS cluster nodes dropping network resolve traffic.
- VPC tunnel routing map misconfigured on WAN interfaces.
- Local authentication token caches corrupted or locked.
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
1. Verify VPN client log file error codes (e.g. timeout on tunnel negotiation).
2. Check VPN controller ping latency to active directory hosts.
3. Verify LDAP connection health check on port 636 via telnet.
4. Query radius daemon status and check CPU thread locks.
5. Inspect Duo authentication API endpoints latency dashboards.
6. Confirm corporate DNS resolver is mapping AD domains correctly.
7. Verify firewall security profiles permit TLS auth packages.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Restart gateway ipsec services.
- Flush outdated Radius server authorization caches.
- Renew SAML authentication certificate mappings.
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
vpn, anyconnect, ipsec, tunnel, authentication, gateway, ldap, radius, duo, okta, saml, active directory, dns, resolver, timeout, latency, port, firewall, certificate, routing, network, wan, vpc, handshake, mfa, login, identity, directory, tls, ssl, token, cache, firewall, packet, drop, saturation, core, infrastructure, checkout, smtp, okta.com, ldap-service, active-directory, dns-resolver, gateway-controller, radius-daemon, ipsec-phase-2, network-saturation

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
