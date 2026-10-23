---
name: cyberstrike-router
description: "Use when starting any security engagement — penetration test, bug bounty, CTF, vulnerability assessment, cloud/AD audit, or compliance review. Routes to the right CyberStrike skill among 7,600+ OWASP WSTG, MITRE ATT&CK, NIST, CIS, attack-playbook and post-exploitation skills, and explains how to look one up by name."
---

# CyberStrike Skill Router

This plugin bundles the security knowledge library from
[CyberStrike](https://github.com/CyberStrikeus/CyberStrike): 7,662 methodology
skills the CyberStrike agent loads at runtime. Each skill is a standalone
document — testing procedures, payloads, tool commands, CWE mappings, and
remediation.

## How to find the right skill

This plugin carries 7,663 skills. Claude Code keeps every skill name in the
listing but budgets descriptions, so with a library this large the descriptions
are usually dropped and the names read as bare labels. Do not rely on guessing a
name — look it up here first.

Read the catalog for the family you need (each is one line per skill, name and
description):

| Family | Catalog |
| ------ | ------- |
| OWASP WSTG web tests | `references/WEB.md` |
| MITRE ATT&CK Enterprise | `references/mitre_attack.md` |
| MITRE ATT&CK Mobile | `references/mitre_attack_mobile.md` |
| MITRE ATT&CK ICS | `references/mitre_attack_ics.md` |
| NIST (CSF, 800-53, 800-171, SSDF) | `references/NIST.md` |
| CIS Benchmarks | `references/CIS_benchmarks.md` |
| Attack playbooks, post-exploitation, domain knowledge | the table below, or `grep` these small files |

Resolve paths with `${CLAUDE_PLUGIN_ROOT}/skills/cyberstrike-router/references/`.
For a keyword search across everything, the machine-readable index is at
`${CLAUDE_PLUGIN_ROOT}/skills/INDEX.json`.

```bash
grep -i -E 'ssrf|request smuggling' "$CLAUDE_PLUGIN_ROOT"/skills/cyberstrike-router/references/*.md
```

Once you have the name, invoke it as `/cyberstrike:<name>`, or read
`${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` directly. Invoking by name works
whether or not descriptions are in the listing.

## Naming conventions

| Family | Prefix | Example | Count |
| ------ | ------ | ------- | ----- |
| OWASP WSTG web tests | `wstg-` | `wstg-inpv-05` (SQLi) | 125 |
| MITRE ATT&CK Enterprise | `t<id>-` | `t1114-002-remote-email-collection` | 691 |
| MITRE ATT&CK Mobile / ICS | `t<id>-` | `t1409-…`, `t0855-…` | 207 |
| NIST (CSF, 800-53, 800-171, SSDF) | plain | `rv-2-2`, `po-4-1`, `gv-oc-01-gvoc-01` | 1,606 |
| CIS Benchmarks (cloud, OS, server, k8s) | `cis-` | `cis-gworkspace-6-3` | 5,000 |
| Attack playbooks | `attack-` | `attack-ssrf`, `attack-jwt` | 16 |
| Post-exploitation | `*-postexploit` | `aws-postexploit`, `linux-postexploit` | 7 |
| Domain knowledge | plain | `ad-security`, `kerberos-attacks`, `recon-methodology`, `llm-security` | 10 |

Names are normalized from the source: lowercased, `_` and `.` become `-`.
`T1114.002_remote-email-collection` becomes `t1114-002-remote-email-collection`.
The original name is preserved in each skill's `metadata.cyberstrike_name`.

## Routing by task

| Task | Start with | Then chain into |
| ---- | ---------- | --------------- |
| Web app pentest | `recon-methodology` | `wstg-info-*` → `wstg-conf-*` / `wstg-idnt-*` → `wstg-authz-*` → `wstg-inpv-*` → `wstg-sess-*` → `wstg-clnt-*` → `wstg-busl-*` |
| API testing | `wstg-apit-00` | `wstg-apit-01` recon → the specific `wstg-inpv-*` test |
| Bug bounty | `recon-methodology` | `attack-subdomain-takeover`, `attack-cache-poison`, `attack-request-smuggling` |
| Specific bug class | `attack-<class>` | follow its `chains_with` list — `attack-ssrf` → `attack-xxe`, `attack-ssti` |
| Active Directory | `ad-security` | `kerberos-attacks` → `windows-postexploit` |
| Cloud audit | `cloud-assessment` | `aws-postexploit` / `azure-postexploit` / `gcp-postexploit`, plus the matching `cis-*` benchmark |
| Kubernetes | `k8s-assessment` | `k8s-postexploit`, `cis-*k8s*` |
| CI/CD | `cicd-attacks` | `ci-assessment` |
| Compliance | NIST / CIS entries | `cis-<platform>-<id>` |
| LLM/agent targets | `llm-security` | `wstg-*` for the web surface |
| Threat modelling | MITRE skills | `t<id>-…` by tactic (`metadata.tactic`) |

## Chains and prerequisites

Skills carry `metadata.chains_with`, `metadata.prerequisites`, and
`metadata.severity_boost` (why a chain raises severity). Read them before
planning a multi-step engagement — e.g. `wstg-inpv-05` notes that SQLi plus IDOR
(`wstg-authz-02`) means account takeover.

## Working with CyberStrike itself

These skills reference CyberStrike's own tooling (`attack_script`, `http_replay`,
`hackbrowser`, Bolt MCP servers). When running Claude Code outside CyberStrike,
translate those to equivalent local tools (`curl`, `nuclei`, `sqlmap`, `nmap`,
Playwright) — or install the harness: `npm i -g @cyberstrike-io/cyberstrike`.

## Responsible use

Everything here is offensive methodology. Only run it against systems you are
authorized to test, and stay inside the agreed scope.