# Economy reasoning and simulation limits

## Useful measures

- **Affordability:** balance plus valid income minus explicit spending, evaluated at the actual decision time. Keep different currencies separate.
- **Reward earning-time equivalent:** reward amount divided by ordinary earning rate for the same stage and currency. If the rate is zero or unstable, report that the equivalent is undefined or scenario-dependent.
- **Marginal upgrade value:** the change in a meaningful outcome at the next legal upgrade, compared with cost and competing choices. Raw stat gain alone may miss targeting, survival or puzzle constraints.
- **Gate delay:** active play, waiting and calendar delay reported separately. Parallel timers do not necessarily add to a sequential wait.
- **Resource pressure:** sources and sinks over a defined progression window. A large balance may be intentional saving; it is not automatically inflation.

These are diagnostic calculations. Their usefulness depends on accurate rules and player behaviour assumptions.

## Scenario ledger

For each run record starting save, configuration revision, strategy, seed, active time, elapsed wall time, input cadence, ad assumptions, legal caps and stopping rule. Include background time and menu time when relevant to real-time entitlements. Mark a forced simulation timeout as censoring; it is not a natural player failure or a game-imposed cap.

Test baseline and candidate against the same starting states. Change one mechanism at a time when trying to explain a difference. Keep corrected runs and discarded fixtures distinguishable so an invalid early test cannot enter the accepted average.

## Overgrowth case: information before balance

**Evidence: simulated and source-tested; review date 2026-10-25.** A synthetic one-dimensional upgrade strategy stalled while a strategy using complementary defensive upgrades progressed. The implemented response offered contextual guidance and navigation. It did not change enemy strength, grant resources or buy an upgrade. This supports testing strategy discovery as a possible cause of a stall. It does not prove that advice changed real-player retention.

## Overgrowth case: stage-relative rewards

**Evidence: simulated; review date 2026-10-25.** The review compared optional daily rewards with ordinary long-run earnings and found that their relative value varied materially by progression stage. It proposed measuring stage-specific reward presentation/value rather than selecting a new amount from a single average. The reusable lesson is to evaluate what an offer enables at the time it is shown; no specific multiplier or daily cap is carried into this library.

## Overgrowth case: clocks and stopping rules

**Evidence: source-inspected and simulated; review date 2026-10-25.** Different temporary benefits used wall time and active-play time. A simulation also imposed an artificial run retirement that differed from a natural end. Correcting those assumptions changed the interpretation of progression and optional-video value. Assumed successful videos in a synthetic scenario cannot estimate ads per real user.

Provenance: original summaries of the owner-provided Overgrowth progression/revenue and economy reviews. Private numeric results, source code, account identifiers and player telemetry are not distributed.
