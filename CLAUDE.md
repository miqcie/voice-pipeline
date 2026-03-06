# Voice Pipeline

## Project Overview
Voice capture and auto-routing: speak anywhere → Claude transcribes + classifies → routes to the right tool.

## Conventions
- Python 3.11+, managed with uv
- Run with: `uv run python -m voice_pipeline <args>`
- API key from 1Password: `op://Developer Vault/Anthropic API Key/credential`
- Use Claude Haiku 4.5 for routing (fast + cheap) — Opus is overkill for classification
- No OpenAI/Whisper dependency — Claude handles audio natively

## Architecture
- `voice_pipeline/process.py` — Single Claude API call: transcribe + classify + clean
- `voice_pipeline/route.py` — Route to destination (clipboard, Notion, Google Docs, beads)
- `voice_pipeline/main.py` — CLI entry point
- `voice_pipeline/prompts/router.md` — Routing system prompt (human-authored rules)
- `scripts/voice-route.sh` — Mac hotkey wrapper (records via sox)

## Testing
- `uv run python -m voice_pipeline --text "test input" --dry-run`
- Dry-run shows routing decision without executing
