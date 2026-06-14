# SOP-108: Troubleshooting Connection Pool Exhaustion

# Incident Category
Database / Application

# Business Impact
High - Latency spikes on transactional APIs, checkout requests dropped.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Application logs show 'HikariPool-1 - Connection is not available, request timed out'.
- Checkout service API latency spikes above 5000ms.
- Database active connection count reaches maximum configured limit.
- PostgreSQL logs show 'FATAL: remaining connection slots are reserved'.
- API gateway returns HTTP 504 gateway timeout on transaction routes.
- Kubernetes pod CPU usage spikes due to thread pool waiting.
- SSO portal returns timeout errors loading user session databases.
- LDAP query binds fail due to connection pool locks.
- SMTP mail delivery drops due to thread pool starvation.
- DNS lookup failures for database connection endpoints.
- Application active thread counts match pool saturation limits.
- VPN gateway logging database times out on pool acquisition.
- SQL query execution metrics show high queue backlogs.
- MFA validation responses fail to save to transaction db.
- Kubernetes pods memory usage spikes due to connection queueing.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Application connection leak (connections not closed in code).
- Database connections capacity set too low (max_connections).
- HikariCP connection pool acquisition timeout set too low.
- Long-running unoptimized SQL queries locking connections.
- Sudden spike in application request traffic load.
- Database locks blocked by uncommitted transaction queries.
- Database CPU saturation causing query execution time spikes.
- Connection pool size misconfigured during rolling deploy.
- Network latency on DB connection handshakes.
- DNS resolution timeouts on database lookup calls.
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
1. Check HikariPool metrics in Prometheus dashboard.
2. Run pg_stat_activity query to find active connections and locks.
3. Check for long-running uncommitted database transactions.
4. Verify database CPU and memory metrics on RDS master.
5. Identify slow queries in PostgreSQL logs.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Terminate long-running idle database transaction processes.
- Increase PostgreSQL max_connections setting configuration.
- Increase application connection pool sizes and reload config.
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
connection, pool, exhaustion, hikaricp, hikari, timeout, postgresql, sql, max_connections, checkout, api, latency, active, thread, starvation, db, database, postgres, slots, fatal, uncommitted, transaction, dns, resolve, sso, ldap, smtp, vpn, gateway, query, lock, queue, capacity, leak, microservice, kubernetes, hikari-pool, connection-pool, pg-connections, pool-exhaustion, connection-leak

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
