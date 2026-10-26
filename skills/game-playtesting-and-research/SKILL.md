---
name: game-playtesting-and-research
description: Plan, conduct or analyse mobile-game playtests and player research to resolve design, comprehension, engagement and accessibility questions. Use for human observation and evidence synthesis rather than telemetry implementation or paid acquisition.
license: MIT
---

# Game playtesting and research

Turn a design uncertainty into an observable player task and a bounded decision.
Distinguish what people do, what they say, and what the researcher infers. A
developer who knows every rule is not a substitute for an unfamiliar player.

## Choose the question and method

Inspect the build, brief, existing feedback and available telemetry first. Define
the decision this study will change: understanding a mechanic, finding a menu,
choosing a strategy, wanting another run, tolerating an interruption, or returning
later. A broad request to prove the game is engaging needs several questions.

Use [study recipes and worked cases](references/study-recipes.md) to choose
moderated observation, unmoderated tasks, a diary/return study, an interview or
an instrumented comparison. Pick the least expensive method that can answer
the question. A survey about willingness to return does not measure retention;
an event log does not explain why a player misunderstood a rule.

## Make the session interpretable

Complete [the study plan](assets/study-plan.md). Specify the audience, recruitment
criteria, build and save state, device/input conditions, research tasks,
observation window, assistance rules, consent/recording choices and decision
criteria. Participants' relevant experience matters: genre experts, novices,
returning players and players with access needs can encounter different barriers.
Do not infer a population effect from a convenience sample or a fixed small
number of testers. Recruitment or contacting players is an external action;
only do it within the user's authorisation.

Use realistic goals instead of instructions that reveal the interface. Say
“prepare for a tougher wave” rather than “tap Research and buy armour.” Begin
without coaching. Log assistance precisely; do not count an assisted completion
as an unaided one. Let participants stop, skip questions and decline recording.
Follow the project's consent/privacy process, including any requirements for
research involving children; do not invent legal clearance.

## Observe meaningful engagement

Record decision quality, understanding of consequences, useful strategy changes,
voluntary next-run choice and ability to identify an attainable next goal. Keep
active play, menus, waiting, advertising and background time separate. A long
session caused by confusion or inability to exit is not stronger engagement.

Use [the observation log](assets/observation-log.csv) with anonymous study IDs.
Write observable actions first, participant explanation second, hypothesis third.
Do not collect identifying or sensitive details merely to make richer notes.
Store recordings separately with access and deletion rules from the study plan.

## Synthesize into a decision

Group findings by underlying obstacle, not by which participant mentioned them.
Preserve contradictory observations and successful paths. Rank a finding by
impact on the target task, persistence/recoverability, observed reach and evidence
strength; do not multiply invented scores into false precision.

For each proposed change, provide the observed problem, competing explanation,
smallest useful change and a check that could disprove the hypothesis. Report
sample composition, attrition, coaching, excluded sessions and exposure limits.
Distinguish source inspection, recorded playtest behavior, simulation and live
cohort measurement. Validate the revised journey with fresh or appropriately
counterbalanced participants; familiarity can hide a remaining onboarding issue.

Deliver the study materials and findings, or execute the authorised study stage.
Do not label a prototype preference, test completion or attractive screen as a
measured retention or revenue improvement.
