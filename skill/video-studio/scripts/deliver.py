#!/usr/bin/env python3
"""
deliver.py — the last gate. Checks a finished video, sends it and its post kit, then logs it.

  python3 deliver.py <video-dir>             # check, send, append to $STUDIO_ROOT/ledger.json
  python3 deliver.py <video-dir> --dry-run   # check and print the kit; send and log nothing
  python3 deliver.py <video-dir> --revision  # re-deliver a revised video; updates its entry

It refuses (prints `Failed: …`, exits 1) unless:
  - POST.json is complete and its texts contain no URLs (links are built here, in code);
  - PLAN.md carries the four review pass lines, written only on a reviewer's or the linter's PASS:
    `A16: PASS (judge)`, `A18: PASS`, `A19: PASS (expert)`, `A20: PASS (cold viewer)`;
  - every voice line was made by voice_build.py and starts and ends on silence (B17);
  - a 9:16 render fills its frame down to the bottom edge (B18).

POST.json (written by the skill at the end of a run):

  {
    "slug": "two-sum-hash-map",            # unique; also the utm_campaign suffix
    "pillar": "python",
    "format": "short",                     # short | longform | companion
    "track": "daily",                      # a track in config.json
    "topic": "Two Sum in O(n) with a hash map",
    "render": "hf/renders/video.mp4",      # relative to <video-dir>
    "duration_s": 47,
    "titles": ["...", "...", "..."],       # first is the pick
    "youtube_description": "...",          # no URLs — links are appended in code
    "caption": "...",                      # Instagram/Facebook caption, no URLs
    "hashtags": ["python", "..."],
    "pinned_comment": "...",
    "product": "my-app" | null,            # a key of brand/products.json "products", or
    "service": "websites" | null,          # a key of its "services"
    "thumbnail_at": 1.2,                   # seconds; the frame to use as cover
    "sources": ["https://..."],
    "notes": "anything you should know, including any gate that failed",
    "cost_usd": 18.35,                     # optional; what the run cost
    "look": {                              # the visual treatment — feeds the variety gate
      "look_family": "documentary",        # references/looks.md
      "preset": "editorial-forest",
      "caption_skin": "boxed-word",        # assets/captions/<name>.html
      "hook_type": "result-first",         # craft/hooks.md taxonomy
      "transitions": ["cut", "zoom-through"],
      "fonts": ["Archivo Black", "IBM Plex Mono"],
      "footage_share": 0.62,               # share of runtime with real footage ≥ 80% of frame
      "signature": "registry:chart-race"   # the video's one hero moment
    }
  }

Delivery goes through the `notify` plugin if config.json names one, else telegram.py; with
neither configured, the kit is saved as <video-dir>/POST-KIT.html. Prints one count line,
never just a status, so a scheduler can tell "made a video" from "exited 0":

  Rendered: <slug> 47s 18.2MB msg <id> parts=<n>
"""
import json
import os
import subprocess
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fill_check  # noqa: E402
import studio_config as sc  # noqa: E402
import telegram  # noqa: E402
from ledger import LOOK_FIELDS, delivery_date, load, save  # noqa: E402
from voice_build import check as voice_check  # noqa: E402

esc = telegram.esc

REQUIRED = ("slug", "pillar", "format", "topic", "render", "titles", "youtube_description", "caption", "hashtags")
LOOK_REQUIRED = ("look_family", "caption_skin", "hook_type")
PASS_LINES = ("A16: PASS (judge)", "A18: PASS", "A19: PASS (expert)", "A20: PASS (cold viewer)")
# Teaching videos must start from a problem people are asking about (problem-scout.md, A21).
PROBLEM_PILLARS = {"ai-term", "python", "build", "longform-ai", "longform-sd", "companion"}
PROBLEM_LINE = "A21: PASS (real problem)"


# ---- links: the plugin, or brand/products.json ------------------------------------------------

