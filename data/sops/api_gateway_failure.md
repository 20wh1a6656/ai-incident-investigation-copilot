# SOP-111: Resolving API Gateway Outages and Failures

# Incident Category
Network / Application

# Business Impact
Critical - All public API endpoints blocked, frontend cannot communicate with backend.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Frontend console reports '502 Bad Gateway' or '504 Gateway Timeout'.
- Kong/Nginx API gateway logs show 'Upstream connection timeout'.
- Public API request routing latency spikes above 6000ms.
- SSO portal redirects return API gateway timeout errors.
- VPN gateway authentication times out due to gateway routing block.
- SMTP notifications fail because mail service API is unreachable.
- Kubernetes pods reporting DNS resolver timeouts on gateway names.
- Active connections to the API gateway drop to 0.
- Firewall logs show high TCP connection drops on port 443.
- LDAP bind failures registered in gateway auth plugins logs.
- MFA push notifications fail due to gateway connection timeouts.
- Load balancer health checks report API gateway offline.
- Gateway SSL/TLS certificate validation failures logged.
- DNS queries for API gateway domain return SERVFAIL.
- API gateway memory usage spikes right before crashes.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- API gateway cluster nodes running out of memory (OOM).
- SSL/TLS security certificate expired on gateway interfaces.
- Upstream microservice connection pool starvation.
- DNS resolution failure mapping upstream services hostnames.
- Firewall configuration rules blocking gateway ports.
- Load balancer failing to route traffic to gateway nodes.
- API rate limit configuration settings set too low.
- VPC subnet routes changed during cloud infrastructure update.
- ChromaDB client requests saturating gateway connection pools.
- Incorrect Nginx routing configuration file deployed.
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
1. Check load balancer health status metrics on gateway target groups.
2. Verify gateway SSL/TLS certificate expiration dates.
3. Inspect Nginx/Kong error logs for upstream timeout strings.
4. Test DNS resolution of upstream services from gateway node.
5. Confirm that firewall rules permit traffic on ports 80/443.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Restart API gateway service cluster.
- Deploy renewed SSL/TLS certificates.
- Revert recent routing config changes.
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
api, gateway, outage, timeout, latency, nginx, kong, upstream, connection, pool, sso, vpn, smtp, ldap, dns, resolve, ssl, tls, certificate, load, balancer, firewall, port, network, route, vpc, subnet, rate, limit, bad, gateway, error, mfa, duo, okta, authentication, kubernetes, pod, config, hikaricp, api-gateway, upstream-timeout, ssl-certificate, gateway-outage, api-routing

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
