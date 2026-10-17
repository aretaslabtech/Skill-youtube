"""Tests for the studio's deterministic parts. Run from scripts/: python3 -m unittest

Every test runs against a throwaway STUDIO_ROOT holding a fixture config.json and
brand/products.json, so nothing here reads or writes a real studio, and nothing is sent.
"""
import json
import os
import tempfile
import subprocess
import unittest
from datetime import date, datetime
from pathlib import Path

os.environ["STUDIO_NO_PLANNER"] = "1"
_ROOT = tempfile.TemporaryDirectory()
os.environ["STUDIO_ROOT"] = _ROOT.name
for k in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
    os.environ.pop(k, None)

# Three tracks, the way a channel with a teaching rotation, product promos and a daily blog
# explainer would set them up (see examples/cybiqon/config.json).
CONFIG = {
    "timezone": "Asia/Kolkata",
    "default_track": "daily",
    "tracks": {
        "daily": {"days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
                  "rotation": {"mon": "ai-term", "tue": "python", "wed": "longform-ai", "thu": "build",
                               "fri": "tech-blog", "sat": "either:ai-term|python", "sun": "longform-sd"}},
        "promo": {"days": ["mon", "thu", "sat"], "rotation": "promo"},
        "blog": {"rotation": "blog-explainer"},
    },
}
PRODUCTS = {
    "products": {
        "my-app": {"name": "My App", "url": "https://play.google.com/store/apps/details?id=com.example.app"},
        "my-tool": {"name": "My Tool", "url": "https://example.com/tool", "web": "https://example.com"},
    },
    "services": {"websites": {"name": "Websites", "url": "https://example.com/services/websites"}},
    "contact": {"label": "Contact", "url": "https://example.com/contact"},
}
(Path(_ROOT.name) / "brand").mkdir()
(Path(_ROOT.name) / "config.json").write_text(json.dumps(CONFIG))
(Path(_ROOT.name) / "brand" / "products.json").write_text(json.dumps(PRODUCTS))

import deliver  # noqa: E402
import post_text  # noqa: E402
import ledger  # noqa: E402
import studio_config as sc  # noqa: E402
import voice_build  # noqa: E402

deliver.fill_errors = lambda video, post: []  # B18 has its own tests; fixtures use fake MP4s


class Config(unittest.TestCase):
    def test_defaults_fill_what_config_leaves_out(self):
        c = sc.load()
        self.assertEqual(c["variety"]["look_family_gap"], 6)
        self.assertIn("ai-term", c["pillars"])
        self.assertEqual(c["timezone"], "Asia/Kolkata")

    def test_user_tracks_replace_the_default_tracks(self):
        self.assertEqual(sorted(sc.load()["tracks"]), ["blog", "daily", "promo"])

    def test_voice_defaults_to_the_open_source_english_engine(self):
        self.assertEqual(sc.load()["voice"]["engine"], "pocket")

    def test_brand_falls_back_to_the_placeholder(self):
        self.assertEqual(sc.brand_file("products.json").parent.name, "brand")
        self.assertTrue(sc.brand_file("brand-core.md").is_file())

    def test_no_plugins_by_default(self):
        self.assertIsNone(sc.plugin("links"))

    def test_env_file_fills_but_never_overrides(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / ".env").write_text("# c\nSTUDIO_T_A=from-file\nexport STUDIO_T_B=\"quoted\"\nSTUDIO_T_C=file\n")
            os.environ["STUDIO_ENV_FILE"] = str(Path(d) / ".env")
            os.environ["STUDIO_T_C"] = "already-set"
            try:
                sc.load_env()
                self.assertEqual((os.environ["STUDIO_T_A"], os.environ["STUDIO_T_B"], os.environ["STUDIO_T_C"]),
                                 ("from-file", "quoted", "already-set"))
            finally:
                for k in ("STUDIO_ENV_FILE", "STUDIO_T_A", "STUDIO_T_B", "STUDIO_T_C"):
                    os.environ.pop(k, None)

    def test_studio_track_env_picks_the_track(self):
        os.environ["STUDIO_TRACK"] = "blog"
        try:
            self.assertEqual(ledger.today_plan(date(2026, 10, 13))["track"], "blog")
        finally:
            del os.environ["STUDIO_TRACK"]

    def test_root_is_taken_from_a_video_path(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "config.json").write_text("{}")
            (Path(d) / "videos" / "2026-10-12-x").mkdir(parents=True)
            saved = os.environ.pop("STUDIO_ROOT")
            try:
                sc.adopt_root_from(Path(d) / "videos" / "2026-10-12-x")
                self.assertEqual(sc.root(), Path(d).resolve())
            finally:
                os.environ["STUDIO_ROOT"] = saved

    def test_a_chatty_planner_plugin_cannot_corrupt_todays_json(self):
        import contextlib, io
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "planner.py").write_text(
                "def topic(day, track, pillar, slot):\n    print('! planner: offline')\n    return 'tokens'\n"
                "def context(day, track):\n    print('noise')\n    return {'x': 1}\n")
            (Path(d) / "config.json").write_text(json.dumps({"plugins": {"planner": "planner.py"}}))
            saved = os.environ["STUDIO_ROOT"]
            os.environ["STUDIO_ROOT"] = d
            del os.environ["STUDIO_NO_PLANNER"]
            out = io.StringIO()
            try:
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                    ledger.main(["today"])
            finally:
                os.environ["STUDIO_ROOT"] = saved
                os.environ["STUDIO_NO_PLANNER"] = "1"
            plan = json.loads(out.getvalue())
            self.assertEqual((plan["planned_topic"], plan["planner_context"]), ("tokens", {"x": 1}))


