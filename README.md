# Rucoy Online — scammer reports archive

A machine-readable archive of **scammer report channels** from public Rucoy Online
trading Discord servers, collected on **24 September 2026**.

Trading in Rucoy Online happens on Discord, and every market server keeps its own
scammer list. Those lists are scattered, formatted differently, and disappear when a
server dies. This archive puts them in one place so they can be searched, compared
and preserved.

## What's here

| File | What it is |
|---|---|
| `scammers-verdict.json` | **Start here.** 120 accused accounts keyed by permanent Discord ID, each with a confidence rating and its evidence |
| `identified.json` | All 501 accounts with a permanent ID, tagged `accused` / `staff-or-trader` / `mentioned-only` |
| `by-name-only.json` | 352 bot-ban records that carry a username and nothing else |
| `scammers-all.json` | All channels merged into one file (2.8 MB) |
| `raw/<server>/<channel>.json` | Per-channel exports, unmodified |
| `SOURCES.md` | Table of servers and message counts |
| `merge.py`, `identify.py` | The scripts that build everything above from `raw/` |

**4892 messages from 22 channels across 9 servers.** Full breakdown in
[SOURCES.md](SOURCES.md).

## The identifier problem

Usernames are not identities. Discord dropped discriminators in 2023, people rename
themselves, and accounts get resold — a 2023 ban on `Name#1234` says nothing about
whoever holds that name today.

The only stable key here is the **Discord user ID**, a snowflake that is issued once
and never changes. It is not stored in the ban messages, but it *is* embedded in
every `@mention`: Discord inlines the mentioned user's profile into the message, so
each mention yields a permanent ID plus that account's username **as of the export
date**. That is where all 501 identified accounts come from.

A snowflake also encodes its own creation time, which is enough to catch mismatches.
Worked example from this archive: `Maximus⚡#1665` was banned on 2023-04-25, while the
account accused as "Maximus" in 2026 is ID `1396924766635688109`, created 2025-07-21.
Two different accounts, two years apart, one name. Merging them would have been wrong.

## Confidence, and why most entries have none

`scammers-verdict.json` rates each accused account by **how many distinct people**
reported it:

| Rating | Meaning | Count |
|---|---|---|
| `high` | 3+ distinct reporters | 1 |
| `medium` | 2 distinct reporters | 5 |
| `low` | a single source | 98 |

**Count reporters, not servers.** People cross-post the same accusation to every
market server they are in, which makes one complaint look like three. `maximum.7799`
appears on three servers but every post came from the same reporter. Use
`distinctReporters`; treat `serversAccusing` as context, not corroboration.

**Replies are not accusations.** On Discord a reply auto-mentions the author of the
message it answers. A victim who posts "scammed for 400kk" therefore gets mentioned
in every reply to their own report — and a naive extractor files them as the accused.
Sixteen accounts were wrongly listed this way before `type: "Reply"` was checked
against the referenced message's author; they are excluded now, and the count of
ignored reply pings is kept per account in `replyPingsIgnored`.

Six of 104 accounts have corroboration from a second reporter. The rest is one
person's word, unverified. That is a property of the source material, not of the
processing.
