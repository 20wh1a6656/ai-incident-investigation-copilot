# SOP-094: PostgreSQL Connection Pool Exhaustion

## Overview
Connection pool capacity drops below 5% or connection slots leak when connections are not released cleanly back to the HikariCP pool.

## Diagnostics Steps
1. Verify if logs display `org.postgresql.util.PSQLException: FATAL: remaining connection slots are reserved`.
2. Check database engine active session lists.
3. Identify long-running transaction queries blocking connection acquisition slots.

## Mitigation Action
1. Terminate orphaned backend processes:
```sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle';
```
2. Provision additional slots configuration limits:
```sql
ALTER SYSTEM SET max_connections = 400;
```
Restart replica masters to apply new pool limits.
