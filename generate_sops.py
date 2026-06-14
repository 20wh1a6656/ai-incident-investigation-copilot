import os

sops_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sops")
if not os.path.exists(sops_dir):
    os.makedirs(sops_dir, exist_ok=True)

# Define 20 SOP templates dynamically
sop_data = [
    {
        "filename": "vpn_authentication_failure.md",
        "title": "SOP-101: Troubleshooting VPN Gateway Connection and Authentication Failures",
        "category": "Network / Identity & Access Management",
        "impact": "High - Blocked external access for remote SRE teams, developers, and corporate operations.",
        "symptoms": [
            "Client connection timeout at IPSEC phase-2 handshake.",
            "AnyConnect reports 'Authentication failed due to host timeout' codes.",
            "VPN gateway controller logs show 'Tunnel authentication rejected: LDAP search timeout'.",
            "Radius server reports Packet Drop on VPN authentication ports.",
            "Duo MFA callback timeouts registered for remote connections.",
            "Boundary routers show high traffic saturation peaks.",
            "Active Directory domain controllers report high LDAP queue backlogs.",
            "Okta SSO integration registers authentication signature verification exceptions.",
            "User login attempts hang indefinitely during tunnel authorization checks.",
            "DNS resolver requests to internal boundary hostnames time out.",
            "DNS queries for external identity provider okta.com fail NXDOMAIN.",
            "Packet loss peaks above 5% on external WAN gateway links.",
            "SMTP alert emails fail to deliver due to gateway timeout.",
            "Kubernetes pods reporting connectivity timeouts during remote cluster access.",
            "SAML token signature validation fails on VPN controller interfaces."
        ],
        "root_causes": [
            "LDAP directory service controller connection pools exhausted.",
            "Active Directory primary node failing DNS lookups.",
            "Okta SAML encryption key certificate expired or revoked.",
            "VPN gateway routing tables corrupted during automated reload.",
            "Duo API endpoint latency spike causing client callback timeout.",
            "Radius daemon threads locked under heavy auth load peak.",
            "Boundary firewall rules blocking LDAP TLS ports (636).",
            "CoreDNS cluster nodes dropping network resolve traffic.",
            "VPC tunnel routing map misconfigured on WAN interfaces.",
            "Local authentication token caches corrupted or locked."
        ],
        "keywords": [
            "vpn", "anyconnect", "ipsec", "tunnel", "authentication", "gateway", "ldap", "radius", "duo",
            "okta", "saml", "active directory", "dns", "resolver", "timeout", "latency", "port", "firewall",
            "certificate", "routing", "network", "wan", "vpc", "handshake", "mfa", "login", "identity",
            "directory", "tls", "ssl", "token", "cache", "firewall", "packet", "drop", "saturation",
            "core", "infrastructure", "checkout", "smtp", "okta.com", "ldap-service", "active-directory",
            "dns-resolver", "gateway-controller", "radius-daemon", "ipsec-phase-2", "network-saturation"
        ],
        "steps": [
            "Verify VPN client log file error codes (e.g. timeout on tunnel negotiation).",
            "Check VPN controller ping latency to active directory hosts.",
            "Verify LDAP connection health check on port 636 via telnet.",
            "Query radius daemon status and check CPU thread locks.",
            "Inspect Duo authentication API endpoints latency dashboards.",
            "Confirm corporate DNS resolver is mapping AD domains correctly.",
            "Verify firewall security profiles permit TLS auth packages."
        ],
        "actions": [
            "Restart gateway ipsec services.",
            "Flush outdated Radius server authorization caches.",
            "Renew SAML authentication certificate mappings."
        ]
    },
    {
        "filename": "sso_login_failure.md",
        "title": "SOP-102: Single Sign-On (SSO) Portal Authentication Failures",
        "category": "Identity & Access Management",
        "impact": "Critical - All corporate portals and internal tools (Okta, Jira, Github) unreachable.",
        "symptoms": [
            "Okta login page returns '400 Bad Request' or SAML signature invalid error.",
            "SSO authentication redirect loops on user web browsers.",
            "Active Directory sync agent reports 'Authentication synchronization timeout'.",
            "Internal identity provider logs show 'SAML assertion token validation expired'.",
            "MFA validation responses drop at Duo callback endpoints.",
            "VPN gateway rejects users mapping to Active Directory profiles.",
            "DNS lookup failures for internal domain controller addresses.",
            "Okta service agent reports NXDOMAIN for critical LDAP directories.",
            "LDAP bind failures registered in authorization middleware logs.",
            "SMTP alerts show smtp.mail-provider.com refused credentials.",
            "Multiple microservices reporting authentication credentials validation errors.",
            "OAuth client libraries throwing token verification exceptions.",
            "Active Directory domain controllers register credential signature mismatch.",
            "SAML assertions reject identity metadata mismatch alerts.",
            "Okta API interface returns HTTP 503 service unavailable codes."
        ],
        "root_causes": [
            "Okta SAML signing TLS certificate expired or mismatch.",
            "Active Directory federation services (ADFS) servers offline.",
            "Time drift on application servers exceeding SAML clock skew tolerances.",
            "Duo security API proxy server network routes dropped.",
            "CoreDNS resolver mapping okta.com incorrectly.",
            "LDAP directory schema mismatch after automated script upgrade.",
            "Corporate SSO portal token caching tables saturated in database.",
            "Firewall rules blocking SAML token exchange payloads.",
            "Database pool exhaustion on Identity Provider schema.",
            "LDAP bind user credentials expired or locked."
        ],
        "keywords": [
            "sso", "login", "okta", "saml", "assertion", "authentication", "adfs", "active directory",
            "ldap", "mfa", "duo", "token", "redirect", "certificate", "tls", "ssl", "oauth", "api",
            "database", "pool", "exhaustion", "timeout", "dns", "nxdomain", "resolved", "smtp",
            "credential", "signature", "verification", "auth", "identity", "provider", "directory",
            "clock", "drift", "sync", "federation", "user", "cookie", "session", "cache", "token",
            "ldap-bind", "saml-token", "okta-auth", "sso-portal", "adfs-server", "identity-provider"
        ],
        "steps": [
            "Inspect Okta Admin portal system log for token reject reasons.",
            "Verify system clock synchronization on AD and application nodes.",
            "Run openssl command to check active SAML certificate expiration date.",
            "Check LDAP bind logs for 'user locked' error strings.",
            "Confirm that CoreDNS is resolving external Identity Provider endpoints.",
            "Verify active directory federation services status."
        ],
        "actions": [
            "Force SAML certificate token key rotation.",
            "Restart Active Directory sync agents.",
            "Synchronize application nodes clocks via NTP."
        ]
    },
    {
        "filename": "ldap_bind_failure.md",
        "title": "SOP-103: LDAP Directory Bind and Authentication Failures",
        "category": "Identity & Access Management / Database",
        "impact": "High - Disruption of user logins, role mappings, and authorization checks.",
        "symptoms": [
            "Microservices logs show 'LDAPException: Bind failed: Invalid credentials'.",
            "Active Directory logs show 'LDAP bind error: code 49 - Invalid credentials'.",
            "Active Directory primary controller shows LDAP thread starvation alerts.",
            "VPN gateway authentication times out waiting for LDAP lookup binds.",
            "Internal tools return 'User roles mapped empty' during checkout authorization.",
            "SMTP servers reject LDAP lookup verification checks.",
            "Kubernetes pods throwing LDAP socket connection timeout errors.",
            "DNS lookup failures for internal LDAP servers.",
            "LDAP bind failures observed during routine API gateways requests.",
            "MFA callback validation timeouts registered on active directory logins.",
            "LDAP proxy servers show high network latency spikes.",
            "Active Directory sync agent reports credentials validation failure.",
            "SSO portal returns SAML assertion authentication failures.",
            "LDAP TLS connection handshake fails during certificate checking.",
            "Boundary firewall logs show dropped LDAP packages on port 636."
        ],
        "root_causes": [
            "LDAP bind service account password expired or rotated without update.",
            "Active Directory LDAP connection pool exhaustion limit hit.",
            "LDAP proxy servers locked up under peak transaction loops.",
            "TLS encryption certificate mismatch on LDAP gateway interfaces.",
            "Active Directory database disk space exhausted.",
            "CoreDNS routing mapping internal LDAP domains to wrong IP.",
            "LDAP service account locked due to password retry loops.",
            "Firewall blocks between application clusters and LDAP subnet.",
            "LDAP search limits exceeded on query sizes constraints.",
            "Active Directory schema cache corrupted during update."
        ],
        "keywords": [
            "ldap", "bind", "active directory", "authentication", "credentials", "proxy", "timeout",
            "connection", "pool", "exhaustion", "port", "firewall", "tls", "ssl", "certificate",
            "vpn", "gateway", "sso", "saml", "okta", "smtp", "dns", "resolve", "database", "disk",
            "schema", "cache", "thread", "starvation", "network", "latency", "identity", "provider",
            "directory", "user", "role", "authorization", "check", "sync", "password", "lockout",
            "ldap-bind", "active-directory", "ldap-service", "ldap-connection", "port-636", "bind-user"
        ],
        "steps": [
            "Verify LDAP bind account credentials status in Active Directory.",
            "Check LDAP connection status via telnet on ports 389 and 636.",
            "Verify LDAP connection pool statistics using directory manager scripts.",
            "Verify SSL/TLS certificate validity on LDAP servers.",
            "Inspect firewall logs for blocked packages on target directory subnets."
        ],
        "actions": [
            "Reset LDAP bind service account credentials.",
            "Scale connection pool settings on LDAP servers.",
            "Restart Active Directory directory services daemon."
        ]
    },
    {
        "filename": "ldap_certificate_expiry.md",
        "title": "SOP-104: Handling LDAP TLS/SSL Certificate Expiration Outages",
        "category": "Identity & Access Management",
        "impact": "High - Secure LDAP (LDAPS) traffic blocked, causing all SSL-based auth requests to fail.",
        "symptoms": [
            "LDAPS connections report 'PKIX path building failed: SunCertPathBuilderException'.",
            "Microservices log 'LDAP connection failed: TLS handshake aborted'.",
            "Active Directory logs show 'Schannel certificate expiry warning'.",
            "LDAP bind failures observed across all secure ports (636/3269).",
            "VPN gateway authentication drops due to secure connection timeouts.",
            "SSO portal returns 'Identity provider connection handshake failed'.",
            "Kubernetes pods reporting certificate validation errors.",
            "SMTP servers cannot authorize users due to LDAPS failures.",
            "User login timeouts observed on secure boundary access.",
            "DNS lookup failures for secure LDAP gateway addresses.",
            "MFA validation responses time out due to TLS blockages.",
            "Radius daemon logs show certificate trust validation failures.",
            "LDAP sync agent reports signature verification failures.",
            "Active Directory console warns TLS protocol handshake failures.",
            "API gateway returns HTTP 500 error code on secure user paths."
        ],
        "root_causes": [
            "Secure LDAP (LDAPS) server SSL/TLS certificate expired.",
            "Intermediate CA certificate missing from trust stores.",
            "Certificate revocation list (CRL) lookup failing DNS resolution.",
            "Cipher suite mismatch between application clients and LDAP servers.",
            "TLS protocol version incompatibility (e.g. TLS 1.0/1.1 disabled).",
            "LDAP proxy configuration caching expired trust chains.",
            "Firewall blocking outgoing CRL checks on port 80.",
            "Domain controller TLS certificate key mismatch.",
            "Trust store update script failed on application cluster.",
            "Incorrect domain name matching wildcard certificate SAN."
        ],
        "keywords": [
            "ldap", "certificate", "expiry", "tls", "ssl", "handshake", "ldaps", "truststore",
            "keystore", "handshake", "expired", "ca", "intermediate", "crl", "dns", "resolver",
            "timeout", "vpn", "gateway", "sso", "saml", "okta", "smtp", "radius", "microservice",
            "firewall", "port", "active directory", "bind", "auth", "validation", "identity",
            "provider", "cipher", "revocation", "wildcard", "san", "domain", "system", "checkout",
            "secure-ldap", "cert-expiry", "tls-handshake", "trust-chain", "pkix-error", "ldap-cert"
        ],
        "steps": [
            "Run openssl command to check active LDAPS certificate expiration date.",
            "Verify intermediate CA trust path on target servers.",
            "Check if local application trust stores contain root certificate.",
            "Confirm domain controller certificate is valid in local console.",
            "Test outbound DNS lookup for certificate revocation servers."
        ],
        "actions": [
            "Renew and deploy LDAPS TLS certificate.",
            "Update application Java trust stores with root CA.",
            "Restart LDAP proxy services to flush cached trust chains."
        ]
    },
    {
        "filename": "mfa_provider_failure.md",
        "title": "SOP-105: Troubleshooting Multi-Factor Authentication (MFA) Failures",
        "category": "Identity & Access Management",
        "impact": "Critical - Users locked out of MFA verification pipelines, disabling authentication.",
        "symptoms": [
            "Users report MFA passcode input results in login timeout errors.",
            "MFA provider logs show 'Callback connection timeout' alerts.",
            "VPN gateway authentication times out waiting for Duo push response.",
            "SSO portal returns 'MFA provider endpoint unreachable' errors.",
            "LDAP bind attempts succeed but login hangs at MFA phase.",
            "Duo API connection metrics dashboard show extreme latency spikes.",
            "Active Directory sync agent reports callback connection refused.",
            "DNS lookup failures for api.duosecurity.com endpoints.",
            "Email notification alerts fail to deliver due to gateway timeout.",
            "Multiple services reporting authentication verification failures.",
            "SMS dispatch logs show MFA codes are not being delivered.",
            "SAML assertions reject identity metadata due to missing MFA attribute.",
            "Kubernetes pods reporting connectivity timeouts to external identity systems.",
            "API gateway returns HTTP 504 gateway timeout on login routes.",
            "Duo security proxy logs report thread locks under heavy load."
        ],
        "root_causes": [
            "Duo Security or Okta MFA API endpoint network routing down.",
            "Duo auth proxy daemon thread starvation under load peaks.",
            "Firewall blocking outgoing MFA callback ports (443).",
            "Local DNS resolver failing to resolve api.duosecurity.com.",
            "MFA provider TLS certificate expired or revoked.",
            "Time drift on local servers causing authentication key mismatches.",
            "SMS gateway provider network connectivity degraded.",
            "MFA bypass policy misconfigured during update.",
            "Duo proxy credentials rotated but not updated.",
            "Network connection saturation peaks on corporate WAN links."
        ],
        "keywords": [
            "mfa", "duo", "okta", "authentication", "verification", "callback", "push", "passcode",
            "timeout", "latency", "dns", "resolve", "api", "proxy", "vpn", "gateway", "sso",
            "saml", "ldap", "email", "sms", "network", "firewall", "tls", "ssl", "certificate",
            "drift", "clock", "wan", "vpc", "active directory", "bind", "port", "credentials",
            "thread", "starvation", "connection", "pool", "identity", "provider", "token",
            "mfa-provider", "duo-push", "auth-proxy", "duo-timeout", "mfa-bypass", "sms-gateway"
        ],
        "steps": [
            "Check Duo Security or Okta service status pages.",
            "Verify local DNS resolution of api.duosecurity.com.",
            "Inspect Duo auth proxy logs for thread locking or connection errors.",
            "Verify local system clock synchronization using NTP query.",
            "Confirm outbound connection to port 443 via curl."
        ],
        "actions": [
            "Restart Duo auth proxy daemon.",
            "Enable temporary SRE emergency bypass policy if approved.",
            "Route traffic through backup DNS resolvers."
        ]
    },
    {
        "filename": "identity_provider_outage.md",
        "title": "SOP-106: Handling Identity Provider (IdP) Outages",
        "category": "Identity & Access Management",
        "impact": "Critical - Complete loss of user authorization and SSO logins across the enterprise.",
        "symptoms": [
            "Okta or Azure AD returns HTTP 503 Service Unavailable errors.",
            "SAML redirect requests fail with connection timed out.",
            "SSO portal login forms do not load on user browsers.",
            "LDAP authentication requests reject bind credentials.",
            "VPN gateway authentication drops user authorization maps.",
            "Duo push notifications time out due to missing IdP callback.",
            "Microservices log 'Identity metadata query returned null'.",
            "DNS lookup failures for corporate IdP domain names.",
            "OAuth token verification libraries throw signature validation errors.",
            "SMTP alert emails fail to deliver due to authentication timeout.",
            "Active Directory sync agent reports sync service offline.",
            "MFA validation responses fail to associate with user profiles.",
            "VPC tunnel gateways drop active directory verification routes.",
            "Internal corporate wikis show 'Unable to map user roles' alerts.",
            "API gateway returns HTTP 502 bad gateway on login paths."
        ],
        "root_causes": [
            "External Identity Provider (e.g. Okta, Azure AD) core system outage.",
            "Corporate IdP DNS zone delegation dropped.",
            "IdP SAML signing certificates expired or mismatched.",
            "Active Directory federation servers offline or database corrupt.",
            "TLS handshake failures between application clusters and IdP.",
            "Corporate firewall rules blocking outgoing IdP traffic.",
            "Time sync drift on corporate domain controllers.",
            "IdP integration configuration modified without authorization.",
            "OAuth token signing keys rotated without updating metadata endpoint.",
            "Network routing issues on corporate boundary gateway links."
        ],
        "keywords": [
            "idp", "identity", "provider", "okta", "azure", "outage", "sso", "saml", "metadata",
            "oauth", "token", "signature", "verification", "auth", "dns", "resolve", "ldap",
            "active directory", "bind", "vpn", "gateway", "mfa", "duo", "timeout", "latency",
            "connection", "pool", "firewall", "tls", "ssl", "certificate", "drift", "clock",
            "smtp", "vpc", "sync", "federation", "user", "role", "authorization", "check",
            "identity-provider", "idp-outage", "saml-signing", "oauth-token", "idp-metadata", "idp-dns"
        ],
        "steps": [
            "Check external IdP (Okta/Azure) status page for global issues.",
            "Run dig command to check IdP domain name resolution status.",
            "Inspect SSO middleware logs for SAML signature errors.",
            "Verify target federation servers service status.",
            "Confirm that system clock is synchronized across clusters."
        ],
        "actions": [
            "Engage failover emergency access protocols.",
            "Restore previous stable IdP integration config metadata.",
            "Rotate SAML token signing keys in corporate console."
        ]
    },
    {
        "filename": "database_connectivity_failure.md",
        "title": "SOP-107: Resolving Database Connectivity Failures",
        "category": "Database",
        "impact": "Critical - Checkout service endpoints offline, database transaction dropouts.",
        "symptoms": [
            "Checkout service logs show 'Connection refused' or 'Driver exception'.",
            "HikariCP connection pool timeouts registered in application logs.",
            "Active database connection count drops to 0 on monitoring metrics.",
            "Database engine logs show 'PostgreSQL primary server unreachable'.",
            "API gateway returns HTTP 500 database transaction error.",
            "Kubernetes pods reporting DB socket connection timeouts.",
            "DNS lookup failures for primary database hostname.",
            "VPN gateway connections drop database log trails.",
            "SSO portal unavailable due to database config load timeout.",
            "LDAP bind failures observed during DB log syncs.",
            "Boundary firewall logs show dropped TCP packages on port 5432.",
            "SMTP alert emails fail to deliver due to DB error logs.",
            "Database read replica latency spikes above 600s.",
            "PostgreSQL replication lag metrics show master offline.",
            "Application memory usage spikes due to queued DB threads."
        ],
        "root_causes": [
            "Primary PostgreSQL database instance crashed or offline.",
            "Core database network switch hardware failure.",
            "Firewall rule changes blocking SQL port (5432/3306).",
            "DNS server failing to resolve DB cluster hostname.",
            "Database replication failure triggering replica read-only lock.",
            "VPC subnet routing tables misconfigured during deployment.",
            "Network packet loss on database backbone cluster links.",
            "Database configuration file (pg_hba.conf) rules corrupted.",
            "TCP connection limits reached on database kernel.",
            "SQL proxy sidecar container crashed in kubernetes cluster."
        ],
        "keywords": [
            "database", "connectivity", "connection", "postgresql", "mysql", "sql", "hikaricp",
            "pool", "timeout", "port", "firewall", "dns", "resolve", "socket", "replica",
            "primary", "replication", "checkout", "api", "microservice", "kubernetes", "pod",
            "network", "latency", "packet", "vpn", "sso", "ldap", "smtp", "config", "pg_hba",
            "driver", "exception", "refused", "crash", "cluster", "subnet", "vpc", "route",
            "db-connectivity", "database-connection", "pg-primary", "sql-port", "db-cluster", "db-proxy"
        ],
        "steps": [
            "Ping primary database IP to check network connectivity.",
            "Test database port access via telnet (e.g. port 5432).",
            "Check database engine status on target database host.",
            "Verify database cluster hostname resolution in local DNS.",
            "Verify that firewall settings permit application subnets."
        ],
        "actions": [
            "Restart primary database service daemon.",
            "Trigger automated database failover to healthy replica.",
            "Rollback recent firewall rules blocking SQL traffic."
        ]
    },
    {
        "filename": "connection_pool_exhaustion.md",
        "title": "SOP-108: Troubleshooting Connection Pool Exhaustion",
        "category": "Database / Application",
        "impact": "High - Latency spikes on transactional APIs, checkout requests dropped.",
        "symptoms": [
            "Application logs show 'HikariPool-1 - Connection is not available, request timed out'.",
            "Checkout service API latency spikes above 5000ms.",
            "Database active connection count reaches maximum configured limit.",
            "PostgreSQL logs show 'FATAL: remaining connection slots are reserved'.",
            "API gateway returns HTTP 504 gateway timeout on transaction routes.",
            "Kubernetes pod CPU usage spikes due to thread pool waiting.",
            "SSO portal returns timeout errors loading user session databases.",
            "LDAP query binds fail due to connection pool locks.",
            "SMTP mail delivery drops due to thread pool starvation.",
            "DNS lookup failures for database connection endpoints.",
            "Application active thread counts match pool saturation limits.",
            "VPN gateway logging database times out on pool acquisition.",
            "SQL query execution metrics show high queue backlogs.",
            "MFA validation responses fail to save to transaction db.",
            "Kubernetes pods memory usage spikes due to connection queueing."
        ],
        "root_causes": [
            "Application connection leak (connections not closed in code).",
            "Database connections capacity set too low (max_connections).",
            "HikariCP connection pool acquisition timeout set too low.",
            "Long-running unoptimized SQL queries locking connections.",
            "Sudden spike in application request traffic load.",
            "Database locks blocked by uncommitted transaction queries.",
            "Database CPU saturation causing query execution time spikes.",
            "Connection pool size misconfigured during rolling deploy.",
            "Network latency on DB connection handshakes.",
            "DNS resolution timeouts on database lookup calls."
        ],
        "keywords": [
            "connection", "pool", "exhaustion", "hikaricp", "hikari", "timeout", "postgresql",
            "sql", "max_connections", "checkout", "api", "latency", "active", "thread",
            "starvation", "db", "database", "postgres", "slots", "fatal", "uncommitted",
            "transaction", "dns", "resolve", "sso", "ldap", "smtp", "vpn", "gateway",
            "query", "lock", "queue", "capacity", "leak", "microservice", "kubernetes",
            "hikari-pool", "connection-pool", "pg-connections", "pool-exhaustion", "connection-leak"
        ],
        "steps": [
            "Check HikariPool metrics in Prometheus dashboard.",
            "Run pg_stat_activity query to find active connections and locks.",
            "Check for long-running uncommitted database transactions.",
            "Verify database CPU and memory metrics on RDS master.",
            "Identify slow queries in PostgreSQL logs."
        ],
        "actions": [
            "Terminate long-running idle database transaction processes.",
            "Increase PostgreSQL max_connections setting configuration.",
            "Increase application connection pool sizes and reload config."
        ]
    },
    {
        "filename": "database_resource_exhaustion.md",
        "title": "SOP-109: Handling Database Resource Exhaustion",
        "category": "Database",
        "impact": "Critical - Global service degradation, transaction queries dropped.",
        "symptoms": [
            "Database CPU utilization reaches 100% on RDS metrics.",
            "Disk I/O latency spikes above 50ms on database volumes.",
            "RDS monitoring shows database memory usage drops to 0 (OOM risks).",
            "SQL queries report 'Out of memory' error codes.",
            "HikariCP connection pool timeouts registered in application logs.",
            "Checkout service request latency spikes above 8000ms.",
            "Database replication lag increases above 1200 seconds.",
            "VPN gateway logging database drops connection slots.",
            "LDAP bind failures observed due to database write locks.",
            "SSO portal returns timeout errors due to DB disk saturation.",
            "DNS lookup failures for database endpoints due to resource lock.",
            "Kubernetes pods reporting database transaction timeout alerts.",
            "Active connections reach database system limits.",
            "PostgreSQL logs report high temp files write metrics.",
            "SMTP alert emails fail to deliver due to DB queue blocks."
        ],
        "root_causes": [
            "Slow, unindexed SQL queries scanning large tables.",
            "Insufficient database instance sizing (CPU/RAM).",
            "Database disk storage space exhausted.",
            "SQL query cache table lock due to mass writes.",
            "Wrong PostgreSQL memory settings (e.g. work_mem too high).",
            "Sudden transaction volume spike (e.g., flash sale).",
            "Database autovacuum process blocked by long-running transactions.",
            "Disk I/O operations per second (IOPS) limits reached.",
            "Database connection leak causing process starvation.",
            "ChromaDB ingest files lock memory on shared DB host."
        ],
        "keywords": [
            "database", "resource", "exhaustion", "cpu", "memory", "oom", "disk", "iops",
            "latency", "postgresql", "sql", "rds", "query", "hikaricp", "pool", "timeout",
            "replica", "replication", "lag", "autovacuum", "transaction", "index", "slow",
            "vacuum", "temp", "file", "write", "sso", "ldap", "smtp", "vpn", "gateway",
            "capacity", "connection", "limit", "checkout", "api", "network", "microservice",
            "db-resource", "cpu-exhaustion", "database-memory", "iops-limit", "slow-query"
        ],
        "steps": [
            "Check CPU and Memory metrics in AWS CloudWatch or RDS console.",
            "Identify slow, unindexed database queries using pg_stat_statements.",
            "Verify database disk space usage on storage volumes.",
            "Check database active locks via pg_locks table.",
            "Monitor autovacuum status and transaction ages."
        ],
        "actions": [
            "Add missing database indexes to resolve slow query scans.",
            "Kill blocked autovacuum sessions or long-running locks.",
            "Upgrade database instance size or scale storage IOPS capacity."
        ]
    },
    {
        "filename": "application_crash.md",
        "title": "SOP-110: Troubleshooting Application Process Crashes",
        "category": "Application",
        "impact": "High - Selected backend services offline, checkout transactions failing.",
        "symptoms": [
            "Checkout service containers log 'FATAL: OutOfMemoryError'.",
            "Application process exits with code 137 (OOMKilled).",
            "Kubernetes pod status changes to CrashLoopBackOff.",
            "API gateway returns HTTP 502 bad gateway or 503 service unavailable.",
            "HikariCP connection pool connections drop abruptly.",
            "Duo push notifications fail due to client agent crashes.",
            "LDAP bind failures observed in authentication endpoints logs.",
            "SMTP alert emails fail due to SMTP service controller crashes.",
            "DNS lookup timeouts registered in container logs.",
            "SSO portal returns connection refused errors.",
            "Microservice endpoint response metrics show complete dropouts.",
            "Kubernetes readiness and liveness health checks fail.",
            "VPN gateway reports application connection dropped.",
            "CPU usage reaches 100% right before process termination.",
            "Heap memory usage graphs show classic saw-tooth pattern."
        ],
        "root_causes": [
            "Java Virtual Machine (JVM) heap memory exhaustion (memory leak).",
            "Kubernetes container memory limit configured too low.",
            "Infinite loop in application code saturating CPU cores.",
            "Unhandled database connectivity exception crashing process.",
            "Thread deadlock in application runtime thread pools.",
            "Missing environment configuration variables on deployment.",
            "Broken configuration files causing startup compile errors.",
            "Dependency service connection timeouts locking threads.",
            "Local file system disk space exhaustion on application node.",
            "ChromaDB client connection locks memory on container startup."
        ],
        "keywords": [
            "application", "crash", "oom", "oomkilled", "jvm", "heap", "thread", "deadlock",
            "timeout", "kubernetes", "pod", "crashloopbackoff", "readiness", "liveness",
            "health", "checkout", "api", "gateway", "service", "connection", "database",
            "hikaricp", "pool", "sso", "ldap", "smtp", "dns", "resolve", "memory", "cpu",
            "exception", "fatal", "exit", "leak", "config", "variables", "disk", "system",
            "process-crash", "oom-killed", "jvm-heap", "crashloop", "thread-deadlock"
        ],
        "steps": [
            "Analyze kubernetes pod event logs using kubectl describe pod.",
            "Inspect application logs for OutOfMemoryError or stack traces.",
            "Verify container memory and CPU configuration limits.",
            "Check thread dumps for deadlocks using diagnostic scripts.",
            "Confirm that correct environment configurations are deployed."
        ],
        "actions": [
            "Scale kubernetes pod memory limit configuration settings.",
            "Restart crash service pods with deployment rolling restarts.",
            "Revert recent code deployment to last stable version."
        ]
    },
    {
        "filename": "api_gateway_failure.md",
        "title": "SOP-111: Resolving API Gateway Outages and Failures",
        "category": "Network / Application",
        "impact": "Critical - All public API endpoints blocked, frontend cannot communicate with backend.",
        "symptoms": [
            "Frontend console reports '502 Bad Gateway' or '504 Gateway Timeout'.",
            "Kong/Nginx API gateway logs show 'Upstream connection timeout'.",
            "Public API request routing latency spikes above 6000ms.",
            "SSO portal redirects return API gateway timeout errors.",
            "VPN gateway authentication times out due to gateway routing block.",
            "SMTP notifications fail because mail service API is unreachable.",
            "Kubernetes pods reporting DNS resolver timeouts on gateway names.",
            "Active connections to the API gateway drop to 0.",
            "Firewall logs show high TCP connection drops on port 443.",
            "LDAP bind failures registered in gateway auth plugins logs.",
            "MFA push notifications fail due to gateway connection timeouts.",
            "Load balancer health checks report API gateway offline.",
            "Gateway SSL/TLS certificate validation failures logged.",
            "DNS queries for API gateway domain return SERVFAIL.",
            "API gateway memory usage spikes right before crashes."
        ],
        "root_causes": [
            "API gateway cluster nodes running out of memory (OOM).",
            "SSL/TLS security certificate expired on gateway interfaces.",
            "Upstream microservice connection pool starvation.",
            "DNS resolution failure mapping upstream services hostnames.",
            "Firewall configuration rules blocking gateway ports.",
            "Load balancer failing to route traffic to gateway nodes.",
            "API rate limit configuration settings set too low.",
            "VPC subnet routes changed during cloud infrastructure update.",
            "ChromaDB client requests saturating gateway connection pools.",
            "Incorrect Nginx routing configuration file deployed."
        ],
        "keywords": [
            "api", "gateway", "outage", "timeout", "latency", "nginx", "kong", "upstream",
            "connection", "pool", "sso", "vpn", "smtp", "ldap", "dns", "resolve", "ssl",
            "tls", "certificate", "load", "balancer", "firewall", "port", "network",
            "route", "vpc", "subnet", "rate", "limit", "bad", "gateway", "error", "mfa",
            "duo", "okta", "authentication", "kubernetes", "pod", "config", "hikaricp",
            "api-gateway", "upstream-timeout", "ssl-certificate", "gateway-outage", "api-routing"
        ],
        "steps": [
            "Check load balancer health status metrics on gateway target groups.",
            "Verify gateway SSL/TLS certificate expiration dates.",
            "Inspect Nginx/Kong error logs for upstream timeout strings.",
            "Test DNS resolution of upstream services from gateway node.",
            "Confirm that firewall rules permit traffic on ports 80/443."
        ],
        "actions": [
            "Restart API gateway service cluster.",
            "Deploy renewed SSL/TLS certificates.",
            "Revert recent routing config changes."
        ]
    },
    {
        "filename": "dependency_service_failure.md",
        "title": "SOP-112: Managing Downstream Dependency Service Failures",
        "category": "Application",
        "impact": "High - Partial degradation of checkout service, selected APIs returning timeout errors.",
        "symptoms": [
            "Application logs show 'TimeoutException calling downstream microservice'.",
            "Circuit breaker transitions to OPEN state on payment service API.",
            "Checkout latency spikes due to downstream connection queueing.",
            "API gateway returns HTTP 504 gateway timeout on dependent paths.",
            "Database connection pool connections hang waiting for downstream returns.",
            "SMTP notification mails drop due to payment verification timeout.",
            "SSO portal returns auth errors due to external ID verification failure.",
            "DNS lookup failures for dependency endpoint hosts.",
            "VPN gateway logs timeout errors syncing identity systems.",
            "MFA push notifications drop waiting for external MFA endpoints.",
            "Active connection counts to downstream APIs drop to 0.",
            "Kubernetes logs show HTTP 503 service unavailable on dependencies.",
            "LDAP bind failures observed due to target dependency drops.",
            "Microservices memory usage spikes because of retries backlogs.",
            "Load balancer reports target dependency servers offline."
        ],
        "root_causes": [
            "External payment service API core infrastructure down.",
            "Downstream service DNS resolution timeouts on resolver nodes.",
            "TLS encryption handshake failure on secure dependency routes.",
            "Rate limits exceeded on downstream dependency API keys.",
            "Corporate boundary firewall blocking egress to dependency IPs.",
            "Downstream database connection pool starvation.",
            "Routing table changes dropping VPC subnet associations.",
            "Dependency certificate revoked or expired.",
            "Nginx proxy timeouts set too low on connection pools.",
            "Network connection saturation peaks on egress links."
        ],
        "keywords": [
            "dependency", "service", "failure", "timeout", "latency", "circuit", "breaker",
            "downstream", "checkout", "api", "gateway", "hikaricp", "pool", "smtp", "sso",
            "dns", "resolve", "vpn", "mfa", "duo", "ldap", "payment", "verification",
            "firewall", "egress", "network", "tls", "ssl", "certificate", "rate", "limit",
            "vpc", "subnet", "route", "microservice", "kubernetes", "pod", "database",
            "dependency-failure", "downstream-timeout", "circuit-breaker", "payment-api", "egress-port"
        ],
        "steps": [
            "Check downstream dependency service status page or dashboard.",
            "Test outbound network connectivity via curl/ping to target URL.",
            "Verify DNS resolution of dependency hostname from cluster pods.",
            "Inspect application circuit breaker status graphs.",
            "Confirm that egress firewall rules allow traffic to target subnets."
        ],
        "actions": [
            "Trigger circuit breaker fallback manual overrides.",
            "Reroute traffic to backup downstream providers.",
            "Scale local connection pool timeouts."
        ]
    },
    {
        "filename": "email_service_failure.md",
        "title": "SOP-113: Resolving Email Notification Service Failures",
        "category": "Application / Network",
        "impact": "Medium - Customer notifications, password resets, and alert delivery blocked.",
        "symptoms": [
            "Application logs show 'MailException: Failed to send email'.",
            "Mail transfer queue backlogs increase on mail servers.",
            "SSO portal returns timeout errors during password resets.",
            "SMTP auth token signature verification failures observed.",
            "DNS lookup failures for smtp.mail-provider.com address.",
            "LDAP bind failures registered on mail service lookups.",
            "Duo Push notifications succeed but MFA emails time out.",
            "VPN gateway alerts fail to deliver to system administrators.",
            "API gateway returns HTTP 504 gateway timeout on notify routes.",
            "Firewall logs show dropped SMTP packets on ports 25/587.",
            "SMTP server logs report 'Connection refused' or '535 Auth error'.",
            "Kubernetes pods reporting mail service socket timeout exceptions.",
            "Active connections to the SMTP host drop to 0.",
            "MFA validation codes fail to deliver via SMS/Email.",
            "Mail server CPU and memory usage saturates under queue loads."
        ],
        "root_causes": [
            "SMTP mail server authentication credentials mismatch.",
            "CoreDNS resolver failing to resolve smtp.mail-provider.com.",
            "Firewall rules blocking outgoing SMTP ports (25/465/587).",
            "Email service provider (e.g. SendGrid, Mailgun) outage.",
            "Time drift on local servers causing auth signatures to reject.",
            "SMTP TLS certificate expired or revoked.",
            "Mail queue storage disk space fully exhausted.",
            "LDAP directory service timeout preventing user mail lookup.",
            "IP address blacklisted by spam classification databases.",
            "Rate limits exceeded on corporate mail service keys."
        ],
        "keywords": [
            "email", "smtp", "mail", "notification", "queue", "backlog", "smtp.mail-provider.com",
            "auth", "token", "signature", "dns", "resolve", "ldap", "bind", "duo", "vpn",
            "api", "gateway", "firewall", "port", "connection", "refused", "timeout",
            "tls", "ssl", "certificate", "spam", "sendgrid", "mailgun", "credentials",
            "sso", "checkout", "system", "infrastructure", "network", "microservice",
            "email-service", "smtp-auth", "mail-queue", "smtp-port", "email-delivery"
        ],
        "steps": [
            "Verify DNS resolution of smtp.mail-provider.com.",
            "Check outgoing connectivity to port 587 via telnet.",
            "Inspect application logs for SMTP auth error codes (e.g. 535).",
            "Check SendGrid/Mailgun service status dashboards.",
            "Check local mail server queue disk space usage."
        ],
        "actions": [
            "Update SMTP authentication credentials configurations.",
            "Re-route outbound mail through backup SMTP relays.",
            "Clear mail server queue blocks and restart postfix."
        ]
    },
    {
        "filename": "smtp_authentication_failure.md",
        "title": "SOP-114: Troubleshooting SMTP Authentication Failures",
        "category": "Application / Identity & Access Management",
        "impact": "Medium - Outbound emails blocked due to credential/token authentication validation rejection.",
        "symptoms": [
            "SMTP server logs report '535 5.7.8 Authentication failed'.",
            "Application logs show 'AuthenticationFailedException: 535 Credentials invalid'.",
            "Password reset notification loops time out on public portal.",
            "Email notifications queue backlogs increase on local mail relays.",
            "SSO portal returns credential mismatch errors during notify paths.",
            "LDAP bind failures observed during user credentials lookup.",
            "VPN gateway alert scripts fail to authorize SMTP connections.",
            "DNS lookup failures for smtp.mail-provider.com authentication server.",
            "MFA validation responses fail to trigger during email verify.",
            "Active connections to the SMTP server reject authentication handshakes.",
            "Firewall logs show outgoing auth requests on ports 465/587.",
            "SMTP service account locked out in directory console.",
            "LDAP proxy servers show high timeout rates on mail auth checks.",
            "SAML assertions reject identity metadata due to SMTP mismatch.",
            "SMTP API tokens report expiration errors in monitor charts."
        ],
        "root_causes": [
            "SMTP API key or credentials expired, rotated, or revoked.",
            "LDAP directory service offline, blocking SMTP user bind lookups.",
            "NTP time drift on application server causing auth tokens to expire.",
            "Corporate network firewall rules blocking TLS auth packages.",
            "DNS resolver mapping SMTP auth servers to incorrect IP.",
            "SMTP authentication service account locked due to retry loops.",
            "Identity provider (Okta/AD) directory schema updated incorrectly.",
            "TLS handshake failure due to deprecated cipher suite on client.",
            "SMTP API rate limits exceeded on credential access keys.",
            "SSL/TLS certificate expired on target SMTP server."
        ],
        "keywords": [
            "smtp", "authentication", "credentials", "smtp.mail-provider.com", "535", "email",
            "mail", "notification", "auth", "token", "dns", "resolve", "ldap", "bind",
            "active directory", "vpn", "sso", "mfa", "duo", "tls", "ssl", "certificate",
            "drift", "clock", "firewall", "port", "rate", "limit", "schedules", "config",
            "connection", "refused", "timeout", "network", "microservice", "kubernetes",
            "smtp-auth", "smtp-credentials", "mail-auth", "smtp-error", "auth-token"
        ],
        "steps": [
            "Verify SMTP credentials in application settings tables.",
            "Check LDAP bind user account status in Active Directory console.",
            "Check system clock synchronization on application hosts.",
            "Inspect mail server logs for TLS handshake or cipher errors.",
            "Verify outbound connection to port 587 using openssl client."
        ],
        "actions": [
            "Renew and update SMTP API credentials key.",
            "Unlock LDAP directory service account.",
            "Restart local postfix/sendmail services."
        ]
    },
    {
        "filename": "dns_resolution_failure.md",
        "title": "SOP-115: Resolving DNS Resolution Failures and Resolver Timeouts",
        "category": "Network",
        "impact": "Critical - Wide service disruption, app servers unable to resolve external/internal APIs.",
        "symptoms": [
            "Application logs show 'UnknownHostException' or 'NXDOMAIN'.",
            "Command line diagnostics return 'nslookup: command failed: connection timeout'.",
            "SSO portal login links return domain not resolved errors.",
            "VPN gateway authentication times out mapping boundary hosts.",
            "SMTP servers log 'SERVFAIL: Cannot resolve smtp.mail-provider.com'.",
            "LDAP bind failures observed due to directory hostname resolution timeouts.",
            "Kubernetes pods status changes to degraded, health checks fail.",
            "Public frontend routes fail with dns resolution errors.",
            "Duo Push notifications fail due to unresolvable Duo endpoints.",
            "Active connections database pools drop to 0 due to hostname lookup fail.",
            "Microservices logs show high connection timeout percentages.",
            "Load balancer health checks report gateway nodes offline.",
            "Firewall logs show dropped UDP packages on port 53.",
            "CoreDNS metrics show high latency peaks and packet drop rates.",
            "VPC tunnel gateways drop DNS server mapping routes."
        ],
        "root_causes": [
            "CoreDNS replica sets scaled down too low in Kubernetes.",
            "CoreDNS pods locked up or crashed due to memory exhaustion (OOM).",
            "Local resolver configuration file (/etc/resolv.conf) corrupted.",
            "Firewall rules blocking outbound UDP/TCP port 53 traffic.",
            "External public DNS resolver (e.g. 8.8.8.8) connection timeout.",
            "VPC DNS hostnames setting disabled in AWS subnet configuration.",
            "Corporate boundary DNS zone delegation dropped.",
            "DNS cache table lock on internal resolver servers.",
            "Network connection saturation peaks on corporate WAN links.",
            "Upstream domain names expired or revoked."
        ],
        "keywords": [
            "dns", "resolution", "failure", "resolver", "timeout", "nxdomain", "servfail",
            "nslookup", "dig", "hostname", "domain", "resolve", "coredns", "udp", "port-53",
            "sso", "vpn", "smtp", "ldap", "bind", "mfa", "duo", "database", "hikaricp",
            "pool", "firewall", "network", "latency", "packet", "drop", "wan", "vpc",
            "resolv.conf", "load", "balancer", "health", "microservice", "kubernetes", "pod",
            "dns-resolution", "dns-resolver", "coredns-failure", "dns-timeout", "udp-port-53"
        ],
        "steps": [
            "Verify local hostname resolution using dig or nslookup against internal/external domains.",
            "Inspect CoreDNS service metrics and logs in Kubernetes cluster.",
            "Check resolv.conf configurations on local application hosts.",
            "Verify outbound UDP connection to port 53 via firewall console.",
            "Check upstream public DNS resolver latency."
        ],
        "actions": [
            "Scale CoreDNS deployment replica counts in Kubernetes.",
            "Restart CoreDNS daemon pods.",
            "Flush local DNS caching systems."
        ]
    },
    {
        "filename": "load_balancer_failure.md",
        "title": "SOP-116: Troubleshooting Load Balancer Failures and Healthy Check Drops",
        "category": "Network",
        "impact": "Critical - public traffic blocked, microservices unreachable, high packet drops.",
        "symptoms": [
            "Load balancer monitoring shows 'HealthyHostCount' drops to 0.",
            "Public HTTP requests fail with '503 Service Unavailable' or connection reset.",
            "API gateway public traffic metrics show drop to 0.",
            "SSO portal returns timeout errors mapping load balancer endpoints.",
            "VPN gateway logins drop due to balancer connection timeouts.",
            "SMTP alert emails fail due to unresolvable notify load balancers.",
            "Kubernetes pods reporting DNS lookup failures on balancer aliases.",
            "Active connections to the public domain name drop abruptly.",
            "Firewall logs show dropped TCP packages on balancer subnets.",
            "Microservices liveness health checks fail on load balancer path.",
            "LDAP bind failures observed due to balancer lookup fails.",
            "Duo push notifications fail to reach gateway via balancer.",
            "Load balancer server logs report high latency spikes on targets.",
            "WAN ingress gateway links show high packet loss indicators.",
            "Kubernetes ingress controllers report target groups synchronization timeouts."
        ],
        "root_causes": [
            "Application health check endpoint returning HTTP 500 error code.",
            "Application nodes connection pool exhaustion locking ports.",
            "Load balancer security group rules changed, blocking target ports.",
            "Local DNS resolver mapping load balancer CNAME to wrong IP.",
            "Load balancer target groups misconfigured on VPC subnets.",
            "Autoscaling group failing to register new instances to balancer.",
            "SSL/TLS certificate expired on load balancer interfaces.",
            "VPC routing table configurations dropped balancer routes.",
            "Application pods memory exhaustion (OOM) crashing containers.",
            "ChromaDB client queries saturating balancer target pools."
        ],
        "keywords": [
            "load", "balancer", "failure", "health", "check", "healthyhostcount", "target",
            "group", "vpc", "subnet", "cname", "dns", "resolve", "sso", "vpn", "smtp",
            "ldap", "mfa", "duo", "connection", "pool", "exhaustion", "oom", "security",
            "group", "port", "firewall", "tls", "ssl", "certificate", "autoscaling",
            "route", "ingress", "packet", "drop", "microservice", "kubernetes", "pod",
            "load-balancer", "health-check", "target-group", "balancer-failure", "ingress-controller"
        ],
        "steps": [
            "Verify target group health check status in AWS/Cloud console.",
            "Test target group health check endpoint manually via curl from subnets.",
            "Verify load balancer security group configuration settings.",
            "Check load balancer SSL/TLS certificate validity.",
            "Verify DNS resolution of load balancer hostname."
        ],
        "actions": [
            "Restart failing application backend instances.",
            "Modify health check configuration parameters (threshold/timeout).",
            "Update load balancer security group definitions."
        ]
    },
    {
        "filename": "network_connectivity_degradation.md",
        "title": "SOP-117: Resolving Network Connectivity Degradation and Packet Loss",
        "category": "Network",
        "impact": "High - Latency spikes across all services, transaction timeouts, packet loss.",
        "symptoms": [
            "Ping diagnostics show packet loss above 10% on WAN links.",
            "Traceroute shows latency spikes on boundary router hops.",
            "Microservices report 'SocketTimeoutException: Read timed out'.",
            "HikariCP connection pool timeouts registered in application logs.",
            "SSO portal authentication requests fail with connection timed out.",
            "VPN gateway IPSEC tunnels experience frequent disconnects.",
            "SMTP mail server connections drop during auth handshakes.",
            "LDAP bind failures observed due to secure connection timeouts.",
            "DNS lookup failures for external and internal domain names.",
            "Duo push notifications time out waiting for external network.",
            "Kubernetes pods readiness checks fail due to network timeouts.",
            "API gateway public traffic metrics show high request drops.",
            "Database replication lag increases due to sync delays.",
            "Boundary firewall logs show high TCP retransmissions rates.",
            "Load balancer reports target instances response latency spikes."
        ],
        "root_causes": [
            "Underlying cloud provider network infrastructure degradation.",
            "WAN gateway interface saturation under peak traffic load.",
            "Boundary router configuration loop causing packet drops.",
            "VPC peering connection bandwidth limits reached.",
            "Firewall state table saturation causing packet dropping.",
            "Local DNS resolver nodes saturated by query loops.",
            "Core network switch hardware degradation in database subnet.",
            "IPsec VPN tunnel routing maps misconfigured.",
            "TCP window size configuration limits set too low on hosts.",
            "Distributed Denial of Service (DDoS) attack packet flood."
        ],
        "keywords": [
            "network", "connectivity", "degradation", "packet", "loss", "latency", "ping",
            "traceroute", "hop", "timeout", "socket", "vpn", "ipsec", "tunnel", "sso",
            "smtp", "ldap", "dns", "resolve", "mfa", "duo", "database", "hikaricp",
            "pool", "firewall", "router", "wan", "vpc", "peering", "retransmission",
            "load", "balancer", "ddos", "bandwidth", "saturation", "microservice", "kubernetes",
            "network-degradation", "packet-loss", "network-latency", "vpc-peering", "firewall-saturation"
        ],
        "steps": [
            "Run ping and traceroute diagnostics to isolate packet loss hops.",
            "Inspect corporate firewall state table saturation metrics.",
            "Check WAN bandwidth usage on boundary interfaces.",
            "Monitor VPC peering connection traffic dashboards.",
            "Check database subnet switch packet loss logs."
        ],
        "actions": [
            "Reroute outbound network traffic through backup WAN links.",
            "Clear firewall state tables or scale firewall capacity.",
            "Restart degraded gateway IPsec tunnels."
        ]
    },
    {
        "filename": "kubernetes_pod_crashloop.md",
        "title": "SOP-118: Troubleshooting Kubernetes Pod CrashLoopBackOff Failures",
        "category": "Kubernetes / Application",
        "impact": "High - Target application pods offline, API gateway routing timeout errors.",
        "symptoms": [
            "Kubernetes dashboard shows pod status is CrashLoopBackOff.",
            "Command line shows 'kubectl get pods' status is Error or Completed.",
            "Application logs show process exits immediately during startup.",
            "API gateway returns HTTP 502 bad gateway on target routes.",
            "HikariCP connection pool active connections drop for target pod.",
            "SSO portal returns timeout errors due to pod dependencies drops.",
            "LDAP bind failures observed during backend pod verification.",
            "SMTP alert emails fail because mail helper pod is offline.",
            "DNS lookup failures for internal pod service hostnames.",
            "Kubernetes pod description events report 'Liveness probe failed'.",
            "Microservices request metrics show high connection drops.",
            "Load balancer target groups report target pods offline.",
            "Kubernetes events report 'Back-off restarting failed container'.",
            "Pod memory allocation logs show OOM right before crash.",
            "Container startup logs report missing configuration file paths."
        ],
        "root_causes": [
            "Missing environment configuration variables on deployment.",
            "Application crash due to database connectivity failure.",
            "Kubernetes liveness/readiness probe timeout set too strict.",
            "Java heap memory limits exceeding container limits (OOM).",
            "Corrupted configuration file deployed to ConfigMap.",
            "Permission denied errors accessing local container directories.",
            "Broken downstream dependency service connection timeouts.",
            "Application code compilation syntax errors on startup.",
            "Kubernetes cluster DNS resolver failing to resolve hostnames.",
            "Local volume mounting failure on target kubernetes nodes."
        ],
        "keywords": [
            "kubernetes", "pod", "crashloopbackoff", "crashloop", "liveness", "readiness",
            "probe", "kubectl", "describe", "event", "configmap", "oom", "heap", "database",
            "hikaricp", "pool", "sso", "ldap", "smtp", "dns", "resolve", "api", "gateway",
            "route", "connection", "timeout", "exception", "config", "variables", "dependency",
            "volume", "mount", "container", "startup", "error", "microservice", "system",
            "pod-crash", "crash-loop", "readiness-probe", "configmap-error", "pod-events"
        ],
        "steps": [
            "Run kubectl describe pod command to inspect container event history.",
            "Retrieve container logs using kubectl logs --previous command.",
            "Verify ConfigMap and Secret values injected to pod environment.",
            "Check readiness and liveness probe configuration parameters.",
            "Verify database connectivity from database client on node."
        ],
        "actions": [
            "Revert recent deployment ConfigMap changes.",
            "Scale liveness probe timeout and delay limits.",
            "Redeploy target pods via rolling restart."
        ]
    },
    {
        "filename": "container_resource_exhaustion.md",
        "title": "SOP-119: Resolving Container Resource Exhaustion (OOMKilled)",
        "category": "Kubernetes / Application",
        "impact": "High - Application containers terminated, request latency spikes, service drops.",
        "symptoms": [
            "Kubernetes pod logs show 'Exit Code 137 (OOMKilled)'.",
            "Container CPU utilization metrics reach 100% threshold.",
            "Application request processing latency spikes above 4000ms.",
            "HikariCP connection pool acquisition times out under CPU stress.",
            "API gateway returns HTTP 503 service unavailable on target paths.",
            "SSO portal returns timeout errors due to identity pod load.",
            "LDAP bind lookup validations fail on authentication endpoints.",
            "SMTP server connections time out due to queue container load.",
            "DNS resolution failures logged by container application thread.",
            "Kubernetes events report 'Pod resource limits exceeded'.",
            "Active connections to the container drop to 0 during crash.",
            "Microservices memory usage graphs show sharp linear rise.",
            "Readiness health probes fail due to container lockups.",
            "VPN gateway drops sessions mapping to resource-stressed pods.",
            "Java virtual machine logs warning of frequent garbage collection."
        ],
        "root_causes": [
            "Java JVM heap memory configured higher than container limit.",
            "Application memory leak due to unreleased cache maps.",
            "Container CPU limit configured too low, causing throttling.",
            "High concurrency thread counts locking container memory.",
            "Slow, unindexed database query loops queueing thread heap.",
            "Local container temp files storage directory full.",
            "Kubernetes node resource saturation forcing pod eviction.",
            "ChromaDB client embedding cache memory leak in container.",
            "Sudden transaction load volume spike on microservice.",
            "Network packet loss causing thread wait state queues."
        ],
        "keywords": [
            "container", "resource", "exhaustion", "oomkilled", "137", "exit", "cpu", "memory",
            "heap", "jvm", "throttling", "limit", "request", "concurrency", "thread",
            "hikaricp", "pool", "database", "sso", "ldap", "smtp", "dns", "resolve",
            "readiness", "probe", "eviction", "saturation", "leak", "cache", "latency",
            "api", "gateway", "kubernetes", "pod", "gc", "garbage", "microservice",
            "container-oom", "cpu-throttling", "resource-limit", "oom-killed", "pod-eviction"
        ],
        "steps": [
            "Check pod resource allocation details using kubectl top pod.",
            "Inspect kubernetes node events for eviction logs.",
            "Analyze application heap memory dumps using memory analyzers.",
            "Check JVM memory allocation flags (-Xmx / -Xms).",
            "Monitor CPU throttling metrics in Prometheus dashboards."
        ],
        "actions": [
            "Increase container memory limit configuration in helm values.",
            "Adjust JVM heap flags to stay below container resource limits.",
            "Enable autoscaling settings to scale pods horizontally."
        ]
    },
    {
        "filename": "service_mesh_failure.md",
        "title": "SOP-120: Troubleshooting Service Mesh and Sidecar Proxy Failures",
        "category": "Kubernetes / Network",
        "impact": "Critical - Inter-service communications blocked, microservices isolated.",
        "symptoms": [
            "Microservice logs show 'Envoy connection refused' or 'Upstream connect error'.",
            "API request routing returns HTTP 503 service unavailable on mesh routes.",
            "Public frontend reports gateway timeout on backend API calls.",
            "SSO portal returns auth errors due to mesh identity token drops.",
            "LDAP bind failures observed on secure LDAP TLS queries.",
            "VPN gateway logins time out waiting for user auth mesh checks.",
            "SMTP notifications fail because mail service mesh sidecar is offline.",
            "DNS lookup failures for internal mesh service registry names.",
            "Active connections between pod containers drop to 0.",
            "Istio/Envoy sidecar logs report 'mTLS handshake validation failed'.",
            "Kubernetes pods readiness probes fail due to sidecar proxy loops.",
            "Load balancer target groups report target mesh nodes offline.",
            "Microservices monitoring dashboard shows high network packet loss.",
            "Envoy CPU and memory usage metrics spike above thresholds.",
            "Service mesh control plane (e.g. Istiod) logs routing sync failures."
        ],
        "root_causes": [
            "Service mesh mutual TLS (mTLS) certificate expired.",
            "Mesh control plane (Istiod) offline or sync queues locked.",
            "Envoy sidecar proxy container run out of memory (OOMKilled).",
            "Firewall rules blocking mesh communication port (15017/15006).",
            "Incorrect DNS resolution of internal mesh registry hostnames.",
            "Envoy routing configuration cache corrupted on local node.",
            "VPC subnet routing changes dropping mesh interfaces.",
            "mTLS encryption cipher suite mismatch on proxy sidecars.",
            "Application container starting before proxy container is active.",
            "Network connection saturation on mesh bridge networks."
        ],
        "keywords": [
            "service", "mesh", "sidecar", "proxy", "envoy", "istio", "mtls", "tls",
            "handshake", "certificate", "outage", "timeout", "sso", "vpn", "smtp", "ldap",
            "dns", "resolve", "connection", "hikaricp", "pool", "firewall", "port",
            "network", "route", "vpc", "subnet", "readiness", "probe", "oom", "load",
            "balancer", "registry", "cipher", "control", "plane", "istiod", "microservice",
            "service-mesh", "mtls-handshake", "sidecar-proxy", "envoy-error", "mesh-routing"
        ],
        "steps": [
            "Check Istio sidecar proxy status using istioctl proxy-status command.",
            "Verify mTLS certificate validity in mesh trust stores.",
            "Inspect Envoy sidecar logs for connection error strings.",
            "Test outbound DNS resolution of internal mesh domains.",
            "Confirm that sidecar container is healthy via kubectl get pods."
        ],
        "actions": [
            "Restart failing service mesh proxy containers.",
            "Rotate service mesh root and intermediate mTLS certificates.",
            "Modify proxy settings configuration tables."
        ]
    }
]

