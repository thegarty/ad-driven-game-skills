# Official sources

Checked **2026-10-26**. Verify the exact selected SDK family, version and adapter at implementation time.

| Source | Use |
|---|---|
| [Google rewarded ads, Android](https://developers.google.com/admob/android/rewarded) | Load/presentation lifecycle, earned callbacks and test ads; follow the current platform selector for SDK family |
| [Google UMP, Android](https://developers.google.com/admob/android/privacy) | Consent update, forms and request eligibility |
| [Google UMP, iOS](https://developers.google.com/admob/ios/privacy) | iOS privacy flow and privacy options |
| [Godot Android plugins](https://docs.godotengine.org/en/stable/tutorials/platform/android/android_plugin.html) | Native plugin/export boundary |
| [Godot iOS plugins](https://docs.godotengine.org/en/stable/tutorials/platform/ios/ios_plugin.html) | iOS native plugin/export boundary |
| [Firebase ad revenue](https://firebase.google.com/docs/analytics/measure-ad-revenue) | Revenue event ownership |
| [Firebase collection configuration](https://firebase.google.com/docs/analytics/configure-data-collection) | Collection controls |

The local reward journal and atomic-grant contract are original application architecture recommendations, not a claim that AdMob supplies a persistent exactly-once local transaction service.
