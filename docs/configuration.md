# Configuration

Everything about *your* studio lives in the studio folder (`$STUDIO_ROOT`), never in the
skill. The skill reads it through `scripts/studio_config.py`; run that script to print the
effective config (your `config.json` over the defaults).

```
my-studio/
  config.json        tracks, rotation, timezone, voice, variety gaps, plugins
  .env               secrets (mode 600, gitignored)
  brand/             brand-core.md, logo.png, pillars.md, products.json
  plugins/           optional Python plugins (below)
  videos/            one folder per video
  ledger.json        every delivered video (written by deliver.py)
  logs/              scheduled-run logs
```

## `config.json`

```json
{
  "timezone": "UTC",
  "next_day_from_hour": 18,
  "voice": { "provider": "heygen", "voice_id": "", "speed": 0.75, "gap": 0.35 },
  "default_track": "daily",
  "tracks": { "...": "below" },
  "variety": { "look_family_gap": 6, "signature_gap": 5 },
  "plugins": { "links": null, "notify": null, "planner": null }
}
```

| Key | Meaning |
|---|---|
| `timezone` | IANA name (`Asia/Kolkata`, `America/New_York`). Decides the delivery date and weekday |
| `next_day_from_hour` | A run started at or after this local hour makes *tomorrow's* video, so an 11 pm cron delivers a video for the next morning |
| `voice.voice_id` | Your HeyGen voice. `HEYGEN_VOICE_ID` in `.env` overrides it |
| `voice.speed`, `voice.gap` | TTS speed per sentence and the breath between sentences. 0.75 and 0.35 s land near 2 words/s for a clone that speaks fast |
| `default_track` | The track `/video-studio daily` uses |
| `variety.look_family_gap` | A look family can't repeat within this many videos |
| `variety.signature_gap` | A signature beat can't repeat within this many videos |
| `pillars` | Optional: override or add pillar formats (`{"format", "aspect", "length"}`) |
| `companion_pillars` | Pillars whose day also makes a 9:16 companion Short (default: both long-forms) |

Keys you leave out keep their defaults. Unknown keys are ignored, so you can keep notes in
the file.

## Tracks and the rotation

A **track** is one stream of videos with its own schedule: a teaching channel, product
promos, a daily blog explainer. Each track has the weekdays it runs on and a rotation.

```json
"tracks": {
  "daily": {
    "days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
    "rotation": {
      "mon": "ai-term", "tue": "python", "wed": "longform-ai", "thu": "build",
      "fri": "tech-blog", "sat": "either:ai-term|python", "sun": "longform-sd"
    }
  },
  "promo": { "days": ["mon", "thu", "sat"], "rotation": "promo" },
  "blog":  { "rotation": "blog-explainer" }
}
```

A **slot** is one of:
- a pillar name: `ai-term`, `python`, `build`, `tech-blog`, `blog-explainer`, `product`,
  `service`, `longform-ai`, `longform-sd` (see `references/pillars.md`);
- `promo`: alternates product, service, product… across the track's run days;
- `either:a|b`: whichever of `a` or `b` was made less recently.

`rotation` is either a weekday map or one slot used every run day. Listing your own
`tracks` replaces the default ones entirely.

Run a track with `/video-studio daily` (the default track), `/video-studio promo` or
`/video-studio blog`; `bin/run.sh` maps those modes to the tracks of the same name, and
`STUDIO_TRACK=<name>` picks another track for `daily`.

**Check:** `python3 <skill>/scripts/ledger.py today --track promo` prints today's pillar,
or `"skip"` if the track doesn't run today.

## `brand/`

| File | Read by | Purpose |
|---|---|---|
| `brand-core.md` | the agent, every run | The few things that never change: voice, one accent, end mark, safe zones, truth rules |
| `logo.png` | the agent | End mark only, ≤ 120 px |
| `pillars.md` | the agent, every run | Your audience, honest tie-ins, products, where their real footage lives, and any house rules |
| `products.json` | `deliver.py` | The links in each post kit |

Each falls back to the skill's placeholder in `assets/` when missing.

`products.json`:

```json
{
  "products": {
    "my-app": { "name": "My App", "url": "https://play.google.com/store/apps/details?id=com.example.app" },
    "my-tool": { "name": "My Tool", "url": "https://example.com/tool", "web": "https://example.com" }
  },
  "services": {
    "websites": { "name": "Websites", "url": "https://example.com/services/websites" }
  },
  "contact": { "label": "WhatsApp", "url": "https://wa.me/..." }
}
```

`deliver.py` adds `utm_source` (youtube, instagram, facebook), `utm_medium=video` and
`utm_campaign=<date>-<slug>`. Play Store links carry them inside `referrer`, as Play
requires. The agent never writes a URL itself; POST.json texts that contain one are refused.

## Plugins

Four optional Python files, named in `config.json` → `plugins` (paths relative to the
studio). Each replaces a built-in. They are how a studio connects private systems without
forking the skill.

| Plugin | Functions | Replaces |
|---|---|---|
| `links` | `validate(post) -> list[str]`, `links(post, campaign) -> dict[label, url]` | `brand/products.json` link building |
| `notify` | `send(text) -> dict`, `send_video(path, caption, duration) -> dict`, `UPLOAD_LIMIT` (bytes) | `telegram.py` (e.g. Slack, email, your own bot) |
| `planner` | `topic(day, track, pillar, slot) -> str \| None`, `mark_made(day, post, message_id) -> int`, optional `context(day, track) -> dict` | none: lets a content calendar choose topics and get marked "made" |
| `archive` | `store(video, post, revision) -> str` | none: keeps each delivered video's final render somewhere else (cloud storage, a NAS); a revision should replace, not add |

`send` and `send_video` return `{"ok": True, "message_id": ...}` or
`{"ok": False, "error": "..."}` and must never raise. Planner failures are logged and never
stop a run. An `archive` failure is logged and sent as a notice; the delivery still counts.

A minimal `notify` plugin that posts to a Slack webhook:

```python
# plugins/slack.py
import json, os, urllib.request
UPLOAD_LIMIT = 0  # never upload the file; send a message with its path instead

def send(text):
    req = urllib.request.Request(os.environ["SLACK_WEBHOOK"], data=json.dumps({"text": text}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=30)
        return {"ok": True, "message_id": "slack"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def send_video(path, caption="", duration=None):
    return send(f"{caption}\n{path}")
```

```json
"plugins": { "notify": "plugins/slack.py" }
```

Our own studio uses all four: links built by our product catalogue, delivery through the
company's Telegram bot, a content planner that schedules topics, and an archive of final renders
in Google Drive.

## Environment variables

| Variable | Used by | Meaning |
|---|---|---|
| `HEYGEN_API_KEY` | voice | Required |
| `HEYGEN_VOICE_ID` | voice | Overrides `voice.voice_id` |
| `HEYGEN_TTS_SCRIPT` | voice | Full path to `heygen-tts.mjs` if it isn't in the usual skill folders |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | delivery, alerts | Optional Telegram delivery |
| `STUDIO_ROOT` | everything | The studio folder (default: the current directory, or the folder above `videos/` when a script is given a video path) |
| `STUDIO_DATE` | ledger | `YYYY-MM-DD`: make up a missed day's video |
| `STUDIO_NO_PLANNER` | ledger, deliver | Skip the planner plugin (the tests set it) |
| `MANIM_BIN` | Manim engine | Path to the `manim` executable (default `~/.venvs/manim/bin/manim`) |

`bin/run.sh` adds its own scheduling variables; see [scheduling.md](scheduling.md).
