#!/usr/bin/env bash
# run.sh — run the video studio unattended (from cron), and alert when no video came out.
#
#   bin/run.sh                 # today's video on the default track (config.json "default_track")
#   bin/run.sh promo           # any skill mode: daily | promo | blog | plan <topic> | build <slug> | …
#
# It runs `claude -p "/video-studio <mode>"` inside $STUDIO_ROOT with:
#   - a lock, so two runs never overlap (a second run waits up to STUDIO_LOCK_WAIT seconds);
#   - a wall-clock ceiling and a spend cap: 3 h / $25 for a Short, 7 h / $60 when today's
#     video is a long-form (override with STUDIO_LIMIT=90m STUDIO_BUDGET=20);
#   - every tool allowed except pushing, downloading with curl/wget, sudo, ssh, crontab and
#     rm -rf, and no MCP servers. A headless run can't answer a permission prompt, so a
#     per-command allowlist only stalls it; the denies are the safety. There is no
#     --dangerously-skip-permissions;
#   - success judged by COUNT, not status: the run must print deliver.py's `Rendered:` line.
#     Exit code 0 with no video is a failure, and you get an alert saying why.
#
# Environment (all optional except where noted):
#   STUDIO_ROOT        the studio folder (default: the current directory)
#   STUDIO_ENV_FILE    file to load secrets from (default: $STUDIO_ROOT/.env; needs HEYGEN_API_KEY)
#   STUDIO_TRACK       the track for `daily` (default: config.json "default_track"); modes
#                      `promo` and `blog` use the tracks of the same name. Exported, so the
#                      skill's ledger.py and deliver.py use it too
#   STUDIO_LIMIT       timeout(1) duration, e.g. 3h          STUDIO_BUDGET   USD cap, e.g. 25
#   STUDIO_LOCK        lock file (default: /tmp/video-studio-<uid>.lock)
#   STUDIO_LOCK_WAIT   seconds to wait for the lock (default 7200)
#   STUDIO_DATE        YYYY-MM-DD: make up a missed day's video
#   STUDIO_ALERT_CMD   command that receives the alert text as $1 (default: Telegram via
#                      telegram.py when TELEGRAM_BOT_TOKEN/CHAT_ID are set, else stderr)
#
# Example crontab (times are the machine's local time):
#   0 23 * * *        STUDIO_ROOT=$HOME/my-studio $HOME/faceless-video-studio/bin/run.sh
#   15 15 * * 1,4,6   STUDIO_ROOT=$HOME/my-studio STUDIO_LIMIT=75m $HOME/faceless-video-studio/bin/run.sh promo
set -u
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL="$REPO/skill/video-studio"
STUDIO_ROOT="$(cd "${STUDIO_ROOT:-$PWD}" && pwd)"
export STUDIO_ROOT
ENV_FILE="${STUDIO_ENV_FILE:-$STUDIO_ROOT/.env}"
LOG="$STUDIO_ROOT/logs/run-$(date -u +%Y%m%d).log"
mkdir -p "$STUDIO_ROOT/logs"

ARGS="${*:-daily}"
MODE="${ARGS%% *}"

