# SOP-112: Managing Downstream Dependency Service Failures

# Incident Category
Application

# Business Impact
High - Partial degradation of checkout service, selected APIs returning timeout errors.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Application logs show 'TimeoutException calling downstream microservice'.
- Circuit breaker transitions to OPEN state on payment service API.
- Checkout latency spikes due to downstream connection queueing.
- API gateway returns HTTP 504 gateway timeout on dependent paths.
- Database connection pool connections hang waiting for downstream returns.
- SMTP notification mails drop due to payment verification timeout.
- SSO portal returns auth errors due to external ID verification failure.
- DNS lookup failures for dependency endpoint hosts.
- VPN gateway logs timeout errors syncing identity systems.
- MFA push notifications drop waiting for external MFA endpoints.
- Active connection counts to downstream APIs drop to 0.
- Kubernetes logs show HTTP 503 service unavailable on dependencies.
- LDAP bind failures observed due to target dependency drops.
- Microservices memory usage spikes because of retries backlogs.
- Load balancer reports target dependency servers offline.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- External payment service API core infrastructure down.
- Downstream service DNS resolution timeouts on resolver nodes.
- TLS encryption handshake failure on secure dependency routes.
- Rate limits exceeded on downstream dependency API keys.
- Corporate boundary firewall blocking egress to dependency IPs.
- Downstream database connection pool starvation.
- Routing table changes dropping VPC subnet associations.
- Dependency certificate revoked or expired.
- Nginx proxy timeouts set too low on connection pools.
- Network connection saturation peaks on egress links.
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
1. Check downstream dependency service status page or dashboard.
2. Test outbound network connectivity via curl/ping to target URL.
3. Verify DNS resolution of dependency hostname from cluster pods.
4. Inspect application circuit breaker status graphs.
5. Confirm that egress firewall rules allow traffic to target subnets.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Trigger circuit breaker fallback manual overrides.
- Reroute traffic to backup downstream providers.
- Scale local connection pool timeouts.
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
dependency, service, failure, timeout, latency, circuit, breaker, downstream, checkout, api, gateway, hikaricp, pool, smtp, sso, dns, resolve, vpn, mfa, duo, ldap, payment, verification, firewall, egress, network, tls, ssl, certificate, rate, limit, vpc, subnet, route, microservice, kubernetes, pod, database, dependency-failure, downstream-timeout, circuit-breaker, payment-api, egress-port

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
