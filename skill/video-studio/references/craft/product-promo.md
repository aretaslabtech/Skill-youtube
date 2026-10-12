# Product and service promos — demo-led, native, true

Product days spend the audience that teaching days earn. The only way that works is if a
product video is as watchable as a teaching one: it shows the thing doing something
surprising, with real footage, in the first two seconds. Everything below assumes the
asset map in your `brand/pillars.md` and facts you can cite for the product.

## What the platforms' own creative research says

| Source | Finding | Our rule |
|---|---|---|
| Google, 2,000+ Shorts ads | Winners are "Shorts-first": look like organic Shorts, low-key tone, conversational, scrappy production beats polish, open with a question; for action goals put the invitation at the very start | No ad aesthetics: no logo sting, no stock music swell, no slogan cards |
| Google ABCD (Kantar, 11,000 ads) | **A**ttract from the first frame (tight framing, large text, strong contrast, sound on), **B**rand naturally, **C**onnect emotionally, **D**irect with a clear CTA → +30 % short-term sales likelihood | Brand = the product's UI on screen, not a logo; CTA = one named action |
| Meta Reels analysis (via Adobe) | 9:16 + sound on + safe zones + ≥ 1 extra element (human presence, text overlay, voice-over, lo-fi, early hook) → −20 % CPC, +56 % CTR, +93 % ThruPlay | Always VO + on-screen labels + safe zones; add a human element (your voice/face, a real user's message) when we have one |
| TikTok auction-ads guide | ~63 % of highest-CTR ads show the key message/product in the first 3 s; fast tracks (~120 BPM+) correlate with higher view-through; story still matters | Product visible by 1.5 s; music bed ~110–125 BPM for product, calmer for teaching |
| Google Play promo-video practice | One YouTube URL (public/unlisted, embeddable, ads off); only the first ~30 s may autoplay **muted**; real app within 10 s and ≥ 80 % real UX; no "Best", "#1", "Top", "New", prices, testimonials or "Download now"; no black bars or nested frames | Play cut: captions burned in, app on screen at 0 s, no ranking/price words, cleared music only (a claim re-enables ads) |
| Chrome Web Store listing guide | Screenshots/video must show the actual UX of the current version (1280×800 shots); no claims like "Editor's Choice"/"Number One"; no superlatives | Extension videos show the real popup/page; claims only from facts you can cite |

## The spine: Problem → Moment of magic → Proof → CTA

Default order on Shorts/Reels is **magic first**, then the problem it removed (result-first hook).

| Beat | Short (30 s) | What's on screen | Rules |
|---|---|---|---|
| Magic (hook) | 0–3 s | The one action that shows the value, real recording | The "aha" is a *state change*: map pins → spreadsheet rows; plain page → arcade game; level solved |
| Problem | 3–8 s | The painful old way, fast (a manual copy-paste loop, a boring tab) | Viewer's words, not ours ("copying 200 addresses by hand") |
| How (2–3 moments) | 8–22 s | Real screen recordings/screenshots, zoomed to the relevant 40 % of the UI | Each moment = one feature as an outcome; cut login/setup/menus |
| Proof | 22–26 s | One real number or real user words | From your product facts or the store console only |
| CTA | 26–30 s | Store badge / "Free on Play" / "Chrome Web Store" + the product name | One action; no URL typed by us (deliver.py builds tracked links) |

Write the script **backwards from the magic moment**: pick the single action that makes a
viewer go "oh", then find the shortest path to it. If the product needs > 2 steps before
anything visible happens, start the video *after* those steps.

## Show, don't tell — footage rules

- **Real UI only**: store screenshots, framed device shots, launch-film captures, or a
  fresh screen recording. Never recreate an app's UI in HTML and pass it off as the app.
  The one exception is an app that shows private data (a finance app): use a recreated UI
  with demo data and say nothing that implies it is a capture of real data.
- **Device frames**: one consistent frame per video; the screen occupies ≥ 55 % of the frame
  width on 9:16. No angled 3-D phone mockups floating in space (slop tell).
- **Zoom, don't shrink**: push in to the 30–40 % of the screen that matters (600–900 ms
  ease-in-out), hold ~0.6–0.8 s, pull out. A full phone screen at 9:16 shows text at ~1/3 size —
  unreadable.
- **Cursor/tap**: show taps as a 48 px ring that pulses once (`caution`), only on the tap that
  matters. Hide the system cursor in recordings; add our own.
- **Blur** personal data, notifications, other apps; record with a clean test account.
- **Speed**: real-time for the magic moment (it must feel believable); 1.5–2× for setup if any
  setup is shown at all, with a small "2×" tag.
- **Sound**: UI sounds from the recording are kept low (−24 dB) — they're proof it's real.

## Social proof — only what exists

Allowed (from your own records or store consoles, with the date): installs, rating and
review count, a real review quoted verbatim with the reviewer's display name, a real
client's words with permission, a GitHub star count, press mentions.
Not allowed: "trusted by thousands", "loved by developers", invented testimonials, stock
avatars, logos of companies that aren't customers, "#1", "best". If there's no proof yet,
the proof beat is a **demonstration** (a timer: "3 s to export 120 rows") — measured live.

## Product-specific playbook

| Type | Magic moment candidates | Watch-outs |
|---|---|---|
| Mobile puzzle game | A level resolving in one move; a new world's mechanic doing its trick | Gameplay must be real capture; show 2–3 s of satisfying loop; no fake "level 999" |
| Chrome extension | The page transforms on click; data appears in a sheet | Show the browser chrome so it reads as an extension; 16:9 for the store listing (screenshots 1280×800), 9:16 crop for Reels |
| News or feed app | A morning's AI news collapsing into 5 bytes | Headlines on screen must be real and dated; no invented stories |
| Finance app | A recreated UI with demo data only | Never real captures of anyone's finances |

