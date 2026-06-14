# SOP-103: Application Crash Loop Backoff Failures

## Overview
Occurs when deployment pods fail health checks or run out of memory (OOMKilled) under load.

## Diagnostics Steps
1. Run `kubectl describe pod` to verify termination reasons.
2. Check memory utilization peaks in log traces.
3. Verify if environment context variable definitions are correct.

## Mitigation Action
1. Increase kubernetes pod memory thresholds:
```yaml
resources:
  limits:
    memory: "2Gi"
```
2. Restart crash pods using rollout commands:
```bash
kubectl rollout restart deployment/checkout-service
```
