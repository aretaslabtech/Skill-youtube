# Quality rubric — the gate against AI slop

Score the plan **before building** (gate A) and the snapshots **before rendering** (gate B).
Each line is pass or fail; there is no partial credit.

- A plan that fails any **hard** line is rewritten. It gets one rewrite; if it fails again,
  pick a different topic.
- A build that fails a hard line in gate B is fixed (at most 2 loops). If it still fails,
  deliver with the failure stated in `POST.json.notes`. Never deliver silently.

## Gate A — the plan (`PLAN.md`)

| # | Check | Hard |
|---|---|---|
| A1 | **One idea.** The `message` is one sentence, and every beat serves it | ✔ |
| A2 | **Hook = subject + tension, then the proof** (`craft/hooks.md`). Sentence 1, spoken at 0 s, is **≤ 14 words and names the concrete subject** (a language, tool, company, number or line of code) **plus a tension** (a mistake, surprise, stake or contradiction), from the hook library. The proof (code, output, number or diagram, readable with the sound off) is on screen **by 1.5 s**. No analogy, definition, riddle, "have you ever", greeting, logo, title card or brand sting in the first 3 s. Why: 67 % of viewers swiped away in the first 3 s on hooks that were clear but named nothing concrete | ✔ |
| A3 | **Three hooks of different types were written and scored out of 12** (`references/craft/hooks.md`); the best scores ≥ 8 (otherwise rewrite), and its reason is written down | ✔ |
| A4 | **Every fact has a source** in `research/sources.md`, and every number on screen traces to one | ✔ |
| A5 | **Code was run.** `research/solution.py` (or the demo script) ran; the output on screen is pasted from `research/run.txt` | ✔ (teaching) |
| A6 | **Every beat has a visual that explains**: a state change, a comparison, a diagram, a real screen. A beat whose visual is only "text appears" is rewritten | ✔ |
| A7 | **Narration ≠ on-screen text.** On-screen text is ≤ 6 words per beat (labels, numbers, the key term), never the sentence being spoken | ✔ |
| A8 | **Length and pauses.** A teaching Short runs **35–60 s, hard cap 75 s** (long-form keeps its own budget). The pause between sentences is the studio's (`config.json` "pacing", "voice.gap"; some channels want ~1 s after every sentence), and speech inside a sentence stays brisk (never slow the voice down to fill time). Fit the length by **cutting sentences**: fewer, denser ones. One idea per beat. Never compress the pauses to fit more in | ✔ |
| A9 | **Re-hook.** Something new happens on screen at least every 3–4 s on a Short, and a spoken rehook ("but", "here's the catch", "the last one is the weird one") lands every 10–15 s; on long-form, a re-hook every 45–75 s | ✔ (Shorts) |
| A10 | **Payoff earned, no recap.** The answer or artifact lands in the last third, not in the hook (the hook *promises* it). The video ends on the payoff or the artifact, not a summary | |
| A11 | **Specific CTA, ≤ 4 s, send-shaped.** One action, named: "Send this to whoever still uses `lstrip` for this", "free on Play — link in bio". Never "like and subscribe for more content" | ✔ |
| A12 | **Real assets first.** Product videos use the asset map in `pillars.md`; nothing is faked | ✔ |
| A13 | **Not a repeat.** `ledger.py check <slug> <topic>` passed | ✔ |
| A14 | **The viewer is fixed** (`craft/script-voice.md`): a working developer or CS student who writes code every week and has used ChatGPT or Copilot. The known terms (function, API, cache, token, model, thread…) are **never defined**. PLAN's `audience` line can narrow it (which developers), but it **can't lower it to non-coders**. Why: the earlier "smart 12-year-old who never coded" rule made scripts that viewers called "childish… I didn't get anything useful" | ✔ |
| A15 | **Specific and save-worthy.** At least **one artifact** (a command, code line, config line, function name, real number with its unit, or a "use X when Y" rule), spoken and on screen for ≥ 2 s; **≥ 3 named real things per 30 s** (tools, versions, companies, dates, measured numbers), each sourced. A term beyond a CS student gets a gloss of ≤ 8 words, or is cut. An analogy is optional, one sentence at most, and the next sentence names the real thing | ✔ |
| A16 | **The new-to-me review passed, graded by a separate judge** (procedure below): a mid-level developer names a concrete thing they didn't know and who they would send the video to. PLAN §10 must contain the literal line `A16: PASS (judge)`; `deliver.py` refuses otherwise | ✔ |
| A17 | **Recaps (long-form).** Every chapter ends on a one-line on-screen recap; the video ends on the map with every chapter filled in | ✔ (long-form) |
| A18 | **`script_lint.py hf/SCRIPT.md` passes**, before audio is generated: hook ≤ 14 words with a concrete subject and no banned opener, no sentence over 20 words, ≥ 3 named specifics per 30 s, no term from `jargon.txt` before its gloss, no idioms. Paste its output into PLAN §10; `deliver.py` checks the line `A18: PASS` | ✔ |
| A20 | **The cold-viewer hook test passed** (procedure below). A developer scrolling Reels, given only the first 3 s, names the concrete subject, the tension and what they expect to learn, and would keep watching. PLAN §10 must contain `A20: PASS (cold viewer)`; `deliver.py` refuses otherwise | ✔ |
| A21 | **A real problem** (`problem-scout.md`). Teaching pillars only. The chosen problem is in `research/problems.md` with the asker's words, ≥ 2 evidence links and a score ≥ 9/15 (no 0 on Frequency or Everyday), and sentence 1 opens on its situation. PLAN §10 must contain `A21: PASS (real problem)`; `deliver.py` refuses otherwise. Added after the read-only-MCP Short: true and built, but about a problem nobody had | ✔ |
| A19 | **The expert accuracy review passed** (procedure below). Simplified is fine; false is not. Every "because" is technically true, no analogy plants a misconception, and no advice implies a setting or tool guarantees correctness. PLAN §10 must contain `A19: PASS (expert)`; `deliver.py` refuses otherwise. Added after an outside review of the temperature Short caught three simplifications that had become untrue ("tea came next most often in everything it read", "GPT-2 is an older version of ChatGPT", "low temperature… that's usually right") | ✔ |

