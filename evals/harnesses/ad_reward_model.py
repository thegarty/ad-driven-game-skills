#!/usr/bin/env python3
"""Original standalone Python 3.9+ ad lifecycle and reward design model.

This is not a Godot plugin or an ad SDK implementation. It performs no network
requests, uses no production identifiers, and provides no native/device or live
ad validation. All claim/run IDs, rewards and timing values are synthetic.

The fake provider's five-second timeout, three-attempt limit, and retry delays
are test inputs, not universal operating recommendations. Rewards are integer
units in a synthetic per-run balance. SQLite databases live in temporary
directories and are removed after each test.

Crash boundaries use injected exceptions and database close/reopen. These
tests do not exercise process termination, physical power loss, real disk
failure, backup migration, or an SDK's initialization and thread behavior.

The initial evaluation executed this model through Python standard input with
/tmp as its working directory; there was no previously saved harness file.
Run: python3 evals/harnesses/ad_reward_model.py -v
"""

import os
import sqlite3
import tempfile
import unittest


class SimulatedCrash(Exception):
    pass


class RewardStore:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS presentations (
                pid TEXT PRIMARY KEY, claim TEXT UNIQUE, run TEXT, reward INTEGER
            );
            CREATE TABLE IF NOT EXISTS receipts (
                claim TEXT PRIMARY KEY, run TEXT, reward INTEGER
            );
            CREATE TABLE IF NOT EXISTS balances (
                run TEXT PRIMARY KEY, amount INTEGER
            );
            CREATE TABLE IF NOT EXISTS applied (claim TEXT PRIMARY KEY);
            """
        )

    def present(self, pid, claim, run, reward):
        with self.db:
            self.db.execute(
                "INSERT INTO presentations VALUES (?,?,?,?)",
                (pid, claim, run, reward),
            )

    def receive(self, pid, fail=False):
        row = self.db.execute(
            "SELECT claim,run,reward FROM presentations WHERE pid=?", (pid,)
        ).fetchone()
        if row is None:
            return False
        if fail:
            raise OSError("injected receipt-write failure")
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO receipts VALUES (?,?,?)", row)
        return True

    def settle(self, claim, fail=False, crash_after_commit=False):
        row = self.db.execute(
            "SELECT run,reward FROM receipts WHERE claim=?", (claim,)
        ).fetchone()
        if row is None:
            return
        run, reward = row
        with self.db:
            if not self.db.execute(
                "SELECT 1 FROM applied WHERE claim=?", (claim,)
            ).fetchone():
                self.db.execute(
                    "INSERT OR IGNORE INTO balances VALUES (?,0)", (run,)
                )
                self.db.execute(
                    "UPDATE balances SET amount=amount+? WHERE run=?",
                    (reward, run),
                )
                if fail:
                    raise OSError("injected grant transaction failure")
                self.db.execute("INSERT INTO applied VALUES (?)", (claim,))
        if crash_after_commit:
            raise SimulatedCrash()
        # This also runs when the durable claim was already applied.
        with self.db:
            self.db.execute("DELETE FROM receipts WHERE claim=?", (claim,))

    def recover(self):
        for (claim,) in self.db.execute("SELECT claim FROM receipts").fetchall():
            self.settle(claim)

    def balance(self, run="run-A"):
        row = self.db.execute(
            "SELECT amount FROM balances WHERE run=?", (run,)
        ).fetchone()
        return 0 if row is None else row[0]

    def pending(self):
        return self.db.execute("SELECT count(*) FROM receipts").fetchone()[0]

    def close(self):
        self.db.close()


class FakeProvider:
    def __init__(self):
        self.loads = []
        self.shows = []

    def load(self, token):
        self.loads.append(token)

    def show(self, pid):
        self.shows.append(pid)


class Broker:
    # App-owned simulation methods; these are not Godot/AdMob APIs.
    def __init__(self, store):
        self.store = store
        self.provider = FakeProvider()
        self.now = 0
        self.privacy = True
        self.valid = True
        self.foreground = True
        self.state = "unavailable"
        self.generation = 0
        self.token = None
        self.attempts = 0
        self.retry_at = 0
        self.deadline = None
        self.fullscreen = None
        self.claim = "claim-A"
        self.run = "run-A"
        self.reward = 7

    def prepare(self):
        if (
            not self.privacy
            or not self.valid
            or self.fullscreen
            or self.token
            or self.state == "ready"
        ):
            return False
        if self.attempts >= 3 or self.now < self.retry_at:
            return False
        self.attempts += 1
        self.generation += 1
        self.token = self.generation
        self.state = "loading"
        self.deadline = self.now + 5
        self.provider.load(self.token)
        return True

    def loaded(self, token, ok):
        if token != self.token or not self.privacy or not self.valid:
            return
        self.token = None
        self.deadline = None
        self.state = "ready" if ok else "unavailable"
        if not ok:
            self.retry_at = self.now + 2**self.attempts

    def tick(self, seconds):
        self.now += seconds
        if self.deadline is not None and self.now >= self.deadline:
            self.loaded(self.token, False)

    def reconnect(self):
        return self.prepare()

    def watch(self):
        if (
            self.state != "ready"
            or not self.privacy
            or not self.valid
            or not self.foreground
            or self.fullscreen
        ):
            return False
        pid = "presentation-" + self.claim
        self.store.present(pid, self.claim, self.run, self.reward)
        self.fullscreen = pid
        self.state = "showing"
        self.provider.show(pid)
        return True

    def closed(self, pid):
        if pid == self.fullscreen:
            self.fullscreen = None
            self.state = "unavailable"

    def earned(self, pid):
        if self.store.receive(pid):
            claim = self.store.db.execute(
                "SELECT claim FROM presentations WHERE pid=?", (pid,)
            ).fetchone()[0]
            self.store.settle(claim)

    def privacy_change(self, allowed):
        self.privacy = allowed
        self.generation += 1
        self.token = None
        self.deadline = None
        if not self.fullscreen:
            self.state = "unavailable"


class Checks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "rewards.db")
        self.s = RewardStore(self.path)
        self.b = Broker(self.s)

    def tearDown(self):
        self.s.close()
        self.tmp.cleanup()

    def ready(self):
        self.assertTrue(self.b.prepare())
        self.b.loaded(self.b.token, True)

    def show(self):
        self.ready()
        self.assertTrue(self.b.watch())
        return self.b.fullscreen

    def reopen(self):
        self.s.close()
        self.s = RewardStore(self.path)

    def test_no_fill_clears_spinner_and_reconnect_requires_fresh_watch(self):
        self.b.prepare()
        self.b.loaded(self.b.token, False)
        self.assertEqual(self.b.state, "unavailable")
        self.assertFalse(self.b.watch())
        self.b.tick(2)
        self.assertTrue(self.b.reconnect())
        self.b.loaded(self.b.token, True)
        self.assertEqual(self.b.provider.shows, [])
        self.assertEqual(self.b.state, "ready")
        self.assertTrue(self.b.watch())
        self.assertEqual(len(self.b.provider.shows), 1)

    def test_timeout_and_retry_are_bounded(self):
        for delay in [2, 4, 8]:
            self.assertTrue(self.b.prepare())
            self.b.tick(5)
            self.assertEqual(self.b.state, "unavailable")
            self.assertFalse(self.b.prepare())
            self.b.tick(delay)
        self.assertFalse(self.b.reconnect())
        self.assertEqual(len(self.b.provider.loads), 3)

    def test_stale_load_after_timeout_is_ignored(self):
        self.b.prepare()
        stale = self.b.token
        self.b.tick(5)
        self.b.tick(2)
        self.b.prepare()
        current = self.b.token
        self.b.loaded(stale, True)
        self.assertEqual(self.b.state, "loading")
        self.b.loaded(current, True)
        self.assertEqual(self.b.provider.shows, [])

    def test_privacy_generation_invalidates_old_load(self):
        self.b.prepare()
        old = self.b.token
        self.b.privacy_change(False)
        self.b.loaded(old, True)
        self.assertEqual(self.b.state, "unavailable")
        self.assertFalse(self.b.watch())

    def test_resume_does_not_present_and_double_tap_cannot_present_twice(self):
        self.ready()
        self.b.foreground = False
        self.assertFalse(self.b.watch())
        self.b.foreground = True
        self.assertEqual(self.b.provider.shows, [])
        self.assertTrue(self.b.watch())
        self.assertFalse(self.b.watch())
        self.assertEqual(len(self.b.provider.shows), 1)

    def test_expired_offer_revalidated_before_show(self):
        self.ready()
        self.b.valid = False
        self.assertFalse(self.b.watch())
        self.assertEqual(self.b.provider.shows, [])

    def test_close_then_duplicate_earn_is_one_grant(self):
        pid = self.show()
        self.b.closed(pid)
        self.assertEqual(self.s.balance(), 0)
        self.b.earned(pid)
        self.b.earned(pid)
        self.assertEqual(self.s.balance(), 7)
        self.assertEqual(self.s.pending(), 0)

    def test_earn_twice_then_close_is_one_grant(self):
        pid = self.show()
        self.b.earned(pid)
        self.b.earned(pid)
        self.b.closed(pid)
        self.assertEqual(self.s.balance(), 7)

    def test_previous_run_callback_uses_original_claim(self):
        pid = self.show()
        self.b.closed(pid)
        self.b.run = "run-B"
        self.b.reward = 999
        self.b.earned(pid)
        self.assertEqual(self.s.balance("run-A"), 7)
        self.assertEqual(self.s.balance("run-B"), 0)

    def test_privacy_withdrawal_and_expiry_during_show_preserve_earned_reward(self):
        pid = self.show()
        self.b.privacy_change(False)
        self.b.valid = False
        self.b.earned(pid)
        self.assertEqual(self.s.balance(), 7)
        self.assertFalse(self.b.prepare())

    def test_failed_grant_transaction_rolls_back_wallet_and_keeps_receipt(self):
        pid = self.show()
        self.s.receive(pid)
        with self.assertRaises(OSError):
            self.s.settle("claim-A", fail=True)
        self.assertEqual(self.s.balance(), 0)
        self.assertEqual(self.s.pending(), 1)
        self.reopen()
        self.s.recover()
        self.assertEqual(self.s.balance(), 7)
        self.assertEqual(self.s.pending(), 0)

    def test_crash_after_receipt_before_grant_replays(self):
        pid = self.show()
        self.s.receive(pid)
        self.reopen()
        self.s.recover()
        self.assertEqual(self.s.balance(), 7)
        self.assertEqual(self.s.pending(), 0)

    def test_crash_after_commit_before_ack_deduplicates_then_acks(self):
        pid = self.show()
        self.s.receive(pid)
        with self.assertRaises(SimulatedCrash):
            self.s.settle("claim-A", crash_after_commit=True)
        self.assertEqual(self.s.balance(), 7)
        self.assertEqual(self.s.pending(), 1)
        self.reopen()
        self.s.recover()
        self.assertEqual(self.s.balance(), 7)
        self.assertEqual(self.s.pending(), 0)
        self.s.receive(pid)
        self.s.recover()
        self.assertEqual(self.s.balance(), 7)

    def test_unknown_presentation_is_rejected(self):
        self.b.earned("unknown")
        self.assertEqual(self.s.balance(), 0)
        self.assertEqual(self.s.pending(), 0)

    def test_failed_receipt_then_restart_cannot_infer_earned_reward(self):
        pid = self.show()
        with self.assertRaises(OSError):
            self.s.receive(pid, fail=True)
        self.reopen()
        self.s.recover()
        self.assertEqual(self.s.balance(), 0)
        self.assertEqual(self.s.pending(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
