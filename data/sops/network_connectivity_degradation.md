# SOP-117: Resolving Network Connectivity Degradation and Packet Loss

# Incident Category
Network

# Business Impact
High - Latency spikes across all services, transaction timeouts, packet loss.
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
- Ping diagnostics show packet loss above 10% on WAN links.
- Traceroute shows latency spikes on boundary router hops.
- Microservices report 'SocketTimeoutException: Read timed out'.
- HikariCP connection pool timeouts registered in application logs.
- SSO portal authentication requests fail with connection timed out.
- VPN gateway IPSEC tunnels experience frequent disconnects.
- SMTP mail server connections drop during auth handshakes.
- LDAP bind failures observed due to secure connection timeouts.
- DNS lookup failures for external and internal domain names.
- Duo push notifications time out waiting for external network.
- Kubernetes pods readiness checks fail due to network timeouts.
- API gateway public traffic metrics show high request drops.
- Database replication lag increases due to sync delays.
- Boundary firewall logs show high TCP retransmissions rates.
- Load balancer reports target instances response latency spikes.
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
- Underlying cloud provider network infrastructure degradation.
- WAN gateway interface saturation under peak traffic load.
- Boundary router configuration loop causing packet drops.
- VPC peering connection bandwidth limits reached.
- Firewall state table saturation causing packet dropping.
- Local DNS resolver nodes saturated by query loops.
- Core network switch hardware degradation in database subnet.
- IPsec VPN tunnel routing maps misconfigured.
- TCP window size configuration limits set too low on hosts.
- Distributed Denial of Service (DDoS) attack packet flood.
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
1. Run ping and traceroute diagnostics to isolate packet loss hops.
2. Inspect corporate firewall state table saturation metrics.
3. Check WAN bandwidth usage on boundary interfaces.
4. Monitor VPC peering connection traffic dashboards.
5. Check database subnet switch packet loss logs.
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
- Reroute outbound network traffic through backup WAN links.
- Clear firewall state tables or scale firewall capacity.
- Restart degraded gateway IPsec tunnels.
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
network, connectivity, degradation, packet, loss, latency, ping, traceroute, hop, timeout, socket, vpn, ipsec, tunnel, sso, smtp, ldap, dns, resolve, mfa, duo, database, hikaricp, pool, firewall, router, wan, vpc, peering, retransmission, load, balancer, ddos, bandwidth, saturation, microservice, kubernetes, network-degradation, packet-loss, network-latency, vpc-peering, firewall-saturation

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
