# SOP-120: Troubleshooting Service Mesh and Sidecar Proxy Failures

# Incident Category
Kubernetes / Network

# Business Impact
Critical - Inter-service communications blocked, microservices isolated.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Microservice logs show 'Envoy connection refused' or 'Upstream connect error'.
- API request routing returns HTTP 503 service unavailable on mesh routes.
- Public frontend reports gateway timeout on backend API calls.
- SSO portal returns auth errors due to mesh identity token drops.
- LDAP bind failures observed on secure LDAP TLS queries.
- VPN gateway logins time out waiting for user auth mesh checks.
- SMTP notifications fail because mail service mesh sidecar is offline.
- DNS lookup failures for internal mesh service registry names.
- Active connections between pod containers drop to 0.
- Istio/Envoy sidecar logs report 'mTLS handshake validation failed'.
- Kubernetes pods readiness probes fail due to sidecar proxy loops.
- Load balancer target groups report target mesh nodes offline.
- Microservices monitoring dashboard shows high network packet loss.
- Envoy CPU and memory usage metrics spike above thresholds.
- Service mesh control plane (e.g. Istiod) logs routing sync failures.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Service mesh mutual TLS (mTLS) certificate expired.
- Mesh control plane (Istiod) offline or sync queues locked.
- Envoy sidecar proxy container run out of memory (OOMKilled).
- Firewall rules blocking mesh communication port (15017/15006).
- Incorrect DNS resolution of internal mesh registry hostnames.
- Envoy routing configuration cache corrupted on local node.
- VPC subnet routing changes dropping mesh interfaces.
- mTLS encryption cipher suite mismatch on proxy sidecars.
- Application container starting before proxy container is active.
- Network connection saturation on mesh bridge networks.
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
1. Check Istio sidecar proxy status using istioctl proxy-status command.
2. Verify mTLS certificate validity in mesh trust stores.
3. Inspect Envoy sidecar logs for connection error strings.
4. Test outbound DNS resolution of internal mesh domains.
5. Confirm that sidecar container is healthy via kubectl get pods.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Restart failing service mesh proxy containers.
- Rotate service mesh root and intermediate mTLS certificates.
- Modify proxy settings configuration tables.
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
service, mesh, sidecar, proxy, envoy, istio, mtls, tls, handshake, certificate, outage, timeout, sso, vpn, smtp, ldap, dns, resolve, connection, hikaricp, pool, firewall, port, network, route, vpc, subnet, readiness, probe, oom, load, balancer, registry, cipher, control, plane, istiod, microservice, service-mesh, mtls-handshake, sidecar-proxy, envoy-error, mesh-routing

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
