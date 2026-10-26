# Artifact inventory and budget helper

Python 3.9+, standard library only. Use a frozen, comparable release artifact.
From this skill directory:

```sh
python3 scripts/artifact_size.py /path/to/game.aab > baseline-size.json
python3 scripts/artifact_size.py /path/to/new-game.aab \
  --baseline baseline-size.json --max-bytes 90000000 --max-growth-bytes 3000000
```

The numerical budgets above are **synthetic examples**, not recommendations or
store limits. Choose your game's actual budget and use integer bytes. Keep the
baseline report separate from the output file to avoid shell redirection
truncating an input before the script runs.

## Contract

- Positional `artifact`: regular file or directory. AAB, APK, IPA, APKS and ZIP
  extensions must contain a readable ZIP directory. PCK/other files are opaque.
- `--top`: largest entries to show, between 1 and 1,000; defaults to 10.
- `--max-bytes`: maximum local container file size, or sum of regular file sizes
  for a directory. It does not validate Apple/Google limits.
- `--baseline`: prior version-1 JSON report from this tool. Its artifact kind
  and measurement must match. Caller verifies platform/variant/content comparability.
- `--max-growth-bytes`: nonnegative permitted growth; requires `--baseline`.
  A baseline without this flag reports growth without imposing a growth gate.
  Negative measured growth is a reduction and passes.

JSON goes to stdout. Exit code **0** means inspection completed and configured
budgets passed (or none were configured); **1** means a budget was exceeded;
**2** means invalid input/read failure. An unconfigured budget is labelled
`not_configured`, never presented as passing a size goal.

Reports include the container/directory measure, largest entries, extension totals,
duplicate ZIP names and applicable budget results. ZIP entry sizes come from
metadata without extracting files. Sum of entry-compressed bytes excludes ZIP
headers and is distinct from actual container length. Directory sizes are logical
file lengths, not allocated blocks. Symlinks are rejected to avoid silently
counting external content. Nested PCKs/APKs/archives remain opaque; use engine or
platform tools for deeper attribution. CRC/integrity, store thinning, installed
caches, peak memory and runtime cost are not measured.
Reported growth is the difference in local artifact sizes, not the transferred
size of an app-store update or binary patch.

Attach the report to the size ledger, then use bundletool/App Store Connect and
physical-device measurements for the other footprint categories. The helper
does not delete, recompress or rewrite anything.
