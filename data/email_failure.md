# SOP-104: SMTP / Email Notification Delivery Failures

## Overview
Occurs when downstream SMTP hosts drop notification socket attempts due to auth changes or load peaks.

## Diagnostics Steps
1. Verify if logs register `Connection refused` or `535 Authentication failed` codes.
2. Check email server queue backlogs.
3. Test direct telnet ports access connectivity limits.

## Mitigation Action
Verify configuration environment variables:
```bash
telnet smtp.mail-provider.com 587
```
Update SMTP auth tokens configurations inside settings tables.
