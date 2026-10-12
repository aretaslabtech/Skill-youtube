#!/usr/bin/env python3
"""
telegram.py — the studio's default delivery: a Telegram bot sends you the video and its kit.

Set two variables in $STUDIO_ROOT/.env (never commit that file):

  TELEGRAM_BOT_TOKEN   from @BotFather
  TELEGRAM_CHAT_ID     your chat with the bot (send it a message, then open
                       https://api.telegram.org/bot<token>/getUpdates and read chat.id)

Without them, delivery still works: the kit is written to <video>/POST-KIT.html and the
returned message id is "local". Every function returns {"ok": ..., ...} and never raises,
because delivery reporting must not crash the thing it reports on.

  cd <your studio> && python3 <skill>/scripts/telegram.py "test"   # check token and chat id
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

UPLOAD_LIMIT = 50 * 1024 * 1024   # the Bot API's upload ceiling for sendVideo
MSG_LIMIT = 4096


def _creds() -> tuple[str, str] | None:
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    return (token, chat) if token and chat else None


def configured() -> bool:
    return _creds() is not None


def esc(s) -> str:
    """Escape text for Telegram's HTML parse mode."""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def split_message(text: str, limit: int = MSG_LIMIT) -> list[str]:
    """Split on blank lines, then lines, so no part exceeds Telegram's limit."""
    parts, cur = [], ""
    for block in text.split("\n\n"):
        pieces = [block] if len(block) <= limit else block.split("\n")
        for j, piece in enumerate(pieces):
            piece = piece[:limit]
            sep = "\n\n" if j == 0 else "\n"
            if cur and len(cur) + len(sep) + len(piece) > limit:
                parts.append(cur)
                cur = piece
            else:
                cur = f"{cur}{sep}{piece}" if cur else piece
    if cur:
        parts.append(cur)
    return parts


def _post(method: str, data: bytes, content_type: str, timeout: int) -> dict:
    token, _ = _creds()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=data,
                                 headers={"Content-Type": content_type})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)}
    if not resp.get("ok"):
        return {"ok": False, "error": resp.get("description", "unknown telegram error")}
    return {"ok": True, "message_id": resp["result"]["message_id"]}


def send(text: str, parse_mode: str = "HTML") -> dict:
    if not configured():
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set"}
    _, chat = _creds()
    body = {"chat_id": chat, "text": text.strip()[:MSG_LIMIT], "disable_web_page_preview": "true"}
    if parse_mode:
        body["parse_mode"] = parse_mode
    return _post("sendMessage", urllib.parse.urlencode(body).encode(),
                 "application/x-www-form-urlencoded", 30)


def send_video(path, caption: str = "", duration=None) -> dict:
    """Upload an MP4 so it plays inline. Refuses above UPLOAD_LIMIT instead of failing late."""
    if not configured():
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set"}
    p = Path(path)
    try:
        size = p.stat().st_size
    except OSError as e:
        return {"ok": False, "error": str(e)}
    if size > UPLOAD_LIMIT:
        return {"ok": False, "error": f"too large for the Bot API: {size / 1e6:.1f} MB > 50 MB"}
    _, chat = _creds()
    fields = {"chat_id": chat, "caption": caption[:1024], "supports_streaming": "true"}
    if duration:
        fields["duration"] = str(int(float(duration)))
    boundary = "faceless-video-studio-boundary"
    parts = [f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
             for k, v in fields.items()]
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="video"; filename="{p.name}"\r\n'
                 f"Content-Type: video/mp4\r\n\r\n".encode() + p.read_bytes() + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return _post("sendVideo", b"".join(parts), f"multipart/form-data; boundary={boundary}", 300)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import studio_config
    studio_config.load_env()   # $STUDIO_ROOT/.env (run it from your studio folder)
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    r = send(" ".join(sys.argv[1:]))
    print(json.dumps(r))
    sys.exit(0 if r["ok"] else 1)
