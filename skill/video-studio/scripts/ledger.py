#!/usr/bin/env python3
"""
ledger.py — what the studio has made, and what it should make today.

The ledger is $STUDIO_ROOT/ledger.json, one entry per delivered video. Everything that can be
decided without taste is decided here, so a run never re-litigates it:

  python3 ledger.py today [--track <name>]   # today's pillar, format, aspect, a planned topic
                                             # (if a planner plugin is set) + history (JSON)
  python3 ledger.py recent [--days 30]       # entries from the last N days (JSON)
  python3 ledger.py check <slug> <topic words...>
                                             # exit 1 + reason if the slug or a near-identical
                                             # topic was ever used
  python3 ledger.py looks [--last 5]         # the visual treatment of recent videos (JSON)
  python3 ledger.py rotation                 # look families, least recently used first
  python3 ledger.py look-check <family> <hook_type> <caption_skin> [signature]
                                             # exit 1 if the family was used in the last
                                             # `look_family_gap` videos (config, default 6), or
                                             # the hook type / caption skin repeats the last one
  python3 ledger.py mark-posted <slug> [--date YYYY-MM-DD]
                                             # you published it; sets `posted`

Tracks, the weekly rotation, formats and the timezone come from config.json (see
studio_config.py). Entries are appended by deliver.py, never by hand, and only after the
video was delivered.
"""
import contextlib
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_config as sc  # noqa: E402

_STOP = {"a", "an", "the", "of", "in", "to", "and", "for", "with", "how", "why", "what",
         "is", "your", "you", "i", "my", "it", "on", "vs", "python", "using"}

# The fields deliver.py records from POST.json["look"]. Only the brand core is constant; the
# look rotates, because videos that share a template soon read as AI-generated.
LOOK_FIELDS = ("look_family", "preset", "caption_skin", "hook_type", "transitions", "fonts", "footage_share", "signature")
LOOKS_MD = Path(__file__).resolve().parent.parent / "references" / "looks.md"


def local_today() -> date:
    return datetime.now(sc.tz()).date()


def delivery_date(now: datetime | None = None) -> date:
    """The morning this run's video lands. Runs from `next_day_from_hour` deliver tomorrow.
    STUDIO_DATE=YYYY-MM-DD overrides it, for a make-up run of a missed day."""
    if os.environ.get("STUDIO_DATE") and now is None:
        return date.fromisoformat(os.environ["STUDIO_DATE"])
    cfg = sc.load()
    zone = sc.tz()
    now = (now or datetime.now(zone)).astimezone(zone)
    return now.date() + timedelta(days=1) if now.hour >= cfg["next_day_from_hour"] else now.date()


def track_conf(track: str) -> dict:
    tracks = sc.load()["tracks"]
    if track not in tracks:
        raise SystemExit(f"Failed: unknown track {track!r}; config.json has {sorted(tracks)}")
    return tracks[track]


def track_slot(track: str, day: date) -> str | None:
    """The rotation slot for a track on a delivery day (None = this track doesn't run today)."""
    t = track_conf(track)
    wd = sc.WEEKDAYS[day.weekday()]
    if wd not in t.get("days", sc.WEEKDAYS):
        return None
    rot = t.get("rotation")
    if isinstance(rot, str):
        return rot
    return (rot or {}).get(wd)


def resolve_pillar(slot: str, day: date, entries: list[dict], days: list[str] | None = None) -> str:
    """Turn a rotation slot into a concrete pillar.

    promo:        product, service, product, … across the track's run days and weeks.
    either:a|b:   whichever of a or b was made less recently (never made = oldest).
    """
    if slot == "promo":
        days = days or list(sc.WEEKDAYS)
        wd = sc.WEEKDAYS[day.weekday()]
        n = day.isocalendar()[1] * len(days) + (days.index(wd) if wd in days else 0)
        return "product" if n % 2 == 0 else "service"
    if slot.startswith("either:"):
        options = slot.split(":", 1)[1].split("|")

        def last(p):
            ds = [e.get("date", "") for e in entries if e.get("pillar") == p]
            return max(ds) if ds else ""
        return min(options, key=lambda p: (last(p), p))
    return slot


