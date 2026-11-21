#!/usr/bin/env sh
# Downloads the Piper voice used by the agent into api/_data/voices.
# Run once from the project root, then commit the two files.
set -e
VOICE="${1:-en_US-lessac-medium}"
LANG_DIR="$(echo "$VOICE" | cut -d_ -f1)"          # en
LOCALE="$(echo "$VOICE" | cut -d- -f1)"            # en_US
NAME="$(echo "$VOICE" | cut -d- -f2)"              # lessac
QUALITY="$(echo "$VOICE" | cut -d- -f3)"           # medium
BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main/$LANG_DIR/$LOCALE/$NAME/$QUALITY"
mkdir -p api/_data/voices
curl -fL "$BASE/$VOICE.onnx" -o "api/_data/voices/$VOICE.onnx"
curl -fL "$BASE/$VOICE.onnx.json" -o "api/_data/voices/$VOICE.onnx.json"
echo "Saved api/_data/voices/$VOICE.onnx"
