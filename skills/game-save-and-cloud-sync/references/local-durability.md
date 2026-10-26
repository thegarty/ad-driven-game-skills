# Local durability and schema migration

## Coherent write protocol

Define the invariant before choosing files or a database. A snapshot can contain
the wallet, inventory, applied-claim IDs, pending settlements and offline
checkpoint as one versioned state. A database can commit the equivalent rows in
one transaction. Separate successful writes are not the same atomic operation.

For snapshot storage, validate a candidate in memory, write a new temporary
version, check errors, and use the target platform's supported replacement and
flush/recovery semantics. Retain a compatible previous generation. Record the
new authoritative revision only once the write protocol succeeds. A rename is
not by itself proof of power-loss durability on every filesystem.

Maintain generation/checksum metadata for corruption diagnosis, not as proof
that a hostile client cannot edit its save. Avoid logging raw personal data
when diagnosing a rejected candidate.

## Load and migrate

1. Discover bounded candidate generations without modifying them.
2. Parse and validate structural fields, schema version, IDs and domain rules.
3. If migration is needed, transform a copy through explicit version steps.
   Each step has before/after fixtures and must not duplicate rewards.
4. Validate the complete migrated candidate and compatibility of its claim and
   checkpoint ledger; only then write a new authoritative generation.
5. Keep prior valid data recoverable. If current and backup candidates fail,
   expose recovery/support options rather than silently replacing them with zero.

A downgrade may not understand a newer save. Preserve that state and report the
version mismatch instead of coercing it to an older schema. A rollout rollback
therefore needs save compatibility or a forward-fix path, not only an older app.

## Failure matrix

| Injected point | Required observable outcome |
|---|---|
| Candidate validation fails | Current save and backup unchanged |
| Temporary write fails | No success indication; earlier valid generation loads |
| Process ends before replacement | Earlier generation remains recoverable |
| Replacement succeeds, acknowledgement fails | Reopen recognizes committed revision/claim |
| Migration step fails | Original source preserved, no partial migrated state used |
| Wallet backup and claim ledger disagree | Reject incoherent restore; resolve together |
| New content ID missing | Explicit supported migration/fallback, not a crash or wrong item |

## First-party source

Verified **2026-10-26**: [Godot saving games](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html)
provides serialization/FileAccess building blocks. Its tutorial is not a complete
atomic migration, backup or cloud-conflict implementation. Verify filesystem
behavior in the exact export and device environment.
