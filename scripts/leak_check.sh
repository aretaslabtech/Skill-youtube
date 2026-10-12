#!/usr/bin/env bash
# leak_check.sh — refuse to publish secrets, personal paths or account ids.
#
#   scripts/leak_check.sh                  # scan every file git would publish (tracked + new)
#   LEAK_PATTERNS_FILE=~/.config/x.txt scripts/leak_check.sh
#                                          # plus your own private patterns (one regex per line),
#                                          # kept OUTSIDE the repo: your voice id, chat id, …
#
# Prints every hit and a count, and exits 1 on any hit. CI runs it on every push.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Files that would be published: tracked plus untracked-but-not-ignored. Skip vendored code
# (checked against its upstream commit instead) and binaries (grep -I).
mapfile -t FILES < <(git ls-files --cached --others --exclude-standard 2>/dev/null \
  | grep -v '^skill/video-studio/vendor/animate/' | grep -v '^scripts/leak_check.sh$')
[ "${#FILES[@]}" -gt 0 ] || { echo "leak_check: no files to scan (run inside the git repo)"; exit 1; }

PATTERNS=(
  # credentials
  'sk-[A-Za-z0-9_-]{20,}'                       # OpenAI/Anthropic-style keys
  'gh[pousr]_[A-Za-z0-9]{20,}'                  # GitHub tokens
  'github_pat_[A-Za-z0-9_]{20,}'
  'AKIA[0-9A-Z]{16}'                            # AWS access key id
  'xox[abprs]-[A-Za-z0-9-]{10,}'                # Slack tokens
  '[0-9]{8,10}:AA[A-Za-z0-9_-]{30,}'            # Telegram bot token
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  'Bearer [A-Za-z0-9._~+/-]{20,}'
  '^[[:space:]]*(HEYGEN_API_KEY|HEYGEN_VOICE_ID|TELEGRAM_BOT_TOKEN|TELEGRAM_CHAT_ID|[A-Z_]*(TOKEN|SECRET|PASSWORD))=[^[:space:]<$]'
  '"(voice_id|chat_id|api_key|token)"[[:space:]]*:[[:space:]]*"[^"]{8,}"'
  # personal paths and contact details
  '/home/[a-z][a-z0-9_-]+/'
  '/Users/[A-Za-z][A-Za-z0-9_-]+/'
  '/mnt/[a-z]+/'
  '[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail|proton|icloud)\.[a-z.]+'
  '\+[0-9]{1,3}[ -]?[0-9]{9,10}\b'
  'wa\.me/[0-9]{8,}'
  # 32-hex ids (HeyGen voice and user ids look like this)
  '\b[0-9a-f]{32}\b'
)
if [ -n "${LEAK_PATTERNS_FILE:-}" ]; then
  [ -r "$LEAK_PATTERNS_FILE" ] || { echo "leak_check: can't read $LEAK_PATTERNS_FILE"; exit 1; }
  while IFS= read -r p; do [ -n "$p" ] && [ "${p:0:1}" != "#" ] && PATTERNS+=("$p"); done < "$LEAK_PATTERNS_FILE"
fi

hits=0
for p in "${PATTERNS[@]}"; do
  out="$(grep -InE -- "$p" "${FILES[@]}" 2>/dev/null)"
  if [ -n "$out" ]; then
    # Show where, but never echo a matched secret in full.
    while IFS= read -r line; do
      echo "  HIT [${p:0:28}] ${line%%:*}:$(cut -d: -f2 <<<"$line")"
      hits=$((hits + 1))
    done <<<"$out"
  fi
done
echo "leak_check: ${#FILES[@]} files, ${#PATTERNS[@]} patterns, $hits hit(s)"
[ "$hits" -eq 0 ]
