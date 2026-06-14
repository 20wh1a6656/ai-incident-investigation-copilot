# SOP-118: Troubleshooting Kubernetes Pod CrashLoopBackOff Failures

# Incident Category
Kubernetes / Application

# Business Impact
High - Target application pods offline, API gateway routing timeout errors.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Kubernetes dashboard shows pod status is CrashLoopBackOff.
- Command line shows 'kubectl get pods' status is Error or Completed.
- Application logs show process exits immediately during startup.
- API gateway returns HTTP 502 bad gateway on target routes.
- HikariCP connection pool active connections drop for target pod.
- SSO portal returns timeout errors due to pod dependencies drops.
- LDAP bind failures observed during backend pod verification.
- SMTP alert emails fail because mail helper pod is offline.
- DNS lookup failures for internal pod service hostnames.
- Kubernetes pod description events report 'Liveness probe failed'.
- Microservices request metrics show high connection drops.
- Load balancer target groups report target pods offline.
- Kubernetes events report 'Back-off restarting failed container'.
- Pod memory allocation logs show OOM right before crash.
- Container startup logs report missing configuration file paths.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Missing environment configuration variables on deployment.
- Application crash due to database connectivity failure.
- Kubernetes liveness/readiness probe timeout set too strict.
- Java heap memory limits exceeding container limits (OOM).
- Corrupted configuration file deployed to ConfigMap.
- Permission denied errors accessing local container directories.
- Broken downstream dependency service connection timeouts.
- Application code compilation syntax errors on startup.
- Kubernetes cluster DNS resolver failing to resolve hostnames.
- Local volume mounting failure on target kubernetes nodes.
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
1. Run kubectl describe pod command to inspect container event history.
2. Retrieve container logs using kubectl logs --previous command.
3. Verify ConfigMap and Secret values injected to pod environment.
4. Check readiness and liveness probe configuration parameters.
5. Verify database connectivity from database client on node.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Revert recent deployment ConfigMap changes.
- Scale liveness probe timeout and delay limits.
- Redeploy target pods via rolling restart.
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
kubernetes, pod, crashloopbackoff, crashloop, liveness, readiness, probe, kubectl, describe, event, configmap, oom, heap, database, hikaricp, pool, sso, ldap, smtp, dns, resolve, api, gateway, route, connection, timeout, exception, config, variables, dependency, volume, mount, container, startup, error, microservice, system, pod-crash, crash-loop, readiness-probe, configmap-error, pod-events

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
