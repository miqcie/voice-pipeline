# Voice Pipeline

Speak anywhere. Auto-transcribe, classify, and route to the right tool.

```
Voice → Claude API (transcribe + classify) → Route to destination
```

## Destinations

| Destination | What goes there |
|-------------|----------------|
| **clipboard** | Code tasks, Claude Code instructions |
| **notion** | Tasks, follow-ups, meeting notes |
| **google_doc** | Blog drafts, long-form writing |
| **beads** | Decisions, architectural context |

## Usage

```bash
# From audio file
uv run python -m voice_pipeline recording.wav

# From text (skip transcription)
uv run python -m voice_pipeline --text "Blog idea: why CMMC compliance is broken"

# Dry run (show routing without executing)
uv run python -m voice_pipeline --text "Follow up with Melissa" --dry-run
```

## Setup

```bash
# Install dependencies
uv sync

# Set API key (via 1Password)
export ANTHROPIC_API_KEY=$(op read 'op://Developer Vault/Anthropic API Key/credential')
```

## Mac Hotkey (records from mic)

```bash
# Requires sox: brew install sox
./scripts/voice-route.sh
```

## Architecture

Single Claude API call handles transcription + classification + cleanup:

```
Audio/Text → Claude Haiku 4.5 → { destination, cleaned_text, metadata }
                                         │
                                  ┌──────┼──────┬──────────┐
                                  ▼      ▼      ▼          ▼
                              clipboard notion google_doc beads
```

## License

MIT
