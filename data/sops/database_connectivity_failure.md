# SOP-107: Resolving Database Connectivity Failures

# Incident Category
Database

# Business Impact
Critical - Checkout service endpoints offline, database transaction dropouts.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Checkout service logs show 'Connection refused' or 'Driver exception'.
- HikariCP connection pool timeouts registered in application logs.
- Active database connection count drops to 0 on monitoring metrics.
- Database engine logs show 'PostgreSQL primary server unreachable'.
- API gateway returns HTTP 500 database transaction error.
- Kubernetes pods reporting DB socket connection timeouts.
- DNS lookup failures for primary database hostname.
- VPN gateway connections drop database log trails.
- SSO portal unavailable due to database config load timeout.
- LDAP bind failures observed during DB log syncs.
- Boundary firewall logs show dropped TCP packages on port 5432.
- SMTP alert emails fail to deliver due to DB error logs.
- Database read replica latency spikes above 600s.
- PostgreSQL replication lag metrics show master offline.
- Application memory usage spikes due to queued DB threads.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Primary PostgreSQL database instance crashed or offline.
- Core database network switch hardware failure.
- Firewall rule changes blocking SQL port (5432/3306).
- DNS server failing to resolve DB cluster hostname.
- Database replication failure triggering replica read-only lock.
- VPC subnet routing tables misconfigured during deployment.
- Network packet loss on database backbone cluster links.
- Database configuration file (pg_hba.conf) rules corrupted.
- TCP connection limits reached on database kernel.
- SQL proxy sidecar container crashed in kubernetes cluster.
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
1. Ping primary database IP to check network connectivity.
2. Test database port access via telnet (e.g. port 5432).
3. Check database engine status on target database host.
4. Verify database cluster hostname resolution in local DNS.
5. Verify that firewall settings permit application subnets.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Restart primary database service daemon.
- Trigger automated database failover to healthy replica.
- Rollback recent firewall rules blocking SQL traffic.
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
database, connectivity, connection, postgresql, mysql, sql, hikaricp, pool, timeout, port, firewall, dns, resolve, socket, replica, primary, replication, checkout, api, microservice, kubernetes, pod, network, latency, packet, vpn, sso, ldap, smtp, config, pg_hba, driver, exception, refused, crash, cluster, subnet, vpc, route, db-connectivity, database-connection, pg-primary, sql-port, db-cluster, db-proxy

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
