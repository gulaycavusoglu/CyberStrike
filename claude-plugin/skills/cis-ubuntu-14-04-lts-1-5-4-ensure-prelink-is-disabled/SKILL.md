---
name: cis-ubuntu-14-04-lts-1-5-4-ensure-prelink-is-disabled
description: "Verify that prelink is disabled to prevent interference with AIDE integrity checking"
metadata:
  cyberstrike_name: "CIS Ubuntu 14.04 LTS - 1.5.4 Ensure prelink is disabled"
  source: ".cyberstrike/skill/CIS_benchmarks/Operating_Systems/Ubuntu/cis-ubuntu-linux-14-04-lts-benchmark-v2/cis-ubuntu1404-v210-1-5-4/SKILL.md"
  category: "cis-os-hardening"
  version: "2.1.0"
  author: "cyberstrike-official"
  tags:
    - cis
    - ubuntu
    - ubuntu-14.04
    - level-1
    - scored
    - hardening
  cis_id: "1.5.4"
  cis_benchmark: "CIS Ubuntu Linux 14.04 LTS Benchmark v2.1.0"
  tech_stack:
    - ubuntu
    - linux
  cwe_ids: []
  chains_with:
    - cis-ubuntu1404-v210-1-3-1
  prerequisites: []
  severity_boost: "medium"
---

# 1.5.4 Ensure prelink is disabled (Scored)

## Profile Applicability

- Level 1 - Server
- Level 1 - Workstation

## Description

`prelink` is a program that modifies ELF shared libraries and ELF dynamically linked binaries in such a way that the time needed for the dynamic linker to perform relocations at startup significantly decreases.

## Rationale

The prelinking feature can interfere with the operation of AIDE, because it changes binaries. Prelinking can also increase the vulnerability of the system if a malicious user is able to compromise a common library such as libc.

## Audit Procedure

Run the following command and verify `prelink` is not installed:

```bash
dpkg -s prelink
```

## Expected Result

The output should indicate that the package is not installed.

## Remediation

Run the following command to restore binaries to normal:

```bash
prelink -ua
```

Run the following command to uninstall `prelink`:

```bash
apt-get remove prelink
```

## Default Value

`prelink` is not installed by default.

## References

- CIS Controls: 3.5 Use File Integrity Tools For Critical System Files

## Profile

- Level 1 - Server
- Level 1 - Workstation
