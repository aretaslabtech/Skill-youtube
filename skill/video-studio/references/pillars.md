# Content pillars

`scripts/ledger.py today` names today's pillar, keyed off the **delivery** morning (an
overnight run makes tomorrow's video). The rotation lives in `config.json` → `tracks`; the
default is:

| Mon | Tue | **Wed** | Thu | Fri | Sat | **Sun** |
|---|---|---|---|---|---|---|
| ai-term | python | **longform-ai** | build | tech-blog | ai-term or python | **longform-sd** |

Your channel's specifics — audience, products, honest tie-ins, where the real footage lives —
are in **`brand/pillars.md`** in your studio (`studio_config.brand_file("pillars.md")`). Read
it together with the pillar's section below.

**Defaults that came from watching real viewers:**
- **Teaching Shorts run 35–60 s (75 s cap), for a developer who already codes**
  (`craft/script-voice.md`). Sentence 1 names the subject plus a tension; every Short leaves
  an artifact worth saving. Pauses between sentences follow the studio's config; the length
  comes from cutting sentences, not rushing. (An earlier 60–90 s, beginner-level default
  read as "childish", and 67 % of viewers swiped away in 3 s.)
- **Two long-form videos a week** go deeper than a Short can.
- **No interview-question format** by default: explainers and how-tos travel further.

Every teaching video may carry one honest tie-in from `brand/pillars.md`. Never invent a
tie-in that doesn't fit. "Follow for the next one" is a fine CTA.

**Where to find what's trending (research step 1):**
- AI: Hacker News front page, the Anthropic/OpenAI/Google/Meta release notes, Hugging
  Face trending, GitHub trending (Python), r/LocalLLaMA.
- Python: python.org "What's New", PEP index, the Python Discourse, real PyPI release
  notes.
- System design: questions people ask on r/ExperiencedDevs, engineering blogs (Discord,
  Stripe, Cloudflare, Netflix tech blogs), and the concepts behind this week's AI news
  (e.g. "how does a vector DB index work").

Pick what's **confusing or new this week**, not what's evergreen-and-saturated.

---

## ai-term — one AI term through the model's real behaviour, 35–60 s

Examples: RAG, embeddings, tokens, context window, MCP, agents, fine-tuning vs prompting,
quantization, temperature, hallucination, distillation, attention, vector search.

- **Arc:** the model's real behaviour first (actual output, real numbers: "same prompt,
  temperature 0 vs 1.5") → the name → the mechanism in one or two true sentences → when it
  matters in real code (the setting, the flag, the decision rule) → the artifact. Follow
  `craft/script-voice.md`: written for a developer, no kids' analogy.
- **Rules:**
  - Numbers on screen come from running something (`research/solution.py`, e.g. a real
    tokenizer count or a real cosine similarity), or from a cited source.

## python — a Python mistake, gotcha or new feature, 35–60 s

Examples:
- 3.13/3.14 features: free-threaded build, the new REPL, template strings, deferred
  annotations;
- concepts: the GIL, generators, decorators, async, context managers, `__slots__`, the
  walrus, `match`.

- **Arc:** mistake → run it (real output) → why → fix (code on screen), or the new
  feature's result first → the old way → a real run → when to use it.
- **Rules:**
  - Every snippet is run on the stated Python version, and the output pasted from
    `run.txt`.
  - Name the version on screen.
  - "New" claims cite the official "What's New" page.

## build — build a small thing in Python, 35–60 s

Examples: a CLI in 20 lines, a web scraper, a mini RAG over a PDF, a Telegram bot, a file
organizer, a QR generator.

- **Arc:** the finished thing working (result first) → the 3 decisions that mattered,
  each showing the code that changed and its visible effect → it runs.
- **Rules:**
  - The project is **actually built and run** in `research/` (pin the versions).
  - Every step on screen is a real state of that code; the final run's output is
    real.
  - At most ~8 lines of code on screen at once; cut to the lines that changed.

## tech-blog — the week's biggest AI or tech story, for developers, 35–60 s

- **Arc:** stake hook (named company, system, number) → the named people and systems →
  how it actually worked → what a developer should do about it (the artifact).
- **Rules:** claims follow the **primary source** (the lab's announcement, the paper),
  never a write-up of it. Where they disagree, the primary source wins.

## blog-explainer — explain one written post, 90–150 s, 16:9 (it is embedded in the post)

- **Footage:** the real source page, captured in a browser at 2× with a highlighter drawn on
  the exact sentences being discussed (read the rectangles from the DOM, never guess them).
- **Rules:** every claim comes from the post's own cited sources, re-verified (A19).

## promo — a product or service (the `promo` slot alternates them)

### product — a product in action, 30–50 s

Use the real assets listed in `brand/pillars.md` (store screenshots, recorded gameplay or
UI, launch films). Always prefer them over anything generated.

- **Arc:** the moment of magic in the first 2 s → the problem it solves → 2–3 real
  moments → proof (a real number you can cite) → one CTA.
- **Rules:**
  - Never fake UI.
  - Never invent ratings, installs or user counts.
  - Facts come from the product facts named in `brand/pillars.md`.
- **Rotation:** don't promote the same product twice in 14 days (`ledger.py today` lists
  them).

### service — a service you sell, 30–50 s

- **Audience:** the business owner who would buy it. Not developers.
- **Arc:** the buyer's real pain in their words ("customers message at 11pm and you lose
  them") → what it costs → what the fix looks like, shown with a before/after → one honest
  proof → one CTA.
- **Rules:**
  - No invented clients or testimonials.
  - Proof can be a demo, a number from a public source, or a real case you can show.

## longform-ai and longform-sd — the deep dives, 16:9, 4–8 min

- **longform-ai:** a trending AI tool or topic, explained in depth. What it is, how it
  works under the hood, a real demo or worked example, when to use it, and its limits.
  Examples: "MCP, explained by building one", "How coding agents actually edit your
  code", "What a reasoning model does differently".
- **longform-sd:** a system-design or Python deep dive. Examples: caching and
  invalidation, rate limiting (token bucket vs sliding window), message queues,
  consistent hashing, how a vector DB index works (HNSW), how Python's dict is
  implemented.
- **Don't repeat the week's other long-form area.**

**Arc (both):**
1. **Cold open (0–20 s):** the result, the problem, or the surprising fact. No logo, no
   "welcome".
2. **Promise (by 30 s):** "by the end you'll be able to …", specific.
3. **Map (30–45 s):** 3–5 chapters drawn as a path. It returns at each chapter break
   with the finished chapter ticked.
4. **Chapters:** each is a mini hook → build → payoff loop on its own consistent
   stage, ending on a **one-line recap** shown on screen.
5. **Biggest payoff at ~70%:** the "aha" diagram or demo.
6. **Recap (last 30–45 s):** the map, fully filled, one line per chapter.
7. **One CTA:** the next video, or one honest tie-in.

**Rules:**
- **Prerequisites are named in PLAN.md.** Anything beyond them is introduced on screen
  before it's used.
- Every term is defined in one plain line at first use.
- Every demo is real (run in `research/`).
- **Fresh-viewer review** (rubric A16) is mandatory before audio.
- System design diagrams follow the ByteByteGo rule: a fixed structure (≤ 7 boxes per
  frame) with one moving flow.

## companion — the long-form's best idea as a 9:16 Short, 35–60 s

Made on long-form days after the long-form is delivered: its own hook, the same research and
look family, the full gates, and an ending that points to the long version.

## build-story (optional) — how you built something

If you write about your own work (a blog, release notes, a post-mortem), one true finding
with numbers makes a strong 35–60 s Short. The CTA is the product or the write-up.
