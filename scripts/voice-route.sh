#!/usr/bin/env bash
# voice-route.sh — Record from mic, pipe to voice pipeline
# Requires: brew install sox
# Usage: ./scripts/voice-route.sh [--dry-run]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
RECORDING_DIR="${TMPDIR:-/tmp}/voice-pipeline"
mkdir -p "$RECORDING_DIR"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
AUDIO_FILE="$RECORDING_DIR/recording-$TIMESTAMP.wav"

# Check for sox
if ! command -v sox &>/dev/null; then
    echo "sox not found. Install with: brew install sox"
    exit 1
fi

# Check for API key
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    if command -v op &>/dev/null; then
        export ANTHROPIC_API_KEY=$(op read 'op://Developer Vault/Anthropic API Key/credential')
    else
        echo "Set ANTHROPIC_API_KEY or install 1Password CLI"
        exit 1
    fi
fi

echo "Recording... (press Ctrl+C to stop, or silence will auto-stop)"
echo ""

# Record from default mic
# silence 1 0.1 3% = start recording after 0.1s of sound above 3%
# silence 1 2.0 3% = stop after 2s of silence below 3%
sox -d "$AUDIO_FILE" \
    rate 16000 \
    channels 1 \
    silence 1 0.1 3% 1 2.0 3% \
    2>/dev/null || true

if [ ! -f "$AUDIO_FILE" ] || [ ! -s "$AUDIO_FILE" ]; then
    echo "No audio recorded."
    exit 1
fi

DURATION=$(sox --i -D "$AUDIO_FILE" 2>/dev/null || echo "unknown")
echo "Recorded ${DURATION}s of audio"
echo "Processing..."
echo ""

# Run pipeline
cd "$PROJECT_DIR"
uv run python -m voice_pipeline "$AUDIO_FILE" "$@"

# Clean up recording
rm -f "$AUDIO_FILE"
