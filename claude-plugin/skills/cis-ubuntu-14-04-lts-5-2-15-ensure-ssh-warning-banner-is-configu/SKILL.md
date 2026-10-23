---
name: cis-ubuntu-14-04-lts-5-2-15-ensure-ssh-warning-banner-is-configu
description: "Verify SSH Banner is configured to display a warning message before authentication"
metadata:
  cyberstrike_name: "CIS Ubuntu 14.04 LTS - 5.2.15 Ensure SSH warning banner is configured"
  source: ".cyberstrike/skill/CIS_benchmarks/Operating_Systems/Ubuntu/cis-ubuntu-linux-14-04-lts-benchmark-v2/cis-ubuntu1404-v210-5-2-15/SKILL.md"
  category: "cis-os-hardening"
  version: "2.1.0"
  author: "cyberstrike-official"
  tags:
    - cis
    - ubuntu
    - ubuntu-14.04
    - level-1
    - scored
    - ssh
  cis_id: "5.2.15"
  cis_benchmark: "CIS Ubuntu Linux 14.04 LTS Benchmark v2.1.0"
  tech_stack:
    - ubuntu
    - linux
  cwe_ids: []
  chains_with: []
  prerequisites: []
  severity_boost: "low"
---

# 5.2.15 Ensure SSH warning banner is configured (Scored)

## Profile Applicability

- Level 1 - Server
- Level 1 - Workstation

## Description

The `Banner` parameter specifies a file whose contents must be sent to the remote user before authentication is permitted. By default, no banner is displayed.

## Rationale

Banners are used to warn connecting users of the particular site's policy regarding connection. Presenting a warning message prior to the normal user login may assist the prosecution of trespassers on the computer system.

## Audit Procedure

Run the following command and verify that output matches:

```bash
grep "^Banner" /etc/ssh/sshd_config
```

## Expected Result

```
Banner /etc/issue.net
```

## Remediation

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```
Banner /etc/issue.net
```

## Default Value

Banner none

## References

- CIS Controls: 16 - Account Monitoring and Control

## Profile

- Level 1 - Server
- Level 1 - Workstation