class Rotation(unittest.TestCase):
    def test_every_weekday_resolves_to_a_known_pillar(self):
        for d in range(5, 12):  # 5–11 Oct 2026, Mon–Sun
            self.assertIn(ledger.today_plan(date(2026, 10, d))["pillar"], sc.load()["pillars"])

    def test_wednesday_and_sunday_are_longform_16x9(self):
        for d in (date(2026, 10, 14), date(2026, 10, 11)):  # Wed, Sun
            p = ledger.today_plan(d)
            self.assertEqual((p["format"], p["aspect"]), ("longform", "1920x1080"))

    def test_shorts_are_vertical_and_teaching_runs_35_to_60s(self):
        p = ledger.today_plan(date(2026, 10, 12))  # Mon
        self.assertEqual((p["pillar"], p["aspect"], p["length"]), ("ai-term", "1080x1920", "35-60s"))

    def test_promo_slots_alternate_product_and_service(self):
        days = [date(2026, 10, 12), date(2026, 10, 15), date(2026, 10, 17), date(2026, 10, 19)]  # Mon Thu Sat Mon
        got = [ledger.resolve_pillar("promo", d, [], ["mon", "thu", "sat"]) for d in days]
        self.assertEqual(got, ["product", "service", "product", "service"])

    def test_tracks(self):
        self.assertIsNone(ledger.today_plan(date(2026, 10, 13), "promo")["pillar"])     # Tue: no promo
        self.assertIn(ledger.today_plan(date(2026, 10, 15), "promo")["pillar"], ("product", "service"))
        self.assertEqual(ledger.today_plan(date(2026, 10, 13), "blog")["pillar"], "blog-explainer")
        # The blog video is embedded in the post, so it is 16:9.
        self.assertEqual(ledger.today_plan(date(2026, 10, 13), "blog")["aspect"], "1920x1080")
        self.assertTrue(ledger.today_plan(date(2026, 10, 14))["companion"])            # Wed long-form

    def test_unknown_track_fails_loudly(self):
        with self.assertRaises(SystemExit):
            ledger.today_plan(date(2026, 10, 13), "nope")

    def test_either_picks_the_less_recent_pillar(self):
        e = [{"pillar": "ai-term", "date": "2026-10-05"}, {"pillar": "python", "date": "2026-10-06"}]
        self.assertEqual(ledger.resolve_pillar("either:ai-term|python", date(2026, 10, 10), e), "ai-term")
        e.append({"pillar": "ai-term", "date": "2026-10-08"})
        self.assertEqual(ledger.resolve_pillar("either:ai-term|python", date(2026, 10, 10), e), "python")

    def test_night_runs_deliver_next_morning(self):
        tz = sc.tz()
        self.assertEqual(ledger.delivery_date(datetime(2026, 10, 8, 23, 0, tzinfo=tz)), date(2026, 10, 9))
        self.assertEqual(ledger.delivery_date(datetime(2026, 10, 9, 2, 30, tzinfo=tz)), date(2026, 10, 9))
        self.assertEqual(ledger.delivery_date(datetime(2026, 10, 9, 17, 59, tzinfo=tz)), date(2026, 10, 9))


