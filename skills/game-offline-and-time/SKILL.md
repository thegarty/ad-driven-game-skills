---
name: game-offline-and-time
description: Design or implement idle earnings, offline progression, daily resets, boost expiry and mobile pause/resume clocks. Use when time changes, repeated launches or restored saves could miscalculate progress or repeat claims.
license: MIT
---

# Game offline progression and time

Define the player's time promise before calculating rewards. Offline production,
research completion, daily availability and active-play boosts have different
clocks; a single elapsed-time variable cannot implement them honestly.

## Establish clock and authority

Inspect existing timestamps, saved checkpoints, timer owners, background/resume
behavior, backend time and configured earning rules. Use the
[time-policy template](assets/time-policy.md) to specify each feature's clock,
pause behavior, authority, cap, expiry and reset semantics.

Read [clock and claim recipes](references/clocks-and-claims.md). Use monotonic
elapsed time for in-process durations; it does not supply a persisted wall-clock
history across a restart. Treat device UTC/calendar time as potentially changed.
If server time is used, document freshness, offset and behavior when unavailable.
Do not describe a local checksum or monotonic timer as anti-cheat protection.

## Freeze the earning rule

Decide explicitly which rate/configuration applies during absence, which interval
is eligible, whether boosts expire while absent, which seconds a cap retains,
and how fractional currency is rounded or carried. A newly purchased upgrade or
new remote configuration must not retroactively change a sealed claim without
an explicit product policy.

Separate an offer to collect from the already-earned base. If a rewarded video
multiplies an offline claim, persist the base claim once and bind the extra grant
to its immutable identity. Ad failure must not erase the base or cause replay to
award it again. Describe what happens if the optional offer expires or another
device settles the same interval.

## Settle atomically

Calculate a candidate from an authoritative checkpoint and a rule snapshot.
Commit the currency delta, interval/claim receipt and next checkpoint together.
On failure, keep the prior state and retry the same transaction, not a new claim.
A restored wallet without its claim ledger can recreate already-settled time.
Choose a complete-state recovery policy and a cloud-conflict policy if multiple
devices can earn or spend offline.

The [offline helper](references/offline-helper.md) and
[synthetic fixture](assets/offline-example.json) model capped intervals, expiring
boosts and exclusion of already-settled time. Run
`python3 scripts/offline_accrual.py assets/offline-example.json` from this skill
directory. It proposes a settlement; it never reads a real save, commits a reward,
verifies a clock or connects to a backend.

## Verify adversarial timing and ordinary returns

Test same-instant reopen, repeated settlement, overlapping prior intervals,
negative elapsed time, long absence, cap boundaries, boost expiry, timezone/DST
changes, app suspension, save failure and backup restore. Test exact fractional
arithmetic and the game's final rounding contract. Calendar streak/reset tests
need the chosen timezone rules separately from elapsed-time tests.

Return the time policy, implementation/model, player-visible result and evidence.
Do not claim that a simulation predicts human return behavior or provides secure
server reconciliation. Keep normal play usable when a time source is uncertain.
