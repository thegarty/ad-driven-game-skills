# Native diagnostics for a Godot mobile build

Official sources checked **2026-10-26**. Discover the actual Godot/native plugin APIs and pinned SDKs; Firebase has native platform SDKs, not a universal built-in Godot crash API.

## Build correlation contract

Keep a private release manifest: source revision, export/build number, signing/distribution channel, artifact hash, engine version, native/plugin/adapter versions, architecture, configuration schema and symbols location. Record the effective remote configuration revision separately because the same binary may behave differently after a configuration change.

Store build artifacts and matching symbols with access control and retention. Do not inflate the player download by shipping developer archives merely to make diagnostics work. A freshly rebuilt binary from the same source can have different symbols/build IDs; retain those belonging to the distributed artifact.

## Failure-to-evidence map

| Symptom | First useful evidence | Common interpretation error |
|---|---|---|
| Native fatal crash | Symbolicated stack, exception/signal, threads, exact binary | Blaming the SDK named in the top frame without reproduction |
| Android ANR | Main/worker thread traces, lock/I/O work, foreground state | Calling a hang a crash or counting only crash SDK events |
| Apple memory termination | Jetsam/system memory report, memory pressure, device class | Expecting every OS termination to have a crash stack |
| Godot gameplay error | Sanitized state transition and script failure | Assuming all engine errors become native fatal reports |
| Lost reward/save | Immutable grant/save revision and persistence outcome | Treating a successful animation or ad close as committed state |

Android ANRs can result from blocked UI work and other lifecycle timeouts; inspect the relevant traces and move/limit the actual expensive operation. Do not hardcode a single universal timeout as an ANR detector. [Android ANR diagnosis](https://developer.android.com/topic/performance/issues/anr).

Apple crash, device-console and jetsam reports contain different evidence. Symbolication requires the distributed build's symbols; jetsam describes memory conditions without providing the same executing-thread stack data as a crash report. [Apple crash and device logs](https://developer.apple.com/documentation/xcode/diagnosing-issues-using-crash-reports-and-device-logs).

## Firebase adapter exercise

1. Inspect native dependencies and startup wiring. For Android with native engine libraries, determine whether Java/Kotlin reporting alone covers the failure; evaluate the documented [Crashlytics NDK setup](https://firebase.google.com/docs/crashlytics/android/get-started-ndk) and symbol upload for the actual native libraries. Do not assume a plugin captures GDScript failures automatically.
2. For Apple, configure and verify matching dSYM upload using the [Crashlytics symbol guide](https://firebase.google.com/docs/crashlytics/ios/get-deobfuscated-reports). Missing symbols can make grouping appear functional while leaving stacks unusable.
3. Attach a bounded set of diagnostic fields: build, feature/config revision, screen/state enum, last operation type and redacted error category. Use a bounded breadcrumb buffer. No ad tokens, receipts, access tokens, email, full device IDs or raw save payloads. Check collection behavior against the app's audience, permissions and disclosures. [Crashlytics custom reports and collection controls](https://firebase.google.com/docs/crashlytics/customize-crash-reports).
4. On a nonproduction packaged build, trigger a controlled test crash through the installed native integration, restart if reporting requires it, and verify the report, build, stack readability and redaction. Separately exercise a handled script failure and a controlled reward/save interruption. Mark unsupported telemetry paths explicitly.
5. Confirm release optimization does not break the bridge, callbacks or symbols pipeline. Verify offline buffering/reporting behavior without claiming that every offline failure will arrive.

## Rates and missingness

Define “crash-free players,” “crash-free sessions” and “user-perceived ANR rate” by the source's actual denominators. A store report and a consent-limited analytics export can measure different populations. Report affected counts, denominator, build age, coverage and ingestion delay. If diagnostics stop when startup fails, lower reporting volume can itself be an incident signal.

For performance, pair error counts with launch success, time to interactive, frame-time distribution, memory high-water mark and battery/thermal observations on stated hardware. Adding diagnostics has cost: bound log size, upload volume and SDK footprint and remove data without a decision use.