class Repeats(unittest.TestCase):
    entries = [{"date": "2026-10-01", "slug": "two-sum", "topic": "Two Sum with a hash map", "title": "Two Sum in O(n)"}]

    def test_same_slug(self):
        self.assertIsNotNone(ledger.check("two-sum", "anything", self.entries, date(2026, 10, 8)))

    def test_similar_topic(self):
        self.assertIsNotNone(ledger.check("ts2", "Two Sum hash map O(n)", self.entries, date(2026, 10, 8)))

    def test_similar_topic_is_refused_at_any_age(self):
        self.assertIsNotNone(ledger.check("ts2", "Two Sum hash map O(n)", self.entries, date(2026, 12, 1)))

    def test_long_stored_topic_still_catches_a_short_repeat(self):
        entries = [{"date": "2026-10-11", "slug": "too-many-requests",
                    "topic": "Rate limiting: why ChatGPT says 'too many requests', the token bucket, buckets per person"}]
        self.assertIsNotNone(ledger.check("x", "Rate limiting why ChatGPT says too many requests", entries, date(2026, 11, 1)))

    def test_same_day_companion_is_not_a_repeat(self):
        entries = [{"date": "2026-10-11", "slug": "too-many-requests", "topic": "Rate limiting too many requests"}]
        self.assertIsNone(ledger.check("too-many-requests-short", "Rate limiting too many requests", entries, date(2026, 10, 11)))

    def test_different_topic(self):
        self.assertIsNone(ledger.check("embeddings", "vector embeddings explained", self.entries, date(2026, 10, 8)))


def post(**kw):
    p = {"slug": "s", "pillar": "ai-term", "format": "short", "topic": "t", "render": "hf/renders/video.mp4",
         "titles": ["A"], "youtube_description": "d", "caption": "c", "hashtags": ["python"],
         "thumbnails": [{"file": f"thumbs/{n}.png", "text": n.upper()} for n in "abc"],
         "look": {"look_family": "whiteboard", "caption_skin": "underline-bar", "hook_type": "question"}}
    p.update(kw)
    return p


class Variety(unittest.TestCase):
    hist = [
        {"slug": "a", "look_family": "navy-code", "hook_type": "number-claim", "caption_skin": "glow-word"},
        {"slug": "b", "look_family": "documentary", "hook_type": "result-first", "caption_skin": "boxed-word"},
        {"slug": "c", "look_family": "glass-diorama", "hook_type": "question", "caption_skin": "band-karaoke"},
    ]

    def test_family_used_recently_is_rejected(self):
        self.assertTrue(ledger.look_check("navy-code", "stakes", "underline-bar", self.hist))

    def test_family_older_than_the_gap_is_fine(self):
        hist = self.hist + [{"slug": f"d{i}", "look_family": f"f{i}", "hook_type": "stakes", "caption_skin": "glow-word"}
                            for i in range(6)]
        self.assertEqual(ledger.look_check("navy-code", "question", "boxed-word", hist), [])

    def test_rotation_puts_never_used_families_first(self):
        hist = [{"look_family": "a", "date": "d1"}, {"look_family": "b", "date": "d2"}]
        order = [r["family"] for r in ledger.rotation(hist, ["a", "b", "c"])]
        self.assertEqual(order, ["c", "a", "b"])

    def test_looks_md_lists_all_families(self):
        fams = ledger.families()
        self.assertGreaterEqual(len(fams), 22)
        self.assertIn("pixel-era", fams)

    def test_repeating_previous_hook_or_caption_is_rejected(self):
        errs = ledger.look_check("whiteboard", "question", "band-karaoke", self.hist)
        self.assertEqual(len(errs), 2)

    def test_signature_beat_may_not_repeat_within_five(self):
        entries = [{"look_family": f"f{i}", "signature": "era-morph" if i == 0 else f"s{i}"} for i in range(5)]
        self.assertTrue(any("signature" in e for e in ledger.look_check("new", "", "", entries, "era-morph")))
        self.assertFalse(ledger.look_check("new", "", "", entries + [{"look_family": "x"}], "era-morph"))

    def test_deliver_requires_a_look_block(self):
        p = post(); p.pop("look")
        self.assertTrue(any("look" in e for e in deliver.validate(p)))


