# Offline settlement model

Python 3.9+, standard library only. From the skill directory:

```sh
python3 scripts/offline_accrual.py assets/offline-example.json
```

The [script](../scripts/offline_accrual.py) prints JSON, exits 0 on valid input,
and emits an error with exit 2 on invalid input. The
[fixture](../assets/offline-example.json) is synthetic and earns exactly `175`
units under its stated assumptions.

## Input contract

All keys are required; unknown keys are rejected:

- `schema_version`: integer `1`.
- `timeline_id`, `currency`, `rule_version`: nonempty strings, at most 500 characters.
  A timeline identifies one earning stream within an account/save; currency is
  part of claim identity. Use a new stream identity for genuinely independent
  earnings, not to bypass a prior settlement or change reward rules.
- `checkpoint_unix_s`, `resume_unix_s`, `cap_seconds`: integers from 0 to 10^12.
  Times are UTC epoch seconds already prepared by the caller; no clock is read.
- `base_rate_per_second`: nonnegative plain decimal **string**, at most 64
  characters. Use `"0.25"`, not a floating-point number or scientific notation.
- `boosters`: at most 1,000 nonoverlapping half-open intervals, each with integer
  `start_unix_s`, `end_unix_s` and decimal-string `multiplier` at least `"1"`.
  Overlapping boosters are rejected rather than inventing a stacking rule.
- `settled_intervals`: at most 1,000 half-open intervals with `start_unix_s` and
  `end_unix_s`, all from this timeline and currency. Overlap/duplicates are counted as union
  coverage, not paid twice. These records are trusted caller input.
- `assumptions`: nonempty list of nonempty strings, each at most 500 characters.

## Calculation and settlement

The model retains the first `cap_seconds` after the checkpoint, splits that
window at booster/settled boundaries, excludes already-settled time and sums
`seconds × snapshotted rate × applicable boost`. Decimal arithmetic preserves
fractional amounts; `earned_units` is a decimal string. The model does not round
to a currency's unit or decide whether fractional balances are acceptable.

The returned settlement covers the **full** checkpoint-to-resume interval,
including discarded cap time. Its deterministic claim ID depends on timeline,
currency and interval, not a mutable reward amount. A caller must freeze the rule and
earned amount, then atomically commit the wallet delta, interval marker and
proposed checkpoint. A changed rule cannot redefine an already-sealed claim.

To replay a committed result, retain its full interval in `settled_intervals`
or use its advanced checkpoint. The result then has no payable time. The tool
does not perform that commit; retrying with an unchanged pre-commit input returns
the same candidate and must not be mistaken for another grant.

A replay returning zero new payable units does not rewrite the original stored
claim's earned amount to zero. Keep the original settlement immutable; the zero
describes this calculation's additional delta. The caller must serialize
overlapping claims against its current state revision. Running this read-only
calculator twice concurrently does not reserve or lock an interval.

Backward time returns `clock_rollback`, zero reward and an unchanged checkpoint;
no interval is settled. Equal times return `no_elapsed_time`. A zero cap or fully
covered eligible interval returns `no_unsettled_eligible_time` while proposing
settlement/checkpoint advancement for any positive absence. This prevents the
discarded tail being reclaimed under this specific policy.

This is one deterministic rule, not a general offline engine, secure clock,
calendar/DST implementation or multi-device economy authority. The game still
needs versioned state, atomic persistence and a conflict policy. A restored save
that loses its settlement ledger can repeat time; the helper cannot detect that
missing history.
