# Problem scout — pick a problem people actually have

A teaching video starts from a problem that working developers hit and ask about in
public. It does not start from a fact we found interesting. The scout is a fresh sub-agent
that runs in daily step 1, before anything is chosen. Its only job is to find those
problems, prove that people have them, and rank them.

**Why (owner review, 15 Oct 2026):** "There's no point making a video on a problem which no
one is facing." The mcp-server-read-only Short was true, built and run, but it came from
"confusing or new this week". Nobody had asked how to stop `VACUUM INTO` on a read-only
SQLite connection, so the hook had no problem for the viewer to recognise (see
`craft/hooks.md` "Problem before tool").

## Who has the problem

A developer with 0–5 years of work who meets the problem **every week or every month**. A
20-year veteran would find it ordinary, and that is the point. Edge-case security holes,
version trivia and "did you know" facts score low unless people are visibly asking about
them.

## Where to look (search at least 4 kinds of source, ≥ 12 searches)

| Source | What counts as evidence |
|---|---|
| Stack Overflow (search, tag "frequent" and "votes" tabs) | question views, votes, duplicates closed into it, an answer edited in the last year |
| Reddit: r/learnpython, r/Python, r/ExperiencedDevs, r/cscareerquestions, r/webdev, r/LocalLLaMA, r/ClaudeAI, r/ChatGPTCoding, r/cursor | threads from the last 90 days, upvotes, comment count, "same here" replies |
| GitHub issues on popular tools (the pillar's tools: Python, pip/uv, FastAPI, Django, LangChain, the official agent SDKs, Claude Code, Cursor…) | 👍 reactions, "any update?" comments, duplicates |
| Hacker News "Ask HN" and comment threads | points, and how often the complaint repeats |
| Google "People also ask" and autocomplete ("python why does…", "claude code how to…") | that the question exists in searchers' own words |
| Official forums: Python Discourse, the Anthropic/OpenAI developer forums | reply counts, staff answers |

Quote the asker's own words. The best hook is often the question title itself, tidied up.

## Scoring (0–3 each, max 15)

| Criterion | 0 | 3 |
|---|---|---|
| **Frequency** | one post | many independent askers across ≥ 2 kinds of source, or a question with 100k+ views |
| **Recency** | only before 2024 | asked or still hit in the last 90 days, on current versions |
| **Everyday** | needs an unusual setup | a 0–5-year developer meets it monthly at work |
| **Showable in 35–60 s** | needs a long build-up | the failure and the fix both fit on screen, with a runnable before/after |
| **We can prove it** | we can't reproduce it | we can reproduce it in `research/` and measure the fix |

Discard anything that scores 0 on Frequency or Everyday, whatever its total. Also discard
interview questions (the studio never makes interview content) and anything
`ledger.py check` refuses.

## Output (`research/problems.md`)

```markdown
# Problems — <pillar>, <delivery date>

| # | Problem, in the asker's words | Evidence (≥ 2 links, with the numbers) | F | R | E | S | P | Total |
|---|---|---|---|---|---|---|---|---|
| 1 | "Why does my Claude Code session forget the project rules halfway through?" | [r/ClaudeAI 412↑ 2026-09-30](url) · [GitHub #1234 87👍](url) | 3 | 3 | 3 | 2 | 3 | 14 |
…(8–15 rows)

**Chosen:** #1. **Why:** <one line>. **Situation line for the hook:** "<the viewer's situation, ≤ 14 words>"
```

Then add every row to the problem bank, `research/problem-bank.json` under the studio
root (`studio_config.root()`). Each row is `{problem, pillar, evidence, score, found,
used_by}`. The next run reads the bank first: a high-scoring, unused problem from the last 30
days can be picked without searching again, as long as its evidence is re-checked for
recency.

## Planned topics

When the planner gives a topic, the scout doesn't choose the subject. It finds the
real problems people have **with that topic**, and the video is built on the top one. If
the scout finds no problem that scores ≥ 9 for the topic, say so in the delivery message
(`planned topic has no visible problem: <evidence>`). Still make the video from the best
problem found, because the planner is the owner's call.

## Gate A21 (rubric)

PLAN §1 cites the chosen row of `research/problems.md`: the asker's words and ≥ 2 evidence
links. Write `A21: PASS (real problem)` into PLAN §10 only when the chosen problem totals
≥ 9, has no 0 on Frequency or Everyday, and its situation is sentence 1's situation.
`deliver.py` refuses a teaching video (ai-term, python, build, longform-ai, longform-sd,
companion) without that line or without `research/problems.md`.

## Scout prompt (give it to a fresh sub-agent, nothing else)

> You are a research assistant for a developer-education channel. Find the problems that
> working developers (0–5 years of experience) are actually hitting **this quarter** in
> <pillar scope, e.g. "Python itself" / "using AI coding tools and LLM APIs" / "building
> small Python tools">. Do at least 12 web searches across at least 4 kinds of source:
> Stack Overflow, Reddit (subs: …), GitHub issues of popular tools, Hacker News, Google
> "People also ask", official forums. For each problem, quote the asker's words and give
> ≥ 2 links with their numbers (views, upvotes, 👍, comments, date). Score each problem
> 0–3 on Frequency, Recency, Everyday, Showable in 35–60 s, and We can prove it (the
> rubric is below), and return 8–15 rows as the markdown table in this format, sorted by
> total. Skip interview questions. Don't invent numbers: if a count isn't visible, write
> "n/a" and score lower. Already made (skip these): <ledger topics, last 90 days>.
> <rubric and table format pasted from this file>