def unfinished(today: date, days: int = 2) -> list[str]:
    """Video folders from the last `days` days with a PLAN.md but no ledger entry —
    a run that died or hit its ceiling. The next run resumes these first."""
    made = {e.get("slug") for e in load()}
    out = []
    for d in sorted(sc.videos_dir().glob("*/PLAN.md")):
        folder = d.parent.name
        try:
            fdate = date.fromisoformat(folder[:10])
        except ValueError:
            continue
        slug = folder[11:]
        if slug not in made and timedelta(0) <= today - fdate <= timedelta(days=days):
            out.append(str(d.parent))
    return out


def load(path: Path | None = None) -> list[dict]:
    try:
        data = json.loads((path or sc.ledger_path()).read_text())
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save(entries: list[dict]) -> None:
    p = sc.ledger_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n")


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if w not in _STOP and len(w) > 2}


def similar(a: str, b: str) -> float:
    """Jaccard overlap of content words — crude, but it catches 'Two Sum in O(n)' twice."""
    wa, wb = words(a), words(b)
    return len(wa & wb) / len(wa | wb) if wa and wb else 0.0


def recent(entries: list[dict], today: date, days: int = 30) -> list[dict]:
    cutoff = today - timedelta(days=days)
    out = []
    for e in entries:
        try:
            if date.fromisoformat(e.get("date", "")) >= cutoff:
                out.append(e)
        except ValueError:
            continue
    return out


def check(slug: str, topic: str, entries: list[dict], today: date) -> str | None:
    for e in entries:
        if e.get("slug") == slug:
            return f"slug {slug!r} already used on {e.get('date')}"
    # All time, not a window: an audience remembers. Same-day entries are skipped, because a
    # long-form and its companion Short share a topic on purpose.
    new = words(topic)
    for e in entries:
        if e.get("date") == today.isoformat():
            continue
        old = f"{e.get('topic', '')} {e.get('title', '')} {e.get('slug', '').replace('-', ' ')}"
        shared = new & words(old)
        cover = len(shared) / len(new) if new else 0.0
        s = similar(topic, old)
        if s >= 0.5 or (len(shared) >= 3 and cover >= 0.6):
            return f"topic overlaps {max(s, cover):.0%} with {e.get('slug')!r} ({e.get('date')})"
    return None


def families(path: Path = LOOKS_MD) -> list[str]:
    """Every look family in references/looks.md ("## 16. pixel-era  · engine: animate" → "pixel-era")."""
    try:
        return re.findall(r"^## \d+\. ([a-z0-9-]+)", path.read_text(), re.M)
    except OSError:
        return []


def rotation(entries: list[dict], fams: list[str] | None = None) -> list[dict]:
    """Families in the order to use them next: never used first, then the longest ago."""
    fams = fams if fams is not None else families()
    last = {}
    for i, e in enumerate(entries):
        if e.get("look_family"):
            last[e["look_family"]] = (i, e.get("date"))
    order = sorted(fams, key=lambda f: last.get(f, (-1, None))[0])
    return [{"family": f, "last_used": last.get(f, (None, None))[1], "uses": sum(e.get("look_family") == f for e in entries)}
            for f in order]


def looks(entries: list[dict], last: int = 5) -> list[dict]:
    return [{"date": e.get("date"), "slug": e.get("slug"), **{k: e.get(k) for k in LOOK_FIELDS}}
            for e in entries[-last:]]


def look_check(family: str, hook_type: str, caption_skin: str, entries: list[dict],
               signature: str | None = None) -> list[str]:
    v = sc.load()["variety"]
    fam_gap, sig_gap = v["look_family_gap"], v["signature_gap"]
    errs = []
    if signature:
        if signature in [e.get("signature") for e in entries[-sig_gap:]]:
            errs.append(f"signature beat {signature!r} was used in the last {sig_gap} videos")
    recent_families = [e.get("look_family") for e in entries[-fam_gap:]]
    if family in recent_families:
        errs.append(f"look family {family!r} was used in the last {fam_gap} videos ({recent_families})")
    if entries:
        prev = entries[-1]
        if hook_type and hook_type == prev.get("hook_type"):
            errs.append(f"hook type {hook_type!r} repeats the previous video ({prev.get('slug')})")
        if caption_skin and caption_skin == prev.get("caption_skin"):
            errs.append(f"caption skin {caption_skin!r} repeats the previous video ({prev.get('slug')})")
    return errs


