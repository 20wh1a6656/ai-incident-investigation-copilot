# SOP-119: Resolving Container Resource Exhaustion (OOMKilled)

# Incident Category
Kubernetes / Application

# Business Impact
High - Application containers terminated, request latency spikes, service drops.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Kubernetes pod logs show 'Exit Code 137 (OOMKilled)'.
- Container CPU utilization metrics reach 100% threshold.
- Application request processing latency spikes above 4000ms.
- HikariCP connection pool acquisition times out under CPU stress.
- API gateway returns HTTP 503 service unavailable on target paths.
- SSO portal returns timeout errors due to identity pod load.
- LDAP bind lookup validations fail on authentication endpoints.
- SMTP server connections time out due to queue container load.
- DNS resolution failures logged by container application thread.
- Kubernetes events report 'Pod resource limits exceeded'.
- Active connections to the container drop to 0 during crash.
- Microservices memory usage graphs show sharp linear rise.
- Readiness health probes fail due to container lockups.
- VPN gateway drops sessions mapping to resource-stressed pods.
- Java virtual machine logs warning of frequent garbage collection.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Java JVM heap memory configured higher than container limit.
- Application memory leak due to unreleased cache maps.
- Container CPU limit configured too low, causing throttling.
- High concurrency thread counts locking container memory.
- Slow, unindexed database query loops queueing thread heap.
- Local container temp files storage directory full.
- Kubernetes node resource saturation forcing pod eviction.
- ChromaDB client embedding cache memory leak in container.
- Sudden transaction load volume spike on microservice.
- Network packet loss causing thread wait state queues.
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
1. Check pod resource allocation details using kubectl top pod.
2. Inspect kubernetes node events for eviction logs.
3. Analyze application heap memory dumps using memory analyzers.
4. Check JVM memory allocation flags (-Xmx / -Xms).
5. Monitor CPU throttling metrics in Prometheus dashboards.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Increase container memory limit configuration in helm values.
- Adjust JVM heap flags to stay below container resource limits.
- Enable autoscaling settings to scale pods horizontally.
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
container, resource, exhaustion, oomkilled, 137, exit, cpu, memory, heap, jvm, throttling, limit, request, concurrency, thread, hikaricp, pool, database, sso, ldap, smtp, dns, resolve, readiness, probe, eviction, saturation, leak, cache, latency, api, gateway, kubernetes, pod, gc, garbage, microservice, container-oom, cpu-throttling, resource-limit, oom-killed, pod-eviction

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
