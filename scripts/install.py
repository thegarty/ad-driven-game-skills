#!/usr/bin/env python3
"""Copy selected skills without overwriting unmanaged or locally edited files."""

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile


MANIFEST = ".ad-driven-game-skills-install.json"
LOCK = ".ad-driven-game-skills-install.lock"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class InstallError(ValueError):
    pass


@contextmanager
def destination_lock(destination):
    """Serialize installers; leave interrupted-process locks for manual review."""
    lock = destination / LOCK
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise InstallError("Destination is locked: %s. Another installer may be running; "
                           "inspect the lock before removing it." % lock) from exc
    try:
        (lock / "owner.txt").write_text("pid=%s\n" % os.getpid(), encoding="utf-8")
        yield
    finally:
        shutil.rmtree(lock)


def files_in(root):
    """Return a content snapshot; ignore only generated Python/macOS cache files."""
    if root.is_symlink():
        raise InstallError("Refusing a symlink skill directory: %s" % root)
    if not root.is_dir():
        raise InstallError("Not a skill directory: %s" % root)
    result = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_symlink():
            raise InstallError("Refusing a symlink in skill: %s" % path)
        if "__pycache__" in rel.parts or path.name == ".DS_Store" or path.suffix == ".pyc":
            continue
        if path.is_file():
            result[rel.as_posix()] = path.read_bytes()
    return result


def hashes(files):
    return {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}


def read_manifest(path):
    if path.is_symlink():
        raise InstallError("Refusing a symlink install manifest")
    if not path.exists():
        return {"schema_version": 1, "skills": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("skills"), dict):
            raise ValueError("unsupported schema")
        for name, item in data["skills"].items():
            if not NAME.fullmatch(name) or not isinstance(item, dict):
                raise ValueError("invalid entry")
            if not isinstance(item.get("files"), dict):
                raise ValueError("invalid file map")
            if not all(isinstance(k, str) and isinstance(v, str) for k, v in item["files"].items()):
                raise ValueError("invalid hashes")
        return data
    except (ValueError, AttributeError, TypeError) as exc:
        raise InstallError("Invalid install manifest: %s" % exc) from exc


def install(repo, destination, selected=None, update=False, dry_run=False):
    repo = Path(repo).resolve()
    destination = Path(destination).expanduser().absolute()
    source_root = repo / "skills"
    if destination.is_symlink():
        raise InstallError("Choose a real destination directory, not a symlink")
    resolved_dest = destination.resolve()
    if resolved_dest == repo or resolved_dest == source_root or source_root in resolved_dest.parents:
        raise InstallError("Destination must be separate from the library source")
    if destination.exists() and not destination.is_dir():
        raise InstallError("Destination is not a directory")
    available = sorted(p.name for p in source_root.iterdir() if (p / "SKILL.md").is_file())
    chosen = list(dict.fromkeys(selected or available))
    if not chosen:
        raise InstallError("No skills found")
    for name in chosen:
        if not NAME.fullmatch(name) or name not in available:
            raise InstallError("Unknown skill: %s" % name)
    version = (repo / "VERSION").read_text(encoding="utf-8").strip()
    if dry_run:
        if (destination / LOCK).exists():
            raise InstallError("Destination is locked: %s" % (destination / LOCK))
        return install_selected(source_root, destination, chosen, version, update, True)
    destination.mkdir(parents=True, exist_ok=True)
    with destination_lock(destination):
        return install_selected(source_root, destination, chosen, version, update, False)


