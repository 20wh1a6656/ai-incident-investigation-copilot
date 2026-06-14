# SOP-104: Handling LDAP TLS/SSL Certificate Expiration Outages

# Incident Category
Identity & Access Management

# Business Impact
High - Secure LDAP (LDAPS) traffic blocked, causing all SSL-based auth requests to fail.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- LDAPS connections report 'PKIX path building failed: SunCertPathBuilderException'.
- Microservices log 'LDAP connection failed: TLS handshake aborted'.
- Active Directory logs show 'Schannel certificate expiry warning'.
- LDAP bind failures observed across all secure ports (636/3269).
- VPN gateway authentication drops due to secure connection timeouts.
- SSO portal returns 'Identity provider connection handshake failed'.
- Kubernetes pods reporting certificate validation errors.
- SMTP servers cannot authorize users due to LDAPS failures.
- User login timeouts observed on secure boundary access.
- DNS lookup failures for secure LDAP gateway addresses.
- MFA validation responses time out due to TLS blockages.
- Radius daemon logs show certificate trust validation failures.
- LDAP sync agent reports signature verification failures.
- Active Directory console warns TLS protocol handshake failures.
- API gateway returns HTTP 500 error code on secure user paths.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Secure LDAP (LDAPS) server SSL/TLS certificate expired.
- Intermediate CA certificate missing from trust stores.
- Certificate revocation list (CRL) lookup failing DNS resolution.
- Cipher suite mismatch between application clients and LDAP servers.
- TLS protocol version incompatibility (e.g. TLS 1.0/1.1 disabled).
- LDAP proxy configuration caching expired trust chains.
- Firewall blocking outgoing CRL checks on port 80.
- Domain controller TLS certificate key mismatch.
- Trust store update script failed on application cluster.
- Incorrect domain name matching wildcard certificate SAN.
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
1. Run openssl command to check active LDAPS certificate expiration date.
2. Verify intermediate CA trust path on target servers.
3. Check if local application trust stores contain root certificate.
4. Confirm domain controller certificate is valid in local console.
5. Test outbound DNS lookup for certificate revocation servers.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Renew and deploy LDAPS TLS certificate.
- Update application Java trust stores with root CA.
- Restart LDAP proxy services to flush cached trust chains.
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
ldap, certificate, expiry, tls, ssl, handshake, ldaps, truststore, keystore, handshake, expired, ca, intermediate, crl, dns, resolver, timeout, vpn, gateway, sso, saml, okta, smtp, radius, microservice, firewall, port, active directory, bind, auth, validation, identity, provider, cipher, revocation, wildcard, san, domain, system, checkout, secure-ldap, cert-expiry, tls-handshake, trust-chain, pkix-error, ldap-cert

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
