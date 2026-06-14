# SOP-114: Troubleshooting SMTP Authentication Failures

# Incident Category
Application / Identity & Access Management

# Business Impact
Medium - Outbound emails blocked due to credential/token authentication validation rejection.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- SMTP server logs report '535 5.7.8 Authentication failed'.
- Application logs show 'AuthenticationFailedException: 535 Credentials invalid'.
- Password reset notification loops time out on public portal.
- Email notifications queue backlogs increase on local mail relays.
- SSO portal returns credential mismatch errors during notify paths.
- LDAP bind failures observed during user credentials lookup.
- VPN gateway alert scripts fail to authorize SMTP connections.
- DNS lookup failures for smtp.mail-provider.com authentication server.
- MFA validation responses fail to trigger during email verify.
- Active connections to the SMTP server reject authentication handshakes.
- Firewall logs show outgoing auth requests on ports 465/587.
- SMTP service account locked out in directory console.
- LDAP proxy servers show high timeout rates on mail auth checks.
- SAML assertions reject identity metadata due to SMTP mismatch.
- SMTP API tokens report expiration errors in monitor charts.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- SMTP API key or credentials expired, rotated, or revoked.
- LDAP directory service offline, blocking SMTP user bind lookups.
- NTP time drift on application server causing auth tokens to expire.
- Corporate network firewall rules blocking TLS auth packages.
- DNS resolver mapping SMTP auth servers to incorrect IP.
- SMTP authentication service account locked due to retry loops.
- Identity provider (Okta/AD) directory schema updated incorrectly.
- TLS handshake failure due to deprecated cipher suite on client.
- SMTP API rate limits exceeded on credential access keys.
- SSL/TLS certificate expired on target SMTP server.
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
1. Verify SMTP credentials in application settings tables.
2. Check LDAP bind user account status in Active Directory console.
3. Check system clock synchronization on application hosts.
4. Inspect mail server logs for TLS handshake or cipher errors.
5. Verify outbound connection to port 587 using openssl client.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Renew and update SMTP API credentials key.
- Unlock LDAP directory service account.
- Restart local postfix/sendmail services.
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
smtp, authentication, credentials, smtp.mail-provider.com, 535, email, mail, notification, auth, token, dns, resolve, ldap, bind, active directory, vpn, sso, mfa, duo, tls, ssl, certificate, drift, clock, firewall, port, rate, limit, schedules, config, connection, refused, timeout, network, microservice, kubernetes, smtp-auth, smtp-credentials, mail-auth, smtp-error, auth-token

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
