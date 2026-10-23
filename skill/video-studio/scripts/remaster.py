#!/usr/bin/env python3
"""
remaster.py: rebuild the final audio from the composition's own stems, voice first.

  python3 remaster.py <video-dir>                 # hf/renders/video.mp4 → video.mp4 (raw kept as video-raw.mp4)
  python3 remaster.py <video-dir> --lufs -11      # override mix.master_lufs (-9.5)
  python3 remaster.py <video-dir> --out x.mp4     # write elsewhere, leave the render alone

Why: the render's mixed track can only be turned up as a whole, so making a video louder made
the music and effects louder too, and the voice still sounded low next to other people's posts
(owner, 17 Oct 2026). Every voice line, the music bed and each sound effect are separate
<audio> clips in hf/index.html, so this re-mixes them:
  - voice: a high-pass at 80 Hz, a presence lift at 3 kHz (phone speakers), 3:1 compression,
    so every word sits at one level;
  - music bed: its data-volume x mix.bed_scale (0.25), never compressed. HyperFrames plays a
    data-volume quieter than ffmpeg's linear volume does, so 0.25 keeps the music between
    sentences where the render had it (measured on a 1 s gap: -38.0 → -37.0 LUFS);
  - effects: their data-volume x mix.sfx_scale (0.5);
  - master: a limiter, then two-pass loudnorm towards mix.master_lufs (-9.5) at mix.master_tp
    (-1.5 dBTP). The peak cap usually lands it near -10.5 LUFS integrated, with speech near
    -9.3: Reels level. YouTube turns anything louder than -14 down, so nothing is lost there.
Owner-approved by ear on 17 Oct 2026, against the -14 LUFS master it replaces: voice +4.5 dB,
music unchanged.

check(video) is the gate deliver.py runs (B19): the final file must sit at -12 LUFS or louder.
The video stream is copied untouched. Prints one line:
  remaster: <slug> -11.0 LUFS tp -1.6 clips=38
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_config as sc  # noqa: E402

VOICE_CHAIN = ("highpass=f=80,equalizer=f=3000:width_type=o:width=1.4:g=3,"
               "acompressor=threshold=-24dB:ratio=3:attack=5:release=90:makeup=3dB")


def clips(index: str) -> list[dict]:
    out = []
    for tag in re.findall(r"<audio\b[^>]*>", index):
        a = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
        if not a.get("src"):
            continue
        out.append({"src": a["src"], "start": float(a.get("data-start", 0)),
                    "dur": float(a["data-duration"]) if a.get("data-duration") else None,
                    "vol": float(a.get("data-volume", 1)),
                    "kind": "voice" if "/voice/" in a["src"] else ("bed" if "/music/" in a["src"] else "sfx")})
    return out


def loud(path: Path, filt: str = "") -> dict:
    af = (filt + "," if filt else "") + "loudnorm=print_format=json"
    s = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", af, "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return json.loads(s[s.rindex("{"):])


LOUD_MIN = -12.0


def check(video: Path) -> list[str]:
    """B19: the delivered file was remastered (a plain -14 LUFS render sounds quiet next to Reels)."""
    try:
        i = float(loud(video)["input_i"])
    except (ValueError, KeyError, json.JSONDecodeError):
        return [f"B19: couldn't measure the loudness of {video.name}"]
    if i < LOUD_MIN:
        return [f"B19: {video.name} is {i:.1f} LUFS; run scripts/remaster.py (voice first, about -10.5 LUFS)"]
    return []


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    vdir = Path(argv[0]).resolve()
    sc.adopt_root_from(vdir)
    mix = sc.load().get("mix", {})
    lufs = float(argv[argv.index("--lufs") + 1]) if "--lufs" in argv else float(mix.get("master_lufs", -9.5))
    tp = float(mix.get("master_tp", -1.5))
    sfx_scale = float(mix.get("sfx_scale", 0.5))
    bed_scale = float(mix.get("bed_scale", 0.25))
    hf = next((d for d in (vdir / "hf", vdir / "hf-short") if (d / "index.html").is_file()), None)
    if not hf:
        print(f"Failed: no hf/index.html in {vdir}")
        return 1
    render = hf / "renders" / "video.mp4"
    raw = hf / "renders" / "video-raw.mp4"
    stamp = hf / "renders" / ".remastered.json"
    # A re-render after a remaster writes a new video.mp4 beside the old video-raw.mp4. The stamp
    # records the file this script wrote; if video.mp4 no longer matches it, it is a new render and
    # the stale raw must not be used (it silently shipped the old picture on 18 Oct 2026).
    if raw.is_file() and render.is_file() and stamp.is_file():
        st = render.stat()
        if json.loads(stamp.read_text()) != {"size": st.st_size, "mtime": st.st_mtime}:
            raw.unlink()
    src_video = raw if raw.is_file() else render
    out = Path(argv[argv.index("--out") + 1]).resolve() if "--out" in argv else render
    cs = [c for c in clips((hf / "index.html").read_text()) if (hf / c["src"]).is_file()]
    if not any(c["kind"] == "voice" for c in cs):
        print("Failed: no voice clips found in index.html")
        return 1

    inputs, parts, groups = ["-i", str(src_video)], [], {"voice": [], "bed": [], "sfx": []}
    for i, c in enumerate(cs, 1):
        inputs += ["-i", str(hf / c["src"])]
        trim = f"atrim=0:{c['dur']}," if c["dur"] else ""
        vol = c["vol"] * {"sfx": sfx_scale, "bed": bed_scale}.get(c["kind"], 1)
        ms = int(round(c["start"] * 1000))
        parts.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}"
                     f"volume={vol:.4f},adelay={ms}|{ms}[c{i}]")
        groups[c["kind"]].append(f"[c{i}]")

    def bus(name: str) -> str:
        g = groups[name]
        if not g:
            return ""
        parts.append(f"{''.join(g)}amix=inputs={len(g)}:normalize=0:dropout_transition=0[{name}]" if len(g) > 1
                     else f"{g[0]}anull[{name}]")
        return f"[{name}]"

    voice, bed, sfx = bus("voice"), bus("bed"), bus("sfx")
    parts.append(f"{voice}{VOICE_CHAIN}[vox]")
    final = ["[vox]"] + ([bed] if bed else [])
    if sfx:
        final.append(sfx)
    parts.append(f"{''.join(final)}amix=inputs={len(final)}:normalize=0:dropout_transition=0,"
                 f"alimiter=limit=0.9:attack=3:release=60:level=false,apad[mix]")   # silent end hold: pad to the picture (-t bounds it), or -shortest cuts the end mark
    graph = ";".join(parts)

    tmp = out.with_name("remaster-premaster.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[mix]",
                    "-t", str(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                    "-of", "csv=p=0", str(src_video)], capture_output=True,
                                                   text=True).stdout.strip() or 0)),
                    "-ar", "48000", str(tmp)], check=True)
    m = loud(tmp)
    norm = (f"loudnorm=I={lufs}:TP={tp}:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    if out == render and not raw.is_file():
        render.rename(raw)
        src_video = raw
    tmp_out = out.with_name(out.stem + ".remaster-tmp.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src_video), "-i", str(tmp), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", norm, "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", str(tmp_out)], check=True)
    tmp_out.replace(out)
    if out == render:
        st = render.stat()
        stamp.write_text(json.dumps({"size": st.st_size, "mtime": st.st_mtime}))
    tmp.unlink(missing_ok=True)
    f = loud(out)
    print(f"remaster: {vdir.name} {float(f['input_i']):.1f} LUFS tp {float(f['input_tp']):.1f} clips={len(cs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