def planned_topic(day: date, track: str, pillar: str, slot: str) -> str | None:
    """A topic you scheduled for this date and track, from the optional planner plugin."""
    if os.environ.get("STUDIO_NO_PLANNER"):   # tests set this, so they never hit the network
        return None
    try:
        # A plugin's own messages go to stderr: `ledger.py today` must print clean JSON.
        with contextlib.redirect_stdout(sys.stderr):
            p = sc.plugin("planner")
            return p.topic(day.isoformat(), track, pillar, slot) if p else None
    except Exception as e:  # noqa: BLE001 — the planner is optional and must never stop a run
        print(f"  ! planner: {e}", file=sys.stderr)
        return None


def planner_context(day: date, track: str) -> dict:
    """Anything else the planner plugin wants the run to see (its optional context())."""
    if os.environ.get("STUDIO_NO_PLANNER"):
        return {}
    try:
        with contextlib.redirect_stdout(sys.stderr):
            p = sc.plugin("planner")
            return p.context(day.isoformat(), track) if p and hasattr(p, "context") else {}
    except Exception as e:  # noqa: BLE001
        print(f"  ! planner: {e}", file=sys.stderr)
        return {}


def today_plan(today: date, track: str | None = None) -> dict:
    cfg = sc.load()
    track = track or os.environ.get("STUDIO_TRACK") or cfg["default_track"]
    entries = load()
    slot = track_slot(track, today)
    if slot is None:
        return {"date": today.isoformat(), "weekday": today.strftime("%A"), "track": track,
                "pillar": None, "skip": f"the {track} track doesn't run on {today.strftime('%A')}"}
    pillar = resolve_pillar(slot, today, entries, track_conf(track).get("days"))
    if pillar not in cfg["pillars"]:
        raise SystemExit(f"Failed: pillar {pillar!r} has no entry in config.json \"pillars\"")
    f = cfg["pillars"][pillar]
    return {
        "date": today.isoformat(),          # the DELIVERY date — use it for the video folder
        "weekday": today.strftime("%A"),
        "track": track,
        "planned_topic": planned_topic(today, track, pillar, slot),  # if set, this IS the topic
        "companion": pillar in cfg["companion_pillars"],  # long-form days also make a 9:16 companion
        "resume_first": unfinished(today),
        "pillar": pillar,
        "slot": slot,
        "format": f["format"],
        "aspect": f["aspect"],
        "length": f["length"],
        "videos_made": len(entries),
        "recent": [
            {k: e.get(k) for k in ("date", "slug", "pillar", "topic", "title", "product", "service")}
            for e in recent(entries, today)
        ],
        "recent_looks": looks(entries, 5),
        "products_promoted_last_14d": sorted({e["product"] for e in recent(entries, today, 14) if e.get("product")}),
        "planner_context": planner_context(today, track),
    }


def main(argv: list[str]) -> int:
    today = delivery_date()
    if not argv or argv[0] == "today":
        track = argv[argv.index("--track") + 1] if "--track" in argv else None
        print(json.dumps(today_plan(today, track), indent=1, ensure_ascii=False))
        return 0
    if argv[0] == "recent":
        days = int(argv[argv.index("--days") + 1]) if "--days" in argv else 30
        print(json.dumps(recent(load(), today, days), indent=1, ensure_ascii=False))
        return 0
    if argv[0] == "check" and len(argv) >= 3:
        reason = check(argv[1], " ".join(argv[2:]), load(), today)
        print(json.dumps({"ok": reason is None, "reason": reason}))
        return 0 if reason is None else 1
    if argv[0] == "rotation":
        for r in rotation(load()):
            print(f"{r['family']:<22} last used {r['last_used'] or 'never':<11} ({r['uses']}×)")
        return 0
    if argv[0] == "looks":
        last = int(argv[argv.index("--last") + 1]) if "--last" in argv else 5
        print(json.dumps(looks(load(), last), indent=1, ensure_ascii=False))
        return 0
    if argv[0] == "look-check" and len(argv) >= 4:
        errs = look_check(argv[1], argv[2], argv[3], load(), argv[4] if len(argv) > 4 else None)
        print(json.dumps({"ok": not errs, "reasons": errs}, ensure_ascii=False))
        return 0 if not errs else 1
    if argv[0] == "mark-posted" and len(argv) >= 2:
        entries = load()
        when = argv[argv.index("--date") + 1] if "--date" in argv else today.isoformat()
        hit = [e for e in entries if e.get("slug") == argv[1]]
        if not hit:
            print(json.dumps({"ok": False, "reason": f"no entry {argv[1]!r}"}))
            return 1
        for e in hit:
            e["posted"] = when
        save(entries)
        print(json.dumps({"ok": True, "posted": when}))
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
