#!/usr/bin/env python3
"""Validate this library's portable packaging (stdlib-only, Python 3.9+).

The local authoring convention uses one-line scalar YAML fields. This validator
intentionally does not implement arbitrary YAML or certify skill decisions.
"""

import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


EXPECTED = {
    "ad-game-director", "game-concept-and-loops", "game-prototyping",
    "game-feel-and-onboarding", "game-progression-and-economy",
    "game-retention-and-liveops", "game-art-audio-and-content",
    "game-ad-monetization", "game-ad-integration", "game-ad-operations",
    "game-privacy-and-platform-policy", "game-analytics-and-experiments",
    "game-quality-and-release", "game-growth-and-acquisition",
    "game-profitability-and-priorities", "game-size-and-performance",
    "game-playtesting-and-research", "game-level-design-and-difficulty",
    "game-accessibility-and-localization", "game-systems-architecture",
    "game-save-and-cloud-sync", "game-offline-and-time",
    "game-remote-config-and-delivery", "game-iap-and-entitlements",
    "game-observability-and-incidents", "game-player-support-and-reviews",
    "game-ui-and-navigation", "game-ux-writing-and-instructions",
    "game-security-and-integrity", "game-prompts-and-permissions",
    "game-notifications-and-messaging",
    "game-platform-services", "game-quests-and-objectives",
}
LINK = re.compile(r"\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def frontmatter(text):
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    fields = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        pair = re.fullmatch(r"([a-z][a-z-]*):\s+(.+)", line)
        if not pair:
            raise ValueError("use one-line scalar YAML fields")
        key, value = pair.groups()
        if key in fields:
            raise ValueError("duplicate frontmatter key: " + key)
        if value.startswith('"'):
            value = json.loads(value)
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
        elif ": " in value or " #" in value or value[0] in "[{}&*!|>@`":
            raise ValueError("quote ambiguous YAML scalar: " + key)
        fields[key] = value
    return fields


def linked_files(path):
    for match in LINK.finditer(path.read_text(encoding="utf-8")):
        raw = match.group(1).strip("<>")
        split = urlsplit(raw)
        if split.scheme or split.netloc or not split.path:
            continue
        yield raw, (path.parent / unquote(split.path)).resolve()


def validate_skill(skill):
    skill = Path(skill).resolve()
    errors = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return ["missing SKILL.md"]
    try:
        text = entry.read_text(encoding="utf-8")
        fields = frontmatter(text)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64 or name != skill.name:
            errors.append("name must be valid and match the directory")
        if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
            errors.append("description must have 1–1024 characters")
        if fields.get("license") != "MIT":
            errors.append("license must be MIT")
        if set(fields) - {"name", "description", "license", "compatibility"}:
            errors.append("unsupported field in this library's scalar metadata convention")
        if len(text.splitlines()) > 500:
            errors.append("entry point exceeds 500 lines; use focused references")
    except (ValueError, TypeError) as exc:
        errors.append(str(exc))
    if not (skill / "LICENSE").is_file():
        errors.append("missing portable licence notice")
    for file in skill.rglob("*"):
        if file.is_symlink():
            errors.append("symlink is not portable: " + str(file.relative_to(skill)))
        if file.is_file() and file.suffix == ".md":
            for raw, target in linked_files(file):
                if target != skill and skill not in target.parents:
                    errors.append("resource escapes standalone skill: " + raw)
                elif not target.exists():
                    errors.append("missing linked resource: " + raw)
    return errors


def validate_library(root):
    root = Path(root).resolve()
    errors = []
    skills = root / "skills"
    found = {p.name for p in skills.iterdir() if p.is_dir() and not p.name.startswith(".")}
    if found != EXPECTED:
        errors.append("skill coverage mismatch: missing=%s extra=%s" % (sorted(EXPECTED - found), sorted(found - EXPECTED)))
    for name in sorted(found):
        errors.extend(name + ": " + error for error in validate_skill(skills / name))
    for folder in [root / "docs", root / "evals", root / "scripts", root / "tests", skills]:
        if not folder.exists():
            errors.append("missing directory: " + folder.name)
            continue
        for path in folder.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            try:
                if path.suffix == ".py":
                    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                elif path.suffix == ".json":
                    json.loads(path.read_text(encoding="utf-8"), parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite JSON: " + value)))
            except (SyntaxError, ValueError) as exc:
                errors.append(str(path.relative_to(root)) + ": " + str(exc))
    docs = list(root.glob("*.md")) + list((root / "docs").rglob("*.md")) + list((root / "evals").rglob("*.md"))
    for path in docs:
        for raw, target in linked_files(path):
            if root not in target.parents and target != root:
                errors.append(str(path.relative_to(root)) + ": link escapes repository: " + raw)
            elif not target.exists():
                errors.append(str(path.relative_to(root)) + ": missing resource: " + raw)
    catalog = root / "CATALOG.md"
    if not catalog.exists():
        errors.append("missing CATALOG.md")
    else:
        content = catalog.read_text(encoding="utf-8")
        for name in EXPECTED:
            if "skills/%s/SKILL.md" % name not in content:
                errors.append("catalog missing: " + name)
    version = root / "VERSION"
    if not version.exists() or not re.fullmatch(r"\d+\.\d+\.\d+\n?", version.read_text(encoding="utf-8")):
        errors.append("VERSION must contain a semantic release number")
    try:
        profiles = json.loads((root / "profiles.json").read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        if not isinstance(profiles, dict) or not profiles:
            raise ValueError("profiles must be a nonempty object")
        covered = set()
        for name, members in profiles.items():
            if not NAME.fullmatch(name) or not isinstance(members, list) or not members:
                raise ValueError("invalid profile: " + str(name))
            if any(not isinstance(item, str) or item not in EXPECTED for item in members):
                raise ValueError("unknown skill in profile: " + name)
            if len(members) != len(set(members)):
                raise ValueError("duplicate skill in profile: " + name)
            covered.update(members)
        if covered != EXPECTED:
            raise ValueError("skills missing from profiles: " + ", ".join(sorted(EXPECTED - covered)))
    except (OSError, ValueError, TypeError) as exc:
        errors.append("profiles.json: " + str(exc))
    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    errors = validate_library(root)
    if errors:
        print("Validation failed:\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    print("Validated %d skills: metadata, portable resources, catalogue, links, Python syntax and JSON." % len(EXPECTED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
