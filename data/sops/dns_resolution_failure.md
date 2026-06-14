# SOP-115: Resolving DNS Resolution Failures and Resolver Timeouts

# Incident Category
Network

# Business Impact
Critical - Wide service disruption, app servers unable to resolve external/internal APIs.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Application logs show 'UnknownHostException' or 'NXDOMAIN'.
- Command line diagnostics return 'nslookup: command failed: connection timeout'.
- SSO portal login links return domain not resolved errors.
- VPN gateway authentication times out mapping boundary hosts.
- SMTP servers log 'SERVFAIL: Cannot resolve smtp.mail-provider.com'.
- LDAP bind failures observed due to directory hostname resolution timeouts.
- Kubernetes pods status changes to degraded, health checks fail.
- Public frontend routes fail with dns resolution errors.
- Duo Push notifications fail due to unresolvable Duo endpoints.
- Active connections database pools drop to 0 due to hostname lookup fail.
- Microservices logs show high connection timeout percentages.
- Load balancer health checks report gateway nodes offline.
- Firewall logs show dropped UDP packages on port 53.
- CoreDNS metrics show high latency peaks and packet drop rates.
- VPC tunnel gateways drop DNS server mapping routes.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- CoreDNS replica sets scaled down too low in Kubernetes.
- CoreDNS pods locked up or crashed due to memory exhaustion (OOM).
- Local resolver configuration file (/etc/resolv.conf) corrupted.
- Firewall rules blocking outbound UDP/TCP port 53 traffic.
- External public DNS resolver (e.g. 8.8.8.8) connection timeout.
- VPC DNS hostnames setting disabled in AWS subnet configuration.
- Corporate boundary DNS zone delegation dropped.
- DNS cache table lock on internal resolver servers.
- Network connection saturation peaks on corporate WAN links.
- Upstream domain names expired or revoked.
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
1. Verify local hostname resolution using dig or nslookup against internal/external domains.
2. Inspect CoreDNS service metrics and logs in Kubernetes cluster.
3. Check resolv.conf configurations on local application hosts.
4. Verify outbound UDP connection to port 53 via firewall console.
5. Check upstream public DNS resolver latency.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Scale CoreDNS deployment replica counts in Kubernetes.
- Restart CoreDNS daemon pods.
- Flush local DNS caching systems.
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
dns, resolution, failure, resolver, timeout, nxdomain, servfail, nslookup, dig, hostname, domain, resolve, coredns, udp, port-53, sso, vpn, smtp, ldap, bind, mfa, duo, database, hikaricp, pool, firewall, network, latency, packet, drop, wan, vpc, resolv.conf, load, balancer, health, microservice, kubernetes, pod, dns-resolution, dns-resolver, coredns-failure, dns-timeout, udp-port-53

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
