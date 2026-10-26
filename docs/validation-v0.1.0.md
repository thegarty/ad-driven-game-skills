# v0.1.0 validation

Validated on **26 October 2026**, using Python 3.9.6 on macOS. This record covers
the skill library and its tools, not a built or released mobile game.

| Check | Observed result |
|---|---|
| Bundled skill-creator metadata validator | All 16 skill folders passed; run in an isolated environment with PyYAML 6.0.3 |
| Library package validator | Metadata, required coverage, standalone local references, catalogue, Python syntax and JSON checked |
| Unit suite | 74 tests passed across calculators, installer, packaging and artifact-size checker |
| Independent ad design model | 15 fake-provider/SQLite checks passed |
| Behavioral evaluations | Nine realistic scenarios assessed; actual outcomes and corrections in the [evaluation record](../evals/results/v0.1.0.md) |
| Installation | Dry run, selected copies, full installation and clean updates exercised in temporary destinations; originals in user skill folders were untouched |
| Installed helper use | Economy, cohort and revenue helpers executed against their synthetic fixtures from copied skill folders |
| Codex discovery | Codex CLI 0.146.0 discovered project-local installed skills and read the selected skill plus linked cohort reference |
| Claude Code and Cursor | Official installation/format documentation checked; no executable smoke test because their clients were unavailable |
| Public-content review | Original guidance/synthetic fixtures; scans found no private machine paths, ad publisher IDs, credentials or unfinished scaffold markers in public content |

The Codex smoke request supplied a skill name, without its file path. In a
temporary project it loaded `.agents/skills/game-analytics-and-experiments/SKILL.md`
and `references/cohort-helper.md`, correctly described the separate install and
activity inputs, and explained immature-cohort handling. This verifies one
explicit selection and supporting-resource flow; it is not proof of every
automatic-routing behavior across clients.

## Correctness checks

- Economy and revenue: known arithmetic, finite inputs, invalid/missing fields,
  reward caps, unaffordable spends, decimal affordability, exact break-even,
  real shortfalls, overflow and CLI errors.
- Cohorts: complete install denominator, duplicates, conflicting identities,
  exact-day definitions, weighted aggregate, date cutoffs, empty populations and
  immature cohorts represented as unavailable rather than zero.
- Installer: selective/complete copies, dry runs, idempotence, explicit clean
  updates, local additions/edits/deletions, unmanaged folders, symlinks, invalid
  manifests, locking, concurrent edits and failure recovery.
- Artifact inventory: local file/directory/ZIP measures, absolute/growth budgets,
  baseline compatibility, duplicate names, invalid archives, symlinks and CLI
  exit status. These are synthetic files, not store-produced app variants.
- Ad design model: bounded retries, stale callbacks, consent generations,
  explicit Watch intent, close/earn ordering, duplicate rewards, immutable claims
  and transactional recovery after injected exceptions/database reopen.

## Findings fixed before publication

Independent review reproduced an installer rollback failure that could delete
the remaining backup if restoration failed. The installer now preserves recovery
files, reports their location and attempts the remaining rollbacks. It also
locks destinations and rechecks moved/replacement content to detect edits during
an update.

Fractional binary floating-point values could reject an exactly affordable spend
or classify exact break-even as a tiny loss. Economy and revenue decisions now
use decimal arithmetic internally; output remains finite JSON numbers with the
documented representation limits. The reward recipe's already-applied branch
was clarified so it also acknowledges the pending receipt after confirming the
durable result. Regression tests and the independent model cover these changes.

## Reproduce

```sh
python3 scripts/validate_library.py
python3 -m unittest discover -s tests -v
python3 evals/harnesses/ad_reward_model.py -v
```

The GitHub workflow repeats the repository checks on Python 3.9 and 3.13 using
Ubuntu 24.04 and
exercises an isolated full install/update. Its commit-specific outcome is
available in GitHub Actions; this document records the local run separately.
The initial `ubuntu-latest` run selected Ubuntu 26.04, where the setup action
could not provide Python 3.9; Python 3.13's checks completed successfully. The
workflow now pins a runner with published builds for both supported versions.

## Limits

No native Godot SDK/plugin implementation, physical-device game, store upload,
real advertising, purchase or paid acquisition campaign was validated. The
recipes instruct those checks for the actual game. Current store size limits
were checked against official Apple and Google sources, but the artifact helper
does not certify store eligibility or measure store downloads, update transfers,
installed caches or device memory.

Overgrowth cases are sanitised source-review, test and simulation lessons.
Neither those cases nor the library evaluations establish retention or revenue
uplift. Client compatibility and policy/API details must be rechecked as clients,
SDKs and store requirements change.
