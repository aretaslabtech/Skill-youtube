#!/usr/bin/env python3
"""
studio_config.py — where the studio lives and how it is configured.

Every script in this skill reads its paths and settings from here, so nothing is
hard-coded to one machine:

  STUDIO_ROOT   the studio workspace (videos/, ledger.json, config.json, brand/, .env).
                Defaults to the current directory.
  config.json   tracks, rotation, timezone, voice, variety gaps and optional plugins.
                Missing keys fall back to DEFAULTS below.

  python3 studio_config.py              # print the effective config (secrets never live here)
  python3 studio_config.py --root       # print STUDIO_ROOT
  python3 studio_config.py --media-use  # print where the HyperFrames media-use skill is

Plugins are optional Python files named in config.json "plugins" (paths relative to
STUDIO_ROOT). Each one replaces a built-in:

  links    validate(post) -> list[str]; links(post, campaign) -> dict[label, url]
           default: brand/products.json, with UTM parameters added in code
  notify   send(text) -> {"ok", "message_id"|"error"}; send_video(path, caption, duration)
           and UPLOAD_LIMIT (bytes). default: telegram.py (TELEGRAM_BOT_TOKEN/CHAT_ID),
           or the post kit saved next to the video when Telegram isn't configured
  planner  topic(day_iso, track, pillar, slot) -> str|None;
           mark_made(day_iso, post, message_id) -> int. default: none
  archive  store(video, post, revision) -> str: the final render kept elsewhere after delivery;
           a revision replaces it. default: none
"""
import copy
import importlib.util
import json
import os
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

SKILL_DIR = Path(__file__).resolve().parent.parent

WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

DEFAULTS = {
    "timezone": "UTC",
    # A run started at or after this local hour delivers the next morning, so the rotation is
    # keyed off tomorrow's weekday (an overnight cron makes "tomorrow's" video).
    "next_day_from_hour": 18,
    "voice": {"provider": "heygen", "voice_id": "", "speed": 0.75, "gap": 0.35},
    # Silence between sentences (rubric A8/B16). gap_check.py fails any gap over max_gap, except
    # one payoff beat up to payoff_gap. A channel that wants a pause after every sentence sets
    # max_gap ~1.3 and voice.gap ~0.8 (with a matching gap between lines in the composition).
    "pacing": {"max_gap": 0.7, "payoff_gap": 1.2},
    "default_track": "daily",
    "tracks": {
        # One teaching video a day. A slot is a pillar name, "promo" (alternates product and
        # service), or "either:a|b" (whichever of a or b was made less recently).
        "daily": {
            "days": list(WEEKDAYS),
            "rotation": {
                "mon": "ai-term", "tue": "python", "wed": "longform-ai", "thu": "build",
                "fri": "tech-blog", "sat": "either:ai-term|python", "sun": "longform-sd",
            },
        },
        # Product and service promos three days a week (needs brand/products.json).
        "promo": {"days": ["mon", "thu", "sat"], "rotation": "promo"},
        # A daily explainer of your own blog's post (say where it lives in brand/pillars.md).
        "blog": {"days": list(WEEKDAYS), "rotation": "blog-explainer"},
    },
    "pillars": {
        "ai-term": {"format": "short", "aspect": "1080x1920", "length": "35-60s"},
        "python": {"format": "short", "aspect": "1080x1920", "length": "35-60s"},
        "build": {"format": "short", "aspect": "1080x1920", "length": "35-60s"},
        "tech-blog": {"format": "short", "aspect": "1080x1920", "length": "35-60s"},
        "companion": {"format": "companion", "aspect": "1080x1920", "length": "35-60s"},
        "blog-explainer": {"format": "blog-explainer", "aspect": "1920x1080", "length": "90-150s"},  # 16:9: the video is embedded in the post
        "product": {"format": "short", "aspect": "1080x1920", "length": "30-50s"},
        "service": {"format": "short", "aspect": "1080x1920", "length": "30-50s"},
        "longform-ai": {"format": "longform", "aspect": "1920x1080", "length": "4-8min"},
        "longform-sd": {"format": "longform", "aspect": "1920x1080", "length": "4-8min"},
    },
    # Long-form days also make a 9:16 companion Short from the same research.
    "companion_pillars": ["longform-ai", "longform-sd"],
    "variety": {"look_family_gap": 6, "signature_gap": 5},
    "plugins": {"links": None, "notify": None, "planner": None},
}


