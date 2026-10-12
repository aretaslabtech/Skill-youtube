# Cybiqon's channels (a worked example of brand/pillars.md)

This is the brand file the studio was built and run with, trimmed of paths on our own
machine. Use it to see how specific this file should be. Our real copy also lists the folder
each product's footage lives in.

## Who watches

- **YouTube @itspyguru** (the `itspyguru` track): about 20k subscribers, people learning
  Python. Known for explainers and how-tos, so **no interview questions**. Teaching Shorts
  run 60–90 s at ≤ 2 words/s; long-form deep dives on Wednesday (AI) and Sunday (system
  design or Python).
- **Instagram / Facebook / YouTube @cybiqonai** (the `promo` track, Mon/Thu/Sat): product
  and service promos for people who would use the product or buy the service.
- **YouTube @cybiqonai** (the `blog` track, daily): the day's post on our AI news blog,
  explained.
- **Language:** English. Many viewers speak it as a second language, so no idioms.

## Honest tie-ins

- ai-term, tech-blog: "the daily version of this is on LLMBytes" (our AI news app and blog).
- build: a product that does the grown-up version, only if true (MapWit for scraping;
  LLMBytes for AI pipelines).

## Products (promo track)

| Product (`products.json` key) | Real assets | Watch-outs |
|---|---|---|
| Lumina `lumina` | Play Store feature graphic and screenshots, framed device shots | a puzzle game: gameplay is always real capture |
| Orbitone `orbitone` | Play Store screenshots and feature graphic | — |
| ChitraYatra `chitrayatra` | store screenshots, the launch film, gameplay clips recorded by the game's own capture test | Indian art traditions: name them correctly |
| LLMBytes `llmbytes` | store screenshots, the launch film, llmbytes.dev | headlines on screen must be real and dated |
| MapWit `mapwit` | Chrome Web Store screenshots | show the browser chrome, so it reads as an extension |
| Page Arcade `page-arcade` | Chrome Web Store marquee and screenshots | the page turning into a game is the magic moment |

- **Facts** come from each product's own documentation and store listing. Never invent
  ratings, installs or user counts.
- **Rotation:** never the same product twice in 14 days.

## Services (promo track)

Custom websites, AI agents, WhatsApp automation, Android apps, admin panels, Chrome
extensions and web scraping, for small businesses in India.

- **Audience:** shop owners, clinics, coaching centres, D2C brands. Not developers.
- **Ground:** the light pillar variant.
- **Arc:** the owner's real pain in their words ("customers message at 11pm and you lose
  them") → what it costs → the fix as a before/after → one honest proof → one CTA.
- **Proof:** a demo, a number from a public source, or a real case we built. Never claim
  clients we don't have.
- English voice-over, plain words, an Indian setting; on-screen pain quotes in the
  customer's real phrasing ("Price kya hai?").

## Blog (blog track)

Explain the day's LLMBytes post (published late morning IST, so the blog track runs at
12:30 and retries at 14:00). The tracked link uses the `llmbytes` web link. If the post isn't
live yet, fail the run with `Failed: no blog post for <date>` rather than invent one.
