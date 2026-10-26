# When to ask, what to say and when to stop

This is original design guidance. The worked journeys are **synthetic**, not measured engagement results. Native constraints are separately documented in [platform rules](native-rules.md).

## Decision table

| Ask | Useful moment and benefit | Appropriate action/decline | Recurrence and suppression |
|---|---|---|---|
| Optional rewarded ad | Player can see a relevant, available reward at a natural choice point | State reward and watching requirement; ordinary continue route remains | Re-check eligibility/value/availability; no forced popup loop after decline |
| Purchase | Player intentionally inspects a permanent benefit or shop; promise matches actual entitlement | Store price and exact benefit/limits; close/back works | Do not reopen after every loss; suppress owned products and unresolved purchases |
| Review | Enough neutral experience at a quiet transition | Native request or optional store link; no reward or rating filter | Respect system suppression and own burden budget; no fallback nag |
| Feedback | Context-specific, short research question after the relevant task | Optional answer/skip; state purpose without directing rating | Separate from review eligibility; do not repeatedly survey the same friction |
| Save/sign-in | Player chooses cloud backup, cross-device progress or a feature requiring identity | Explain what will sync and account conflict; guest route where supported | Avoid universal first-launch gate; do not promise backup before successful sync |
| Notifications | Player chooses a specific useful reminder | Explain what/when, then the appropriate native permission flow | Denial leaves the timer/game usable; do not reopen the OS request at every return |
| Camera/photos/microphone | Player invokes a feature that actually needs that resource | Specific purpose and native choice; narrower alternatives when available | Re-check current permission; preserve nondependent play after denial |
| Ad privacy/ATT | Before the relevant data operation under applicable requirements | Accurate disclosure/native or provider flow; genuine choice | SDK/provider and OS status govern timing; no tracking before required authorization |

This table does not override platform-specific UI constraints. In particular an Apple explanatory pre-alert must follow Apple's design rules; do not blindly add “Allow/No thanks” to a fake system prompt. Optional game offers and native permission explanations are different surfaces.

## A useful request contract

Write one plain sentence answering “what happens if I choose this?” Prefer “Watch an ad to claim 50 wood” when that is the actual reward over “Boost now!” Show the non-ad action just as clearly. For a reminder, identify the chosen event; “Remind me when this upgrade finishes” is more useful than a vague demand to enable all notifications. These are original copy examples, not evidence of conversion lift.

Give decline semantics meaning. “Not now” can defer only to a newly relevant context under a declared cooldown. “Don't ask again” must suppress that app invitation until the player changes the setting. A system denial follows the platform rules. Re-entering a scene, returning after an ad or retrying a network call must not erase decline history.

Do not make failure itself an automatic purchase trigger. First show earned progress, explain the loss and provide an attainable next action. Useful strategy guidance can be more appropriate than an offer. Do not hide the ordinary reward behind a double-reward button or claim an optional reward was already earned before its conditions are met.

## One coordinator, not competing timers

Each subsystem submits a candidate with reason, priority, scope, relevant screen, expiry and required states. On a safe transition the coordinator:

1. Rejects ineligible, stale, already-resolved and suppressed candidates.
2. Respects a modal lock across app, ad, store and OS UI. Defers or expires candidates if the player leaves the context.
3. Prioritizes the action the player requested and required recovery/disclosure. Optional marketing cannot outrank an unresolved purchase or save conflict. A required privacy step must still precede the operation it governs even when the optional budget is exhausted.
4. Applies a project-specific burden budget covering interruptive offers across systems, minimum quiet intervals and per-purpose recurrence. Record any intentional chain, such as player-selected reminder→system permission, as one coherent interaction with its actual UI count. No universal “one prompt every N minutes” is assumed.
5. Re-checks state just before display, records the attempt, and releases the lock on success, cancellation, error or background/restart recovery. Persist enough history to prevent relaunch spam without storing unnecessary personal data.

Reserve budget before showing to prevent two simultaneous callbacks both passing eligibility. A deferred offer is not a debt the player must eventually pay. Add an expiry/context generation so stale end-of-run offers disappear when a new run begins.

## Worked first-session journey

The player opens a synthetic idle-defense game. Required privacy setup is completed before any governed SDK operation; optional sign-in and notifications do not block the first playable action. The player learns one defense interaction and earns an upgrade. Show its result without automatically layering a shop, review card and notification request.

Later the player intentionally chooses a timer reminder. Explain that particular reminder and invoke the current native permission flow where eligible. If denied, keep the upgrade/timer usable. A rewarded offer on the results screen stays available as an explicit choice, subject to the overall interruption budget. These steps are a design hypothesis, not a mandated order or proven retention recipe.

## Worked return journey

The player returns with completed production, a failed cloud-sync retry, and several newly eligible marketing requests. First recover/present the saved progress and explain any unresolved sync problem. Do not show all queued asks. After the player chooses the next action, a relevant optional offer may remain in context; expired requests are discarded. A previously declined notification invitation does not return simply because another session started.

## Evaluate the experience

Measure request eligibility, app invitation shown, request attempted, known platform result, completed benefit and return/abandonment. Do not claim an OS dialog was shown unless the API provides that evidence; do not infer a review was submitted. Compare the full assigned population when testing timing: analyzing only accepters selects for willingness. Review comprehension, accidental taps, dismiss accessibility, prompt conflicts and complaints alongside commercial outcomes.