class Deliver(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(deliver.validate(post(product="my-app")), [])

    def test_rejects_urls_and_unknown_slugs(self):
        errs = deliver.validate(post(caption="see https://x.y", product="nope", service="nah"))
        self.assertEqual(len(errs), 3)

    def test_links_are_tracked(self):
        m = deliver.links(post(product="my-app", service="websites"), "20261008-s")
        self.assertIn("referrer=utm_source%3Dyoutube%26utm_medium%3Dvideo%26utm_campaign%3D20261008-s", m["YouTube"])
        self.assertTrue(m["Service (Instagram)"].endswith("?utm_source=instagram&utm_medium=video&utm_campaign=20261008-s"))
        self.assertEqual(m["Contact"], PRODUCTS["contact"]["url"])

    def test_web_link_for_a_product_with_a_site(self):
        self.assertIn("Web", deliver.links(post(product="my-tool"), "c"))

    def test_teaching_video_without_tie_in_has_no_links(self):
        self.assertEqual(deliver.links(post(), "c"), {})

    def test_dry_run_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            voice(v)
            render(v)
            (v / "POST.json").write_text(json.dumps(post(product="my-tool", titles=["T1", "T2"])))
            (v / "PLAN.md").write_text("## 10\n" + "\n".join(deliver.PASS_LINES + (deliver.PROBLEM_LINE,)) + "\n")
            self.assertEqual(deliver.main([str(v), "--dry-run"]), 0)

    def test_without_telegram_the_kit_is_saved_and_logged(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            voice(v)
            render(v)
            (v / "POST.json").write_text(json.dumps(post(slug="local-one")))
            (v / "PLAN.md").write_text("\n".join(deliver.PASS_LINES + (deliver.PROBLEM_LINE,)) + "\n")
            self.assertEqual(deliver.main([str(v)]), 0)
            self.assertTrue((v / "POST-KIT.html").is_file())
            self.assertEqual(ledger.load()[-1]["slug"], "local-one")
            self.assertEqual(ledger.load()[-1]["telegram_message_id"], "local")
            self.assertEqual(deliver.main([str(v)]), 1)  # the same slug twice is refused

    def test_refuses_without_judge_and_lint_pass(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            render(v)
            (v / "POST.json").write_text(json.dumps(post()))
            (v / "PLAN.md").write_text("A16: pass (self-graded)\n")
            self.assertEqual(deliver.main([str(v), "--dry-run"]), 1)

    def test_refuses_a_teaching_video_without_a_real_problem(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            voice(v)
            render(v)
            (v / "POST.json").write_text(json.dumps(post()))
            (v / "PLAN.md").write_text("\n".join(deliver.PASS_LINES) + "\n")
            self.assertEqual(deliver.main([str(v), "--dry-run"]), 1)
            (v / "PLAN.md").write_text("\n".join(deliver.PASS_LINES + (deliver.PROBLEM_LINE,)) + "\n")
            (v / "research" / "problems.md").unlink()
            self.assertEqual(deliver.main([str(v), "--dry-run"]), 1)

    def test_a_promo_needs_no_problem_scout(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            voice(v)
            render(v)
            (v / "research" / "problems.md").unlink()
            (v / "POST.json").write_text(json.dumps(post(pillar="promo", product="my-tool")))
            (v / "PLAN.md").write_text("\n".join(deliver.PASS_LINES) + "\n")
            self.assertEqual(deliver.main([str(v), "--dry-run"]), 0)

    def test_refuses_a_voice_line_cut_on_speech(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            voice(v, starts_on_speech=True)
            render(v)
            (v / "POST.json").write_text(json.dumps(post()))
            (v / "PLAN.md").write_text("\n".join(deliver.PASS_LINES + (deliver.PROBLEM_LINE,)) + "\n")
            self.assertEqual(deliver.main([str(v), "--dry-run"]), 1)
            self.assertIn("01.wav starts or ends on speech", " ".join(voice_build.check(v)))

    def test_refuses_voice_not_made_by_voice_build(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            voice(v)
            (v / "hf" / "assets" / "voice" / "voice_build.json").unlink()
            self.assertIn("no voice_build.json", voice_build.check(v)[0])


def render(v: Path):
    (v / "hf" / "renders").mkdir(parents=True, exist_ok=True)
    (v / "hf" / "renders" / "video.mp4").write_bytes(b"\0" * 1000)
    (v / "thumbs").mkdir(exist_ok=True)
    for n in "abc":   # packaging gate (A24): three designed thumbnails
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=navy:s=1280x720",
                        "-frames:v", "1", str(v / "thumbs" / f"{n}.png")], check=True)
    (v / "research").mkdir(exist_ok=True)
    (v / "research" / "problems.md").write_text("# Problems\n")


def voice(v: Path, starts_on_speech: bool = False):
    """A one-line voice folder as voice_build.py leaves it: a tone with silent edges + manifest."""
    import math, struct, wave
    out = v / "hf" / "assets" / "voice"
    out.mkdir(parents=True)
    sr = 8000
    lead = 0 if starts_on_speech else int(0.1 * sr)
    tone = [int(12000 * math.sin(2 * math.pi * 220 * n / sr)) for n in range(int(0.5 * sr))]
    with wave.open(str(out / "01.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(struct.pack(f"<{lead + len(tone) + 800}h", *([0] * lead + tone + [0] * 800)))
    (out / "voice_build.json").write_text(json.dumps({"files": {"01.wav": voice_build.sha1(out / "01.wav")}}))


class PostText(unittest.TestCase):
    """Rubric A23: the text published under the video."""

    def test_six_hashtags_are_refused(self):
        errs, _ = post_text.check_post(post(hashtags=["a", "b", "c", "d", "e", "f"]))
        self.assertTrue(any("6 hashtags" in e for e in errs))

    def test_five_topic_hashtags_pass(self):
        errs, _ = post_text.check_post(post(caption="Python 3.15 makes UTF-8 the default.",
                                            hashtags=["python", "utf8", "unicode", "pep686", "coding"]))
        self.assertEqual(errs, [])

    def test_generic_tag_and_hashtag_opener_are_refused(self):
        errs, _ = post_text.check_post(post(hashtags=["python", "fyp"]))
        self.assertTrue(any("#fyp" in e for e in errs))
        errs, _ = post_text.check_post(post(caption="#python tip: set a timeout."))
        self.assertTrue(any("first line" in e for e in errs))

    def test_invisible_characters_em_dashes_and_curly_quotes_are_fixed(self):
        p = post(caption="requests\u200b has no timeout \u2014 it \u201cwaits\u201d.")
        _, notes = post_text.check_post(p)
        self.assertEqual(p["caption"], 'requests has no timeout, it "waits".')
        self.assertTrue(any("fixed" in n for n in notes))

    def test_arrows_ranges_and_urls_are_left_alone(self):
        text = "scores 0.73\u20130.82 \u2192 0.39 https://a.example/x\u2014y"
        self.assertEqual(post_text.clean(text)[0], text)

    def test_hindi_keeps_its_joiners(self):
        text = "\u0915\u094d\u200d\u0937 \u2014 test"
        cleaned, _ = post_text.clean(text)
        self.assertIn("\u200d", cleaned)
        self.assertNotIn("\u2014", cleaned)

    def test_deliver_refuses_eight_hashtags(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            voice(v)
            render(v)
            (v / "POST.json").write_text(json.dumps(post(pillar="product", product="my-app",
                                                         hashtags=list("abcdefgh"))))
            (v / "PLAN.md").write_text("\n".join(deliver.PASS_LINES) + "\n")
            self.assertEqual(deliver.main([str(v), "--dry-run"]), 1)

    def test_deliver_writes_the_cleaned_caption_back(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            voice(v)
            render(v)
            (v / "POST.json").write_text(json.dumps(post(slug="clean-one", pillar="product", product="my-app",
                                                         caption="Tap once \u2014 that\u2019s it.")))
            (v / "PLAN.md").write_text("\n".join(deliver.PASS_LINES) + "\n")
            self.assertEqual(deliver.main([str(v), "--dry-run"]), 0)
            self.assertIn("\u2014", json.loads((v / "POST.json").read_text())["caption"])  # dry run writes nothing
            self.assertEqual(deliver.main([str(v)]), 0)
            saved = json.loads((v / "POST.json").read_text())
            self.assertEqual(saved["caption"], "Tap once, that's it.")
            self.assertNotIn("_text_check", saved)


if __name__ == "__main__":
    unittest.main()
