# First-play and recap review

## Observation matrix

| Moment | What the player must understand | Useful observation |
|---|---|---|
| First action | What can be touched and what it changes | Hesitation, wrong-target taps, time to meaningful action |
| First threat | What can fail and how to react | Can the player explain the cause of loss? |
| First upgrade | The tradeoff and its visible effect | Can the player predict a useful outcome? |
| First recap | What was earned, retained and unlocked | Can they identify progress and a sensible next goal? |
| First return | What changed while away and what can be done | Can they resume without rereading the entire tutorial? |

Counts require a defined population and collection method. Small observed sessions are useful for finding usability failures, not estimating population retention.

## Overgrowth case: strategy discovery

**Evidence: simulated and source-tested; review date 2026-10-25.** Synthetic strategies in a garden-defence game showed that a one-dimensional build could stall while a more balanced build progressed. A source change added contextual guidance and navigation after repeated early defeats without granting currency or purchasing the suggested upgrade. Local checks verified that behaviour. This does not establish how real novices learn or whether retention improved.

Reusable experiment: identify a likely missing decision, present concise advice at the relevant failure, and measure whether real players understand and try the alternative. Compare against current behaviour before altering enemy strength or adding free currency. The reviewed game's thresholds and upgrade names are intentionally omitted; each game needs its own trigger and explanation.

## Overgrowth case: honest progress and compact controls

**Evidence: source-tested with local native rendering/input; review date 2026-10-25.** Earned progress existed in a saved run but was not visible in the recap. Showing it made the recap more informative; longer content also required scrolling while retaining usable actions. Local synthetic touch checks found and verified the interaction. These checks were not physical-phone validation or a measured retention lift.

Acceptance scenarios for a new recap:

- A result that has no recorded progress does not invent any.
- Opening the recap twice cannot credit the reward twice.
- A failed save has a clear pending/retry state; a recovered save updates labels once.
- Scrolling details does not activate the control under the released finger.
- Home/restart remains reachable with long text, multiple notices and an unavailable offer.
- A recovered optional reward opportunity can load again only if still eligible; preparing it does not automatically display an ad.

Provenance: original summaries of the owner-provided Overgrowth progression/revenue and native-journey reviews. No private source, screenshots, identifiers or player telemetry are included.

## Layout reference

[Godot multiple resolutions](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html), verified **2026-10-26**, explains base resolution and scaling controls. Select layout behaviour for the project's orientation and devices; scaling alone does not validate safe areas, touch interactions or accessibility.
