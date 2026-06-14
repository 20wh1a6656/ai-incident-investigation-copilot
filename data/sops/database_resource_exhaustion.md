# SOP-109: Handling Database Resource Exhaustion

# Incident Category
Database

# Business Impact
Critical - Global service degradation, transaction queries dropped.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Database CPU utilization reaches 100% on RDS metrics.
- Disk I/O latency spikes above 50ms on database volumes.
- RDS monitoring shows database memory usage drops to 0 (OOM risks).
- SQL queries report 'Out of memory' error codes.
- HikariCP connection pool timeouts registered in application logs.
- Checkout service request latency spikes above 8000ms.
- Database replication lag increases above 1200 seconds.
- VPN gateway logging database drops connection slots.
- LDAP bind failures observed due to database write locks.
- SSO portal returns timeout errors due to DB disk saturation.
- DNS lookup failures for database endpoints due to resource lock.
- Kubernetes pods reporting database transaction timeout alerts.
- Active connections reach database system limits.
- PostgreSQL logs report high temp files write metrics.
- SMTP alert emails fail to deliver due to DB queue blocks.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Slow, unindexed SQL queries scanning large tables.
- Insufficient database instance sizing (CPU/RAM).
- Database disk storage space exhausted.
- SQL query cache table lock due to mass writes.
- Wrong PostgreSQL memory settings (e.g. work_mem too high).
- Sudden transaction volume spike (e.g., flash sale).
- Database autovacuum process blocked by long-running transactions.
- Disk I/O operations per second (IOPS) limits reached.
- Database connection leak causing process starvation.
- ChromaDB ingest files lock memory on shared DB host.
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
1. Check CPU and Memory metrics in AWS CloudWatch or RDS console.
2. Identify slow, unindexed database queries using pg_stat_statements.
3. Verify database disk space usage on storage volumes.
4. Check database active locks via pg_locks table.
5. Monitor autovacuum status and transaction ages.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Add missing database indexes to resolve slow query scans.
- Kill blocked autovacuum sessions or long-running locks.
- Upgrade database instance size or scale storage IOPS capacity.
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
database, resource, exhaustion, cpu, memory, oom, disk, iops, latency, postgresql, sql, rds, query, hikaricp, pool, timeout, replica, replication, lag, autovacuum, transaction, index, slow, vacuum, temp, file, write, sso, ldap, smtp, vpn, gateway, capacity, connection, limit, checkout, api, network, microservice, db-resource, cpu-exhaustion, database-memory, iops-limit, slow-query

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
