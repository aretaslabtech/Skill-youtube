# Script voice: explain it to a smart 12-year-old

**Review feedback** on an LLM-temperature Short: "the visuals & frames of this
video was very good… but what's bad was the script itself; the script considers the viewer
as an expert, which is wrong. The script should be like you are explaining to a 5 year old,
but not too easy, using proper example. Also explain any other term if it's there in the
script."

This file overrides any audience line a PLAN might otherwise choose. `scripts/script_lint.py`
checks the mechanical parts. The review in rubric A16 checks whether a viewer actually
understands.

## The viewer (fixed, the same for every teaching video)

> **A smart 12-year-old who has used ChatGPT and never written code.** Curious, quick,
> English is often their second language, watching on a phone.

Developers enjoy a clear beginner explanation; a beginner can't use an expert one. If a
sentence only makes sense to someone who already knows the topic, it fails.

## The voice

- A friendly older sibling at the kitchen table, not a lecturer and not "developer to
  developer".
- Say "you" and "we", and use contractions ("it's", "you'll", "don't").
- Short sentences: ≤ 15 words spoken, never over 18 (enforced by the lint).
- Stay concrete: name the actual thing ("the word *tea*"), not a category ("the
  highest-probability token").
- **No idioms or slang:** long shot, flatter odds, under the hood, at the end of the day,
  ballpark, game-changer, no-brainer, deep dive. Many viewers speak English as a second language, so say
  it plainly.
- One small moment of warmth or humour per video: a callback, a sound word
  ("plink!"), or a tiny joke about the example. It mustn't be a pun on jargon.

## The spine (every concept video; replaces the old Format B)

| # | Beat | What it must do | Bad → good (temperature, 10 Oct) |
|---|---|---|---|
| 1 | **Foundation** | What the thing does at all, in one sentence, before anything else | (missing) → "When ChatGPT writes, it picks one word at a time, like filling in a blank." |
| 2 | **Problem** | A situation the viewer has lived, which this concept solves | (missing) → "Ever pressed *regenerate* and got a different answer? Sometimes you want that. Sometimes you really don't." |
| 3 | **One everyday analogy that *is* the mechanism** | Kept for the whole video. Every step of the real thing happens *to the analogy* | "scores ÷ T" → "Picture a jar of paper chits. Tea has the most chits, so it usually comes out." |
| 4 | **Watch it work** | Run the real thing (a simulation or real output) on the analogy's terms | "Twenty rolls: seven teas…" → "Let's pull 20 chits. Tea, tea, coffee, tea… mostly tea." |
| 5 | **Turn the knob** | Change one thing; show the effect and say **because** | "gaps double" → "Turn it down, and tea gets even more chits, so it wins almost every time." |
| 6 | **Name it** | The real term only now, attached to what they already understand | "…the temperature" (first line) → "That knob has a name: **temperature**." |
| 7 | **Where the analogy breaks** | One honest line | "There's no real jar; it's numbers. But the numbers behave like chits." |
| 8 | **One real use** | A concrete when-to-use, with an example | "low for facts and code" → "Writing code? Keep it low, so you get the same answer. Naming your startup? Turn it up." |
| 9 | **Takeaway + loop** | One sentence they could repeat to a friend | "Low means safe and the same; high means surprising." |

## Terms: anything a 12-year-old wouldn't say

- **A term is** jargon (token, model, parameter, embedding, API), maths operations and
  words (divide, probability, distribution, percentage points, exponential), proper nouns
  (GPT-2, Anthropic, a research lab), acronyms, and any idiom.
- **Each term is either cut, or defined in the same breath** with a definition marker:
  "which means", "think of it as", "is like", "is just", "that's called", "we call this".
  Example: "GPT-2, which is an older, smaller cousin of ChatGPT".
- **Never stack two new terms in one sentence.**
- **On-screen labels don't count as definitions.** The words alone must work, because
  half of viewers don't read the screen.

## Logic: every step earns the next

- **No "so", "that's why" or "this means" without a cause the viewer has already seen.**
- **Every change gets a spoken because:** "…*because* tea now has even more chits."
- **No surprise twist that needs new expert ideas.** If the topic has a deep footnote
  (servers drifting, sampling algorithms), it goes in a long-form video or the pinned
  comment, not the Short.

## Simple, but true (added 10 Oct 2026)

An outside review of the temperature Short found three simplifications that had become
untrue:
- "tea came next most often in everything it read" (the model learns what comes next *in
  this kind of sentence*; it doesn't count raw frequencies);
- "GPT-2 is an older version of ChatGPT" (it's an older AI from the same company;
  ChatGPT is a product);
- "keep it low… that's usually right" (low temperature means *consistent*, not
  *correct*).

So:
- **Every "because" must be technically true**, not just intuitive. If the true cause is
  too hard, say what happens without inventing a cause.
- **An analogy may simplify, but not mislead.** Name where it breaks (spine beat 7),
  including the biggest simplification ("it picks word-pieces, not whole words").
- **Advice never implies a setting or tool makes output correct.** "Steady" or
  "predictable" yes; "right" no. Add the check-it habit ("still test the code").
- **Proper nouns get their true relationship**, said simply ("an older AI from the company
  that made ChatGPT").
- **Rubric A19's expert review enforces this.**

## Numbers

- At most **one spoken number per ~10 s** (lint-checked).
- Round them ("about half", "almost every time", "1 in 20"). Exact figures go on screen,
  where the eye can compare them.
- Say a percentage as a picture: "54 %" becomes "about half the jar".

## Length

Understanding comes first. A concept Short runs **60–90 s**, longer only if the topic needs it. Cut beats,
never the foundation, the problem or the because-lines.

## Self-check before the lint

Read the script aloud and imagine a 12-year-old's face. For each sentence:
1. Would they need to ask "what's that?"
2. Would they need to ask "why?"

If either, rewrite the sentence.
