---
version: 1
name: Placeholder brand core (copy to your studio's brand/brand-core.md and edit)
description: >
  The only things every video shares. Everything else about the look (palette, fonts,
  layout grammar, motion vocabulary, transitions, captions) is chosen per video from
  references/looks.md and must differ from recent videos, because videos that share a
  template soon read as AI-generated. This file is what stays. The skill reads
  $STUDIO_ROOT/brand/brand-core.md first and falls back to this placeholder.
---

# Constant

1. **Voice:** one HeyGen voice, `voice.voice_id` in `config.json`. Same voice, every video.
2. **One accent:** the brand accent **`#00D890`** (change it here) appears **at least once**,
   as the accent of whatever look is used: the answer, the CTA, the key word, a highlight.
   The rest of the palette belongs to the look. If the look's own accent is another hue, the
   brand accent replaces it; never two accent hues at once.
3. **End mark:** the last ≤ 2 s carries your handle (**`@yourhandle`** — change it here) in
   the look's own type, with an optional logo (`brand/logo.png`) at ≤ 120 px. **Never on
   frame 0.** It may sit over the loop frame rather than on its own card.
4. **Safe zones:**
   - **9:16 (1080×1920), organic:** meaning in y 200–1440 (x 64–1016 above y 1150,
     x 64–850 below it); captions y 1440–1600; the bottom 1600–1920 continues the scene and
     is never plain empty ground (B18). The usable width is 952 px; centre shared stages with
     `left = 64 + (952 − width) / 2`, and keep their lower part inside x ≤ 850. Paid ads
     only: the old core zone (`platform-specs.md` §1).
   - **16:9 (1920×1080):** content x 96–1824, y 96–860; captions y 880–1000.
   - **Full-bleed footage is allowed** under every zone. Only *text and key UI* must
     respect them.
5. **Truth:**
   - real numbers, from code that actually ran;
   - real product footage and screenshots, never faked UI;
   - every claim sourced in `research/sources.md`.
6. **Type floor:**
   - 9:16: body ≥ 32 px, headlines ≥ 72 px, code ≥ 30 px with ≤ 22 visible chars per line;
   - 16:9: body ≥ 32 px, code 30 px, ≤ 60 chars per line;
   - never a banned font (HyperFrames `typography.md`).

# Not constant (chosen per video — `references/looks.md`)

These change per video:
- palette, beyond the one accent;
- fonts;
- layout grammar;
- motion vocabulary;
- transitions;
- caption skin (`assets/captions/`);
- ground (dark, light or footage);
- textures.

`ledger.py look-check` enforces four rules:
- no family reused within the last `variety.look_family_gap` videos (default 6;
  `ledger.py rotation` puts the least recently used first);
- no hook type repeated from the previous video;
- no caption skin repeated from the previous video;
- no signature beat reused within the last `variety.signature_gap` videos (default 5).

**Banned defaults** (they read as AI-made):
- purple-to-blue gradients, glowing orbs and "AI brain" stock imagery;
- a row of three identical cards or icons;
- a centred title over a blurred background;
- the same caption skin twice in a row;
- an empty bottom 40 % on a Short (B18).

# Fonts available offline

- **Vendored in `assets/fonts/`:** Plus Jakarta Sans and JetBrains Mono (`fonts.css`,
  SIL Open Font License — see `assets/fonts/OFL-*.txt`).
- **Embedded by the HyperFrames compiler with no setup:** Montserrat, Oswald, League
  Gothic, Archivo Black, Space Mono, IBM Plex Mono, JetBrains Mono, Source Code Pro.
- **Anything else** must be a real Google Font, fetched at build time; it triggers a lint
  warning. If your machine can't reach Google Fonts, pick a look whose fonts are on disk.
- **Never** Inter, Roboto, Poppins or the rest of the banned list.
