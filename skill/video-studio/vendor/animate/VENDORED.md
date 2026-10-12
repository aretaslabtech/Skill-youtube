# Vendored: cth9191/animate

- **Source:** https://github.com/cth9191/animate (`plugins/animate/skills/animate/`)
- **Commit:** `7e5eb56feb2dd573f890e1b7b34748af43d58263` (v0.4.0, 5 Oct 2026)
- **License:** MIT, © 2026 cth9191 (`LICENSE`, kept as required)
- **Vendored:** 12 Oct 2026, for more dynamic videos with less repetition (its pixel style suits
  videos about game design).

**How the studio uses it:** as a second **renderer and technique library**, never as a second
studio. Its intake, check-ins and music are not used. The studio writes a piece (start from
`styles/<style>/demo/`), exports it to MP4 with `../../scripts/animate_clip.sh`, and lays it
into the HyperFrames composition as a full-bleed clip under our voice and captions. See
`SKILL.md` § "Engines" and `references/looks.md` (families tagged `engine: animate`).

**Don't edit files here.** To update, re-vendor a newer commit and re-run the pilot
(`scripts/animate_clip.sh` on `styles/pixel/demo`).
`node_modules/` (Playwright) is local and gitignored.
