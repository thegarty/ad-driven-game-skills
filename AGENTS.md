# Working on this library

Write original, actionable guidance. Each `skills/<name>/` folder must work
when copied alone. Keep the entry point concise; link conditional detail from
`references/` and output templates from `assets/`. Use simple scalar YAML
frontmatter: `name`, `description`, `license: MIT`.

Do not invent platform APIs, universal retention targets or commercial results.
Check current official documentation for SDK/policy changes, record the check
date, and distinguish inspected source, tested behavior, simulations and live
measurement. Case studies must exclude credentials, private identifiers, raw
telemetry, proprietary assets and copied third-party instructions.

Scripts support Python 3.9+ using the standard library. Keep numeric assumptions,
populations, time horizons and units explicit. Never label projections as observed
results. Preserve installed local edits; do not add a force-overwrite installer.

Before publishing changes, run:

```sh
python3 scripts/validate_library.py
python3 -m unittest discover -s tests -v
```

Use the behavioral scenarios in `evals/scenarios.json` when changing decision
guidance. Record actual outcomes and limitations in `docs/validation.md`.
Update `CATALOG.md` when adding or renaming a skill. Keep an MIT licence copy in
each skill folder so selective installations preserve the licence notice.
