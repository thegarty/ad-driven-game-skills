# Contributing

Contributions should improve a real agent decision or repeated workflow. Give a
new skill a distinct task boundary; prefer a focused reference over another
overlapping entry point. Keep each skill independently installable.

## Content

- Write original guidance. Link current official sources for technical and
  policy claims, with the date actually checked and any version/audience limits.
- Label evidence as source-inspected, source-tested, simulated or measured live.
  Explain populations, environments and limits; proposals remain hypotheses.
- Use synthetic fixtures. Do not submit private telemetry, provider identifiers,
  credentials, proprietary assets or someone else's unlicensed instructions.
- Keep assumptions and units explicit. An unknown metric is not zero. A
  simulation or a successful source test does not establish commercial uplift.
- Add useful templates/scripts only when they reduce repeated effort or improve
  correctness. Helpers use Python 3.9+ and the standard library.
- Follow the [evidence standard](docs/evidence-standard.md). Separate primary
  research from platform guidance and original hypotheses. Do not extrapolate
  engagement effects across genres, populations or outcome definitions.
- Keep visual examples original, captioned and labelled as proposals; preserve
  generation prompts/provenance and editable/localisable production text.
- Update catalogue, routing, profiles and coverage when introducing a distinct
  capability. Larger coverage must not force every game to ship every system.

## Verification

Run `python3 scripts/validate_library.py` and
`python3 -m unittest discover -s tests -v`. Add behavioral evaluation when changing
decision guidance. Give an independent agent the user scenario and skill files
without the expected answer; score the actual response against the rubric after
it finishes. Record failures and fixes, not only passing examples.

Use both [core scenarios](evals/scenarios.json) and the
[expanded scenarios](evals/expansion-scenarios.json) as appropriate; record exactly
which were run rather than treating historical results as new executions.

For packaging changes, check selective installation, local-edit detection,
relative references and client discovery in an isolated temporary project.
Document unavailable clients as documentation-checked, not smoke-tested.

## Releases

Update `VERSION` and the pinned example in `README.md` together. Validate the
final source, review public contents, then commit, tag and publish a release.
Preserve release validation notes in `docs/validation.md`; date new entries
instead of presenting old evidence as a new test. Do not run paid campaigns,
publish game releases or alter provider accounts as library validation.