## Services for small businesses (Reels/Facebook) — worked example: India

This section was researched for one market (small businesses in India buying websites, AI
agents and WhatsApp automation). Keep the method, swap the facts for your market.

The viewer is a shop owner, clinic, coaching centre or D2C seller, scrolling in the evening
on Android, often with sound on in Hindi/regional-language feeds.

**Trust signals that matter here** (each one must be real):
- A real person: your own voice (a clone of it is fine) and, when available, your face for 2–3 s.
- A real place: "Built in India, for Indian businesses" only if true for that piece of work;
  city name if the work was local.
- Real past work: a client site or bot we actually built (with permission), shown live.
- Price clarity in **₹** from your published prices, never "starting at" numbers we don't offer.
- A WhatsApp number/keyword as the channel — WhatsApp is where these owners already do
  business: Meta's India MD reported (Feb 2024) that ~60 % of its 500 M+ Indian WhatsApp users
  interact with a business on WhatsApp every week.
- Language: Indian-language internet users already outnumbered English users in 2016
  (234 M vs 175 M, Google–KPMG), and that report is widely quoted as finding most users trust
  local-language content more. A workable rule: English VO, but
  **on-screen pain quotes in the customer's real phrasing**, Hinglish where that's how they
  say it ("Price kya hai?", "Delivery kab tak?"), in Latin script so it renders in our fonts.

**Spine for a service Reel (30–40 s)** — light ground (`light-ground`), `FOR BUSINESSES` kicker:
1. 0–3 s **The owner's pain in their words**: a phone with 30 unread "price kya hai?" chats.
2. 3–10 s **Before/after split**: left, the owner typing the same reply at 11 pm; right, the bot
   answering in 2 s with catalogue + price + UPI link (a demo build, labelled "demo").
3. 10–25 s **How, in 3 steps**: what the owner sends us → what we set up → what the customer sees.
4. 25–32 s **Proof**: real client result or a live demo timer. No invented "40 % more sales".
5. 32–38 s **CTA**: WhatsApp-green button + "Message 'BOT' on WhatsApp" (a keyword you
   actually answer), your handle.

**Native, not salesy** — fails if any is true:
- [ ] The first 3 s look like an ad (logo, slogan, stock music swell, stock office footage).
- [ ] More than one CTA, or a CTA before the proof.
- [ ] Adjectives instead of outcomes ("powerful", "seamless", "cutting-edge", "AI-powered" as the
      selling point).
- [ ] A claim the owner couldn't back up on a phone call tomorrow.
- [ ] Fake WhatsApp chats presented as real customers (demo chats must be labelled "demo").
- [ ] English corporate phrasing in the pain beat ("streamline customer engagement") instead of
      how the owner actually talks.

## Meta Click-to-WhatsApp reference case

WhatsApp Business's success story for **The Little Farm Co** (Indian pickle brand): video
creatives in Click-to-WhatsApp campaigns drove **46 % more messages at 32 % lower cost**;
Instagram video was the best-performing placement (self-reported by Meta). Lesson: for Indian
SMB offers, a video whose CTA opens a WhatsApp chat beats one that sends people to a website.
Organic Reels can use the same creative grammar, so they can be boosted later as ads
without re-cutting.

## Sources

- https://business.google.com/in/think/marketing-strategies/short-form-video-advertising-tips/
- https://business.google.com/us/think/future-of-marketing/creative-best-practices-youtube-ads/
- https://blog.adobe.com/en/publish/2024/11/04/unlock-potential-reels-best-practices-for-creative-success-using-adobe-creative-cloud
- https://megadigital.ai/en/blog/tiktok-ad-creative/
- https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf
- https://developer.chrome.com/docs/webstore/best-listing
- https://www.guidejar.com/blog/how-to-create-a-video-product-demo-that-actually-sells-in-5-steps
- https://whatsappbusiness.com/resources/success-stories/the-little-farm-co/
- https://www.applaunchflow.com/blog/google-play-promo-video-requirements-2026
- https://www.storyboard18.com/how-it-works/meta-doubles-down-on-whatsapp-business-in-india-23713.htm
- https://www.theweek.in/news/sci-tech/Indian-language-Internet-usage-has-overtaken-English.html
- https://www.lindseygamble.com/blog/instagram-is-updating-its-ranking-system-to-support-smaller-original-content-creators

## Footage fills the screen

Two early product Shorts kept the real footage in small device frames and cards. Review
feedback: "the actual visuals were limited to very small space on screen. They could have
gone full screen at places."

- **Full-bleed by default.** Crop real footage to 9:16 and let it fill the frame. Device
  frames are a transition in or out (a beat of context), never the main state. Rubric
  B11: ≥ 80% of the frame for ≥ 50% of the runtime, and a full-bleed moment in the first
  3 s.
- **Punch in on the action:**
  - reframe with `hyperframes-keyframes` (punch-in, Ken Burns) toward where the thing
    happens: the bricks breaking, the pane turning;
  - pre-bake big zooms into the clip with ffmpeg
    (`crop=…,scale=1080:1920`), so the `<video>` isn't nested in a transformed wrapper.
    That also avoids the assembler bug in `SKILL.md`.
- **Labels go on the footage:**
  - lower-thirds, callout rings, arrows and a word-level highlight over the frame, on a
    soft scrim (`canvas@60%`) when the footage is busy;
  - don't shrink the footage to make room for text beside it.
- **Vary the footage treatment per video** (the look decides): documentary push-ins,
  split-screen before/after, picture-in-picture over a diagram, a collage of 3 moments, or a
  full-bleed loop with kinetic type over it.

