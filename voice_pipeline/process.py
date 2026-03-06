"""Claude API processor: transcribe audio + classify + clean in a single call."""

import base64
import json
import os
from pathlib import Path

import anthropic

# Supported audio formats for Claude API
SUPPORTED_FORMATS = {
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
    ".m4a": "audio/mp4",
    ".ogg": "audio/ogg",
    ".webm": "audio/webm",
    ".flac": "audio/flac",
}

VALID_DESTINATIONS = {"clipboard", "notion", "google_doc", "beads"}


def load_router_prompt() -> str:
    """Load the routing system prompt from prompts/router.md."""
    prompt_path = Path(__file__).parent / "prompts" / "router.md"
    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Routing prompt not found at {prompt_path}. "
            "Create it with your routing rules."
        )
    return prompt_path.read_text()


def process_audio(audio_path: str) -> dict:
    """Process an audio file: transcribe + classify + clean via Claude API.

    Returns dict with: destination, cleaned_text, transcript, metadata
    """
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported audio format: {suffix}. "
            f"Supported: {', '.join(SUPPORTED_FORMATS.keys())}"
        )

    audio_data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    media_type = SUPPORTED_FORMATS[suffix]

    return _call_claude(
        content=[
            {
                "type": "text",
                "text": (
                    "Transcribe this audio, then classify and clean it "
                    "according to the routing rules in your system prompt."
                ),
            },
            {
                "type": "audio",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": audio_data,
                },
            },
        ]
    )


def process_text(raw_text: str) -> dict:
    """Process raw text: classify + clean via Claude API.

    Returns dict with: destination, cleaned_text, metadata
    """
    return _call_claude(
        content=[
            {
                "type": "text",
                "text": (
                    "Classify and clean this voice note text "
                    "according to the routing rules in your system prompt.\n\n"
                    f"Voice note: {raw_text}"
                ),
            },
        ]
    )


def _call_claude(content: list) -> dict:
    """Single Claude API call that transcribes/classifies/cleans."""
    client = anthropic.Anthropic()
    router_prompt = load_router_prompt()

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2048,
        system=router_prompt,
        messages=[{"role": "user", "content": content}],
    )

    # Parse the structured JSON response
    response_text = response.content[0].text
    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        # If Claude didn't return pure JSON, try to extract it
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start >= 0 and end > start:
            result = json.loads(response_text[start:end])
        else:
            raise ValueError(
                f"Could not parse routing response as JSON: {response_text[:200]}"
            )

    # Validate destination
    dest = result.get("destination", "clipboard")
    if dest not in VALID_DESTINATIONS:
        dest = "clipboard"
        result["destination"] = dest

    return result
