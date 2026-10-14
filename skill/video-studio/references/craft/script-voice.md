# Script voice: teach a developer something they'll save

**Why this file changed (Oct 2026).** The first rule here was "explain it to a smart
12-year-old who has never coded". It fixed one expert-only script, then overcorrected: the
next scripts defined every term and built the video around an everyday analogy. Review
feedback: "the script itself is too childish. In the end I didn't get anything useful." On
Instagram, 67 % of viewers skipped in the first 3 s and the average watch was 8 s. Research
on what top tech Shorts actually say (Fireship, ByteByteGo, b001, 3Blue1Brown and others) found
the opposite pattern. They name the real thing in the first sentence, use real tools and
numbers without defining the basics, leave one artifact worth saving, and rarely use an analogy.
That research is the basis for this file.

This file overrides any audience line a PLAN might otherwise choose. `scripts/script_lint.py`
checks the mechanical parts (A18). The new-to-me judge (A16) checks the value, and the
cold-viewer test (A20) checks the hook.

## The viewer (fixed, the same for every teaching video)

> **A working developer or CS student who writes code every week and has used ChatGPT or
> Copilot.** Watching on a phone, deciding in under 2 seconds whether to stay. English may be
> their second language, so the sentences are plain, but the content is not dumbed down.

### Known terms: never define these

variable, function, loop, list, dict, class, object, string, API, JSON, HTTP, URL, request,
database, SQL, index, cache, server, client, Git, commit, terminal, command, library,
package, framework, bug, test, deploy, LLM, ChatGPT, prompt, token, model, context window,
thread, async, hash, recursion, CPU, GPU, RAM, latency, memory, file, Docker, cloud.

Defining one of these tells the viewer the video isn't for them.

### Terms beyond a CS student: one clause, right there

A term a final-year CS student might not know (`references/jargon.txt`: epoll, MVCC,
write-ahead log, softmax, KV cache…) gets **one clause of ≤ 8 words**, said right after it
and ideally shown on screen: "epoll, one thread watching every socket". Or cut it. Never
stack two new terms in one sentence.

## The value (what makes it save-worthy)

1. **One artifact, at least.** A command, a code line, a config line, a function name, a real
   number with its unit, or a decision rule ("use X when Y"). It's **spoken and on screen
   for ≥ 2 s**, and in `backticks` in SCRIPT.md's screen notes, so the lint counts it. A list
   video carries 3–5 artifacts.
2. **Specific, every few seconds.** At least **3 named real things per 30 s**: tools,
   functions, companies, versions, dates, measured numbers. Every one is sourced in research
   (A4, A19). "A popular database" fails; "Postgres 17" passes.
3. **Real over analogy.** Show the real output, the real code or the real system. An analogy
   is optional, **one sentence at most, and the very next sentence names the real thing**.
   It is never the spine of the video.
4. **Something new to a mid-level developer.** If the payoff is what a developer already knew
   before pressing play ("caches make things fast"), the video fails A16. Go one level
   deeper: the surprising number, the production failure, the flag nobody uses.

## The hook (the first 3 s decide everything)

- **Sentence 1 is ≤ 14 words, names the concrete subject** (a language, tool, company, number
  or line of code) **plus a tension**: a mistake, a surprise, a stake or a contradiction.
  Use a template from `hooks.md`. Examples: "Python's `lstrip` just deleted half your
  filename." / "Redis runs on one thread and still does 100,000 requests a second." /
  "This one line in CLAUDE.md stopped my agent rewriting whole files."
- **No warm-up.** No "have you ever", "imagine", "in this video", "today we", no greeting, no
  definition, no analogy, no riddle.
- **Proof on screen by 1.5 s**: the code, the output, the number or the diagram, readable
  with the sound off. No logo, title card or brand sting before 3 s.
- **Rehook every 10–15 s.** Use "but", "here's the catch", "the third one is the weird one",
  or a question the next line answers.

## The voice

- One developer showing another something useful at their desk. Not a lecture, not a
  kids' show.
- Say "you", use contractions, and use active verbs.
- Plain sentences: ≤ 20 words spoken (one breath; the lint checks it). Short is better.
- **No idioms or slang** (in a nutshell, game-changer, secret sauce…): the viewer may speak
  English as a second language. Technical words are fine; idioms aren't.
- **No filler sentences.** Each sentence adds a fact, a step or a turn. "This is really
  important" adds nothing, so it goes.

## Templates per pillar

| Pillar | Template |
|---|---|
| python | Mistake → run it (real output) → why → fix (code on screen) |
| ai-term | The model's real behaviour first (actual output, real numbers), then the name, then when it matters |
| build | Result first (the working thing), then the 3 decisions that mattered |
| tech-blog | Stake hook → named people and systems → how it worked → what to do about it |
| system design (companion, long-form) | "N reasons X is fast", **or** a production incident: failure → why → fix → cost |
| AI coding agents | Live agent run → obstacle → mechanism in one line → caveat |

**No interview questions, ever.** An incident or a production gotcha replaces "solve this".

## Logic: every step earns the next

- **No "so" or "that's why" without a cause the viewer has already seen.**
- **Every change gets a true "because".** "…because `lstrip` treats its argument as a set of
  characters."

## Simple, but true

- **Every "because" must be technically true.** If the true cause doesn't fit, say what
  happens without inventing a cause.
- **An analogy may simplify, but not mislead.** If one is used, the next sentence gives the
  real term, and where it breaks if that matters.
- **Advice never implies a setting or tool makes output correct.** "Consistent" yes,
  "right" no. Add the check-it habit where it applies.
- **Proper nouns get their true relationship** (GPT-2 is an older model from OpenAI, not
  "an older ChatGPT").
- **Rubric A19's expert review enforces this.**

## Numbers

Real numbers are specifics, so use them. Say them in a form the ear can hold ("about 100,000
a second", "since 3.9"), and put the exact figure on screen. Every number has a source.

## Length and pace

- **A teaching Short runs 35–60 s; 75 s is the hard cap.** Long-form keeps its own rules.
- Fit the length by **cutting sentences, never by rushing** or trimming the pauses. Fewer,
  denser sentences beat more, thinner ones.
- The pause between sentences is set by the studio (`config.json` "pacing" and
  "voice.gap"; some channels want a full pause after every sentence so each one lands).
  Budget for it: about 10–14 spoken sentences for a 60 s Short with 1 s pauses.
- **A/B option, not a rule:** the research's winners speak at 2.8–3.9 words/s with short
  breaths. To test that against the channel's pause style, render a second variant with
  `voice_build.py --gap 0.35` and short line gaps, post both as trial Reels, and compare
  the skip rate and average watch time after 24 h.

## The ending

- **End on the payoff or the artifact. No recap.**
- CTA ≤ 4 s and send-shaped: "Send this to whoever still uses `lstrip` for this." / "Save
  it for your next migration." Or loop back to the hook's number. "Full video on the
  channel" is never the only reason to stay.

## Self-check before the lint

Read it aloud as a developer with one finger on the screen, ready to swipe:
1. After sentence 1, do I know *what* this is about and *why* I should care?
2. At the end, can I name one thing I didn't know, and someone I'd send it to?
3. Is there any sentence I'd skip?

If 1 or 2 is no, or 3 is yes, rewrite.