def catalogue() -> dict:
    try:
        return json.loads(sc.brand_file("products.json").read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def utm(url: str, source: str, campaign: str) -> str:
    """Add UTM parameters. Play Store links carry them inside `referrer`, as Play requires."""
    q = f"utm_source={source}&utm_medium=video&utm_campaign={campaign}"
    if "play.google.com" in url:
        return f"{url}{'&' if '?' in url else '?'}referrer={urllib.parse.quote(q, safe='')}"
    return f"{url}{'&' if '?' in url else '?'}{q}"


def _validate_links(post: dict) -> list[str]:
    c = catalogue()
    errs = []
    if post.get("product") and post["product"] not in c.get("products", {}):
        errs.append(f"unknown product {post['product']!r}; brand/products.json has {sorted(c.get('products', {}))}")
    if post.get("service") and post["service"] not in c.get("services", {}):
        errs.append(f"unknown service {post['service']!r}; brand/products.json has {sorted(c.get('services', {}))}")
    return errs


def _links(post: dict, campaign: str) -> dict:
    c, out = catalogue(), {}
    if post.get("product"):
        p = c["products"][post["product"]]
        for src, label in (("youtube", "YouTube"), ("instagram", "Instagram"), ("facebook", "Facebook")):
            out[label] = utm(p["url"], src, campaign)
        if p.get("web"):
            out["Web"] = utm(p["web"], "youtube", campaign)
    if post.get("service"):
        s = c["services"][post["service"]]
        out["Service (YouTube)"] = utm(s["url"], "youtube", campaign)
        out["Service (Instagram)"] = utm(s["url"], "instagram", campaign)
        contact = c.get("contact") or {}
        if contact.get("url"):
            out[contact.get("label", "Contact")] = contact["url"]
    return out


def validate(post: dict) -> list[str]:
    errs = [f"missing {k}" for k in REQUIRED if not post.get(k)]
    look = post.get("look")
    if not isinstance(look, dict):
        errs.append("missing look block (look_family, caption_skin, hook_type, …) — the variety gate needs it")
    else:
        errs += [f"look.{k} missing" for k in LOOK_REQUIRED if not look.get(k)]
    p = sc.plugin("links")
    errs += p.validate(post) if p else _validate_links(post)
    for k in ("youtube_description", "caption", "pinned_comment"):
        if "http" in str(post.get(k) or ""):
            errs.append(f"{k} contains a URL — links are added by deliver.py")
    return errs


def links(post: dict, campaign: str) -> dict:
    p = sc.plugin("links")
    return p.links(post, campaign) if p else _links(post, campaign)


# ---- gates on the finished file ---------------------------------------------------------------

def fill_errors(video: Path, post: dict) -> list[str]:
    """Rubric B18 on the final render (9:16 organic posts; paid ads are exempt)."""
    if post.get("ad"):
        return []
    try:
        dur, w, h = fill_check.probe(str(video))
    except Exception as e:  # noqa: BLE001
        return [f"B18: can't read {video.name}: {e}"]
    if h <= w:
        return []
    n = 8
    frames = [{"t": t, **fill_check.frame_stats(fill_check.grab(str(video), t))}
              for t in (dur * (0.08 + 0.84 * k / (n - 1)) for k in range(n))]
    r = fill_check.judge(frames)
    if r["ok"]:
        return []
    return [f"B18: only {r['filled']}/{r['samples']} frames fill the lower visual and the bottom "
            "(an empty bottom 40% reads as unfinished; see platform-specs.md §1)"]


# ---- the kit ----------------------------------------------------------------------------------

def kit(post: dict, link_map: dict) -> str:
    t = post["titles"]
    L = [f"📦 <b>POST KIT — {esc(post['slug'])}</b>",
         f"<i>{esc(post['pillar'])} · {esc(post['format'])} · {esc(post.get('duration_s', '?'))}s</i>", "",
         "<b>TITLE</b>", esc(t[0])]
    if len(t) > 1:
        L += ["<i>Alternatives:</i>"] + [f"• {esc(x)}" for x in t[1:4]]
    yt_links = "\n".join(f"{k}: {v}" for k, v in link_map.items() if "Instagram" not in k and k != "Facebook")
    L += ["", "<b>YOUTUBE DESCRIPTION</b>", esc(post["youtube_description"] + ("\n\n" + yt_links if yt_links else ""))]
    tags = " ".join(f"#{h.lstrip('#')}" for h in post["hashtags"])
    L += ["", "<b>INSTAGRAM / FACEBOOK CAPTION</b>", esc(post["caption"]), esc(tags)]
    if link_map:
        L += ["", "<b>TRACKED LINKS</b> (bio / link sticker / first comment)"]
        L += [f"{esc(k)}: {esc(v)}" for k, v in link_map.items()]
    if post.get("pinned_comment"):
        L += ["", f"📌 <b>Pinned comment:</b> {esc(post['pinned_comment'])}"]
    if post.get("thumbnail_at") is not None:
        L += [f"🖼 Cover frame: {esc(post['thumbnail_at'])}s"]
    if post.get("sources"):
        L += ["", "<i>Sources:</i> " + " · ".join(esc(s) for s in post["sources"][:5])]
    if post.get("notes"):
        L += ["", f"📝 {esc(post['notes'])}"]
    L += ["", f"<i>Published it? Run</i> <code>ledger.py mark-posted {esc(post['slug'])}</code>"]
    return "\n".join(L)


# ---- sending ----------------------------------------------------------------------------------

def notifier():
    """The notify plugin, else telegram.py if configured, else None (save locally)."""
    p = sc.plugin("notify")
    if p:
        return p
    return telegram if telegram.configured() else None


def send_all(vdir: Path, video: Path, post: dict, text: str, revision: bool) -> tuple[object, int, str]:
    """Send the video and the kit. Returns (message id, parts sent, error or "")."""
    n = notifier()
    if n is None:
        (vdir / "POST-KIT.html").write_text(text.replace("\n", "<br>\n"))
        print(f"  ! no Telegram configured: kit saved to {vdir / 'POST-KIT.html'}")
        return "local", 1, ""
    limit = getattr(n, "UPLOAD_LIMIT", telegram.UPLOAD_LIMIT)
    caption = ("🔁 Revised: " if revision else "🎬 ") + post["titles"][0]
    send_path, size_mb = video, video.stat().st_size / 1e6
    if limit and video.stat().st_size > limit:
        # The render is near-lossless; a CRF 24 copy at the same resolution is typically ~40% of
        # the size and looks the same on a phone. Upload the full file to YouTube yourself.
        small = video.with_name("video-telegram.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-c:v", "libx264", "-preset", "slow",
                        "-crf", "24", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(small)],
                       check=False, timeout=1800)
        if small.is_file() and small.stat().st_size <= limit:
            send_path = small
            caption += f" (compressed for Telegram; full quality: {video})"
    if limit and send_path.stat().st_size <= limit:
        r = n.send_video(send_path, caption=caption, duration=post.get("duration_s"))
    else:   # too big for an upload, or a notifier that never uploads (UPLOAD_LIMIT = 0)
        r = n.send(f"🎬 <b>{esc(post['titles'][0])}</b>\n{size_mb:.0f} MB — "
                   f"the file is at <code>{esc(video)}</code>")
    if not r["ok"]:
        return None, 0, f"video — {r.get('error')}"
    parts = 1
    for chunk in telegram.split_message(text):
        k = n.send(chunk)
        if not k["ok"]:
            return r["message_id"], parts, f"kit — {k.get('error')} (video was sent as msg {r['message_id']})"
        parts += 1
    return r["message_id"], parts, ""


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    vdir = Path(argv[0]).resolve()
    sc.adopt_root_from(vdir)
    sc.load_env()   # Telegram keys from the studio's .env, in interactive runs too
    dry = "--dry-run" in argv
    revision = "--revision" in argv
    try:
        post = json.loads((vdir / "POST.json").read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed: POST.json unreadable — {e}")
        return 1
    errs = validate(post)
    known = any(e.get("slug") == post.get("slug") for e in load())
    if known and not dry and not revision:
        errs.append(f"slug {post.get('slug')!r} is already in the ledger")
    # The reviews must have been passed by separate agents and the linter, not self-graded.
    try:
        plan = (vdir / "PLAN.md").read_text()
    except OSError:
        plan = ""
    for line in PASS_LINES:
        if line not in plan:
            errs.append(f"PLAN.md is missing '{line}' (rubric A16/A18/A19/A20)")
    if post.get("pillar") in PROBLEM_PILLARS:
        if PROBLEM_LINE not in plan:
            errs.append(f"PLAN.md is missing '{PROBLEM_LINE}' (rubric A21)")
        if not (vdir / "research" / "problems.md").is_file():
            errs.append("research/problems.md not found (problem scout, rubric A21)")
        if sc.load().get("review", {}).get("second_opinion_model") and \
                not (vdir / "research" / "second-opinion" / "meta.json").is_file():
            errs.append("research/second-opinion/meta.json not found: run scripts/second_opinion.py (rubric A22)")
    # Every voice line must come from voice_build.py and start and end on silence (B17).
    errs += voice_check(vdir)
    video = vdir / post.get("render", "")
    if not video.is_file():
        errs.append(f"render not found: {video}")
    else:
        errs += fill_errors(video, post)
    if errs:
        print("Failed: " + "; ".join(errs))
        return 1

    today = delivery_date()
    campaign = f"{today:%Y%m%d}-{post['slug']}"[:80]
    link_map = links(post, campaign)
    text = kit(post, link_map)
    size_mb = video.stat().st_size / 1e6

    if dry:
        print(text)
        print(f"Dry run: {post['slug']} {post.get('duration_s', '?')}s {size_mb:.1f}MB links={len(link_map)}")
        return 0
    if revision and not known:
        print(f"Failed: --revision but {post['slug']!r} is not in the ledger")
        return 1

    msg, parts, err = send_all(vdir, video, post, text, revision)
    if err:
        print(f"Failed: delivery {err}")
        return 1

    entries = load()
    previous = next((e for e in entries if e.get("slug") == post["slug"]), None) if revision else None
    if previous:
        entries.remove(previous)
    entries.append({
        "date": today.isoformat(),
        "slug": post["slug"],
        "pillar": post["pillar"],
        "track": post.get("track") or os.environ.get("STUDIO_TRACK") or sc.load()["default_track"],
        "format": post["format"],
        "topic": post["topic"],
        "title": post["titles"][0],
        "product": post.get("product"),
        "service": post.get("service"),
        "utm_campaign": campaign,
        "duration_s": post.get("duration_s"),
        "size_mb": round(size_mb, 1),
        "render_path": str(video),
        "sources": post.get("sources", []),
        "telegram_message_id": msg,   # "local" when the kit was saved instead of sent
        "cost_usd": post.get("cost_usd"),
        **{k: (post.get("look") or {}).get(k) for k in LOOK_FIELDS},
        "posted": None,
        "revisions": (previous.get("revisions", 0) + 1) if previous else 0,
    })
    save(entries)
    # Tell the planner plugin the video is made (never fails the delivery).
    if not os.environ.get("STUDIO_NO_PLANNER"):
        try:
            p = sc.plugin("planner")
            if p:
                print(f"Planner: marked {p.mark_made(today.isoformat(), post, msg)} item(s) made")
        except Exception as e:  # noqa: BLE001
            print(f"  ! planner: {e}")
    # Keep the final render with the archive plugin; a failure is reported, never fatal.
    try:
        a = sc.plugin("archive")
        if a:
            print(f"Archive: {a.store(video, post, revision)}")
    except Exception as e:  # noqa: BLE001
        print(f"  ! archive: {e}")
        n = notifier()
        if n:
            n.send(f"⚠️ archive failed for {esc(post['slug'])}: {esc(str(e))[:300]}")
    print(f"Rendered: {post['slug']} {post.get('duration_s', '?')}s {size_mb:.1f}MB msg {msg} parts={parts}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
