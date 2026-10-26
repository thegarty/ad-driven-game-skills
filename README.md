# Ad-Driven Game Skills

Practical skills for AI agents building mobile games that people want to return
to—and that can earn sustainable advertising revenue.

**16 focused skills · Android and iOS · Godot/AdMob/Firebase recipes · MIT**

Use the library to design a new game, improve an existing one, implement reliable
ads, or decide what to test next. It covers gameplay, progression, retention,
creative production, monetisation, measurement, acquisition and release. Optional
purchases and ad-removal entitlements are included. A dedicated size and
performance skill covers store limits, compression, asset/SDK bloat and release
size budgets.

The core guidance is engine-independent. Godot is the first detailed integration
path; native recipes describe contracts and verification steps, not a bundled
production SDK plugin. The library does not include a complete game starter kit.

## Install

You need Git and Python 3.9 or newer. Runtime helpers and the installer use only
the Python standard library. Clone the repository, inspect the contents, and
install copies into your AI client's skill directory:

```sh
git clone https://github.com/thegarty/ad-driven-game-skills.git
cd ad-driven-game-skills
git checkout v0.1.0
python3 scripts/install.py --dest "$HOME/.codex/skills" --dry-run
python3 scripts/install.py --dest "$HOME/.codex/skills"
```

On Windows, use `py -3` instead of `python3` and an explicit destination path.

| Client | User-level destination | Project-level destination |
|---|---|---|
| Codex | `~/.codex/skills` | `<game-project>/.agents/skills` |
| Claude Code | `~/.claude/skills` | `<game-project>/.claude/skills` |
| Cursor | `~/.cursor/skills` | `<game-project>/.cursor/skills` |

Use an actual path with `--dest`; the installer expands `~`. Start a new agent
session after installation. For remote/cloud agents, install into the project
workspace available to that agent; local user directories do not automatically
travel to a remote machine. See [compatibility and source checks](docs/compatibility.md).

Install only what you need by repeating `--skill`:

```sh
python3 scripts/install.py --dest "$HOME/.claude/skills" \
  --skill ad-game-director \
  --skill game-ad-integration \
  --skill game-analytics-and-experiments
```

Each specialist includes its own resources and licence. You can also manually
copy any folder under `skills/` into your client's skill directory. The installer
will not take over a manually copied or otherwise unmanaged folder.

### Update safely

Fetch and check out the release you want, inspect its changes, then rerun the
installer with the same destination and `--update`. To follow the development
branch instead of a pinned release:

```sh
git switch main
git pull --ff-only
python3 scripts/install.py --dest "$HOME/.codex/skills" --update --dry-run
python3 scripts/install.py --dest "$HOME/.codex/skills" --update
```

The installer records file hashes in `.ad-driven-game-skills-install.json` in the
destination. It refuses to overwrite local edits, added files, deleted managed
files or an unrelated skill. Back up and reconcile changes, or choose a fresh
destination. Keep the manifest with the installed copies; there is no force
overwrite option. Run one installation/update process per destination at a time.
The installer also locks the destination and checks for edits during replacement.
If an interrupted process leaves a lock, inspect its recorded process ID before
removing the lock directory. If rollback cannot complete, the error identifies a
recovery directory containing retained originals; preserve it while reconciling.

## Use it

Start with **`ad-game-director`** for a broad request or invoke a specialist for a
focused task. Codex supports `$skill-name`; Claude Code and Cursor support
`/skill-name`. You can also name the skill in natural language. Explicit names
help when your agent has many installed skills.

### Design a new game

> Use ad-game-director to design a portrait idle tower-defence game for Android
> and iOS. I have one developer and two weeks for a Godot prototype. Prioritise
> an enjoyable free loop and optional rewarded ads. Produce a game brief,
> bounded prototype plan, economy assumptions and the first playtest questions.

### Audit an existing game

> Use ad-game-director to review this repository and its available analytics.
> Trace the first session, losing-run recovery, progression and ad opportunities.
> Fix feasible issues within the task scope and rank remaining improvements by
> evidence and effort. Separate source-tested findings from live outcomes.

### Find the next revenue and retention improvements

> Use game-profitability-and-priorities with these cohort and ad reports. Identify
> the largest supported bottleneck, explain uncertainty, and propose one measured
> change with retention and reliability guardrails. State which missing data
> could change the recommendation.

### Fix rewarded ads

> Use game-ad-integration to inspect our Godot/native adapter. Handle no-fill,
> consent changes, late and duplicate callbacks, save failure and restart.
> Show the earned-to-durable-grant contract and test it without real ad traffic.

Give the agent access to your game repository and relevant reports. The
[project-context template](skills/ad-game-director/assets/project-context.md)
helps carry decisions across sessions. Unknown values should stay unknown;
synthetic examples are not benchmarks for your game.

## What's inside

- [Skill catalogue](CATALOG.md): all 16 skills and their concrete deliverables.
- Each skill's `SKILL.md`: task selection and essential workflow.
- `references/`: focused recipes, evidence boundaries and dated official sources.
- `assets/`: project, game, economy, ad-placement, measurement and release templates.
- `scripts/` inside selected skills: economy, cohort and revenue/CPI calculators.
- The size skill's artifact inventory helper: largest shipped files, explicit
  byte budgets and comparison with a previous build.
- [Behavioral evaluations](evals/scenarios.json) and [validation record](docs/validation.md).

The calculators read supplied JSON/CSV and print results locally. Run each with
`--help`; its skill links to an input specification and synthetic fixture.
They do not call ad networks, send telemetry or recommend spend automatically.

Try the bundled synthetic examples from the repository root:

```sh
python3 skills/game-progression-and-economy/scripts/economy_scenario.py \
  skills/game-progression-and-economy/assets/economy-example.json
python3 skills/game-analytics-and-experiments/scripts/cohort_retention.py \
  --installs skills/game-analytics-and-experiments/assets/installs-example.csv \
  --activity skills/game-analytics-and-experiments/assets/activity-example.csv \
  --as-of 2026-01-08 --days 1 7 \
  --population 'Synthetic example install roster' --timezone UTC
python3 skills/game-profitability-and-priorities/scripts/revenue_sensitivity.py \
  skills/game-profitability-and-priorities/assets/revenue-example.json
```

## Evidence and maintenance

[Overgrowth lessons](skills/ad-game-director/references/overgrowth-lessons.md)
inform the library's recovery, progression and measurement guidance. They are
sanitised summaries of inspected source, recorded tests and simulations, with
explicit limits. They do not claim measured retention or revenue uplift.

SDK and policy sources have verification dates. Re-check current official
documentation for the selected version, audience and markets before shipping.
Design hypotheses need playtesting; economic assumptions need real cohorts.

To validate a checkout:

```sh
python3 scripts/validate_library.py
python3 -m unittest discover -s tests -v
python3 evals/harnesses/ad_reward_model.py -v
```

See [contributing](CONTRIBUTING.md) for source, evaluation and release conventions.
Original library content and code are [MIT licensed](LICENSE); linked third-party
documentation retains its own terms. No proprietary Overgrowth source or assets
are included.
