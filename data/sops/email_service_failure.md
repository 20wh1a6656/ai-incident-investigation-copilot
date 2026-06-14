# SOP-113: Resolving Email Notification Service Failures

# Incident Category
Application / Network

# Business Impact
Medium - Customer notifications, password resets, and alert delivery blocked.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Application logs show 'MailException: Failed to send email'.
- Mail transfer queue backlogs increase on mail servers.
- SSO portal returns timeout errors during password resets.
- SMTP auth token signature verification failures observed.
- DNS lookup failures for smtp.mail-provider.com address.
- LDAP bind failures registered on mail service lookups.
- Duo Push notifications succeed but MFA emails time out.
- VPN gateway alerts fail to deliver to system administrators.
- API gateway returns HTTP 504 gateway timeout on notify routes.
- Firewall logs show dropped SMTP packets on ports 25/587.
- SMTP server logs report 'Connection refused' or '535 Auth error'.
- Kubernetes pods reporting mail service socket timeout exceptions.
- Active connections to the SMTP host drop to 0.
- MFA validation codes fail to deliver via SMS/Email.
- Mail server CPU and memory usage saturates under queue loads.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- SMTP mail server authentication credentials mismatch.
- CoreDNS resolver failing to resolve smtp.mail-provider.com.
- Firewall rules blocking outgoing SMTP ports (25/465/587).
- Email service provider (e.g. SendGrid, Mailgun) outage.
- Time drift on local servers causing auth signatures to reject.
- SMTP TLS certificate expired or revoked.
- Mail queue storage disk space fully exhausted.
- LDAP directory service timeout preventing user mail lookup.
- IP address blacklisted by spam classification databases.
- Rate limits exceeded on corporate mail service keys.
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
1. Verify DNS resolution of smtp.mail-provider.com.
2. Check outgoing connectivity to port 587 via telnet.
3. Inspect application logs for SMTP auth error codes (e.g. 535).
4. Check SendGrid/Mailgun service status dashboards.
5. Check local mail server queue disk space usage.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Update SMTP authentication credentials configurations.
- Re-route outbound mail through backup SMTP relays.
- Clear mail server queue blocks and restart postfix.
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
email, smtp, mail, notification, queue, backlog, smtp.mail-provider.com, auth, token, signature, dns, resolve, ldap, bind, duo, vpn, api, gateway, firewall, port, connection, refused, timeout, tls, ssl, certificate, spam, sendgrid, mailgun, credentials, sso, checkout, system, infrastructure, network, microservice, email-service, smtp-auth, mail-queue, smtp-port, email-delivery

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
