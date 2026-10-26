# Incident response and recovery evidence

This is an original operational workflow. Project-specific severity thresholds, permissions and response times must be declared, not inferred from the synthetic examples.

## First response

Assign one incident owner, note onset and preserve the exact current settings/artifact references. Establish impact bounds using provider reports, diagnostics and support cases; avoid adding these sources as if they were disjoint populations. Separate known affected users from potentially exposed users and unknown reporting gaps.

| Situation | Candidate containment | Evidence needed before calling it effective |
|---|---|---|
| New ad adapter crashes on resume | Disable implicated placement/provider through an already implemented safe path; pause rollout if authorized | Affected clients receive the effective config; no residual loaded ad is shown; representative resume succeeds |
| Save migration corrupts progress | Halt new migration/rollout; preserve recoverable copies and evidence | Existing affected saves recover without overwriting the last valid copy |
| Duplicate grant callbacks inflate currency | Close the repeated claim path; retain transaction ledger | Replayed callbacks cannot mint new value; legitimate pending grants can still finish |
| Bad remote content blocks startup | Serve known-good compatible content or fall back locally | Cold launch works offline and with both old/new clients |

A remote switch only helps builds that contain and reach its implementation. A startup crash before configuration fetch may require a new binary. Store release reversal and availability differ; consult the current store workflow instead of promising instant binary rollback. Content/database rollback must account for newer save schemas and irreversible player actions.

## Investigation discipline

Construct a timeline of binary release, config/content changes, SDK/provider changes and first affected event. Test candidate causes against affected and unaffected cohorts with the same device/OS/build conditions. A matching timeline supports a hypothesis; it does not prove causality.

Preserve a minimal reproduction with expected state, observed state and interruption point. Prefer a synthetic save and test transaction. If real private evidence is required, store it privately with access/retention controls and use redacted references in reports.

Validate mitigation in a safe environment and on the actual affected path. Record both successful and failed attempts. If the failure cannot be reproduced, use narrower instrumentation and staged mitigation with explicit uncertainty rather than inventing a root cause.

## Close only what is proven

- **Source-inspected:** the intended fix exists at a revision.
- **Source-tested:** relevant automated checks exercised it; list what they cannot observe.
- **Packaged-device tested:** exact artifact, install route, hardware/OS and steps passed.
- **Measured live:** stated build/config cohort and reporting window meet declared recovery criteria with adequate coverage.

A patch can pass all local checks while old builds continue failing. Track adoption and residual exposure; publish “mitigated” or “repair distributed, recovery pending” where that is the evidence. A postmortem records the trigger, contributing conditions, detection delay, customer recovery, preventable recurrence and one owned follow-up per unresolved risk. Do not equate lack of new support tickets with confirmed recovery.

## Synthetic worked case

A release shows eight crash reports around ad close. There were 80 reporting players on the new build and 4,000 on the old build; the reporting windows differ. The count alone cannot establish a regression rate. Inspect exact build/config, reporting coverage and stacks, reproduce background→close on the affected device class, then disable the implicated path if authorized. Prove the effective switch reaches that build and the repaired artifact passes the reproduction. Live impact remains unmeasured until comparable populations and complete windows exist.
