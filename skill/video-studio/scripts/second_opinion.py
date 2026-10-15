#!/usr/bin/env python3
"""Second opinion on a script from a different model family, via OpenRouter (rubric A22).

The gates A16/A19/A20 are judged by Claude sub-agents, so the writer and every judge share
one model's blind spots. An owner reviewing the scripts found that they passed A16 and still
taught nothing (Oct 2026). This sends the finished script to another model twice:

  review   it grades the script against the studio's rules and returns P1/P2 issues with fixes;
  rewrite  it writes its own script from the same brief and facts, without seeing ours.

The planner reads both, adopts what is true and better, and records the outcome in PLAN §10
(`A22: second opinion (<model>) adopted N, rejected M`). Accuracy still goes through A19.

    python3 second_opinion.py videos/<dir>                # model from config review.second_opinion_model
    python3 second_opinion.py videos/<dir> --model openai/gpt-6.1-sol

Needs OPENROUTER_API_KEY (studio .env). Writes research/second-opinion/{review.json, rewrite.md,
meta.json}. Prints a count line: `second-opinion: model=… issues=N p1=N rewrite_sentences=N`.
With no model configured or no key, prints `second-opinion: skipped (…)` and exits 0.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_config as sc  # noqa: E402

URL = "https://openrouter.ai/api/v1/chat/completions"
RULES = """Studio rules for a teaching Short (35-60 s, 9:16):
- The viewer is a working developer who already codes. Never define basics; gloss only terms beyond a CS student in <= 8 words.
- Sentence 1 (<= 14 words) is the viewer's own situation plus a tension: a problem they already have, in their words. The tool or trick's name comes later, as the answer ("problem before tool").
- The proof (code, output, number) is on screen by 1.5 s. A rehook every 10-15 s.
- The viewer must LEARN something concrete and usable: at least one artifact to save (a code line, command, setting, number or "use X when Y" rule), >= 3 named real things per 30 s.
- No sentence over 20 words, no idioms, no recap at the end, no interview-question framing.
- Every claim must be true and backed by the facts given; never invent numbers."""


def read(p: Path, limit: int = 12000) -> str:
    try:
        return p.read_text()[:limit]
    except OSError:
        return ""


def brief(vdir: Path) -> str:
    plan = read(vdir / "PLAN.md", 4000)
    front = plan.split("\n---", 2)[0] if plan.startswith("---") else plan[:1500]
    problems = read(vdir / "research" / "problems.md", 6000)
    chosen = problems[problems.find("**Chosen:**"):] if "**Chosen:**" in problems else ""
    return "\n\n".join(x for x in (
        "PLAN front matter:\n" + front,
        "The problem it answers (from the problem scout):\n" + chosen,
        "Verified facts and real program output (research/run.txt):\n" + read(vdir / "research" / "run.txt", 6000),
        "Sources (research/sources.md):\n" + read(vdir / "research" / "sources.md", 4000),
    ) if x.strip().endswith(":") is False)


def ask(model: str, key: str, system: str, user: str, as_json: bool) -> tuple[str, dict]:
    body = {"model": model, "messages": [{"role": "system", "content": system},
                                         {"role": "user", "content": user}]}
    if as_json:
        body["response_format"] = {"type": "json_object"}
    # Only the two headers the API needs: no X-Title / HTTP-Referer, so nothing names the studio.
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    return data["choices"][0]["message"]["content"], data.get("usage", {})


def main(argv: list[str]) -> int:
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    vdir = Path(argv[0])
    sc.adopt_root_from(vdir)
    sc.load_env()
    model = argv[argv.index("--model") + 1] if "--model" in argv else \
        sc.load().get("review", {}).get("second_opinion_model", "")
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not model or not key:
        print(f"second-opinion: skipped ({'no review.second_opinion_model' if not model else 'no OPENROUTER_API_KEY'})")
        return 0
    script = read(vdir / "hf" / "SCRIPT.md", 20000)
    if not script:
        print(f"Failed: {vdir}/hf/SCRIPT.md not found")
        return 1
    facts = brief(vdir)
    out = vdir / "research" / "second-opinion"
    out.mkdir(parents=True, exist_ok=True)

    review_sys = ("You are a senior developer-educator reviewing a script for a 35-60 s developer Short, "
                  "written by another AI. Be blunt and specific. " + RULES)
    review_user = (facts + "\n\nTHE SCRIPT:\n" + script + "\n\nReturn JSON only: "
                   '{"verdict": "PASS"|"REVISE", "what_a_developer_learns": "one sentence, or \\"nothing concrete\\"", '
                   '"hook_verdict": "does sentence 1 name a problem the viewer already has?", '
                   '"issues": [{"severity": "P1"|"P2", "line": "quote", "problem": "...", "fix": "rewritten line"}], '
                   '"better_hook": "<= 14 words, problem first"}')
    review_raw, u1 = ask(model, key, review_sys, review_user, as_json=True)
    try:
        review = json.loads(review_raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", review_raw, re.S)
        review = json.loads(m.group(0)) if m else {"verdict": "UNPARSED", "raw": review_raw, "issues": []}
    (out / "review.json").write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n")

    rewrite_sys = "You write scripts for 35-60 s developer Shorts (YouTube Shorts / Instagram Reels). " + RULES
    rewrite_user = (facts + "\n\nWrite the narration script for this Short from scratch: one sentence per line, "
                    "numbered, 9-14 sentences. Under each sentence, one indented line 'SCREEN:' saying what is on "
                    "screen (only things the facts above support). End with one line 'LEARNS:' naming what a "
                    "developer takes away.")
    rewrite, u2 = ask(model, key, rewrite_sys, rewrite_user, as_json=False)
    (out / "rewrite.md").write_text(f"# Rewrite by {model} (it never saw our script)\n\n{rewrite.strip()}\n")

    issues = review.get("issues") or []
    p1 = sum(1 for i in issues if str(i.get("severity", "")).upper() == "P1")
    sentences = len(re.findall(r"^\s*\d+[.)]", rewrite, re.M))
    meta = {"model": model, "usage": {"review": u1, "rewrite": u2}, "verdict": review.get("verdict"),
            "issues": len(issues), "p1": p1, "rewrite_sentences": sentences}
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"second-opinion: model={model} verdict={review.get('verdict')} issues={len(issues)} p1={p1} "
          f"rewrite_sentences={sentences}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
