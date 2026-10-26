# Overgrowth: provider state and game state are separate

Evidence: sanitised **2026-10-25 review**.

- **Measured live, historical:** different platform variants were at different store/readiness stages. One platform's readiness could not establish the other's serving state.
- **Source-tested snapshot:** local ad-recovery fixes did not automatically become part of previously exported or installed builds.
- **Measured live, limited:** an early provider sample showed some delivery but was too small to support retention, lifetime value or acquisition-budget conclusions.
- **Source-inspected:** analytics integration and physical-device verification had their own outstanding work.

Reusable rule: record source correctness, exported artifact identity, device test-ad playback, store availability, provider readiness and measured revenue as separate evidence. This case does not report current production status or a monetization uplift. It contains no provider identifiers or private telemetry.
