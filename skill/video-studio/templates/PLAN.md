---
slug: <kebab-case, unique — ledger.py check>
date: <YYYY-MM-DD>
pillar: <ai-term | python | build | tech-blog | blog-explainer | product | service | build-story | longform-ai | longform-sd | companion>
prerequisites: "<what the viewer must already know; anything beyond is introduced on screen>"
format: <short | longform | companion>
aspect: <1080x1920 | 1920x1080>
length: <e.g. 45s>
message: "<the ONE sentence the viewer leaves with>"
audience: "<which developers exactly (the base viewer is fixed: a developer who already codes)>"
product: <brand/products.json "products" key or null>
service: <brand/products.json "services" key or null>
voice: <config voice engine + variant, e.g. pocket, or indicf5 (hi)>
---

# <working title>

## 1. Why this, why today
<2–4 lines: the trend or search evidence (with links), and why it fits the pillar and isn't a repeat.>

## 2. Research summary
<The facts the video stands on, each with a [n] pointing to research/sources.md. For teaching: the
verified solution, its real output (from research/run.txt), complexity, and the edge cases tried.>

## 3. Hooks (subject + tension, then the proof — craft/hooks.md; 3 different types from the library, score /12, best ≥ 8)
| # | Sentence 1 (≤ 14 words: concrete subject + tension) | Proof visible by 1.5 s | On-screen text | Score | Why |
|---|---|---|---|---|---|
| 1 | | | | /12 | |
| 2 | | | | /12 | |
| 3 | | | | /12 | |
**Chosen:** # — <one line why>

## 4. Story spine
<Hook → setup → tension → turn (the insight) → payoff → CTA, one line each, with timestamps.>

## 5. Look (researched, different every video)
- **References (2–3, found this run):** <creator/video + link + what to take from each; how others visualise THIS topic this year>
- **Family:** <references/looks.md family> (base preset <name>). **Why it suits this topic:** <one line>
- **Different from the last 6:** <`ledger.py looks --last 6` → what changes: palette, layout, motion, captions; `look-check` output>
- **Palette:** <the look's palette + where #00D890 lands as the one accent>
- **Type:** <the look's pairing; no banned fonts>
- **Caption skin:** <assets/captions/<name>, ≠ the previous video's>
- **Hook type:** <taxonomy name, ≠ the previous video's>
- **Footage plan:** <real footage/screens full-bleed ≥ 80% for ≥ 50% of runtime? Which beats are full-bleed; first-3 s full-bleed moment; or "none (faceless)">
- **Motion language:** <2–4 rules from hyperframes-animation/rules-index.md, named>
- **Texture / ambient:** <one, at 12–25% opacity, with its motion>
- **Registry blocks to try:** <results of `npx hyperframes catalog --query ...`>

## 5b. Chapter map (long-form only)
| # | Chapter | The question it answers | One-line recap shown at its end |
|---|---|---|---|

## 6. Storyboard (beat by beat)
| Beat | Time | Visual (what moves, and how it explains) | Narration (exact) | On-screen text (≤ 6 words) | Transition |
|---|---|---|---|---|---|
| 1 hook | 0.0–2.0 | | | | |
| … | | | | | |
| end card | | | | | |

## 7. Script (for a developer who already codes — craft/script-voice.md)
- **Pillar template:** <from script-voice.md "Templates per pillar">
- **The new-to-me fact (what a mid-level developer didn't know):**
- **Artifact(s) to save (spoken + on screen ≥ 2 s, in `backticks`):**
- **Named specifics (≥ 3 per 30 s, each sourced):**
- **Rehooks (every 10–15 s):** <time → line>
- **Terms beyond a CS student, with their ≤ 8-word gloss:** <term → gloss, or "none">

<Then the narration only, as read by the voice; it must match the storyboard. Length 35–60 s
(75 s cap) including the studio's sentence pauses (config "pacing"): N sentences × pause + speech
≤ the target. Cut sentences to fit; never shorten the pauses. Ends on the payoff or the
artifact, no recap.>

## 8. Assets
<path — what it is — which beat. Real screenshots/clips first. Generated images: the prompt and why a real asset couldn't do it.>

## 9. CTA and distribution
- **On screen and spoken:** <the one action>
- **Link target:** <product / service / none — deliver.py builds the tracked links>
- **Title options (3):** <≤ 60 chars, curiosity + clarity, no clickbait the video doesn't pay off>
- **Hashtags (5–8):**

## 10. Gate A — rubric
<A1…A17: pass/fail + one note each. A rewrite is recorded here, not hidden.>

### script_lint (A18)
<paste `script_lint.py` output; then the line `A18: PASS` once it passes>

### New-to-me review (A16)
- **The new-to-me fact + the planner's expected answer** (written before the review):
- **Reviewer JSON** (mid-level developer persona, narration + on-screen text only):
- **Judge JSON** (verdict, P0/P1/P2):
- **Fixes, and the re-run if any:**
- `A16: PASS (judge)` ← only if the judge said PASS

### Second opinion (A22, when configured)
- `second_opinion.py` count line, what was adopted and what was rejected (with reasons):
- `A22: second opinion (<model>) adopted N, rejected M`

### Real problem (A21, teaching pillars)
- **Chosen row of `research/problems.md`** (asker's words, links, score):
- `A21: PASS (real problem)` ← only if it totals ≥ 9 with no 0 on Frequency or Everyday

### Cold-viewer hook test (A20)
- **Input given** (first 2 lines, 3-s on-screen text, 3-s frame description — nothing else):
- **Cold viewer JSON:**
- **Match vs the subject, tension and `message`:**
- `A20: PASS (cold viewer)` ← only on a PASS

### Expert accuracy review (A19)
- **Expert JSON** (issues with severity and a simple, true fix):
- **Fixes applied:**
- `A19: PASS (expert)` ← only if a fresh expert run said PASS

## 11. Review (after snapshots, before render)
<Gate B results, what was fixed, and the honest answer to the self-review question.>
