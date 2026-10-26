# Official sources and implementation boundaries

Checked **2026-10-26**. Verify the selected SDK/platform versions again before implementing their exact interfaces. The skill's transaction and failure contracts are original guidance; these references do not certify a particular game.

- [Firebase App Check](https://firebase.google.com/docs/app-check): app/device attestation complements Firebase Authentication and prevents some, not all, abuse. Check supported products/providers and enforcement coverage.
- [Firebase App Check with App Attest](https://firebase.google.com/docs/app-check/ios/app-attest-provider): Apple-platform provider setup and integration. This is Firebase's provider guide; inspect Apple's current native documentation when implementing a direct native bridge.
- [Play Integrity overview](https://developer.android.com/google/play/integrity/overview): combine signals, verify request context, use proportionate enforcement and plan for errors/outages. A successful verdict is not a game transaction or user-authorization decision.
- [Firebase Security Rules basics](https://firebase.google.com/docs/rules/basics): product-specific access rules and authenticated content ownership. Owner-only storage is not sufficient for a server-authoritative game balance.
- [Cloud Firestore rules conditions](https://firebase.google.com/docs/firestore/security/rules-conditions): authentication/access conditions and the separate server-library/IAM boundary.
- [Firebase rules unit testing](https://firebase.google.com/docs/rules/unit-tests): emulator-based validation of access rules. Use an isolated project and test both permitted and rejected requests.
- [OWASP MASVS](https://mas.owasp.org/MASVS/): a maintained mobile-security verification framework covering storage, authentication, network, platform, code, resilience and privacy. Select applicable controls for deeper review; referencing it does not constitute assessment or certification.

No production attestation, Firebase rules deployment, credential audit or device test was performed by these documentation checks. Provider quotas, support and interfaces can change; no universal threshold or permanent device-compatibility guarantee is supplied here.
