# SOP-103: LDAP Directory Bind and Authentication Failures

# Incident Category
Identity & Access Management / Database

# Business Impact
High - Disruption of user logins, role mappings, and authorization checks.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Microservices logs show 'LDAPException: Bind failed: Invalid credentials'.
- Active Directory logs show 'LDAP bind error: code 49 - Invalid credentials'.
- Active Directory primary controller shows LDAP thread starvation alerts.
- VPN gateway authentication times out waiting for LDAP lookup binds.
- Internal tools return 'User roles mapped empty' during checkout authorization.
- SMTP servers reject LDAP lookup verification checks.
- Kubernetes pods throwing LDAP socket connection timeout errors.
- DNS lookup failures for internal LDAP servers.
- LDAP bind failures observed during routine API gateways requests.
- MFA callback validation timeouts registered on active directory logins.
- LDAP proxy servers show high network latency spikes.
- Active Directory sync agent reports credentials validation failure.
- SSO portal returns SAML assertion authentication failures.
- LDAP TLS connection handshake fails during certificate checking.
- Boundary firewall logs show dropped LDAP packages on port 636.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- LDAP bind service account password expired or rotated without update.
- Active Directory LDAP connection pool exhaustion limit hit.
- LDAP proxy servers locked up under peak transaction loops.
- TLS encryption certificate mismatch on LDAP gateway interfaces.
- Active Directory database disk space exhausted.
- CoreDNS routing mapping internal LDAP domains to wrong IP.
- LDAP service account locked due to password retry loops.
- Firewall blocks between application clusters and LDAP subnet.
- LDAP search limits exceeded on query sizes constraints.
- Active Directory schema cache corrupted during update.
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
1. Verify LDAP bind account credentials status in Active Directory.
2. Check LDAP connection status via telnet on ports 389 and 636.
3. Verify LDAP connection pool statistics using directory manager scripts.
4. Verify SSL/TLS certificate validity on LDAP servers.
5. Inspect firewall logs for blocked packages on target directory subnets.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Reset LDAP bind service account credentials.
- Scale connection pool settings on LDAP servers.
- Restart Active Directory directory services daemon.
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
ldap, bind, active directory, authentication, credentials, proxy, timeout, connection, pool, exhaustion, port, firewall, tls, ssl, certificate, vpn, gateway, sso, saml, okta, smtp, dns, resolve, database, disk, schema, cache, thread, starvation, network, latency, identity, provider, directory, user, role, authorization, check, sync, password, lockout, ldap-bind, active-directory, ldap-service, ldap-connection, port-636, bind-user

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
