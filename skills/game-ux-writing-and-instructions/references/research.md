# What the research supports

Checked 2026-10-26. Sources below support bounded design reasoning. They do not
establish a universal word limit, a modern mobile retention uplift or a measured
neurochemical response. The examples elsewhere in this skill are original
proposals to test, not study results.

| Source and type | Finding relevant here | Transfer limit and practical use |
|---|---|---|
| Andersen et al., CHI 2012, [The Impact of Tutorials on Games of Varying Complexity](https://grail.cs.washington.edu/projects/game-abtesting/chi2012/chi2012.pdf); comparative experiment | Across eight tutorial designs and three games, with over 45,000 players, benefits depended on game complexity. The more complex game benefited in play time/progress; simpler games did not show the same benefit. | These games, users and metrics are not this mobile game's audience. Do not turn play-time findings into a claim of improved return retention. Test contextual teaching against safe discovery for the actual mechanic. |
| [Apple onboarding guidance](https://developer.apple.com/design/human-interface-guidelines/onboarding); platform design guidance | Recommends interactive learning, contextual tips and brief onboarding, with optional tutorials where appropriate. | Expert guidance, not a controlled test of this game. Build a short practice sequence and observe whether it teaches the required action. |
| [Apple alerts guidance](https://developer.apple.com/design/human-interface-guidelines/alerts); platform design guidance | Reserves interruption for essential actionable information and recommends direct, concise titles/messages. | Removing a modal must preserve important consequences and recovery. Prefer an inline status for a routine unavailable service. |
| Nielsen, 1997, [How Users Read on the Web](https://www.nngroup.com/articles/how-users-read-on-the-web/); original usability research summary | Users often scanned web pages; concise, scannable, objective writing improved the study's usability measures. | Old website tasks, not gameplay. Do not import its percentages as mobile engagement predictions or say players never read. Treat scannability as a testable starting point. |

## Evidence-to-test example

Observation: three unfamiliar players place towers outside the valid region
after dismissing a long help panel. This is qualitative evidence of a possible
instruction/layout mismatch, not a population failure rate.

Hypothesis: a visible legal pad, a ghost preview and “Place a tower” teach the
action more clearly than the panel. Show the path and range before placement;
provide a non-animated equivalent. Let players cancel. Test whether they can
place a second tower without the cue and explain why the position matters.

Compare with a short text-only cue if the illustration introduces ambiguity.
Hold mechanics, economy and reward timing constant when attributing a copy or
visual effect. Record novice/experienced mix, device, language, assistance and
the exact revision. A live experiment needs random assignment, adequate outcome
windows and guardrails; a small moderated session does not establish uplift.

For unfamiliar mechanics, offer progressive explanation: action first, the
reason after feedback, strategy on demand. For narrative/lore audiences,
optional longer reading may be part of enjoyment. Never remove required
transaction information to optimise a click-through metric.
