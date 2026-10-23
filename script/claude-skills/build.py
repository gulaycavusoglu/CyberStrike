#!/usr/bin/env python3
"""Convert CyberStrike's .cyberstrike/skill/**/SKILL.md library into a Claude Code plugin.

Claude Code discovers plugin skills at `skills/<name>/SKILL.md` only (one level),
so every skill is flattened into a directory named after its normalized name.
Frontmatter keys Claude Code does not recognize are re-emitted under `metadata:`
so no information is lost.

Run: python3 -I script/claude-skills/build.py
"""

import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, ".cyberstrike", "skill")
OUT = os.path.join(ROOT, "claude-plugin", "skills")

# Frontmatter keys Claude Code understands; everything else is preserved in metadata.
KNOWN = {
    "name",
    "description",
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "disallowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "background",
    "hooks",
    "paths",
    "shell",
    "metadata",
    "license",
    "compatibility",
}

KEY = re.compile(r"^([A-Za-z_][\w.-]*):(.*)$")


def split(text):
    """Return (frontmatter, body) or (None, text) when there is no frontmatter."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    body_start = text.find("\n", end + 4)
    body = text[body_start + 1 :] if body_start >= 0 else ""
    return text[3:end], body


def blocks(fm):
    """Split frontmatter into [(key, inline_value, continuation_lines)] preserving order."""
    out = []
    for line in fm.splitlines():
        m = KEY.match(line)
        if m:
            out.append([m.group(1), m.group(2).strip(), []])
        elif out and line.strip():
            out[-1][2].append(line)
    return [(k, v, lines) for k, v, lines in out]


def indent(lines):
    """Re-indent continuation lines two spaces deeper, relative to their own margin."""
    if not lines:
        return []
    margin = min(len(line) - len(line.lstrip()) for line in lines)
    return ["    " + line[margin:] for line in lines]


def scalar(raw):
    raw = raw.strip()
    if raw.startswith('"') and raw.endswith('"') and len(raw) > 1:
        return raw[1:-1].replace('\\"', '"')
    if raw.startswith("'") and raw.endswith("'") and len(raw) > 1:
        return raw[1:-1].replace("''", "'")
    return raw.strip()


def norm(name):
    s = name.lower().replace("_", "-").replace(".", "-")
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")[:64].strip("-")


def title_of(body):
    m = re.search(r"^#\s+(.+)$", body, re.M)
    return m.group(1).strip() if m else ""


def main():
    if not os.path.isdir(SRC):
        sys.exit(f"source library not found: {SRC}")

    paths = []
    for dirpath, _, files in os.walk(SRC):
        if "SKILL.md" in files:
            paths.append(os.path.join(dirpath, "SKILL.md"))
    paths.sort()

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    seen = {}
    index = []
    categories = {}
    for path in paths:
        text = open(path, encoding="utf-8", errors="replace").read()
        fm, body = split(text)
        pairs = blocks(fm) if fm is not None else []
        meta = {}
        for k, v, _ in pairs:
            meta.setdefault(k, v)

        raw_name = scalar(meta.get("name", "")) or os.path.basename(os.path.dirname(path))
        name = norm(raw_name) or "skill"
        if name in seen:
            seen[name] += 1
            name = f"{name[:61]}-{seen[name]}"
        else:
            seen[name] = 1

        desc = scalar(meta.get("description", ""))
        if not desc:
            title = title_of(body)
            desc = title or f"CyberStrike security skill {raw_name}"
        desc = desc.replace('"', "'")

        cat = scalar(meta.get("category", ""))
        if cat:
            categories[cat] = categories.get(cat, 0) + 1

        extra = [(k, v, more) for k, v, more in pairs if k not in KNOWN and (v or more)]
        lines = ["---", f"name: {name}", f"description: \"{desc}\""]
        if extra:
            lines.append("metadata:")
            lines.append(f"  cyberstrike_name: \"{raw_name}\"")
            lines.append(f"  source: \"{os.path.relpath(path, ROOT)}\"")
            for k, v, more in extra:
                lines.append(f"  {k}:{(' ' + v) if v else ''}")
                lines.extend(indent(more))
        lines.append("---")
        lines.append("")

        # One WSTG skill links a sibling only reachable at its original nested path.
        body = body.replace(
            "](./WSTG-INFO-08.md)", "](../wstg-info-08/SKILL.md)"
        ).replace("](WSTG-INFO-08.md)", "](../wstg-info-08/SKILL.md)")

        target = os.path.join(OUT, name)
        os.makedirs(target)
        with open(os.path.join(target, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + body)

        index.append(
            {
                "name": name,
                "source_name": raw_name,
                "description": desc,
                "category": cat,
                "source": os.path.relpath(path, ROOT),
            }
        )

    # Hand-written skills that live outside the source library (the router).
    templates = os.path.join(ROOT, "script", "claude-skills", "templates")
    for entry in sorted(os.listdir(templates)) if os.path.isdir(templates) else []:
        if entry in seen:
            sys.exit(f"template {entry} collides with a converted skill name")
        shutil.copytree(os.path.join(templates, entry), os.path.join(OUT, entry))
        index.append(
            {"name": entry, "source_name": entry, "description": "", "category": "", "source": "template"}
        )

    with open(os.path.join(OUT, "INDEX.json"), "w", encoding="utf-8") as f:
        json.dump({"count": len(index), "categories": categories, "skills": index}, f, indent=1)

    # Per-family catalogs: small enough for the router to read on demand, unlike INDEX.json.
    refs = os.path.join(OUT, "cyberstrike-router", "references")
    os.makedirs(refs, exist_ok=True)
    if os.path.isdir(refs):
        families = {}
        for entry in index:
            if entry["source"] == "template":
                continue
            top = entry["source"].split("/")[2]
            families.setdefault(top, []).append(entry)
        for top, entries in families.items():
            entries.sort(key=lambda e: e["name"])
            lines = [f"# {top}", "", f"{len(entries)} skills.", ""]
            for e in entries:
                lines.append(f"- `{e['name']}` — {e['description']}")
            with open(os.path.join(refs, f"{top}.md"), "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        print(f"wrote {len(families)} catalogs to {refs}")

    print(f"converted {len(index)} skills into {OUT}")
    for cat, n in sorted(categories.items(), key=lambda kv: -kv[1]):
        print(f"  {cat:32} {n}")


if __name__ == "__main__":
    main()
