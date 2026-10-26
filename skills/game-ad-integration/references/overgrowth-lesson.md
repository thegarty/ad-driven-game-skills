# Overgrowth: recoverable opportunities and trustworthy rewards

Sanitised learning from the 2026-10-25 review and subsequent source inspection on 2026-10-26. No source code or private runtime values are reproduced.

- **Source-tested snapshot:** explicit retries recovered eligible offers after transient initialization/load failures. Retry and Watch remained separate player actions.
- **Source-inspected:** immutable opportunity identity and persistent acknowledgement were necessary to handle callbacks after UI changes and failed saves.
- **Source-inspected:** privacy state evolved separately from gameplay saves; stale load callbacks had to be invalidated without erasing earned rewards.
- **Source-inspected:** native bridge type/initialization behaviour required platform-specific verification.

The reviewed test snapshot did not prove later native builds, production ad playback, retention or revenue uplift. Preserve this distinction when using these cases as acceptance scenarios. Do not transplant timeout constants, age rules or consent-mapping code from one game into another.
