# Setup, step by step

This takes about 30 minutes, most of it recording your voice. Every step says how to check
it worked before you move on.

## 0. What you need

| Tool | Version | Check | Install |
|---|---|---|---|
| Claude Code | current | `claude --version` | <https://code.claude.com> |
| Node.js | 22 or newer | `node -v` | <https://nodejs.org> or `nvm install 22` |
| Python | 3.10 or newer | `python3 --version` | your OS package manager |
| FFmpeg + ffprobe | any recent | `ffmpeg -version` | `sudo apt install ffmpeg` / `brew install ffmpeg` |
| flock | — | `flock --version` | util-linux (Linux); `brew install flock` (macOS). Only for scheduled runs |
| A HeyGen account | API access | — | <https://app.heygen.com> → Settings → API |

The machine we run it on is Ubuntu 24.04 with 4 CPUs and 30 GiB RAM. Rendering is the
heavy part: a 7-minute video took 19.5 minutes there. Any recent laptop works; it's just
slower.

## 1. Install HyperFrames and its skills

HyperFrames is the renderer, and its skills teach Claude how to build compositions. Its
`media-use` skill also contains the HeyGen voice helpers (`heygen-tts.mjs`,
`heygen-voice.mjs`) that this skill calls.

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

or, for any agent that reads skills from `~/.agents/skills` or `~/.claude/skills`:

```bash
npx skills add heygen-com/hyperframes
```

**Check:** `python3 skill/video-studio/scripts/studio_config.py --media-use` (from this repo,
after step 2) prints the folder. It looks in `~/.claude/skills`, `~/.agents/skills` and the
Claude Code plugin cache. If it says "not found" but you know where `heygen-tts.mjs` is, set
`HEYGEN_TTS_SCRIPT` in your studio's `.env` to its full path.

## 2. Install this skill and create a studio

```bash
git clone https://github.com/cybiqon-ai/faceless-video-studio.git
cd faceless-video-studio
./install.sh ~/my-studio
```

The installer:
- prints ✓ or ✗ for every prerequisite (`./install.sh --check` does only that);
- links `~/.claude/skills/video-studio` to `skill/video-studio` in this repo, so a
  `git pull` updates the skill (use `--project DIR` to link it into one project instead);
- creates `~/my-studio` with `config.json`, `brand/`, `.gitignore`, a `.env` with mode 600,
  and empty `videos/`, `voice/` and `logs/` folders.

It never overwrites a file you have already edited.

## 3. Add your HeyGen API key

Open `~/my-studio/.env` and fill in:

```bash
HEYGEN_API_KEY=<your HeyGen API key>
```

The API is billed per call from a prepaid wallet, separately from HeyGen's web plans. Add
a few dollars, then check the key and the balance:

```bash
cd ~/my-studio && set -a && . ./.env && set +a
curl -s -H "X-Api-Key: $HEYGEN_API_KEY" https://api.heygen.com/v3/users/me
```

The reply includes `wallet.remaining_balance`. For scale: a minute of cloned narration cost
us about $0.14.

## 4. Record and clone your voice

Follow [voice.md](voice.md). Save the recording as `~/my-studio/voice/sample.wav`.

## 5. Run setup

```bash
cd ~/my-studio
claude
> /video-studio setup
```

Setup checks FFmpeg, the key and `npx hyperframes auth status`, clones your voice from
`voice/sample.wav`, writes the voice id to `config.json` → `voice.voice_id`, voices two test
sentences and reports words per second, then runs `npx hyperframes doctor`.

**Check:** `python3 ~/faceless-video-studio/skill/video-studio/scripts/studio_config.py`
prints your config with a `voice_id`.

## 6. Make it yours

| File | What to change |
|---|---|
| `brand/brand-core.md` | Your one accent colour (default `#00D890`) and your handle for the end mark |
| `brand/logo.png` | Your logo (square PNG, transparent background) |
| `brand/pillars.md` | Who watches, your honest tie-ins, your products and where their real footage lives |
| `brand/products.json` | Product and service links; `deliver.py` adds UTM parameters to them |
| `config.json` | Your timezone, tracks and weekly rotation ([configuration.md](configuration.md)) |

`examples/cybiqon/` in this repo is a complete, real example of all of these.

## 7. Plan one video, then make one

```bash
> /video-studio plan "what an embedding is"
```

`plan` researches, writes the script and runs Gate A — the linter and the three reviewer
agents — then stops before any voice is generated. Read `videos/<date>-<slug>/PLAN.md`: it is
the best picture of how the studio thinks.

```bash
> /video-studio daily
```

`daily` makes today's video from your rotation, end to end. The MP4 is at
`videos/<date>-<slug>/hf/renders/video.mp4`; the post kit is `POST-KIT.html` beside it (or a
Telegram message, step 8). The last line of the run is the proof:

```
Rendered: what-an-embedding-is 74s 21.3MB msg local parts=1
```

## 8. Optional: Telegram delivery

1. Message [@BotFather](https://t.me/BotFather), create a bot, copy its token.
2. Send your new bot any message.
3. Open `https://api.telegram.org/bot<token>/getUpdates` and copy `chat.id`.
4. Add both to `.env`:

   ```bash
   TELEGRAM_BOT_TOKEN=<token from BotFather>
   TELEGRAM_CHAT_ID=<your chat id>
   ```

5. Test: `set -a; . ./.env; set +a; python3 ~/faceless-video-studio/skill/video-studio/scripts/telegram.py "hello"`

Videos over Telegram's 50 MB bot limit are re-encoded to a smaller copy for the message;
the full-quality file stays on disk for YouTube.

## 9. Optional: the extra engines

```bash
# animate: 7 hand-made styles (pixel, riso, crosshatch, cut-paper, sketchbook, isometric, maths)
cd ~/faceless-video-studio/skill/video-studio/vendor/animate
npm install && npx playwright install chromium

# Manim: maths and algorithm beats, rendered as transparent clips
python3 -m venv ~/.venvs/manim && ~/.venvs/manim/bin/pip install manim
```

Without them, the studio simply skips the looks that need them.

## 10. Schedule it

When a few manual runs look right, see [scheduling.md](scheduling.md).

## Updating

```bash
cd ~/faceless-video-studio && git pull
```

The skill is a link into the repo, so the next run uses the new version. Your studio folder
is never touched by an update.
