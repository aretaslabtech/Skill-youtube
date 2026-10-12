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
| A2 | **Hook = their question, then the proof** (`craft/hooks.md`; review feedback: "the hook doesn't make sense"). Line 1, spoken at 0 s and shown as the text hook, is the viewer's own problem in their words ("Why does your shop's website load so slowly?"). A visible comparison or before/after proves it by 3 s. No riddle, metaphor, bare numbers, product name or mechanism first; no logo, title card or "Hey guys" | ✔ |
| A3 | **Three hooks of different types were written and scored out of 12** (`references/craft/hooks.md`); the best scores ≥ 8 (otherwise rewrite), and its reason is written down | ✔ |
| A4 | **Every fact has a source** in `research/sources.md`, and every number on screen traces to one | ✔ |
| A5 | **Code was run.** `research/solution.py` (or the demo script) ran; the output on screen is pasted from `research/run.txt` | ✔ (teaching) |
| A6 | **Every beat has a visual that explains**: a state change, a comparison, a diagram, a real screen. A beat whose visual is only "text appears" is rewritten | ✔ |
| A7 | **Narration ≠ on-screen text.** On-screen text is ≤ 6 words per beat (labels, numbers, the key term), never the sentence being spoken | ✔ |
| A8 | **Pacing (the #1 review note on the first video: "too fast, too much content").** Narration at most **2.0 words/s** of the length; one idea per beat; a **0.4–0.8 s hold after a key reveal** (the answer, a counter landing, the twist, the takeaway). It's a breath, not a stop; review feedback: "a long gap between two sentences… if we can reduce it by 1 second, it will feel better". If it doesn't fit, cut content or go longer (teaching runs 60–90 s). Never compress | ✔ |
| A9 | **Re-hook.** Something new happens at least every 3–4 s on a Short; on long-form, a re-hook every 45–75 s | |
| A10 | **Payoff earned.** The answer or insight lands in the last third, not in the hook (the hook *promises* it) | |
| A11 | **Specific CTA.** One action, named: "next: how RAG finds the right paragraph", "free on Play — link in bio". Never "like and subscribe for more content" | ✔ |
| A12 | **Real assets first.** Product videos use the asset map in `pillars.md`; nothing is faked | ✔ |
| A13 | **Not a repeat.** `ledger.py check <slug> <topic>` passed | ✔ |
| A14 | **The viewer is fixed** (`craft/script-voice.md`): a smart 12-year-old who has used ChatGPT and never coded. PLAN's `audience` line can add context (who shares it, why), but it **can't raise the level**. Review feedback: "the script considers the viewer as an expert, which is wrong" | ✔ |
| A15 | **Every term defined in the same breath.** A term is anything a 12-year-old wouldn't say: jargon, maths words ("divide", "probability"), proper nouns (GPT-2, a lab), acronyms and idioms. Each is cut, or defined with a spoken marker ("which means…", "think of it as…"). On-screen labels don't count | ✔ |
| A16 | **The teach-back review passed, graded by a separate judge** (procedure below). PLAN §10 must contain the literal line `A16: PASS (judge)`; `deliver.py` refuses otherwise | ✔ |
| A17 | **Recaps (long-form).** Every chapter ends on a one-line on-screen recap; the video ends on the map with every chapter filled in | ✔ (long-form) |
| A18 | **`script_lint.py hf/SCRIPT.md` passes**, before audio is generated: no sentence over 18 words, reading grade ≤ 7, ≤ 1 spoken number per 10 s, no jargon before its definition, no idioms. Paste its output into PLAN §10; `deliver.py` checks the line `A18: PASS` | ✔ |
| A20 | **The cold-viewer hook test passed** (procedure below). A stranger with no context, given only the first 3 s, says who it's for and what problem it's about, matching PLAN's `message` and `audience`. PLAN §10 must contain `A20: PASS (cold viewer)`; `deliver.py` refuses otherwise | ✔ |
| A19 | **The expert accuracy review passed** (procedure below). Simplified is fine; false is not. Every "because" is technically true, no analogy plants a misconception, and no advice implies a setting or tool guarantees correctness. PLAN §10 must contain `A19: PASS (expert)`; `deliver.py` refuses otherwise. Added after an outside review of the temperature Short caught three simplifications that had become untrue ("tea came next most often in everything it read", "GPT-2 is an older version of ChatGPT", "low temperature… that's usually right") | ✔ |

### The teach-back review (A16) — rewritten 10 Oct 2026

The first version let an expert-level script through. The reviewer had been told to be
"a developer", it saw the scene lines (which filled in the gaps), and the planner graded the
result itself. Now:

1. **Planner writes 3 "why" questions** into PLAN §10 before the review. Each must be
   answerable only if the mechanism was understood, e.g. "Why does turning it up give
   weirder words?"
2. **Reviewer sub-agent** (fresh, never sees the research, PLAN or storyboard) gets **only
   the narration lines** and the 3 questions, with this persona:
   > You are 12, smart and curious. You've used ChatGPT but never written code, and English
   > is your second language. Someone reads you this script out loud. Then:
   > (1) explain back, in your own words, what you learned and how it works;
   > (2) answer the 3 questions;
   > (3) list every word or step where you'd have stopped and asked "what's that?" or
   > "why?".
   >
   > Reply in JSON: `{"teach_back": "...", "answers": ["...","...","..."],
   > "lost": [{"at": "...", "why": "..."}], "unknown_words": ["..."]}`.
   > You are not grading anyone. Report your confusion honestly; pretending to understand
   > ruins the video.
3. **Judge sub-agent** (a separate fresh agent) gets the PLAN `message`, the 3 questions with
   the planner's model answers, the reviewer's JSON, **and the narration itself**. That way
   it can tell a real gap from a point the script already explains. It replies
   `{"verdict": "PASS" | "FAIL", "P0": [...], "P1": [...], "P2": [...]}`, where:
   - **P0** = the teach-back is wrong, or a "why" answer is wrong. The viewer didn't get it.
   - **P1** = a "lost" point or unknown word that the narration **really leaves
     unexplained**. For each P1 the judge must quote the line where the gap is and say
     what's missing. A point the narration already explains in plain words is **not** a
     P1, however the reviewer felt.
   - **P2** = friction, polish, or a moment that is already explained.

   **PASS** = the teach-back is correct, all 3 answers are correct, and there's no P1. A
   reviewer pausing at a word the script defines is normal listening, not failure.
   *(Revised 10 Oct 2026: the earlier judge saw only the reviewer's notes, so it failed
   points the script already covered. Each round of fixes added words and created new
   pauses, and a 355-word script grew to 482 without ever passing, although every
   teach-back had been correct.)*
3b. **Fixes may not grow the script past its length budget** (A8, script-voice.md
   "Length"). Fix a gap by replacing words with clearer ones, or by cutting a side idea.
   Never by stacking on more explanation. If a fix can't fit, the side idea goes
   (topic split, or the pinned comment).
4. **The planner never overrides the judge.** On FAIL, fix the script and re-run steps 2
   and 3 once, with fresh agents. A second FAIL means the topic is too big for the
   format: split it, or move it to a long-form slot. Write the literal line
   `A16: PASS (judge)` into PLAN §10 **only** when the judge returned PASS.

### The expert accuracy review (A19) — added 10 Oct 2026

The teach-back (A16) checks that a beginner understands. It doesn't check that what they
understood is **true**, and simplifications are exactly where truth slips. Run this
alongside A16, before any audio:

1. **Expert sub-agent** (fresh; give it the narration lines, the on-screen text from the
   storyboard, and `research/sources.md`) with this persona:
   > You are a senior ML engineer / Python core developer / systems engineer (pick the
   > domain) reviewing a beginner video script. Simplification is expected and fine. Flag
   > only what is **false**, what **plants a misconception** a learner will have to unlearn,
   > causal claims ("because…") that are wrong, numbers not supported by the sources, and
   > advice that overclaims (e.g. implies a setting makes answers correct). For each, give a
   > replacement that is just as simple and true.
   >
   > Reply in JSON: `{"issues": [{"severity": "P0|P1|P2", "line": "...",
   > "problem": "...", "simple_true_fix": "..."}], "verdict": "PASS|FAIL"}`.
   > P0 = false; P1 = misleading or overclaiming; P2 = could be sharper. PASS only with no
   > P0 or P1.
2. **Fix every P0 and P1 with its simple, true wording.** Never trade the plain language
   away; a fix that adds jargon fails A15 and A18. Then re-run `script_lint.py`, and if
   any narration changed, A16 too.
3. **Write `A19: PASS (expert)`** into PLAN §10 only when a fresh run of the expert
   returns PASS.

### The cold-viewer hook test (A20) — added 10 Oct 2026

Review feedback on a promo: "the hook doesn't make sense… I am noticing this in
all videos." The hooks had been scored by the planner, who already knew the topic. Run
this after the script is final and before audio:

1. **Cold viewer sub-agent** (fresh). Give it **only** the first two narration lines, the
   on-screen text of the first 3 s, and a plain description of what is visible in those
   3 s, taken from the storyboard. Don't give it the title, the topic, the PLAN or the
   product name, unless the hook itself says it. Persona:
   > You are scrolling Instagram Reels. You know nothing about this video. Here is
   > everything you saw and heard in its first 3 seconds. Reply in JSON:
   > `{"who_is_it_for": "...", "problem": "...", "would_keep_watching": true|false,
   > "why": "...", "confusing": ["anything you didn't get"]}`.
2. **The planner compares** its `who_is_it_for` and `problem` with PLAN's `audience` and
   `message`. PASS only if both match in substance, `would_keep_watching` is true, and
   `confusing` is empty. Otherwise rewrite the hook to the two-part rule and run a fresh
   cold viewer.
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
| B16 | **No dead air.** Silence between consecutive voice lines is ≤ 0.7 s, with at most one deliberate ≤ 1.2 s beat on the payoff. Run `python3 $SKILL_DIR/scripts/gap_check.py hf/` after `sync-durations` and after any hold padding; it exits 1 on violations. Why: a ~2 s gap "between two sentences" in a long-form felt 1 s too long | ✔ |
| B17 | **Every word is heard.** `voice_build.py --check <video>` prints `Voice check: PASS`: every voice line was made by `voice_build.py` (trimmed on its real sound, not on TTS timestamps) and starts and ends on silence. `deliver.py` runs it and refuses otherwise. Why: an earlier per-sentence trim cut the first ~0.2 s off a third of all sentences | ✔ |
| B18 | **The Short fills the frame (9:16).** `scripts/fill_check.py <final.mp4>` prints `B18: PASS`: in ≥ 75 % of 8 sampled frames the stage reaches the lower visual band (y 1150–1440) and the scene continues in the bottom (y 1600–1920), each ≥ 10 % non-ground. `deliver.py` runs it on the render and refuses otherwise (paid ads with `"ad": true` are exempt). Added 12 Oct: we'd used YouTube's ads safe zone, and every Short's bottom 40 % was empty | ✔ |

## The self-review question

Before rendering, answer in `PLAN.md` § Review, in one honest paragraph:

> *Would a developer who has never heard of you send this to a friend? What is the one
> thing in it they couldn't get from the first Google result?*

If the answer is "nothing", the video isn't done.
