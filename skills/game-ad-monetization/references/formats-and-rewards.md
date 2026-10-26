# Formats and reward decisions

Use the game journey to choose formats. This is a design framework, not a provider approval or a list of universal caps.

| Format | Useful opportunity | Main tradeoff | Design requirement |
|---|---|---|---|
| Voluntary rewarded | A clearly valued revive, bonus, temporary convenience or optional resource offer | Can undermine challenge or make ordinary progress feel deliberately poor | State action and reward before acceptance; retain a meaningful decline route |
| Interstitial | A natural end of a level, completed run or transition | Short-term revenue can reduce repeat play | Evaluate actual break frequency, first-session experience, abandonment and accidental taps |
| Banner | A stable noninteractive region with sufficient space | Screen cost, readability, accidental taps and modest yield | Keep away from controls; measure layout and performance impact on real devices |
| Rewarded interstitial | A separately designed transition offer supported by the selected provider | Different consent/intro requirements from voluntary rewarded ads | Verify current format-specific rules; do not silently substitute for a Watch button |
| App-open | A loading/resumption experience appropriate to the product | Return friction and interruption of resumed play | Treat as an explicit experiment; verify provider guidance and resume behaviour |

AdMob's ordinary rewarded format calls for an affirmative opt-in and accurate reward disclosure. Its reward rules restrict direct monetary and transferable rewards. Use permitted in-game benefits and verify the specific proposal against [the current policy](https://support.google.com/admob/answer/7313578). An ad click or app installation is not a substitute for the provider's earned-reward event.

For interstitials, select a transition where player input has settled; do not allow a delayed load to present after the next level has started. Google's [interstitial guidance](https://support.google.com/admob/answer/6066980) ties placements to natural content transitions. Derive caps from the product, then test; no universal seconds-per-ad number is supplied here.

## Reward value worksheet

For each stage, compute:

- **Ordinary earning time:** reward amount divided by typical currency earned per active minute. Record the representative cohort or simulation assumptions.
- **Useful outcome:** what the reward makes affordable now, including any upgrade or capacity prerequisites.
- **Issuance pressure:** maximum legal rewards per day multiplied by their value, compared with other sources and sinks.
- **Competitive value:** whether another placement dominates the same need. Two offers with equal coins can have different timing value.
- **Challenge impact:** whether the offer removes a meaningful choice, accelerates it, or merely bypasses inconvenience introduced to sell the offer.

For example, an entirely synthetic game might offer 40 seeds when a relevant upgrade costs 160. If ordinary earning is 8 seeds per minute, the offer represents five active minutes. At a later stage earning 160 seeds per minute, the same offer represents 15 seconds. This arithmetic motivates a hypothesis; it does not identify the optimal reward.

Model revive chains and compounded bonuses explicitly. Specify whether reward multipliers stack, whether a base reward is already banked, and whether caps attach to a run, real-world date or rolling duration. Select a clock and time-zone policy before implementation.

Keep ad unavailability separate from deliberate scarcity. A loading failure should not confiscate an earned base reward or corrupt progression. A retry prepares a valid offer; it does not create an additional entitlement.
