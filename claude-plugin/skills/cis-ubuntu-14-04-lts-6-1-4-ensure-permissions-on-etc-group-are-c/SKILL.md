---
name: cis-ubuntu-14-04-lts-6-1-4-ensure-permissions-on-etc-group-are-c
description: "Verify /etc/group has correct ownership (root:root) and permissions (644)"
metadata:
  cyberstrike_name: "CIS Ubuntu 14.04 LTS - 6.1.4 Ensure permissions on /etc/group are configured"
  source: ".cyberstrike/skill/CIS_benchmarks/Operating_Systems/Ubuntu/cis-ubuntu-linux-14-04-lts-benchmark-v2/cis-ubuntu1404-v210-6-1-4/SKILL.md"
  category: "cis-os-hardening"
  version: "2.1.0"
  author: "cyberstrike-official"
  tags:
    - cis
    - ubuntu
    - ubuntu-14.04
    - level-1
    - scored
    - file-permissions
  cis_id: "6.1.4"
  cis_benchmark: "CIS Ubuntu Linux 14.04 LTS Benchmark v2.1.0"
  tech_stack:
    - ubuntu
    - linux
  cwe_ids: []
  chains_with: []
  prerequisites: []
  severity_boost: "medium"
---

# 6.1.4 Ensure permissions on /etc/group are configured (Scored)

## Profile Applicability

- Level 1 - Server
- Level 1 - Workstation

## Description

The `/etc/group` file contains a list of all the valid groups defined in the system. The command below allows read/write access for root and read access for everyone else.

## Rationale

The `/etc/group` file needs to be protected from unauthorized changes by non-privileged users, but needs to be readable as this information is used with many non-privileged programs.

## Audit Procedure

Run the following command and verify `Uid` and `Gid` are both `0/root` and `Access` is `644`:

```bash
stat /etc/group
```

## Expected Result

```
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
```

## Remediation

Run the following command to set permissions on `/etc/group`:

```bash
chown root:root /etc/group
chmod 644 /etc/group
```

## Default Value

Access: (0644/-rw-r--r--) Uid: ( 0/ root) Gid: ( 0/ root)

## References

None

## CIS Controls

16.14 Encrypt/Hash All Authentication Files And Monitor Their Access - Verify that all authentication files are encrypted or hashed and that these files cannot be accessed without root or administrator privileges. Audit all access to password files in the system.

## Profile

- Level 1
