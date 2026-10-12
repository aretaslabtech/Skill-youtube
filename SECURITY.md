# Security policy

## Reporting a vulnerability

Please use GitHub's **private vulnerability reporting**: the repository's *Security* tab →
*Report a vulnerability*. Don't open a public issue for a vulnerability.

You should get an acknowledgement within a week. If the issue is confirmed, the fix and an
advisory are published together.

## Scope

The studio runs an AI agent unattended that **reads the web and then runs code it wrote**
(teaching videos show only code that actually ran). In scope:

- Anything that lets fetched web content, a topic, or a file in the studio escalate the
  agent's permissions beyond `bin/run.sh`'s tool scope, or read `.env`.
- A way for a secret to reach a committed file, a log, a post kit, or a Telegram message.
- A way to bypass `deliver.py`'s checks (the review lines, the voice manifest, the URL rule)
  without editing the code.

## Not in scope

- That the agent runs code at all. That is how "code on screen is code that ran" works, and
  why `bin/run.sh` denies `curl`, `wget`, `ssh`, `sudo`, `git push`, `crontab` and `rm -rf`
  and loads no MCP servers. Run it as an ordinary user with nothing else sensitive in reach.
- Spend: `--max-budget-usd` is checked against Claude Code's own estimate and can be passed.
  Set ceilings you can afford.

## Keeping your own studio safe

- Secrets live only in your studio's `.env` (mode 600, gitignored by the template).
- `logs/` is gitignored: logs can quote tool output.
- Never paste your HeyGen voice id, API key or Telegram chat id into an issue.