def root() -> Path:
    return Path(os.environ.get("STUDIO_ROOT") or os.getcwd()).resolve()


def adopt_root_from(video_dir: Path) -> None:
    """When STUDIO_ROOT isn't set, take it from a video folder's path
    (<studio>/videos/<date>-<slug>), so `deliver.py <studio>/videos/x` works from anywhere."""
    if os.environ.get("STUDIO_ROOT"):
        return
    v = Path(video_dir).resolve()
    if v.parent.name == "videos" and (v.parent.parent / "config.json").is_file():
        os.environ["STUDIO_ROOT"] = str(v.parent.parent)


def _merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        # tracks are replaced whole: a user who lists their own tracks means exactly those,
        # not ours plus theirs. (pillars merge, so a user can add or override one.)
        if k in ("tracks",) or not isinstance(v, dict) or not isinstance(out.get(k), dict):
            out[k] = copy.deepcopy(v)
        else:
            out[k] = _merge(out[k], v)
    return out


def load() -> dict:
    """The effective config: DEFAULTS overlaid with $STUDIO_ROOT/config.json."""
    path = root() / "config.json"
    try:
        user = json.loads(path.read_text())
    except FileNotFoundError:
        user = {}
    except json.JSONDecodeError as e:
        raise SystemExit(f"Failed: {path} is not valid JSON — {e}")
    cfg = _merge(DEFAULTS, user)
    env_voice = os.environ.get("HEYGEN_VOICE_ID")
    if env_voice:
        cfg["voice"]["voice_id"] = env_voice
    return cfg


def tz() -> ZoneInfo:
    return ZoneInfo(load()["timezone"])


def ledger_path() -> Path:
    return root() / "ledger.json"


def videos_dir() -> Path:
    return root() / "videos"


def load_env() -> None:
    """Load $STUDIO_ENV_FILE (default $STUDIO_ROOT/.env) into os.environ, without overriding
    anything already set, so an interactive run finds the same keys a scheduled one does."""
    path = Path(os.environ.get("STUDIO_ENV_FILE") or root() / ".env")
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip().removeprefix("export ").strip(), v.strip().strip('"').strip("'")
        if k and v and k not in os.environ:
            os.environ[k] = v


def media_use_dir() -> Path | None:
    """The HyperFrames `media-use` skill (it holds the HeyGen voice helpers): skills installed
    with `npx skills add`, or with the Claude Code plugin."""
    home = Path.home()
    for p in (home / ".claude/skills/media-use", home / ".agents/skills/media-use"):
        if (p / "audio/scripts/heygen-tts.mjs").is_file():
            return p
    hits = sorted((home / ".claude/plugins").glob("**/skills/media-use/audio/scripts/heygen-tts.mjs"),
                  key=lambda f: f.stat().st_mtime, reverse=True)
    return hits[0].parents[2] if hits else None


def brand_file(name: str) -> Path:
    """A brand asset from $STUDIO_ROOT/brand/, falling back to the skill's placeholder."""
    own = root() / "brand" / name
    return own if own.exists() else SKILL_DIR / "assets" / name


def plugin(name: str):
    """Import the plugin named in config.json "plugins", or return None."""
    rel = (load().get("plugins") or {}).get(name)
    if not rel:
        return None
    path = Path(rel) if Path(rel).is_absolute() else root() / rel
    if not path.is_file():
        raise SystemExit(f"Failed: plugin {name!r} not found at {path}")
    spec = importlib.util.spec_from_file_location(f"studio_plugin_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(mod)
    return mod


def main(argv: list[str]) -> int:
    if argv[:1] == ["--root"]:
        print(root())
        return 0
    if argv[:1] == ["--media-use"]:
        d = media_use_dir()
        print(d or "not found: npx skills add heygen-com/hyperframes")
        return 0 if d else 1
    print(json.dumps(load(), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
