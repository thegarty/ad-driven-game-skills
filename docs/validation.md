# v0.2.0 validation

Validated on **26 October 2026**, using Python 3.9.6 on macOS. This record covers
the library, local helpers and documented evaluation tasks. The
[v0.1.0 validation record](validation-v0.1.0.md) is preserved separately.

| Check | Observed result |
|---|---|
| Bundled skill-creator metadata validator | All 33 skills passed in an isolated environment with PyYAML 6.0.3 |
| Library validator | Required names, metadata, standalone references, catalogue, root/docs/evaluation links, profiles, Python syntax and JSON passed |
| Repository unit suite | 125 tests passed, including experiment readout, offline settlement, contrast and profile selection/protection |
| Ad design model | 15 fake-provider/SQLite tests passed; original scope retained |
| Independent offline oracle | 15 additional temporary test methods passed after the precision fix, including 200 seeded Fraction comparisons and invalid-input subcases |
| Behavioral evaluations | Four independent reviewers answered fourteen expanded scenarios; outcomes and fixes in the [evaluation record](../evals/results/v0.2.0.md) |
| Installation | Full copy, all six profiles, dry runs and clean updates exercised in temporary destinations; every installed skill's resources and MIT copy checked |
| Installed helpers | Economy, cohort, revenue, offline, experiment and contrast helpers ran from copied skill folders against synthetic inputs |
| Codex discovery | CLI 0.146.0 loaded the two named UI/writing skills, linked research/visual/evidence/contrast references and image provenance from a temporary `.agents/skills` installation |
| Claude Code / Cursor | Documentation-checked compatibility; executables unavailable for smoke testing |
| Visual example | Original generated storyboard inspected for readable labels and teaching sequence; prompt, text equivalent and proposal status included |
| Public-content review | Original prose, synthetic examples and licensed notices; no private machine paths, provider IDs, credentials or unfinished scaffold markers found in the text scan |

## What the tests establish

The new experiment helper keeps all assigned units, rejects duplicate/conflicting
assignment and withholds the primary comparison for missing/immature outcomes.
Known means, zero/empty cases, reproducibility, small samples and invalid values
are covered. Its bootstrap interval does not validate the experiment design,
correct optional stopping or automatically select a winner.

Offline tests cover caps, boost expiry, interval union, replay, rollback, exact
decimal totals, claim namespace, missing fields and CLI errors. The helper
returns a proposed settlement; actual persistence, clock authority and cloud
reconciliation remain application responsibilities. Independent review found an
extreme valid-input precision defect, now fixed with a rational regression.

Contrast tests cover known ratios, symmetry, threshold boundaries without
rounding and invalid inputs. This is a colour-pair calculation, not a native
accessibility certificate. Profile tests cover selection unions, malformed or
duplicate definitions, no-write dry runs and local-change preservation. Existing
installer rollback/locking, calculator and artifact-inventory checks remain.

## Client smoke details

The smoke prompt named skills without file paths. The successful Codex execution
read both installed entrypoints, selected linked references and the visual's
provenance; its answer correctly explained evidence limits and contrast CLI exit
codes. It did not generate a new image, modify a game or browse.

The first attempt using the machine's configured model failed because that model
required a newer CLI. Repeating with `--ignore-user-config` and the CLI's own
defaults succeeded. No persistent user settings were changed. This establishes
one explicit discovery/resource flow in that configuration, not universal
automatic routing or compatibility with every model/client version.

## Reproduce

```sh
python3 scripts/validate_library.py
python3 -m unittest discover -s tests -v
python3 evals/harnesses/ad_reward_model.py -v
python3 scripts/install.py --list-profiles
python3 scripts/install.py --dest /your/temporary/skills --profile design-ui --dry-run
```

Use a fresh real temporary destination for installation tests. The GitHub
workflow repeats validation, unit/model checks and isolated full/profile installs
on Python 3.9 and 3.13 with Ubuntu 24.04. GitHub Actions records the outcome for
each commit; local results above are recorded separately.

## Limits

No native Godot plugin, physical-device game, store upload, live ad/purchase,
notification campaign, Game Center/Play Games account or player outcome was
validated. Source-grounded integration recipes require those checks in the
actual project. The generated image is a concept, not a working screen or proof
of learning. Neither the library nor its tests establish retention, revenue,
notification-frequency or neurochemical effects.

Store ceilings, platform capabilities and SDK requirements can change. Their
references include check dates and require verification for the selected version,
audience and markets. Overgrowth lessons remain sanitised source/test/simulation
examples without a claimed live uplift.
