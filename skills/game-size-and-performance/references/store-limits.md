# Store limits and what is being measured

Official sources checked **2026-10-26**. Recheck before release; limits and
delivery programs change. This table covers ordinary mobile apps, not App Clips,
watchOS, TV or PC distribution. Preserve the units used by the providers; do not
silently reinterpret MB/GB as MiB/GiB in a build script.

| Platform/component | Published limit | Measurement scope |
|---|---|---|
| iOS/iPadOS app, iOS 9+ deployment target | 4 GB | Uncompressed app size |
| iOS/iPadOS Mach-O executable, same target | 500 MB | Total `__TEXT` sections in each executable, not the ZIP/IPA size |
| Google Play base module | 500 MB | Compressed download as calculated by Play Console |
| Google Play individual feature module | 500 MB | Same compressed-download basis |
| Google Play individual asset pack | 1.5 GB | Same compressed-download basis |
| Google Play modules plus install-time asset packs | 4 GB combined | Compressed download |
| Google Play on-demand/fast-follow asset packs | 30 GB combined | Compressed download |
| Google Play total app plus those packs | 34 GB | Total compressed download ceiling |
| Legacy Google Play APK publishing | 100 MB | Legacy APK limit; do not apply bundle limits |

Sources: [Apple maximum build file sizes](https://developer.apple.com/help/app-store-connect/reference/app-uploads/maximum-build-file-sizes)
and [Google Play's dedicated size-limit guide](https://support.google.com/googleplay/android-developer/answer/9859372?hl=en).
Google also lists a maximum of 100 asset packs and a non-blocking mobile-data
notice above 200 MB. These are distinct from the current base-module limit.

**Documentation discrepancy:** the general
[Android app-size optimisation article](https://developer.android.com/topic/performance/reduce-apk-size)
still states 200 MB for bundle downloads at this check. Prefer the dedicated
Play Console limits above for limit lookup, then confirm the candidate's actual
validation in the current Console. Do not copy an older 200 MB rule into a
universal hard gate or assume a large local AAB proves rejection.

## Android measurement

An AAB is an upload container covering multiple device configurations. Its file
size and a universal APK are not a user's variant download. Generate a local APK
set with the installed [bundletool](https://developer.android.com/tools/bundletool),
then use its documented `get-size total --apks=game.apks` command. Use device
specifications/dimensions for representative configurations. This is an estimate;
the Play Console uses a similar, not identical, calculation. Keep optional pack
delivery modes visible in the report.

Use APK Analyzer/dependency reports to attribute native libraries, DEX/resources
and assets. Preserve every promised supported architecture; use delivery splits
instead of removing compatibility blindly. Measure installed storage after first
play and optional downloads separately from the APK set.

## Apple measurement

Use Xcode's **App Thinning Size Report.txt** for variant estimates and App Store
Connect's processed build sizes for the uploaded candidate. Apple distinguishes
compressed download from uncompressed installation size. App thinning and store
processing mean the uploaded IPA alone is insufficient. Follow
[Apple's app-size workflow](https://developer.apple.com/documentation/Xcode/reducing-your-app-s-size).
Measure caches and downloaded content separately on devices.

Background Assets can host content separately from a build; adopting it is an
architecture/product decision, not an excuse to hide a mandatory second download.
Verify current program requirements, storage behavior and OS support before use.
Initial-play and fully-downloaded budgets must remain explicit.
