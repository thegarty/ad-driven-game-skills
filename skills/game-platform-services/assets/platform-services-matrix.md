# Platform services integration matrix

- Player benefit and selected feature scope:
- Engine/plugin/native SDK, minimum/target OS and inspected source date:
- App/build/signing/configuration identity references (keep private values private):
- Native profile / game account / store billing / save ownership model:
- Linking, guest transition, account switch and unavailable-play behavior:
- Marginal download/installed size, startup/memory and maintenance costs:

| Feature | Apple capability/binding | Google capability/binding | Minimum OS/program/config prerequisites | Fallback | Verified evidence and limitation |
|---|---|---|---|---|---|
| Authentication/profile | | | | | |
| Leaderboard UI/submission | | | | | |
| Achievements | | | | | |
| Challenges/quests | | | | | |
| Platform reward delivery | | | | | |

## Score and achievement contracts

- Score units/direction/range/rules version/completed-run proof:
- Assistance/paid-boost and comparable-mode rules:
- Season/reset/cutoff/late-submission policy:
- Validation authority, abuse response and uncertainty:
- Achievement progress intent, repeat cycle and native mapping:
- Durable outbox identity/account binding and provider replay semantics:
- Game reward grant identity separate from native display/reporting:
- Retry/rate-limit/ambiguous-result and two-device policy:

## Packaged verification

| Scenario | Expected result | Actual result | Exact artifact/device/account environment | Evidence level |
|---|---|---|---|---|
| Authentication unavailable/declined | | | | |
| Offline run and reconnect | | | | |
| Duplicate/ambiguous callback | | | | |
| Profile/account switch | | | | |
| Season rollover/late run | | | | |
| Invalid/implausible score | | | | |
| Native UI close/background | | | | |
| Native reward delivered once | | | | |
| Service config published and live readback | | | | |

Separate source inspection, local native configuration, sandbox/tester behavior, distributed binary and live service visibility. None automatically proves retention uplift.
