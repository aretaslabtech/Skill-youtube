# Running it on a schedule

Make a few videos by hand first. When they look right, `bin/run.sh` runs the studio from
cron and tells you when it *didn't* make a video.

## The runner

```bash
STUDIO_ROOT=~/my-studio ~/faceless-video-studio/bin/run.sh          # today's video, default track
STUDIO_ROOT=~/my-studio ~/faceless-video-studio/bin/run.sh promo    # any mode
```

It runs `claude -p "/video-studio <mode>"` inside your studio with:

| Safeguard | How |
|---|---|
| **No overlapping runs** | `flock` on `STUDIO_LOCK`; a second run waits up to `STUDIO_LOCK_WAIT` s (default 2 h), then alerts |
| **A wall-clock ceiling** | `timeout`: 3 h for a Short, 7 h when today's video is a long-form |
| **A spend cap** | `--max-budget-usd`: $25 for a Short, $60 for a long-form. Claude Code checks it against its own estimate, which can differ from your bill, and spend can pass the cap, so leave headroom |
| **Scoped tools** | Every tool allowed except `git push`, `curl`, `wget`, `sudo`, `ssh`, `scp`, `crontab` and `rm -rf`. No MCP servers. No `--dangerously-skip-permissions` |
| **Count, not status** | Success is `deliver.py`'s `Rendered:` line in *this* run's log. Exit code 0 with no video is a failure, and you get an alert with the reason |

Why the whole shell is allowed: a headless run can't answer a permission prompt. Our first
unattended run used a per-command allowlist and stalled at `cd hf && node …` — and since
`python3` was already allowed, listing commands bought no safety, only fragility. The deny
list is the safety. The run reads the web and runs code it wrote (because "code on screen is
code that ran"); the tool scope is the limit on what a poisoned page could make it do. Run it
as a normal user with nothing else sensitive in reach.

## Variables

| Variable | Default | Meaning |
|---|---|---|
| `STUDIO_ROOT` | current directory | Your studio |
| `STUDIO_ENV_FILE` | `$STUDIO_ROOT/.env` | Where optional keys (Telegram, `HF_TOKEN`) live |
| `STUDIO_TRACK` | `default_track` | The track for `daily` |
| `STUDIO_LIMIT` | `3h` / `7h` | Any `timeout` duration (`75m`, `2h`) |
| `STUDIO_BUDGET` | `25` / `60` | USD cap per run |
| `STUDIO_LOCK` | `/tmp/video-studio-<uid>.lock` | Share it between all your studio jobs |
| `STUDIO_LOCK_WAIT` | `7200` | Seconds to wait for the lock |
| `STUDIO_DATE` | — | `YYYY-MM-DD`: make up a missed day |
| `STUDIO_ALERT_CMD` | Telegram, else stderr | A command that receives the alert text as its argument |

## A crontab

Cron has a short `PATH` and no shell profile, so set it, and use absolute paths. Times are
the machine's local time; keep them consistent with `config.json` → `timezone`.

```cron
PATH=/home/USER/.nvm/versions/node/v22.11.0/bin:/home/USER/.local/bin:/usr/local/bin:/usr/bin:/bin

# The teaching channel: tonight's run makes tomorrow morning's video
0 23 * * *        STUDIO_ROOT=/home/USER/my-studio /home/USER/faceless-video-studio/bin/run.sh

# Promos three afternoons a week, in 75 minutes
15 15 * * 1,4,6   STUDIO_ROOT=/home/USER/my-studio STUDIO_LIMIT=75m /home/USER/faceless-video-studio/bin/run.sh promo
```

`next_day_from_hour` (default 18) is what makes the 23:00 run produce *tomorrow's* pillar:
a long-form night is the night before a long-form day, and gets the 7-hour ceiling.

**Check:** run it once by hand with the same line, then read `logs/run-<date>.log`. It
starts with `video-studio start: daily (track …, short, limit 3h, $25)` and must end with a
`Rendered:` line.

## When a run fails

- **A run that dies or hits its ceiling isn't abandoned.** The next run sees a video folder
  with a `PLAN.md` and no ledger entry (`resume_first`) and finishes it first.
- **Missed a day** (an outage, a laptop asleep)? `STUDIO_DATE=2026-10-11 bin/run.sh` makes
  that day's video now.
- **Logged out?** The alert says so: run `claude` and `/login` on the machine.
- **Out of credits?** The alert says that too; top up and use `STUDIO_DATE`.

## Things that bit us

- **Changing the server's timezone silently shifts every cron job.** Cron reads entries in
  local time; when our machine moved from UTC to IST, every job fired 5.5 hours early and the
  studio's slot had already passed that night. Convert every entry when you change it.
- **Background jobs inside a run can die at 10 minutes** unless given a longer timeout; the
  voice and render steps are written to resume.
- **Don't run two `claude -p` jobs at once** on a small machine. One shared `STUDIO_LOCK`
  for every studio job queues them instead.
