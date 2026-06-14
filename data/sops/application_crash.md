# SOP-110: Troubleshooting Application Process Crashes

# Incident Category
Application

# Business Impact
High - Selected backend services offline, checkout transactions failing.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Checkout service containers log 'FATAL: OutOfMemoryError'.
- Application process exits with code 137 (OOMKilled).
- Kubernetes pod status changes to CrashLoopBackOff.
- API gateway returns HTTP 502 bad gateway or 503 service unavailable.
- HikariCP connection pool connections drop abruptly.
- Duo push notifications fail due to client agent crashes.
- LDAP bind failures observed in authentication endpoints logs.
- SMTP alert emails fail due to SMTP service controller crashes.
- DNS lookup timeouts registered in container logs.
- SSO portal returns connection refused errors.
- Microservice endpoint response metrics show complete dropouts.
- Kubernetes readiness and liveness health checks fail.
- VPN gateway reports application connection dropped.
- CPU usage reaches 100% right before process termination.
- Heap memory usage graphs show classic saw-tooth pattern.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Java Virtual Machine (JVM) heap memory exhaustion (memory leak).
- Kubernetes container memory limit configured too low.
- Infinite loop in application code saturating CPU cores.
- Unhandled database connectivity exception crashing process.
- Thread deadlock in application runtime thread pools.
- Missing environment configuration variables on deployment.
- Broken configuration files causing startup compile errors.
- Dependency service connection timeouts locking threads.
- Local file system disk space exhaustion on application node.
- ChromaDB client connection locks memory on container startup.
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
1. Analyze kubernetes pod event logs using kubectl describe pod.
2. Inspect application logs for OutOfMemoryError or stack traces.
3. Verify container memory and CPU configuration limits.
4. Check thread dumps for deadlocks using diagnostic scripts.
5. Confirm that correct environment configurations are deployed.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Scale kubernetes pod memory limit configuration settings.
- Restart crash service pods with deployment rolling restarts.
- Revert recent code deployment to last stable version.
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
application, crash, oom, oomkilled, jvm, heap, thread, deadlock, timeout, kubernetes, pod, crashloopbackoff, readiness, liveness, health, checkout, api, gateway, service, connection, database, hikaricp, pool, sso, ldap, smtp, dns, resolve, memory, cpu, exception, fatal, exit, leak, config, variables, disk, system, process-crash, oom-killed, jvm-heap, crashloop, thread-deadlock

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
