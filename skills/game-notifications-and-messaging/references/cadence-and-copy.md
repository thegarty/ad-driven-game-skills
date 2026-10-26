# Trigger, copy and cadence design

The examples are **synthetic design hypotheses**, not tested campaign outcomes or
recommended universal timings. Start with relevance and player control; frequency
is a constraint on useful messages, not a target to fill.

## Match trigger to benefit

| Reason | Eligibility and useful moment | Example title / body | Suppress when |
|---|---|---|---|
| Player-started production completes | Task exists and result remains unclaimed | “Your seedlings are ready” / “Collect your harvest when you’re ready.” | Claimed, task cancelled, result expired or player already viewing it |
| Selected event opens | Player explicitly follows this event type and has access | “The forest challenge is open” / “Try this week’s new wave.” | Unsupported build, inaccessible content, event ended or already entered |
| Previously stated goal becomes attainable | Authoritative state confirms a useful unlock | “A new defence is available” / “Choose your next tower upgrade.” | Goal already completed or the claim depends on stale/private state |
| Return after inactivity | There is relevant new content or an unfinished opted-in task | “A new puzzle set is ready” / “Explore the new garden boards.” | No real new benefit, repeated nonresponse or the player opted out |

Do not claim “your base is under attack” if no attack occurs, “last chance” if the
reward does not expire, or “your friends need you” without real relevant activity.
Do not imply a base reward requires viewing an ad. Keep content useful without
sensitive lock-screen detail. A short title plus one concrete reason is a starting
hypothesis; validate truncation, locale expansion and comprehension rather than
imposing a universal character count.

## Worked schedule and collision policy

Illustrative policy for a fictional adult-audience gardening game: quiet hours
22:00–08:00 in the player's selected local timezone; at most one nonessential
message in any rolling 24 hours; a minimum 18-hour gap; no repeated reminder for
the same task generation. These are explicit prototype assumptions to review,
not established optima. The policy covers reminders and event/marketing contacts
from all integrated senders. A separate exception must have a real reason and
approval within the product policy, not a renamed category to evade the cap.

| Time/state | Candidate | Decision and reason |
|---|---|---|
| Monday 19:00, player starts a task | Harvest completes at 23:10 | If permitted/preferred, consider Tuesday 08:00; do not interrupt quiet hours |
| Completion state remains useful until Tuesday 18:00 | Deferred harvest reminder | 08:00 is before expiry, so it can remain a candidate |
| Tuesday 07:30, player returns and collects | Earlier reminder | Cancel it and release an unsubmitted reservation; the reason disappeared |
| Tuesday 11:00, followed event opens | Event reminder | Re-evaluate current state and global history; a cancelled unsubmitted reminder need not consume a send slot |
| Tuesday 12:00, a generic marketing job also runs | “Come back” message | Suppress if no unique benefit or if another accepted message consumes the cap; no independent campaign allowance |
| Service resumes after an outage, event is over | Queued event reminder | Expire it; do not send old requests to recover a campaign count |

If the harvest expires at 07:00 instead, suppress the original request rather
than postpone it beyond its usefulness. If the player changes timezone, recompute
the next permitted local window using the documented travel policy; do not add a
fixed number of seconds to simulate a calendar day across DST.

## Tune the policy with a holdout

Define “meaningful return” for the trigger: collecting a completed task plus
making a next gameplay choice, completing a challenge or starting a voluntary
run. Keep it distinct from an app foreground event, notification open or a brief
accidental visit. Choose a horizon long enough for that action and complete it
for all compared cohorts before reading the result.

Assign eligible players to a stable no-message holdout and a bounded treatment
policy. Record eligibility and the intended reason even when suppressed by a cap.
A holdout must not accidentally receive the same prompt from another channel.
Predefine the randomisation unit, repeat exposure, cohort maturity, missing-data
handling, stopping rules and precision needed to decide. Analyse assigned eligible
players rather than filtering to delivered/opened messages after assignment.

Test a useful trigger or a constrained cadence change with other behavior kept
stable where possible. More opens can coexist with worse later return or opt-outs.
Evaluate incremental useful actions, later retention, contact volume, permission/
category opt-outs and complaints, with revenue over a stated horizon if relevant.
Report uncertainty and unobservable permission/delivery states. An invalid push
registration alone does not establish why a person left or that they uninstalled.

If evidence is sparse, retain a conservative relevant policy and gather evidence;
do not optimise a frequency to a noisy best-looking point. Stop or reduce a policy
when fatigue guardrails are breached. An experiment's result applies to its
population, trigger, period and implementation, not every game.
