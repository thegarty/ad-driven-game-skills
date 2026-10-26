#!/usr/bin/env python3
"""Inspect local artifact bytes and enforce explicit budgets; never extract archives."""

import argparse
from collections import Counter
import json
from pathlib import Path
import zipfile


def nonnegative_integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("%s must be a nonnegative integer number of bytes" % name)
    return value


def inspect(path, top=10, max_bytes=None, baseline=None, max_growth_bytes=None):
    path = Path(path)
    if isinstance(top, bool) or not isinstance(top, int) or not 1 <= top <= 1000:
        raise ValueError("top must be an integer from 1 to 1000")
    if max_bytes is not None:
        nonnegative_integer(max_bytes, "max_bytes")
    if max_growth_bytes is not None:
        nonnegative_integer(max_growth_bytes, "max_growth_bytes")
        if baseline is None:
            raise ValueError("max_growth_bytes requires a baseline report")
    if path.is_symlink():
        raise ValueError("artifact path must not be a symlink")
    if not path.exists():
        raise ValueError("artifact does not exist")
    entries = []
    duplicate_names = []
    if path.is_dir():
        kind = "directory"
        measurement = "directory_file_bytes"
        for file in sorted(path.rglob("*")):
            if file.is_symlink():
                raise ValueError("directory contains symlink: %s" % file.relative_to(path))
            if file.is_file():
                entries.append({"path": file.relative_to(path).as_posix(), "bytes": file.stat().st_size})
            elif not file.is_dir():
                raise ValueError("directory contains a non-regular entry")
        measured = sum(item["bytes"] for item in entries)
        unpacked = measured
        compressed_entries = None
    elif path.is_file():
        measurement = "container_file_bytes"
        measured = path.stat().st_size
        if zipfile.is_zipfile(path):
            kind = "zip_archive"
            with zipfile.ZipFile(path) as archive:
                for item in archive.infolist():
                    if item.is_dir():
                        continue
                    entries.append({"path": item.filename, "bytes": item.file_size,
                                    "compressed_bytes": item.compress_size})
            names = Counter(item["path"] for item in entries)
            duplicate_names = sorted(name for name, count in names.items() if count > 1)
            unpacked = sum(item["bytes"] for item in entries)
            compressed_entries = sum(item["compressed_bytes"] for item in entries)
        else:
            if path.suffix.lower() in {".zip", ".aab", ".apk", ".ipa", ".apks"}:
                raise ValueError("expected a valid ZIP-based artifact for this extension")
            kind = "opaque_file"
            unpacked = None
            compressed_entries = None
    else:
        raise ValueError("artifact must be a regular file or directory")
    growth = None
    if baseline is not None:
        if not isinstance(baseline, dict) or type(baseline.get("schema_version")) is not int or baseline.get("schema_version") != 1:
            raise ValueError("baseline must be a version 1 artifact report")
        if baseline.get("measurement") != measurement or baseline.get("artifact_kind") != kind:
            raise ValueError("baseline and candidate must use the same artifact kind and measurement")
        previous = nonnegative_integer(baseline.get("measured_bytes"), "baseline measured_bytes")
        growth = measured - previous
    checks = []
    if max_bytes is not None:
        checks.append({"name": "absolute_bytes", "limit_bytes": max_bytes,
                       "observed_bytes": measured, "passed": measured <= max_bytes})
    if max_growth_bytes is not None:
        checks.append({"name": "growth_bytes", "limit_bytes": max_growth_bytes,
                       "observed_bytes": growth, "passed": growth <= max_growth_bytes})
    extensions = {}
    for item in entries:
        extension = Path(item["path"]).suffix.lower() or "[no extension]"
        extensions[extension] = extensions.get(extension, 0) + item["bytes"]
    return {"schema_version": 1, "evidence_type": "local_artifact_inventory",
            "artifact_name": path.name, "artifact_kind": kind,
            "measurement": measurement, "measured_bytes": measured,
            "entry_count": len(entries), "entry_uncompressed_bytes": unpacked,
            "entry_compressed_bytes": compressed_entries,
            "largest_entries": sorted(entries, key=lambda item: (-item["bytes"], item["path"]))[:top],
            "uncompressed_bytes_by_extension": dict(sorted(extensions.items())),
            "duplicate_archive_entry_names": duplicate_names,
            "growth_bytes": growth, "budget_checks": checks,
            "budget_status": "not_configured" if not checks else
                ("passed" if all(check["passed"] for check in checks) else "exceeded"),
            "limitations": ["Local bytes and ZIP metadata are not store-calculated per-device download sizes.",
                            "Archive entries are not decompressed or integrity-checked; nested packs remain opaque.",
                            "File sizes do not measure disk allocation, installed caches or runtime CPU/GPU memory.",
                            "The caller must supply comparable builds and project-specific budgets; no store limits are hard-coded."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--max-bytes", type=int, help="local container bytes, or summed directory file bytes")
    parser.add_argument("--baseline", type=Path, help="previous JSON report from this tool")
    parser.add_argument("--max-growth-bytes", type=int, help="maximum absolute growth versus baseline")
    args = parser.parse_args()
    try:
        baseline = json.loads(args.baseline.read_text(encoding="utf-8")) if args.baseline else None
        result = inspect(args.artifact, args.top, args.max_bytes, baseline, args.max_growth_bytes)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 1 if result["budget_status"] == "exceeded" else 0
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        parser.exit(2, "error: %s\n" % exc)


if __name__ == "__main__":
    raise SystemExit(main())
