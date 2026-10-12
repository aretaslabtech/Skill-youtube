#!/bin/bash
# animate_clip.sh — render an animate piece (vendor/animate, cth9191, MIT) to an MP4 clip that a
# HyperFrames composition lays in as a full-bleed video.
#
#   scripts/animate_clip.sh <piece-dir> <out.mp4> [--aspect 9:16|16:9|1:1] [--fps 30]
#
# <piece-dir> holds piece.json + src/ (start by copying vendor/animate/styles/<style>/demo/).
# Steps: build (tools/build.mjs) → determinism check (tools/framehash.mjs) → frames + mux
# (tools/export.mjs --no-audio: our voice and music live in HyperFrames) → resample to the
# composition's fps. Prints a count line, never just a status:
#   animate: <frames> frames, <seconds>s, <w>x<h>@<fps> → <out.mp4>
# Why a second engine: more varied motion, so videos don't all share one template.
set -euo pipefail
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
ANIM="$SKILL/vendor/animate"
command -v node >/dev/null || { echo "Failed: node not on PATH (Node.js 22+)"; exit 1; }

PIECE="${1:?usage: animate_clip.sh <piece-dir> <out.mp4> [--aspect 9:16] [--fps 30]}"
OUT="${2:?usage: animate_clip.sh <piece-dir> <out.mp4> [--aspect 9:16] [--fps 30]}"
shift 2
ASPECT=""; FPS=30
while [ $# -gt 0 ]; do
  case "$1" in
    --aspect) ASPECT="$2"; shift 2 ;;
    --fps) FPS="$2"; shift 2 ;;
    *) echo "Failed: unknown option $1"; exit 2 ;;
  esac
done
PIECE="$(cd "$PIECE" && pwd)"
[ -f "$PIECE/piece.json" ] || { echo "Failed: no piece.json in $PIECE"; exit 1; }
[ -d "$ANIM/node_modules/playwright" ] || { echo "Failed: Playwright missing — cd $ANIM && npm i playwright@1.64"; exit 1; }

node "$ANIM/tools/build.mjs" "$PIECE" >/dev/null
# Determinism: the same t must give the same pixels (seeded RNG, no clock). framehash exits 1 on drift.
# Two separate page loads, frames seeked out of order: every hash must match.
N_FRAMES="$(node -e "const p=require('$PIECE/piece.json');console.log(p.format?.frames||Math.round((p.format?.duration||4)*(p.format?.fps||24)))")"
cp "$PIECE/index.html" "$PIECE/.twin.html"
if ! node "$ANIM/tools/framehash.mjs" "$PIECE/index.html" "$PIECE/.twin.html" \
     $(( N_FRAMES * 3 / 4 )) 1 $(( N_FRAMES / 2 )) $(( N_FRAMES - 1 )) $(( N_FRAMES / 4 )) >/dev/null 2>&1; then
  rm -f "$PIECE/.twin.html"; echo "Failed: $PIECE is not deterministic (tools/framehash.mjs)"; exit 1
fi
rm -f "$PIECE/.twin.html"

FMT_ARGS=()
[ -n "$ASPECT" ] && FMT_ARGS=(--format "$ASPECT")
rm -rf "$PIECE/frames" "$PIECE"/frames-* "$PIECE/renders"
node "$ANIM/tools/export.mjs" "$PIECE" --no-audio --no-captions "${FMT_ARGS[@]}" >/dev/null
SRC="$(ls -t "$PIECE"/renders/*.mp4 2>/dev/null | head -1)"
[ -n "$SRC" ] || { echo "Failed: export produced no MP4 in $PIECE/renders"; exit 1; }

mkdir -p "$(dirname "$OUT")"
# animate draws most styles "on 2s" at 24 fps; repeat frames up to the composition's rate (no blending).
ffmpeg -v error -y -i "$SRC" -vf "fps=$FPS" -c:v libx264 -pix_fmt yuv420p -crf 16 -movflags +faststart -an "$OUT"
read -r W H N < <(ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=width,height,nb_read_frames -of csv=p=0 "$OUT" | tr ',' ' ')
D="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
echo "animate: $N frames, ${D%.*}s, ${W}x${H}@${FPS} → $OUT"
