#!/bin/bash
# manim_clip.sh — render one Manim scene to a transparent WebM that a HyperFrames composition
# lays **over** its own graphics (alpha is kept: verified 12 Oct 2026, VP9 alpha_mode=1 renders
# correctly through hyperframes@0.8.145).
#
#   scripts/manim_clip.sh <scene.py> <SceneClass> <out.webm> [--aspect 9:16|16:9] [--opaque]
#
# Manim Community 0.22 lives in its own venv (~/.venvs/manim, 480 MB; system libcairo2-dev +
# libpango1.0-dev, 95 MB). No LaTeX: use Text / MarkupText, not MathTex/Tex.
# Measured: a 6.5 s 1080×1920 scene rendered in 17 s, peak RAM 0.86 GB.
# Prints a count line, never just a status:  manim: <frames> frames, <s>s, <w>x<h> alpha → <out>
set -euo pipefail
MANIM="${MANIM_BIN:-$HOME/.venvs/manim/bin/manim}"
[ -x "$MANIM" ] || { echo "Failed: Manim missing — python3 -m venv ~/.venvs/manim && ~/.venvs/manim/bin/pip install manim"; exit 1; }
SRC="${1:?usage: manim_clip.sh <scene.py> <SceneClass> <out.webm> [--aspect 9:16|16:9] [--opaque]}"
SCENE="${2:?usage}"; OUT="${3:?usage}"; shift 3
ASPECT="9:16"; ALPHA=(-t --format webm)
while [ $# -gt 0 ]; do
  case "$1" in
    --aspect) ASPECT="$2"; shift 2 ;;
    --opaque) ALPHA=(--format mp4); shift ;;
    *) echo "Failed: unknown option $1"; exit 2 ;;
  esac
done
case "$ASPECT" in
  9:16) R=1080,1920 ;;
  16:9) R=1920,1080 ;;
  *) echo "Failed: aspect must be 9:16 or 16:9"; exit 2 ;;
esac
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
"$MANIM" -qh --progress_bar none -r "$R" --fps 30 "${ALPHA[@]}" --disable_caching --media_dir "$WORK" "$SRC" "$SCENE" >/dev/null
CLIP="$(find "$WORK" -type f \( -name '*.webm' -o -name '*.mp4' \) -path '*videos*' ! -path '*partial*' | head -1)"
[ -n "$CLIP" ] || { echo "Failed: Manim produced no clip for $SCENE"; exit 1; }
mkdir -p "$(dirname "$OUT")"
cp "$CLIP" "$OUT"
N="$(ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 "$OUT")"
D="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
A="$(ffprobe -v error -show_entries stream_tags=alpha_mode -of csv=p=0 "$OUT")"
echo "manim: $N frames, ${D%.*}s, ${R/,/x} $([ "$A" = 1 ] && echo alpha || echo opaque) → $OUT"