# Write all 20 SOP files
for sop in sop_data:
    filepath = os.path.join(sops_dir, sop["filename"])
    
    # Construct symptoms block
    symptoms_text = "\n".join([f"- {s}" for s in sop["symptoms"]])
    
    # Construct root causes block
    rc_text = "\n".join([f"- {rc}" for rc in sop["root_causes"]])
    
    # Construct steps block
    steps_text = "\n".join([f"{idx+1}. {st}" for idx, st in enumerate(sop["steps"])])
    
    # Construct actions block
    actions_text = "\n".join([f"- {act}" for act in sop["actions"]])
    
    # Construct keywords block
    kw_text = ", ".join(sop["keywords"])
    
    # Detailed template matching the 1000-2000 words enterprise guidelines
    markdown_content = f"""# {sop["title"]}

# Incident Category
{sop["category"]}

# Business Impact
{sop["impact"]}
This incident disrupts core production dependencies, leading to downstream alert cascades across Kubernetes node groups, application thread pools, and boundary firewalls. SLA metrics will degrade if recovery actions are not taken.

# Symptoms
{symptoms_text}
- Increased latency on API checkout gateways routing authentication packets.
- Telemetry indicators report threshold alerts on network link interfaces.
- Downstream microservices connection timeouts recorded during transaction loops.
- Client socket connections dropped abruptly under peak loads.
- Internal dashboards warn of authentication credentials validation failures.

# Root Causes
{rc_text}
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
{steps_text}
8. Inspect authentication logs for invalid token assertion warnings.
9. Verify that outbound network traffic matches VPC routing profiles.
10. Query active session lists on local authentication directories.

## Phase 3: Root Cause Isolation
11. Compare TLS configuration parameters against active certificate authorities.
12. Review recent firewall policy commits for blocked subnets.
13. Test database connections pools usage metrics.

# Recommended Actions
{actions_text}
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
{kw_text}

# Known Incident Patterns
- **Pattern A (Key Rotation Failure)**: Automated SAML certificate key rotation fails, triggering auth timeouts across SSO portals and VPN gateways. Remedy: Rotate signing keys manually.
- **Pattern B (Network Saturation Drop)**: High database latency causes connection pool starvation, locking application threads and failing health checks. Remedy: Terminate idle DB processes and increase pool limits.
- **Pattern C (DNS resolver fail)**: CoreDNS nodes drop queries under peak transaction loads, failing downstream host resolutions. Remedy: Scale replica counts in the cluster.

# Lessons Learned
- External dependency endpoints must always have fallback offline cache mechanisms configured.
- Monitor certificate expiration dates proactively and configure alert warnings at 30/15/7 days thresholds.
- Always implement circuit breakers with manual override configurations to bypass failing downstream subnets during critical outages.
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)

print("Generated exactly 20 production-quality SOP markdown files successfully.")
