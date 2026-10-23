# CyberStrike Security Skills

A Claude Code plugin containing the full security knowledge library from
[CyberStrike](https://github.com/CyberStrikeus/CyberStrike), an open-source
AI agent for offensive security. It converts the harness's runtime skill files
(`.cyberstrike/skill/**/SKILL.md`) into Claude Code plugin skills, so Claude can
load the same methodology documents while working outside CyberStrike.

**7,662 skills** in one plugin:

| Family | Count | Covers |
| ------ | ----- | ------ |
| CIS Benchmarks | 5,000 | AWS, Azure, GCP, Kubernetes (EKS/AKS/GKE/OKE), OpenShift, Docker, Ubuntu/RHEL, Windows, nginx, Apache, Tomcat, BIND, Cassandra, Google Workspace — each control with audit and remediation commands |
| NIST | 1,606 | CSF 2.0, SP 800-53, SP 800-171, SSDF (SP 800-218) |
| MITRE ATT&CK | 898 | Enterprise (691), Mobile (124), ICS (83) techniques and sub-techniques |
| OWASP WSTG 4.2 | 125 | The complete web security testing guide — recon, config, identity, authz, input validation, session, client-side, business logic, error handling, crypto, API |
| Attack playbooks | 16 | SSRF, XXE, SSTI, JWT, GraphQL, CORS, race conditions, request smuggling, cache poisoning, prototype pollution, WebSocket, host header, open redirect, subdomain takeover, rate-limit bypass, IDOR automation |
| Post-exploitation | 7 | AWS, Azure, GCP, Kubernetes, Linux, macOS, Windows |
| Domain knowledge | 10 | AD security, Kerberos, recon methodology, CI/CD attacks, CI assessment, cloud assessment, K8s assessment, eBPF, LLM security, Bun file I/O |

Each skill is a self-contained document: what to check, how to test, ready-to-use
payloads, tool commands, CWE mappings, severity guidance, and remediation.

## Install

From a clone of this repo, this repository doubles as a single-plugin
marketplace (`.claude-plugin/marketplace.json`):

```
/plugin install cyberstrike --marketplace gulaycavusoglu/CyberStrike
```

Or load the plugin folder straight from disk, with no install:

```bash
# point at the plugin folder, not the repo root
claude --plugin-dir /path/to/CyberStrike/claude-plugin
```

Or install it as a personal skills-directory plugin by symlinking the plugin
folder into `~/.claude/skills/`:

```bash
ln -s /path/to/CyberStrike/claude-plugin ~/.claude/skills/cyberstrike
```

Then check it loaded:

```bash
claude plugin validate /path/to/CyberStrike/claude-plugin --profile directory
```

## Use

Skills are model-invoked — their descriptions match the task at hand, and you can
also call one directly as `/cyberstrike:<name>`:

```
/cyberstrike:wstg-inpv-05          # Testing for SQL Injection
/cyberstrike:attack-ssrf           # SSRF playbook
/cyberstrike:t1114-002-remote-email-collection
/cyberstrike:cis-gworkspace-6-3
```

Start with the `cyberstrike-router` skill for a task-to-skill routing table, or
search the catalog:

```bash
grep -i 'kerberoast' skills/INDEX.json
```

### Naming

Names are normalized for Claude Code: lowercased, with `_` and `.` rewritten to
`-`. Each skill keeps its original name in `metadata.cyberstrike_name` and its
original path in `metadata.source`.

### Notes for Claude Code users

The skills reference CyberStrike's own tools (`attack_script`, `http_replay`,
`hackbrowser`, Bolt MCP servers). Outside CyberStrike, translate them to local
equivalents — `curl`, `nuclei`, `sqlmap`, `nmap`, `ffuf`, Playwright. Many of
these skills also carry `metadata.chains_with`, `metadata.prerequisites`, and
`metadata.severity_boost` describing attack chains. Use them to plan multi-step
work.

### Cost and behavior at this scale

Measured with `claude plugin details cyberstrike`, this plugin adds a projected
**~220,000 tokens to every session** — every skill name plus its description in
the always-on listing. Claude Code budgets skill descriptions to ~1% of the
context window, and 7,663 descriptions far exceed that, so at the default
setting **the model sees bare names with no descriptions**:

```
- cyberstrike:ac-1-policy-and-procedures
- cyberstrike:wstg-inpv-05
- cyberstrike:attack-ssrf
```

Consequences:

- **Model auto-invocation does not work from descriptions alone.** Have Claude
  consult `cyberstrike-router` first — it carries per-family catalogs
  (`references/*.md`) with one name + description per line, small enough to read
  on demand.
- **Invoking by name always works** (`/cyberstrike:<name>`, or reading
  `skills/<name>/SKILL.md`), whether or not descriptions are in the listing.
- **To restore descriptions**, raise the listing budget in your settings:

  ```json
  { "skillListingBudgetFraction": 0.25 }
  ```

  0.25 was verified to surface all 7,663 descriptions on a 1M-token context
  window; on a 200K window it would need ~0.97, so pair it with
  `skillOverrides` set to `"name-only"` for the families you rarely use.

## Regenerating

The `skills/` directory is generated. To rebuild it after syncing with upstream:

```bash
python3 -I script/claude-skills/build.py
```

The script flattens the nested library into the `skills/<name>/SKILL.md` layout
Claude Code discovers, normalizes names, and moves frontmatter keys Claude Code
does not recognize (OWASP/CIS/MITRE IDs, tags, chains) into `metadata:`. It is
idempotent — `skills/` is rebuilt from scratch each run.

## Responsible use

Everything here is offensive-security methodology. Only run it against systems
you are authorized to test, and stay inside the agreed scope.

## License

AGPL-3.0, inherited from CyberStrike.
