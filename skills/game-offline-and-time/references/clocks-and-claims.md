# Clock semantics and durable claims

| Feature | Clock decision | Typical mistake |
|---|---|---|
| Combat / active-play boost | Simulation or monotonic foreground duration | Advancing combat while the app is suspended |
| Research / absolute offer expiry | Defined absolute time authority | Resetting the deadline on every launch |
| Offline production | Trusted or explicitly limited wall-time interval | Multiplying the current rate over an unbounded absence |
| Daily availability | Named timezone/calendar and reset policy | Treating every 24 hours as a calendar day |
| Returning-session cooldown | Explicit active or wall duration | Changing clock semantics between UI and save code |

## Mobile time sources

Godot's monotonic tick methods are suitable for elapsed timing in the running
process; device system-clock methods can be changed. Calendar conversions do not
magically handle every timezone/DST policy. Verify the chosen engine APIs and
use a capable timezone source/library where the product needs named-zone rules.
Never persist a tick value and compare it to an unrelated process's tick origin.

For server-assisted time, define which response is trusted, offset/freshness,
network latency treatment and fallback. A timeout is not evidence of cheating.
For a device-clock-only game, define bounded, player-friendly uncertainty
handling; do not silently confiscate progress based on a backward clock jump.

## Worked capped interval

Synthetic rule: earn 0.25 units/second, retain the first 600 seconds after the
checkpoint, and apply a 2× boost only during the first 100 seconds. A 1,000-second
absence yields `100 × 0.5 + 500 × 0.25 = 175` units. The other 400 seconds are
discarded by this explicit cap policy. Advance the checkpoint through the full
absence, or those discarded seconds could be collected in another launch.

Choosing the most recent 600 seconds instead would be a different product rule
and could yield a different boost result. Do not change between the two when
the player reopens the same sealed claim.

## Durable settlement

Persist the rate, relevant boosts/config version and intended recipient when
the earning interval begins or when the architecture establishes its authoritative
snapshot. A claim describes that snapshot and interval. The candidate reward is
not confirmed until balance, claim marker and advanced checkpoint commit as one
coherent state. Replaying a pending claim should confirm the existing commit or
complete it once. Rewarded-ad bonuses use an additional identity linked to the
base claim, not a second execution of the base calculation.

Calendar availability needs an equally explicit period ID. Decide whether a
timezone change can change the current period and how travel is treated. Schedule
notifications from known state and cancel/reschedule obsolete reminders; an OS
notification arriving does not itself establish that a reward is available.

## Sources and limits

Verified **2026-10-26**:

- [Godot Time](https://docs.godotengine.org/en/stable/classes/class_time.html): system-clock versus monotonic tick semantics and calendar conversion limitations.
- [Godot mobile pause/quit handling](https://docs.godotengine.org/en/stable/tutorials/inputs/handling_quit_requests.html): checkpoint before possible background termination, without assuming a final quit callback.

The earning, cap, conflict and rounding rules above are product contracts to
choose and test. The helper does not implement platform lifecycle or calendar
reset logic and cannot prove wall-clock honesty.
