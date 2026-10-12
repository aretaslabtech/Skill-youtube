#!/usr/bin/env bash
# install.sh — link the video-studio skill into Claude Code and create a studio folder.
#
#   ./install.sh ~/my-studio                 # skill → ~/.claude/skills/video-studio, studio → ~/my-studio
#   ./install.sh ~/my-studio --project DIR   # skill → DIR/.claude/skills/video-studio instead
#   ./install.sh --check                     # only check the prerequisites
#
# Safe to re-run: it never overwrites your config, brand or .env, and it only replaces a
# skill link that already points into this repository.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$REPO/skill/video-studio"

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; MISSING=1; }
note() { printf '  · %s\n' "$1"; }

STUDIO=""; PROJECT=""; CHECK_ONLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --project) PROJECT="${2:?--project needs a directory}"; shift 2 ;;
    --check) CHECK_ONLY=1; shift ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) STUDIO="$1"; shift ;;
  esac
done

echo "Prerequisites"
MISSING=0
if command -v node >/dev/null; then
  v="$(node -p 'process.versions.node.split(".")[0]')"
  [ "$v" -ge 22 ] && ok "Node.js $(node -v)" || bad "Node.js 22+ needed (found $(node -v))"
else bad "Node.js 22+ (https://nodejs.org or nvm)"; fi
command -v npx >/dev/null && ok "npx" || bad "npx (comes with Node.js)"
command -v ffmpeg >/dev/null && ok "FFmpeg $(ffmpeg -version | head -1 | awk '{print $3}')" || bad "FFmpeg (apt install ffmpeg / brew install ffmpeg)"
command -v ffprobe >/dev/null && ok "ffprobe" || bad "ffprobe (ships with FFmpeg)"
if command -v python3 >/dev/null && python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
  ok "Python $(python3 -c 'import platform; print(platform.python_version())')"
else bad "Python 3.10+"; fi
command -v claude >/dev/null && ok "Claude Code $(claude --version 2>/dev/null | head -1)" || bad "Claude Code (https://code.claude.com)"
command -v flock >/dev/null && ok "flock (for scheduled runs)" || note "flock not found: only bin/run.sh needs it (util-linux; on macOS: brew install flock)"
command -v timeout >/dev/null && ok "timeout (for scheduled runs)" || note "timeout not found: only bin/run.sh needs it (on macOS: brew install coreutils, then put its gnubin on PATH)"
MEDIA="$(python3 "$SKILL/scripts/studio_config.py" --media-use 2>/dev/null)" || MEDIA=""
if [ -n "$MEDIA" ]; then ok "HyperFrames skills ($MEDIA)"
else bad "HyperFrames skills: run  npx skills add heygen-com/hyperframes  (or the Claude Code plugin, see README)"; fi
[ "$CHECK_ONLY" = 1 ] && exit "$MISSING"

if [ -z "$STUDIO" ]; then
  echo; echo "Usage: ./install.sh <studio-folder> [--project DIR]"; exit 2
fi

echo; echo "Skill"
DEST_ROOT="${PROJECT:+$PROJECT/.claude/skills}"; DEST_ROOT="${DEST_ROOT:-$HOME/.claude/skills}"
DEST="$DEST_ROOT/video-studio"
mkdir -p "$DEST_ROOT"
if [ -L "$DEST" ] && [[ "$(readlink -f "$DEST")" == "$REPO"/* ]]; then
  ln -sfn "$SKILL" "$DEST"; ok "re-linked $DEST → $SKILL"
elif [ -e "$DEST" ]; then
  echo "  $DEST already exists and isn't a link into this repo. Move it away and re-run."; exit 1
else
  ln -s "$SKILL" "$DEST"; ok "linked $DEST → $SKILL"
fi

echo; echo "Studio"
mkdir -p "$STUDIO"; STUDIO="$(cd "$STUDIO" && pwd)"
copy() { if [ -e "$STUDIO/$2" ]; then note "kept your $2"; else cp -R "$REPO/studio.example/$1" "$STUDIO/$2"; ok "created $2"; fi; }
copy config.json config.json
copy brand brand
copy gitignore .gitignore
if [ -e "$STUDIO/.env" ]; then note "kept your .env"
else cp "$REPO/studio.example/env.example" "$STUDIO/.env"; chmod 600 "$STUDIO/.env"; ok "created .env (mode 600) — add your HEYGEN_API_KEY"; fi
mkdir -p "$STUDIO/videos" "$STUDIO/voice" "$STUDIO/logs"

echo; echo "Optional engines"
note "animate (7 hand-made looks): cd \"$SKILL/vendor/animate\" && npm install && npx playwright install chromium"
note "Manim (maths/algorithm beats): python3 -m venv ~/.venvs/manim && ~/.venvs/manim/bin/pip install manim"

cat <<EOF

Next steps
  1. Put your HeyGen API key in $STUDIO/.env
  2. Record a voice sample to $STUDIO/voice/sample.wav (docs/voice.md)
  3. cd "$STUDIO" && claude, then run:  /video-studio setup
  4. Edit brand/brand-core.md, brand/pillars.md and brand/products.json
  5. Make your first video:  /video-studio daily
EOF
if [ "$MISSING" = 1 ]; then
  echo; echo "Some prerequisites are missing (✗ above). Install them, then check with: ./install.sh --check"
fi
exit "$MISSING"