# fd 3 is the terminal (or cron's mail): everything else goes to the log.
exec 3>&2
alert() {
  local msg="⚠️ video-studio: $1"
  echo "$msg"   # into the log
  if [ -n "${STUDIO_ALERT_CMD:-}" ]; then
    $STUDIO_ALERT_CMD "$msg" >/dev/null 2>&1 || echo "$msg" >&3
  elif [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
    python3 "$SKILL/scripts/telegram.py" "$msg" >/dev/null 2>&1 || echo "$msg" >&3
  else
    echo "$msg" >&3
  fi
}

START_LINE=$(( $( [ -f "$LOG" ] && wc -l < "$LOG" || echo 0 ) + 1 ))
{
  # Secrets first, so an alert can reach Telegram even when the run can't start.
  if [ -f "$ENV_FILE" ]; then set -a; . "$ENV_FILE"; set +a; fi
  for bin in claude node npx ffmpeg python3 flock timeout; do   # macOS: brew install coreutils flock (GNU timeout)
    command -v "$bin" >/dev/null || { echo "Failed: $bin not on PATH"; alert "no video: $bin is not on PATH (cron has a short PATH; set it in the crontab)."; exit 1; }
  done
  if [ -z "${HEYGEN_API_KEY:-}" ]; then
    echo "Failed: HEYGEN_API_KEY missing from $ENV_FILE"
    alert "no video: HEYGEN_API_KEY is missing from $ENV_FILE."
    exit 1
  fi

  case "$MODE" in
    promo|blog) TRACK="$MODE" ;;
    *) TRACK="${STUDIO_TRACK:-}" ;;
  esac
  [ -n "$TRACK" ] && export STUDIO_TRACK="$TRACK"
  FORMAT="$(cd "$STUDIO_ROOT" && python3 "$SKILL/scripts/ledger.py" today ${TRACK:+--track "$TRACK"} 2>/dev/null \
    | python3 -c 'import json,sys; print(json.load(sys.stdin).get("format") or "")' 2>/dev/null)"
  case "$FORMAT" in longform) LIMIT=7h; BUDGET=60 ;; *) LIMIT=3h; BUDGET=25 ;; esac
  LIMIT="${STUDIO_LIMIT:-$LIMIT}"; BUDGET="${STUDIO_BUDGET:-$BUDGET}"
  LOCK="${STUDIO_LOCK:-/tmp/video-studio-$(id -u).lock}"
  WAIT="${STUDIO_LOCK_WAIT:-7200}"

  echo "[$(date -u '+%Y-%m-%d %H:%M:%S')Z] video-studio start: $ARGS (track ${TRACK:-default}, ${FORMAT:-?}, limit $LIMIT, \$$BUDGET)"
  cd "$STUDIO_ROOT" || exit 1
  flock -w "$WAIT" -E 75 "$LOCK" timeout "$LIMIT" claude -p "/video-studio $ARGS" \
    --permission-mode acceptEdits \
    --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Skill,Task,TodoWrite,Bash" \
    --disallowedTools "Bash(git push:*),Bash(rm -rf:*),Bash(curl:*),Bash(wget:*),Bash(sudo:*),Bash(crontab:*),Bash(ssh:*),Bash(scp:*)" \
    --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
    --max-budget-usd "$BUDGET" \
    --output-format text
  rc=$?
  echo "[$(date -u '+%Y-%m-%d %H:%M:%S')Z] video-studio exit $rc"

  # The skill ends with deliver.py's `Rendered:` line. No line → no video, whatever rc says.
  # Only THIS run's output counts: several runs can share a day's log.
  THIS_RUN="$(tail -n +"$START_LINE" "$LOG")"
  if ! grep -q "Rendered: " <<<"$THIS_RUN"; then
    case $rc in
      124) why="killed after $LIMIT" ;;
      75)  why="another studio run held the lock for $(( WAIT / 60 )) min" ;;
      0)   why="claude exited 0 but nothing was delivered" ;;
      *)   why="claude exited $rc" ;;
    esac
    if grep -qiE "oauth|not logged|log ?in|authenticat|unauthori[sz]ed" <<<"$THIS_RUN"; then
      why="$why — the Claude CLI looks logged out: run claude and /login"
    fi
    if grep -qiE "credit balance|usage limit|rate limit|overloaded" <<<"$THIS_RUN"; then
      why="$why — Claude access or credits ran out; re-run later with STUDIO_DATE set to the missed day"
    fi
    reason="$(grep -m1 '^Failed:' <<<"$THIS_RUN")"
    alert "no video from \"$MODE\": $why.${reason:+ $reason} Log: $LOG"
    [ "$rc" -eq 0 ] && rc=1   # count, not status: exit 0 with no video is a failure
  fi
  exit $rc
} >> "$LOG" 2>&1