def install_selected(source_root, destination, chosen, version, update, dry_run):
    manifest_path = destination / MANIFEST
    manifest = read_manifest(manifest_path)
    plans = []
    for name in chosen:
        content = files_in(source_root / name)
        desired = hashes(content)
        target = destination / name
        previous = manifest["skills"].get(name)
        if target.is_symlink():
            raise InstallError("Refusing a symlink target: %s" % name)
        if target.exists():
            if previous is None:
                raise InstallError("Unmanaged skill already exists: %s; choose another destination" % name)
            current = hashes(files_in(target))
            if current != previous["files"]:
                changed = sorted(k for k in set(current) | set(previous["files"])
                                 if current.get(k) != previous["files"].get(k))
                raise InstallError("Local changes in %s: %s. Back up and reconcile them before updating."
                                   % (name, ", ".join(changed[:8])))
            if current == desired:
                action = "unchanged"
            elif update:
                action = "update"
            else:
                raise InstallError("New source for %s; rerun with --update" % name)
        elif previous is not None:
            raise InstallError("Managed skill was removed locally: %s; restore it or use a fresh destination" % name)
        else:
            action = "install"
        plans.append({"name": name, "action": action, "files": content, "hashes": desired,
                      "previous": previous["files"] if previous is not None else None})

    # Preflight every selection before making any change. Dry runs create nothing.
    result = [{"skill": p["name"], "action": p["action"]} for p in plans]
    if dry_run or all(p["action"] == "unchanged" for p in plans):
        return result
    destination.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".ad-game-install-", dir=str(destination)))
    swaps = []
    preserve_staging = False
    try:
        for plan in plans:
            if plan["action"] == "unchanged":
                continue
            candidate = staging / (plan["name"] + "-new")
            candidate.mkdir()
            for name, data in plan["files"].items():
                file_path = candidate / name
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_bytes(data)
            target = destination / plan["name"]
            backup = staging / (plan["name"] + "-old")
            if target.is_symlink():
                raise InstallError("Target became a symlink during install: %s" % target)
            if plan["action"] == "update":
                if not target.exists():
                    raise InstallError("Target was removed during install: %s" % target)
                target.rename(backup)
            elif target.exists():
                raise InstallError("Target appeared during install: %s" % target)
            swap = {"target": target, "backup": backup, "installed": False, "plan": plan}
            swaps.append(swap)
            if backup.exists() and hashes(files_in(backup)) != plan["previous"]:
                raise InstallError("Local changes during install: %s; restoring the changed copy" % target)
            candidate.rename(target)
            swap["installed"] = True
            manifest["skills"][plan["name"]] = {"version": version, "files": plan["hashes"]}
        staged_manifest = staging / "manifest.json"
        staged_manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        for swap in swaps:
            if swap["backup"].exists() and hashes(files_in(swap["backup"])) != swap["plan"]["previous"]:
                raise InstallError("Local changes during install: %s" % swap["target"])
            if hashes(files_in(swap["target"])) != swap["plan"]["hashes"]:
                raise InstallError("Installed files changed before commit: %s" % swap["target"])
        os.replace(str(staged_manifest), str(manifest_path))
    except BaseException as exc:
        failures = []
        for swap in reversed(swaps):
            target, backup = swap["target"], swap["backup"]
            try:
                if target.exists() or target.is_symlink():
                    if not swap["installed"] or hashes(files_in(target)) != swap["plan"]["hashes"]:
                        raise InstallError("Refusing to remove a concurrently changed target: %s" % target)
                    shutil.rmtree(target)
                if backup.exists():
                    backup.rename(target)
            except (OSError, InstallError) as restore_error:
                failures.append("%s: %s" % (target.name, restore_error))
        if failures:
            preserve_staging = True
            raise InstallError("Install failed (%s); rollback incomplete. Recover original files from %s. "
                               "Restoration errors: %s" % (exc, staging, "; ".join(failures))) from exc
        raise
    finally:
        if not preserve_staging:
            shutil.rmtree(staging)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, required=True, help="Explicit AI client skill directory")
    parser.add_argument("--skill", action="append", help="Install one skill; repeat to select several (default: all)")
    parser.add_argument("--update", action="store_true", help="Update clean copies managed by this installer")
    parser.add_argument("--dry-run", action="store_true", help="Check and report changes without writing")
    args = parser.parse_args()
    try:
        result = install(Path(__file__).resolve().parents[1], args.dest, args.skill, args.update, args.dry_run)
    except (InstallError, OSError) as exc:
        print("Install error: %s" % exc, file=sys.stderr)
        return 1
    for item in result:
        print("%s%s: %s" % ("would " if args.dry_run else "", item["action"], item["skill"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
