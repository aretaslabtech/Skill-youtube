#!/usr/bin/env bash
# install_voice.sh — set up an open-source voice engine in its own virtualenv.
#
#   STUDIO_ROOT=~/my-studio skill/video-studio/scripts/install_voice.sh pocket    # English
#   STUDIO_ROOT=~/my-studio skill/video-studio/scripts/install_voice.sh indicf5   # Hindi + 10 Indian languages
#
# Creates $STUDIO_ROOT/.venvs/<engine> (CPU builds; no GPU needed) and checks model access.
# Both models are gated on Hugging Face: accept the terms on the model page, then
# `hf auth login` (or set HF_TOKEN) before running this:
#   pocket   https://huggingface.co/kyutai/pocket-tts         (CC-BY-4.0)
#   indicf5  https://huggingface.co/ai4bharat/IndicF5         (MIT)
# Word timings use faster-whisper (MIT), downloaded on first use.
set -euo pipefail
ENGINE="${1:-}"
ROOT="${STUDIO_ROOT:-$PWD}"
VENV="$ROOT/.venvs/$ENGINE"
case "$ENGINE" in
  pocket)
    PKGS=("pocket-tts>=3.3" "faster-whisper>=1.2" soundfile numpy)
    MODEL="kyutai/pocket-tts" ;;
  indicf5)
    # IndicF5 breaks on newer releases: transformers 5.x loads it on the meta device ("Tensor on
    # device cpu is not on the expected device meta"); datasets 4 needs pyarrow ≥ 18, which needs NumPy 2.
    PKGS=("torch==2.8.*" "torchaudio==2.8.*" "git+https://github.com/ai4bharat/IndicF5.git"
          "transformers==4.49.0" "datasets<4" "pyarrow<18" "faster-whisper>=1.2" soundfile "numpy<2")
    MODEL="ai4bharat/IndicF5"
    export GIT_LFS_SKIP_SMUDGE=1 ;;   # a dependency's git checkout needs git-lfs otherwise
  *) echo "usage: install_voice.sh pocket|indicf5" >&2; exit 2 ;;
esac
command -v ffmpeg >/dev/null || { echo "Failed: ffmpeg is not on PATH" >&2; exit 1; }

if command -v uv >/dev/null; then
  uv venv -q --allow-existing -p 3.12 "$VENV"   # re-running upgrades in place
  uv pip install -q -p "$VENV/bin/python" --index-strategy unsafe-best-match \
    --extra-index-url https://download.pytorch.org/whl/cpu "${PKGS[@]}"
else
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --extra-index-url https://download.pytorch.org/whl/cpu "${PKGS[@]}"
fi

# Check access now (gated models fail late otherwise). IndicF5 is fetched whole; Pocket's repo
# holds every language, so the engine fetches only the one it uses on first run.
"$VENV/bin/python" - "$MODEL" <<'PY'
import sys
from huggingface_hub import hf_hub_download, snapshot_download
try:
    hf_hub_download(sys.argv[1], "README.md")
    print("model:", snapshot_download(sys.argv[1]) if sys.argv[1].endswith("IndicF5") else "access ok")
except Exception as e:  # gated: terms not accepted, or not logged in
    sys.exit(f"Failed: could not download {sys.argv[1]} ({type(e).__name__}). Accept its terms on "
             f"https://huggingface.co/{sys.argv[1]} and run `hf auth login`, then re-run.")
PY
echo "OK: $ENGINE engine at $VENV/bin/python"
