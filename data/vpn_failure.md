# SOP-101: Troubleshooting VPN Gateway Connection Failures

## Overview
This standard operating procedure governs resolving network outages and authentication timeouts on the corporate VPN gateway clusters.

## Diagnostics Steps
1. Verify if the client receives the `IPSEC Tunnel Timeout` alert payload.
2. Check gateway server CPU thresholds. If usage exceeds 95%, restart VPN routing tables.
3. Verify VPC tunnel associations inside the routing configuration panels.

## Mitigation Action
Run gateway reset commands:
```bash
systemctl restart ipsec-gateway
```
Ensure VPN traffic limits are scaled up to resolve core network saturation peaks.
