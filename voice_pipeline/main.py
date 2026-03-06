"""CLI entry point for voice-pipeline."""

import argparse
import json
import sys

from voice_pipeline.process import process_audio, process_text
from voice_pipeline.route import route


def main():
    parser = argparse.ArgumentParser(
        description="Voice Pipeline: speak -> transcribe -> classify -> route",
        prog="voice_pipeline",
    )
    parser.add_argument(
        "audio_file",
        nargs="?",
        help="Path to audio file (.wav, .mp3, .m4a, .ogg, .webm, .flac)",
    )
    parser.add_argument(
        "--text", "-t",
        type=str,
        help="Process raw text instead of audio (skip transcription)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show routing decision without executing",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        dest="output_json",
        help="Output raw JSON result instead of routing",
    )

    args = parser.parse_args()

    if not args.audio_file and not args.text:
        parser.error("Provide an audio file or --text 'your text here'")

    try:
        if args.text:
            result = process_text(args.text)
        else:
            result = process_audio(args.audio_file)

        if args.output_json:
            print(json.dumps(result, indent=2))
        else:
            route(result, dry_run=args.dry_run)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
