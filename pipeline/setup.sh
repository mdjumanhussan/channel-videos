#!/usr/bin/env bash
# One-time per session: voice engine + models (from GitHub releases, reachable from the cloud workspace).
set -euo pipefail
pip install --break-system-packages -q kokoro-onnx soundfile
M="${KOKORO_MODELS:-$HOME/.cache/kokoro}"; mkdir -p "$M"
[ -s "$M/kokoro.onnx" ] || curl -sSL -o "$M/kokoro.onnx" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s "$M/voices.bin" ]  || curl -sSL -o "$M/voices.bin"  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
echo "voice engine ready"
