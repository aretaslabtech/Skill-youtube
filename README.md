<div align="center">

# Faceless Video Studio

**A Claude Code skill that researches, scripts, voices and renders a finished explainer video
every day — with [HyperFrames](https://github.com/heygen-com/hyperframes), a
[HeyGen](https://www.heygen.com/) clone of your own voice, and 38 pass/fail gates that stop
AI slop before it ships.**

No camera. No avatar. No editing timeline. You review an MP4 in the morning and post it.

<a href="https://github.com/cybiqon-ai/faceless-video-studio/releases/download/v1.0.1/demo.mp4"><img src="docs/assets/demo.gif" width="800" alt="A 15-second highlight: a real blog-explainer video the studio made, a wall of contact sheets from 14 videos in 9 different looks, seven hand-drawn animation styles, and the repo URL."></a>

<sub>Real output: a blog explainer the studio made on 12 Oct 2026, contact sheets from its first 14 videos, and the demo pieces of the seven animate styles it ships with. ▶ <a href="https://github.com/cybiqon-ai/faceless-video-studio/releases/download/v1.0.1/demo.mp4">Watch the 40-second version with sound</a> (the voice is a HeyGen clone).</sub>

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-cc785c)
![HyperFrames](https://img.shields.io/badge/renderer-HyperFrames-0b0f14)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776ab)
![Node 22+](https://img.shields.io/badge/node-22%2B-339933)

[How it works](#how-it-works) · [Quickstart](#quickstart) · [What it costs](#what-it-costs) ·
[The gates](#the-38-gates) · [Scheduling](docs/scheduling.md) · [The full story](https://cybiqon.in/lab/hyperframes-heygen-ai-video-pipeline)

</div>

---

## What it makes

Real videos made by this studio, narrated by a HeyGen clone of the founder's voice:

| Video | Format | What it shows |
|---|---|---|
| [Google gave its newest AI real jobs](https://youtu.be/Tuv_wF5Yhw4) | 117 s explainer | Real source-page footage with highlights drawn on the exact sentences |
| [Jev, explained](https://youtu.be/el5VAfAQASM) | 118 s explainer | A blog post turned into a teaching video |
| [How OpenAI trained agents to run enterprise software](https://youtu.be/sXXElHX-7SU) | explainer | News explained for a beginner |

It ships with **pillars** for AI terms, Python, build-a-thing, tech news, product and service
promos and blog explainers, plus **4–8 minute long-form deep dives**, **22 look families** so
two videos in a row never share a template, and **three render engines** (HyperFrames,
plus the vendored [animate](https://github.com/cth9191/animate) styles and optional Manim).

## How it works

```mermaid
flowchart LR
    A[1 Pick<br/>ledger + rotation] --> B[2 Research<br/>sources.md, code that ran]
    B --> C[3 Plan<br/>3 scored hooks, script, new look]
    C --> D{4 Gate A<br/>lint + 3 reviewer agents}
    D -->|pass| E[5 Voice<br/>HeyGen clone, one take per sentence]
    D -->|fail| C
    E --> F[6 Frames<br/>one sub-agent per beat]
    F --> G{7 Gate B<br/>check, snapshots, final-file judge}
    G -->|fail, ≤ 2 loops| F
    G -->|pass| H[8 Render + deliver<br/>−14 LUFS MP4 + post kit]
```

1. **Pick.** `ledger.py today` returns the day's pillar and format from your rotation, and
   refuses any topic close to a video you have ever made.
2. **Research.** Every fact gets a source URL. Teaching videos run their code first, and only
   the real output goes on screen.
3. **Plan.** Three hooks scored out of 12, a word-budgeted script for "a smart 12-year-old",
   and a look chosen from the least recently used families.
4. **Gate A — before any money is spent on voice.** A linter, then three fresh sub-agents: a
   12-year-old who explains it back (with a separate judge), an expert who flags anything
   false, and a cold viewer who sees only the first three seconds.
5. **Voice.** One HeyGen take per sentence, trimmed on the real sound (never on TTS
   timestamps, which run late and cut words), with a hash manifest.
6. **Frames.** One sub-agent per beat builds HTML + GSAP in parallel; HyperFrames assembles.
7. **Gate B.** `hyperframes check`, snapshots the agent actually looks at, and a judge that
   reviews frames decoded from the final MP4.
8. **Deliver.** `deliver.py` refuses the video unless every review line is present, every
   voice line is clean and a Short fills its frame; then it sends the MP4 and a post kit
   (titles, descriptions, hashtags, tracked links, sources) to Telegram — or saves it locally.

The studio **never posts**. A person watches it, posts it, and runs `ledger.py mark-posted`.

## Quickstart

You need **Linux** (we run Ubuntu 24.04; macOS works with GNU `timeout` and `flock` from
Homebrew), **Node.js 22+**, **Python 3.10+**, **FFmpeg**,
[Claude Code](https://code.claude.com), and a [HeyGen API](https://app.heygen.com) key.

**1. Install HyperFrames and its agent skills** (they provide the renderer and the HeyGen
voice helpers this skill calls):

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
# or, without the plugin:
npx skills add heygen-com/hyperframes
```

**2. Install this skill.** Either as a Claude Code plugin (one command, auto-updates):

```bash
claude plugin marketplace add cybiqon-ai/faceless-video-studio
claude plugin install faceless-video-studio@faceless-video-studio
mkdir ~/my-studio   # your studio folder; step 5's setup fills it
```

…or clone it and run the installer, which checks your tools, links the skill into
`~/.claude/skills/video-studio` and creates the studio folder from `studio.example/`:

```bash
git clone https://github.com/cybiqon-ai/faceless-video-studio.git
cd faceless-video-studio
./install.sh ~/my-studio
```

As a plugin the command is `/faceless-video-studio:video-studio`; below it's written
`/video-studio`.

**3. Add your HeyGen key** to `~/my-studio/.env` (mode 600, gitignored; with the plugin,
run step 5's setup once first and it creates the file):

```bash
HEYGEN_API_KEY=<your HeyGen API key>
```

Fund the HeyGen API wallet; usage is billed per call. Check the key and balance:

```bash
cd ~/my-studio && set -a && . ./.env && set +a
curl -s -H "X-Api-Key: $HEYGEN_API_KEY" https://api.heygen.com/v3/users/me
```

**4. Record your voice once** — one expressive 90–120 s take in a quiet room, saved as
`~/my-studio/voice/sample.wav`. [docs/voice.md](docs/voice.md) has the script to read and
what makes a clone sound like you.

**5. Run setup.** It checks FFmpeg, the key and HyperFrames, clones your voice, and writes
the voice id into `config.json`:

```bash
cd ~/my-studio && claude
> /video-studio setup
```

**6. Make it yours.** Edit `brand/brand-core.md` (your accent colour and handle),
`brand/pillars.md` (your audience, products and honest tie-ins) and `brand/products.json`
(the links promos point to). `examples/cybiqon/` is a real, filled-in brand.

**7. Make your first video** and watch it end to end:

```bash
> /video-studio plan "what an embedding is"   # research + plan + Gate A only, no spend on voice
> /video-studio daily                          # the full run: today's pillar from your rotation
```

The MP4 lands in `videos/<date>-<slug>/hf/renders/video.mp4`, with `POST-KIT.html` beside it.

**8. Optional: get it on Telegram.** Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to
`.env` and test it from your studio:
`cd ~/my-studio && python3 ~/faceless-video-studio/skill/video-studio/scripts/telegram.py "hello"`.

**9. Optional: more engines.** The animate styles need `npm install` in
`skill/video-studio/vendor/animate`; Manim needs its own venv. The installer prints both
commands.

**10. Schedule it** once a few manual runs look right — see [docs/scheduling.md](docs/scheduling.md):

```cron
PATH=/home/USER/.nvm/versions/node/v22.11.0/bin:/home/USER/.local/bin:/usr/local/bin:/usr/bin:/bin
0 23 * * *  STUDIO_ROOT=/home/USER/my-studio /home/USER/faceless-video-studio/bin/run.sh
```

Cron has a short `PATH`: set it to wherever `claude`, `node` and `npx` live (`which claude node`).
With the plugin install, add `STUDIO_SKILL=faceless-video-studio:video-studio` and call the
`bin/run.sh` from a clone of this repo.

## What it costs

From the studio's own first four days (October 2026), where it made 12 finished videos:

| Item | Cost |
|---|---|
| HeyGen voice, all 12 videos plus revisions and tests | **$8.20** (wallet $15 → $6.80) |
| HeyGen clone TTS, measured | **~$0.14 per minute** of narration |
| HeyGen music retrieval | $0.00 per call in our tests |
| Claude Code run, one 85 s Short | ~$18.35 (estimate reported by Claude Code; ~$10 of it the 11 parallel frame workers) |
| Claude Code run, a 7-minute long-form + its companion Short | ~$26 |
| Rendering | your own CPU: 2.5–19.5 min per video on 4 cores |

Nearly all the spend is the agent, not the voice. `bin/run.sh` caps every run with
`--max-budget-usd` ($25 for a Short, $60 for a long-form by default), and `POST.json` has a
`cost_usd` field: fill it from day one. The full breakdown is in the
[write-up](https://cybiqon.in/lab/hyperframes-heygen-ai-video-pipeline).

## The 38 gates

Most of them exist because a real video failed in exactly that way. `deliver.py` refuses a
video unless the four review pass lines are in its plan, and it checks the voice (B17) and
the frame fill (B18) itself:

| Gate | Rule | The failure behind it |
|---|---|---|
| **A8** | ≤ 2.0 words/s, a breath after every reveal | The first Short: 97 words in 44 s, "too fast" |
| **A14–A16, A18** | Written for a smart 12-year-old; linted; explained back to a separate judge | A script that "considers the viewer as an expert" |
| **A19** | An expert agent flags anything false | Three simplifications that had become untrue |
| **A2, A20** | The hook is the viewer's own question, proven on screen by 3 s | "The hook doesn't make sense" |
| **B11, B13** | Footage fills the frame; no two videos look like one template | "Quite similar… it will soon be noticed as AI generated" |
| **B16, B17** | No silence over 0.7 s; every voice line starts and ends on silence | Gaps of 3–5 s; a third of sentences losing their first word |
| **B18** | A Short fills its frame to the bottom edge | An empty bottom 40% on every Short |

All 38, with what each checks: [docs/gates.md](docs/gates.md). The rubric the agent works
from: [`skill/video-studio/references/quality-rubric.md`](skill/video-studio/references/quality-rubric.md).

## What's in the box

```
skill/video-studio/
  SKILL.md                 the skill: modes, pipeline, rules
  references/              the rubric, 22 looks, pillars, prompt library, 9 craft notes
  scripts/                 ledger, deliver, voice_build, script_lint, gap/fill checks, tests
  templates/               PLAN.md and BRIEF.md
  assets/                  caption skins, fonts (OFL), placeholder brand
  vendor/animate/          cth9191/animate (MIT), a second engine with 7 styles
bin/run.sh                 unattended runner: lock, ceilings, budget cap, count-not-status alert
install.sh                 prerequisite check, skill link, studio scaffold
studio.example/            config.json, .env template, brand/ to copy and edit
examples/cybiqon/          a real, filled-in brand and three-track config
docs/                      setup, configuration, voice, scheduling, gates, troubleshooting
```

## Documentation

- [Setup, step by step](docs/setup.md)
- [Configuration: tracks, rotation, plugins](docs/configuration.md)
- [Cloning your voice](docs/voice.md)
- [Running it on a schedule](docs/scheduling.md)
- [All 38 gates](docs/gates.md)
- [Troubleshooting: every trap we hit](docs/troubleshooting.md)

## FAQ

**Does it need an avatar or a camera?** No. Every visual is an animated HTML scene, a real
web page captured in a browser, or real product footage. HeyGen supplies only the voice
(and, optionally, music).

**Can I use another voice provider?** The voice step calls HeyGen's TTS through the
HyperFrames media-use helper. Swapping providers means replacing `take()` in
`scripts/voice_build.py`; keep the trim-on-real-sound logic and the manifest, because the
B17 gate depends on them.

**Does it post for me?** No, on purpose. It delivers a video and a post kit. YouTube's API
keeps uploads private until an app passes Google's audit, and a person should watch every
video before it goes out.

**How long does a run take?** `bin/run.sh` caps a Short at 3 hours and a long-form at 7
(both configurable); most of that time goes on research and the review agents, not
rendering. Our renders took 2.5–19.5 minutes on 4 cores.

**Will it make the same video twice?** `ledger.py check` refuses a topic that overlaps any
video you have made, and `look-check` refuses a look family used in the last six videos.

## Credits

Built by [Cybiqon](https://cybiqon.in) and run daily on our own channels. The story of how
it was built, what broke and what it cost:
[*Twelve videos in four days. Nobody picked up a camera.*](https://cybiqon.in/lab/hyperframes-heygen-ai-video-pipeline)

Stands on [HyperFrames](https://github.com/heygen-com/hyperframes) (Apache 2.0),
[animate](https://github.com/cth9191/animate) by cth9191 (MIT, vendored),
[Manim](https://www.manim.community/) (MIT, optional), and lessons from
[awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) (MIT). See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## License

[MIT](LICENSE) © 2026 Cybiqon AI Solutions. Vendored and bundled third-party files keep their own licences.