### The new-to-me review (A16) — rewritten Oct 2026

The first version checked that a 12-year-old understood. Scripts passed it and still felt
"childish" to the developers who actually follow a tech page, because nothing in them was
new. Now the review checks **value**:

1. **The planner writes down the new-to-me fact** in PLAN §10 before the review: the one
   concrete thing a mid-level developer probably didn't know, and the artifact they'd save.
2. **Reviewer sub-agent** (fresh, never sees the research, PLAN or storyboard) gets **only
   the narration lines and the on-screen text**, with this persona:
   > You are a mid-level backend developer with 4 years of experience. You write Python and
   > some JavaScript, you use an AI coding assistant daily, and you scroll Reels on your
   > break. Someone shows you this Short. Be honest, not polite. Then:
   > (1) What specific thing did you learn that you didn't know before? Quote it, or say
   > "nothing".
   > (2) Would you save it or send it? To whom, and why?
   > (3) Where would you have swiped away, and why? (a line or a second)
   > (4) Which sentences felt slow, obvious or condescending?
   >
   > Reply in JSON: `{"learned": "...", "already_knew": true|false, "save_or_send": "...",
   > "send_to": "...", "swipe_at": "...", "slow_or_obvious": ["..."]}`.
3. **Judge sub-agent** (a separate fresh agent) gets the PLAN `message`, the planner's
   new-to-me fact, the reviewer's JSON **and the narration**. It replies
   `{"verdict": "PASS" | "FAIL", "P0": [...], "P1": [...], "P2": [...]}`, where:
   - **P0** = the reviewer learned nothing concrete (`already_knew` true, or `learned` is a
     vague concept like "caching matters"), or wouldn't save or send it to anyone.
   - **P1** = a swipe point in the first 15 s, a sentence the reviewer called condescending
     (a known term defined, a kids' analogy), or a term beyond a CS student left unglossed.
     The judge quotes the line.
   - **P2** = polish.

   **PASS** = a concrete `learned`, a named `send_to`, and no P0 or P1.
4. **Fixes may not push the Short past 75 s** (A8). Fix by swapping a weak sentence for a
   sharper one, never by stacking on more.
5. **The planner never overrides the judge.** On FAIL, fix the script and re-run steps 2
   and 3 once, with fresh agents. A second FAIL means the angle is too shallow: go one
   level deeper (a production incident, a measured number), or pick another topic. Write
   `A16: PASS (judge)` into PLAN §10 **only** when the judge returned PASS.

### The expert accuracy review (A19) — added 10 Oct 2026

The new-to-me review (A16) checks that a developer learns something. It doesn't check that
it is **true**, and short, punchy claims are exactly where truth slips. Run this alongside
A16, before any audio:

1. **Expert sub-agent** (fresh; give it the narration lines, the on-screen text from the
   storyboard, and `research/sources.md`) with this persona:
   > You are a senior ML engineer / Python core developer / systems engineer (pick the
   > domain) reviewing a short video script for developers. Brevity is expected. Flag
   > only what is **false**, what **plants a misconception** a learner will have to unlearn,
   > causal claims ("because…") that are wrong, numbers not supported by the sources, and
   > advice that overclaims (e.g. implies a setting makes answers correct). For each, give a
   > replacement that is just as short and true.
   >
   > Reply in JSON: `{"issues": [{"severity": "P0|P1|P2", "line": "...",
   > "problem": "...", "simple_true_fix": "..."}], "verdict": "PASS|FAIL"}`.
   > P0 = false; P1 = misleading or overclaiming; P2 = could be sharper. PASS only with no
   > P0 or P1.
2. **Fix every P0 and P1 with its short, true wording.** Then re-run `script_lint.py`, and
   if any narration changed, A16 too.
3. **Write `A19: PASS (expert)`** into PLAN §10 only when a fresh run of the expert
   returns PASS.

### The cold-viewer hook test (A20) — revised Oct 2026

Hooks scored by the planner, who already knows the topic, kept failing real viewers (first
"the hook doesn't make sense", then a 67 % swipe-away in 3 s). Run this after the script is
final and before audio:

1. **Cold viewer sub-agent** (fresh). Give it **only** the first two narration lines, the
   on-screen text of the first 3 s, and a plain description of what is visible in those
   3 s, taken from the storyboard. Don't give it the title, the topic or the PLAN.
   Persona:
   > You are a working developer scrolling Instagram Reels on a break. You know Python, SQL
   > and the popular AI tools by name, but you have never used the specific library,
   > protocol or flag this video might be about. You swipe away from anything vague, slow,
   > aimed at beginners, or about a problem you don't have. Here is everything you saw and
   > heard in this video's first 3 seconds. Reply in JSON:
   > `{"subject": "the concrete thing it's about", "tension": "what's surprising, wrong or
   > at stake", "my_problem": "the situation in my own work this is about, or null",
   > "unknown_terms": ["every word or name you would have to look up"],
   > "expect_to_learn": "...", "would_keep_watching": true|false, "why": "...",
   > "confusing": ["anything you didn't get"]}`.
2. **The planner checks:** `subject` names the concrete thing (not a category), `tension`
   matches the hook's tension, `my_problem` is a real situation, not null and not "using
   <the tool>", `unknown_terms` and `confusing` are empty, `expect_to_learn` matches PLAN's
   `message` in substance, and `would_keep_watching` is true. Otherwise, rewrite sentence 1
   problem-first (`craft/hooks.md` "Problem before tool") and run a fresh cold viewer.
3. **Write `A20: PASS (cold viewer)`** into PLAN §10, with the JSON, only on a PASS.

## Gate B — the build (snapshots and the contact sheet)

Run `npx hyperframes check --strict --json`, then `npx hyperframes snapshot --at <every
beat midpoint>`, then **Read** `snapshots/contact-sheet.jpg` and every frame PNG.

| # | Check | Hard |
|---|---|---|
| B1 | `check` passes: no contrast errors, no overflow or overlap (ignore 1–4 px on `#caption-word-*`), no `sweep_static` | ✔ |
| B2 | **Safe zones (9:16, organic):** everything essential sits in y 200–1440 (x 64–1016 above y 1150, x 64–850 below it); captions in y 1440–1600; y 0–200 and 1600–1920 carry no text (`references/craft/platform-specs.md` §1) | ✔ |
| B3 | **Readable on a phone:** body ≥ 32 px, headlines ≥ 72 px, code ≥ 30 px with ≤ 22 visible chars per line on 9:16 | ✔ |
| B4 | **One focal point per frame.** The accent (the brand-core accent, default `#00D890`, in every look) appears on at most one element per frame, and at least once in the video | ✔ |
| B5 | **No slop tells:** gradient text, neon cyan or purple, glow stacks, centred card grids, a pure #000 or #fff ground, banned fonts (Inter, Roboto, Poppins, Montserrat-as-display…), stock people, emoji as decoration | ✔ |
| B6 | **Frame 1 works as a thumbnail and cover:** readable title-like text plus a striking visual at t=0 | ✔ |
| B7 | **Motion explains:** at each midpoint, something meaningful is mid-change (a pointer moving, a cell filling, a curve drawing), not a static slide with a drifting background | |
| B8 | **Captions:** word-synced, 2–4 words at a time (the engine groups by speaking speed), inside the caption band (y 1440–1600, x 64–850, set by the caption skin), with the key word in `voltage` | ✔ |
| B9 | **Audio:** the voice is intelligible over the music (BGM at about −20 dB under the voice, ducked); there is no music-only first second on a Short | ✔ |
| B10 | **End mark ≤ 2 s** (handle, optional logo, per `brand/brand-core.md`), and the last frame visually rhymes with the first, so the Short loops | |
| B11 | **Footage fills the screen** (any video with real footage or screen captures). Footage covers **≥ 80% of the frame for ≥ 50% of the runtime**, with one full-bleed footage moment in the first 3 s. Device frames and cards are only transitions in and out, never the main state. Review feedback: "the actual visuals were limited to very small space on screen" | ✔ |
| B12 | **No dead canvas.** No beat midpoint shows more than ~40% empty canvas, except a deliberate held typography beat | ✔ |
| B13 | **Distinct from recent videos.** A fresh sub-agent compares this `look.jpg` with the previous 3 videos' and does **not** call them the same template. `ledger.py look-check` passed: the family is new for the last `look_family_gap` videos (default 6), and the hook type and caption skin differ from the previous video | ✔ |
| B14 | **Final-file review.** Decode ≥ 6 frames from the **final MP4** (`ffmpeg -ss <t> -frames:v 1`), not only browser snapshots, and give them plus the contact sheet to a judge sub-agent that ranks issues P0, P1 and P2: P0 = broken, unreadable or wrong; P1 = looks templated or AI-made, cramped, or empty; P2 = polish. The judge also checks every frame for text that is cut off by the frame edge or overlaps other text or the caption band (the idea behind animate's `tools/textcheck.mjs`), and that the Short fills the frame (B18). Fix every P0 and P1 before delivery | ✔ |
| B15 | **Sound follows motion.** Every key reveal, hit or state change has a sound (tick, pop, thud, whoosh) placed on its frame, and no big reveal lands in silence. Music sits under the voice | |
| B16 | **Pauses, not dead air.** Silence between consecutive voice lines is ≤ config `pacing.max_gap` (default 0.7 s; ~1.3 s for a channel that pauses about 1 s after every sentence), with at most one longer beat ≤ `pacing.payoff_gap` on the payoff. Run `python3 $SKILL_DIR/scripts/gap_check.py hf/` after `sync-durations` and after any hold padding; it reads those limits and exits 1 on violations. Why: a ~2 s gap "between two sentences" felt too long | ✔ |
| B17 | **Every word is heard.** `voice_build.py --check <video>` prints `Voice check: PASS`: every voice line was made by `voice_build.py` (trimmed on its real sound, not on TTS timestamps) and starts and ends on silence. `deliver.py` runs it and refuses otherwise. Why: an earlier per-sentence trim cut the first ~0.2 s off a third of all sentences | ✔ |
| B18 | **The Short fills the frame (9:16).** `scripts/fill_check.py <final.mp4>` prints `B18: PASS`: in ≥ 75 % of 8 sampled frames the stage reaches the lower visual band (y 1150–1440) and the scene continues in the bottom (y 1600–1920), each ≥ 10 % non-ground. `deliver.py` runs it on the render and refuses otherwise (paid ads with `"ad": true` are exempt). Added 12 Oct: we'd used YouTube's ads safe zone, and every Short's bottom 40 % was empty | ✔ |

## The self-review question

Before rendering, answer in `PLAN.md` § Review, in one honest paragraph:

> *Would a developer who has never heard of you send this to a friend? What is the one
> thing in it they couldn't get from the first Google result?*

If the answer is "nothing", the video isn't done.
