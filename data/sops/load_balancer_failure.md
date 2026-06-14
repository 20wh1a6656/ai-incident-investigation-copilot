# SOP-116: Troubleshooting Load Balancer Failures and Healthy Check Drops

# Incident Category
Network

# Business Impact
Critical - public traffic blocked, microservices unreachable, high packet drops.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Load balancer monitoring shows 'HealthyHostCount' drops to 0.
- Public HTTP requests fail with '503 Service Unavailable' or connection reset.
- API gateway public traffic metrics show drop to 0.
- SSO portal returns timeout errors mapping load balancer endpoints.
- VPN gateway logins drop due to balancer connection timeouts.
- SMTP alert emails fail due to unresolvable notify load balancers.
- Kubernetes pods reporting DNS lookup failures on balancer aliases.
- Active connections to the public domain name drop abruptly.
- Firewall logs show dropped TCP packages on balancer subnets.
- Microservices liveness health checks fail on load balancer path.
- LDAP bind failures observed due to balancer lookup fails.
- Duo push notifications fail to reach gateway via balancer.
- Load balancer server logs report high latency spikes on targets.
- WAN ingress gateway links show high packet loss indicators.
- Kubernetes ingress controllers report target groups synchronization timeouts.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Application health check endpoint returning HTTP 500 error code.
- Application nodes connection pool exhaustion locking ports.
- Load balancer security group rules changed, blocking target ports.
- Local DNS resolver mapping load balancer CNAME to wrong IP.
- Load balancer target groups misconfigured on VPC subnets.
- Autoscaling group failing to register new instances to balancer.
- SSL/TLS certificate expired on load balancer interfaces.
- VPC routing table configurations dropped balancer routes.
- Application pods memory exhaustion (OOM) crashing containers.
- ChromaDB client queries saturating balancer target pools.
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
1. Verify target group health check status in AWS/Cloud console.
2. Test target group health check endpoint manually via curl from subnets.
3. Verify load balancer security group configuration settings.
4. Check load balancer SSL/TLS certificate validity.
5. Verify DNS resolution of load balancer hostname.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Restart failing application backend instances.
- Modify health check configuration parameters (threshold/timeout).
- Update load balancer security group definitions.
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
load, balancer, failure, health, check, healthyhostcount, target, group, vpc, subnet, cname, dns, resolve, sso, vpn, smtp, ldap, mfa, duo, connection, pool, exhaustion, oom, security, group, port, firewall, tls, ssl, certificate, autoscaling, route, ingress, packet, drop, microservice, kubernetes, pod, load-balancer, health-check, target-group, balancer-failure, ingress-controller

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
