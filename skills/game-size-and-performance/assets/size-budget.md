# Release size budget

Choose values from the game's audience, download conditions, offline promise and
supported devices. Empty entries mean unmeasured, not zero or automatically safe.
Use raw bytes for automation; label human-facing MB (10^6) or MiB (2^20).

- Source revision, build/version and date:
- Engine/export template, SDK/plugin versions and release configuration:
- Platform, device variant, ABI/architecture, language and content selection:
- Initial-play/offline promise and optional-download policy:
- Previous comparable build and measurement method:

| Measure | Budget | Previous | Candidate | Delta | Evidence/tool |
|---|---|---|---|---|---|
| Local upload/archive bytes | | | | | |
| Store initial download per device | | | | | |
| Fully downloaded content | | | | | |
| Installed app plus assets | | | | | |
| Cache/save growth after representative play | | | | | |
| Peak process and GPU memory | | | | | |
| Cold start / content load time | | | | | |
| Frame-time/thermal guardrails | | | | | |

## Largest contributors and proposed changes

| Asset/dependency | Purpose | Bytes before/after | Change | Quality/runtime tradeoff | Owner |
|---|---|---|---|---|---|

## Acceptance evidence

Record store-limit source/date, actual processed-build result, clean install,
update, interrupted/optional download, cache eviction, offline play, dynamic
resources, audio loops, UI readability, localization, native services and target
device results. Capture comparable screenshots/listening notes where needed.

Any budget exception needs the measured increase, player benefit, owner and
follow-up decision. Do not raise a threshold silently to clear a failing check.
