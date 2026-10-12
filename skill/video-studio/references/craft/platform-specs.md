# Platform specs (checked Oct 2026)

Where official numbers exist they are marked **[official]**; third-party measurements are
marked **[3p]**. Platform UIs change — if a number here disagrees with the live app on a
phone, the phone wins; update this file.

## 1. Safe zones on 1080×1920 (the numbers)

| Platform | Top | Bottom | Left | Right | Source |
|---|---|---|---|---|---|
| YouTube Shorts (ads safe-zone PNG, read pixel-by-pixel) | **288** | **672** (content must end above y 1248) | 48 | **192** | [3p reading of Google's official overlay] |
| YouTube Shorts (organic estimate) | 120 | 300 (360 with description expanded) | — | 96 | [3p] |
| Instagram Reels (Meta guidance) | **14 % ≈ 270** | **35 % ≈ 672** | 6 % ≈ 65 | 6 % ≈ 65; action buttons cover the right ~230 px in the bottom 40 % | [Meta via Hopper] |
| Instagram/Facebook Reels **ads with a disclaimer** | 270 | **40 % ≈ 768** | 65 | 65 | [Meta via Hopper] |
| Facebook Reels | same Meta 14 / 35 / 6 % | | | | [Meta via 3p] |

**Organic layout (use this).** An earlier version of this table used the **ads** numbers
above (nothing below y 1248), so every Short left its bottom ~40 % empty, and a reviewer
noticed: "the entire content of the short is filled in first 60% height… the bottom
40% is just empty space". Organic Shorts/Reels UI only covers ~the bottom 300–400 px plus the
right action rail. Fill the frame:

| Zone | Box | What may go there |
|---|---|---|
| **Top UI** | y 0–200 | Ground colour, texture, or footage bleeding up. No text |
| **Hook / title** | y 200–440, x 64–1016 | Hook text, kicker, chapter title |
| **Main visual** | y 440–1440; x 64–1016 above y 1150, **x 64–850 below y 1150** (the action rail) | The visual, code, numbers, the answer. **It must use this whole height:** the stage reaches at least y 1400 |
| **Caption band** | y **1440–1600**, x 64–850 | Word-synced captions (no opaque full-width band behind them) |
| **Bottom** | y 1600–1920 | **Never plain empty ground.** The visual, footage or stage continues (bleeds off-frame), or a deliberate ground/horizon/gradient that belongs to the scene. No text, no key numbers |

Instagram's organic overlay hasn't been measured on a phone here; 1600 is a conservative line.
If the phone shows the UI higher, the phone wins (move the caption band up, keep the fill).

**Paid ads profile (only when a piece is a paid ad):** meaning in x 65–888,
y 288–1248, captions 1150–1248. Rubric B18 doesn't apply to ads.

Taller phones may zoom-to-fill (crops the sides) on Meta; keep 65 px side margins even for
background-critical art.

## 2. YouTube Shorts

| Item | Spec |
|---|---|
| Length | Up to **3 min** for square/vertical uploads (on/after 15 Oct 2024) [official]. Anything 16:9 is long-form |
| Copyright | A Short **> 1 min with any active Content ID claim is blocked globally** [official]. Audio-library songs: most usable for 90 s, some 60/30 s. Use royalty-free YouTube Audio Library or our own beds |
| Resolution / fps | 1080×1920, 30 fps CFR (render at the rate you'll upload) |
| Encoding (YouTube's upload recs) [official] | MP4, moov atom at front (faststart), H.264 High, CABAC, progressive, 2 consecutive B-frames, closed GOP = half the frame rate, 4:2:0, VBR; **1080p SDR: 8 Mbps @24–30 fps, 12 Mbps @48–60 fps**; BT.709 primaries/transfer/matrix; audio AAC-LC 48 kHz, 384 kbps stereo |
| Our export | 1080×1920, 30 fps, H.264 High, yuv420p, BT.709 tagged, **12–16 Mbps** (above YouTube's floor, because flat dark graphics band), AAC-LC 48 kHz 320–384 kbps, `-movflags +faststart`. A 45 s Short ≈ 70–90 MB |
| Loudness (house standard) | −14 LUFS integrated, true peak ≤ −1 dBTP; VO peaks −6 to −3 dBFS before the master |
| Views | Since **31 Mar 2025** a view = every start or replay; legacy "engaged views" (Advanced Mode) still drive monetisation and are the right metric for before/after comparisons [official via TechCrunch] |
| Title | ≤ 100 characters; front-load the hook claim in the first ~40 characters (feed truncation). No hashtags in the title unless one is the subject |
| Description | First line restates the promise in different words; credits/sources; no URLs from us (deliver.py appends tracked links) |
| Hashtags [official] | In title or description. Up to **3** from the description show above the title. **> 60 hashtags → all ignored**. Misleading/unrelated tags can get the video removed. We use 3–5: `#python` + one topic tag + one format tag (e.g. `#codinginterview`) |
| Related video [official] | YouTube Studio → Content → the Short → Related video → save. Public/unlisted video from our channel; shows under the handle; needs advanced features; **not settable via API** → put "set related video to X" in `POST.json.notes` |
| Thumbnail / cover [official] | Custom Shorts thumbnail 9:16, recommended 2160×3840, min height 640, desktop Studio only, verified account. Otherwise pick the frame in-app — which is why frame 0 is designed as the cover |
| Long-form thumbnail [official] | 16:9, 3840×2160 recommended, min width 640 px, JPG/PNG, ≤ 2 MB from mobile / 50 MB desktop. Test & Compare (up to 3 variants, long-form only) picks by **watch-time share** |

## 3. Instagram Reels

| Item | Spec |
|---|---|
| Canvas | 1080×1920, 9:16; accepted 1.91:1–9:16 but only 9:16 fills the screen; min width 720 [3p, Hopper Sep 2026] |
| File | MP4 (MOV ok), H.264, AAC ≥ 128 kbps, ≥ 30 fps, ≤ 4 GB [3p] |
| Length | **3 min** in the Reels camera (raised from 90 s in Jan 2025, Mosseri) [official via Engadget]. Uploads reportedly up to 15 min (20 for some accounts) [3p] — we stay ≤ 60 s anyway |
| Cover | Upload 1080×1920. Profile grid is **3:4** since Jan 2025 → centre 1080×1440 shows (240 px cut top and bottom). Treat the cover as final; Hopper reports it can't be changed after posting |
| Hashtags | **Max 5 per post, enforced** (Instagram @creators, Dec 2025); caption + comments share the 5. Use: 1–2 niche (10K–500K posts), 1–2 topic, 0–1 branded |
| Ranking signals | Mosseri (Jan 2025, via secondary reports): **watch time (incl. replays), likes per reach, sends per reach**; sends matter most for non-follower reach — write a takeaway worth sending to a friend, and make it loop |
| Originality | Reposted content is replaced by the original in recommendations; aggregators are removed from recommendations; visible watermarks from other apps are de-ranked. Post our master file directly; never re-upload a YouTube-watermarked export |
| Trial Reels | Toggle "Trial" on the share screen → shown **only to non-followers**, not on the grid or followers' feeds; insights after ~24 h; "Share to everyone automatically" graduates it if it does well in the first 72 h; public accounts with ≥ 1,000 followers. Use it to test a second hook on the same body [3p] |
| Audio | Our VO + bed → shows as "Original audio" (reusable by others = free distribution). Don't add trending licensed songs under VO |
| Captions | Burn in ours (word-synced). Instagram's auto-captions can stay off to avoid double captions |

## 4. Facebook Reels

| Item | Spec |
|---|---|
| Format | Since **June 2025 all new Facebook videos are Reels**; the 90-s Reel cap no longer applies; older videos keep their format [official announcement via RouteNote] |
| Canvas / safe zones | Same as Instagram: 1080×1920, Meta's 14 % / 35 % / 6 % margins |
| Audience | A Reel defaults to the same audience as Feed posts (prompted on first share) |
| Cross-posting | Post natively (not "share to Facebook" from Instagram) when the caption needs a different CTA; same MP4 |

## 5. Caption style (burned-in, all platforms)

- Word-synced from the TTS/transcript timestamps; **2–4 words on screen** (rubric B8), 1 line preferred, 2 max.
- Plus Jakarta Sans 800, **54–70 px**, `text`; the key term of the sentence in `voltage`
  (one word per caption group, not every caption).
- Position: caption band y 1440–1600, left-aligned to x 64 or centred within x 64–850 (never
  under the right rail). On 16:9: bottom 15 %, above the end-screen zone.
- Backing: none on the flat `canvas`; on busy footage use a `canvas@70 %` pill with 12 px radius — never a
  black box or heavy stroke.
- Captions never cover the line of code or the cell being discussed — move the caption band,
  not the content.
- Long-form: also upload an SRT (sources from the same timestamps) for search and accessibility.

## 6. Posting times (example: an Indian + global developer audience)

Public data is thin. SocialPilot's study (~250K Reels, 30K+ accounts) gives a global peak of
8 AM–12 PM Mon–Thu, and sparse India slots: Mon 7:30 pm, Thu 10:30–11:30 am, Fri 10:30 pm,
Sat 8:30 pm IST — not a dev audience. A starting rule for that audience (shift it to yours):

| Content | Slot (IST) | Why |
|---|---|---|
| Daily Short/Reel (Mon–Sat) | **18:30–20:00** | Indian evening commute/after-work + US East-Coast morning (8–12 ET ≈ 18:30–22:30 IST in winter, 17:30–21:30 IST in US summer time) |
| Sunday long-form | **18:30–19:30** | Indian Sunday evening = US Sunday morning; gives the video Monday in both regions |
| Service Reels (Fri) | **20:00–21:30** | Shop owners close up and scroll after business hours |

After 6 posts per slot, switch to the data: YouTube Studio → Audience → "When your viewers are
on YouTube", and Instagram Professional dashboard → "Most active times". Record the change in
your studio notes.

## 7. Pre-upload checklist (for whoever posts; goes in POST.json notes when relevant)

- [ ] 9:16 MP4, 1080×1920, 30 fps, H.264 High, AAC 48 kHz, faststart; ffprobe shows bt709.
- [ ] Meaning inside y 200–1440 (x ≤ 850 below y 1150); captions inside y 1440–1600; the bottom band isn't plain empty ground (B18).
- [ ] Length ≤ 60 s unless every beat changes state; > 60 s → zero licensed music.
- [ ] YouTube: title ≤ 100 chars, 3–5 hashtags, related video set, cover = frame 0.
- [ ] Instagram: ≤ 5 hashtags, cover chosen (frame 0), optional Trial for a hook test.
- [ ] Facebook: posted natively; CTA line fits the Facebook audience (businesses on service days).

## Sources

- https://support.google.com/youtube/answer/15424877
- https://support.google.com/youtube/answer/1722171
- https://support.google.com/youtube/answer/6390658
- https://support.google.com/youtube/answer/14075157
- https://support.google.com/youtube/answer/72431
- https://support.google.com/youtube/answer/13861714
- https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted
- https://www.somake.ai/blog/youtube-shorts-aspect-ratio
- https://www.hopperhq.com/blog/instagram-reel-size/
- https://www.engadget.com/social-media/instagram-swoops-in-with-3-minute-reels-and-rectangular-profile-grids-as-the-tiktok-ban-gets-real-201316339.html
- https://later.com/blog/instagram-hashtags/amp
- https://vistasocial.com/insights/instagram-trial-reels/
- https://dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers
- https://www.socialpilot.co/?p=553523
- https://postplanify.com/tools/youtube-shorts-safe-zone-checker
- https://www.lindseygamble.com/blog/instagram-is-updating-its-ranking-system-to-support-smaller-original-content-creators
- https://routenote.com/blog/all-facebook-videos-are-now-reels/
- https://blog.adobe.com/en/publish/2024/11/04/unlock-potential-reels-best-practices-for-creative-success-using-adobe-creative-cloud
