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
| `scammers-all.json` | All channels merged into one file (2.8 MB) |
| `raw/<server>/<channel>.json` | Per-channel exports, unmodified |
| `SOURCES.md` | Table of servers and message counts |
| `merge.py` | The script that builds the merged file from `raw/` |

**4892 messages from 22 channels across 9 servers.** Full breakdown in
[SOURCES.md](SOURCES.md).

## Format

```json
{
  "sources": [ { "server": "...", "channel": "...", "messageCount": 609 } ],
  "messageCount": 4892,
  "messages": [
    {
      "server": "Europe-Market",
      "channel": "scammer-proofs",
      "channelId": "983274544250904576",
      "messageId": "985227296443101235",
      "timestamp": "2022-06-11T17:01:32.11+00:00",
      "author": { "name": "...", "nickname": "...", "id": "..." },
      "content": "i have proof that ... is a scammer",
      "attachments": ["https://cdn.discordapp.com/..."],
      "embeds": [],
      "reactions": [],
      "link": "https://discord.com/channels/972502585825173514/983274544250904576/985227296443101235"
    }
  ]
}
```

Messages are sorted by timestamp. Every entry carries a `link` back to the original
message on Discord — **always check the original before acting on anything here.**

## Read this before you use it

**These are accusations, not verdicts.** Anyone with access to those channels could
post a name. Reports here include mistakes, grudges, revenge posts, and cases that
were later resolved. Treating this file as a blocklist without reading the source
messages will get innocent players banned.

**Screenshots will rot.** The `attachments` URLs point at Discord's CDN, which stops
serving old files. They worked on the collection date; many will be dead by the time
you read this. The message `link` is the durable reference, not the image URL.

**Coverage is partial.** Four channels on Asian Market and one on Rucoy Online Market
Place require a role the collecting account did not have, so they are missing.
Servers that have since closed are not represented at all.

**Names, not people.** Entries identify Discord and in-game accounts. Accounts get
sold, shared, stolen and renamed — an account named in 2022 may have nothing to do
with whoever holds it now.

## Provenance

Collected with [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)
v2.48.0 from servers the collecting account was a member of. Nothing was edited: the
merge step only adds the `server`, `channel` and `link` fields and drops binary
payloads. Re-run `merge.py raw/` to rebuild `scammers-all.json` yourself.

Not affiliated with Rucoy Online or any of the servers listed.

## Takedown

If you are named here and believe it is wrong, open an issue with the message link
and your side of it. Corrections are appended rather than silently deleted, so the
record stays honest in both directions.
