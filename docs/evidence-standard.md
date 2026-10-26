# Evidence standard

The library is evidence-informed guidance plus tested local tools. It is not a
promise that following a checklist maximises engagement or revenue. Use the
smallest reliable change that addresses the observed problem and test outcomes
in the actual game.

## Record two separate dimensions

| Basis for a claim | Appropriate use | Limit |
|---|---|---|
| Current official requirement or API documentation | Implement the stated platform contract within its scope | Does not establish player preference or commercial uplift |
| Primary empirical research | Explain a plausible mechanism or test choice | Preserve method, population, setting and metric; do not assume transfer |
| Platform/expert design guidance | Starting design constraints and heuristics | Guidance is not a causal experiment in this game |
| Local source, test, simulation or player data | Diagnose a concrete project | Scope to revision, device, population, time and measurement coverage |
| Original design proposal | Make a change or test reviewable | No observed result yet |

Separately label validation: **proposed**, **source-inspected**, **source-tested**,
**simulated**, or **measured live**. Describe moderated player studies as observed
research with their actual setting. For a controlled experiment, record the
assignment, unit, comparison, outcome window and analysis limitations. These
labels are not an automatic ladder of certainty: biased live data can be less
useful than a precise source test for a particular engineering question.

## Do not overstate engagement

Define the desired outcome: understandable choices, enjoyable interaction,
mastery, voluntary replay or return. Separate active gameplay from menus, ads,
loading and idle time. Longer time can reflect confusion; notification opens can
reflect pressure; higher ad revenue can coexist with worse cohort contribution.

“Dopamine hit” is not an observed metric here. Translate the intent into a
satisfying earned success, visible consequence and attainable next goal. Test
recognition, learning and enjoyment. Do not claim a reward schedule manipulates
brain chemistry or has an optimal universal timing.

Primary tutorial research found differing results across games of varying
complexity; it does not justify removing all instructions. The library's
[instruction research note](../skills/game-ux-writing-and-instructions/references/research.md)
preserves this context. Motivation theory provides test rationales, with limits
documented in the [UI evidence note](../skills/game-ui-and-navigation/references/evidence.md).

No universal D1/D7 target, eCPM, ad interval, notification frequency or tutorial
word count is prescribed. Explicit synthetic values illustrate a calculation
or lifecycle; they are not industry benchmarks. Strong claims require stronger
evidence than an attractive mockup or a single before/after aggregate.

## Evidence card for a design decision

```text
Claim and decision:
Source URL, publication date and verification date:
Basis / validation label:
Method, population, platform, genre and outcome:
What the source actually supports:
Limits, competing explanations and missing evidence:
Applicability to this project and original hypothesis:
Artifact/revision and intended change:
Measure, guardrails, comparison and observation window:
Observed result or explicitly pending:
Next decision and review date:
```

Use original explanations and link sources. Do not copy papers, proprietary
screens, assets, private telemetry or SDK documentation into the library. Keep
source-specific summaries brief and distinguish a quoted rule from our
interpretation. Generated examples need provenance, a text equivalent and a
clear proposal label. Neither a generated image nor source-tested code proves
human engagement.

## Updating evidence

Check current primary documentation before implementing mutable policy or SDK
facts; record exact version/platform/market. If sources conflict, identify which
one owns the specific rule and disclose uncertainty. A dated source is not
automatically current. Update the affected scenario and validation record when
guidance changes. Record negative or inconclusive results rather than quietly
replacing them with a success story.
