# Vendored: Jakeschincariol/instagram-agent-skill (text tools only)

- **Source:** https://github.com/Jakeschincariol/instagram-agent-skill
  (`skills/ig-caption/caption.py`, `skills/ig-human/{humanize.py,detect.py,slop.json}`)
- **Commit:** `d03c56bb598be770c60b201f94237e5d1a4268a6` (13 Sep 2026)
- **License:** MIT (`LICENSE`, kept as required)
- **Vendored:** 17 Oct 2026, because nothing checked the text published under a video: all 12
  kits of 15–17 Oct carried 6–8 hashtags against Instagram's cap of 5.

**How the studio uses it:** only through `../../scripts/post_text.py` (rubric A23), imported
in-process. The tools are pure text in, text out: no network, no subprocess, and no file writes
except `humanize.py --out`. Its eleven other skills (reel writing, hook scoring, DMs, comments,
stories, planning) are not vendored: our hook gates (A2, A3, A18, A20) already cover the
script, and the rest manage an account rather than make a video.

**Don't edit files here.** To update, re-vendor a newer commit and run
`python3 scripts/test_studio.py`.
