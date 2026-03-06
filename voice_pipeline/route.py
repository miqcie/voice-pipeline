"""Route classified voice notes to their destination."""

import json
import os
import subprocess
import sys


def route(result: dict, dry_run: bool = False) -> None:
    """Route a classified result to its destination.

    Args:
        result: Dict with destination, cleaned_text, and optional metadata.
        dry_run: If True, print what would happen without executing.
    """
    dest = result["destination"]
    text = result["cleaned_text"]
    metadata = result.get("metadata", {})

    if dry_run:
        _print_dry_run(dest, text, metadata)
        return

    routers = {
        "clipboard": _route_clipboard,
        "notion": _route_notion,
        "google_doc": _route_google_doc,
        "beads": _route_beads,
    }

    router_fn = routers.get(dest)
    if not router_fn:
        print(f"Unknown destination '{dest}', falling back to clipboard")
        router_fn = _route_clipboard

    router_fn(text, metadata)


def _print_dry_run(dest: str, text: str, metadata: dict) -> None:
    """Print routing decision without executing."""
    print(f"\n--- DRY RUN ---")
    print(f"Destination: {dest}")
    print(f"Text: {text[:200]}{'...' if len(text) > 200 else ''}")
    if metadata:
        print(f"Metadata: {json.dumps(metadata, indent=2)}")
    print(f"--- END DRY RUN ---\n")


def _route_clipboard(text: str, metadata: dict) -> None:
    """Copy text to macOS clipboard via pbcopy."""
    proc = subprocess.run(
        ["pbcopy"],
        input=text.encode("utf-8"),
        check=True,
    )
    print(f"Copied to clipboard ({len(text)} chars)")


def _route_notion(text: str, metadata: dict) -> None:
    """Create a Notion task/page via the Notion API.

    Uses NOTION_API_TOKEN env var or 1Password lookup.
    """
    token = os.environ.get("NOTION_API_TOKEN")
    if not token:
        # Try 1Password
        try:
            result = subprocess.run(
                ["op", "read", "op://Developer Vault/mtzpsrt2oazpb7p7esq5n6mxia/credential"],
                capture_output=True, text=True, check=True,
            )
            token = result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("No Notion API token found. Set NOTION_API_TOKEN or configure 1Password.")
            print("Falling back to clipboard.")
            _route_clipboard(text, metadata)
            return

    import requests

    # Database ID from CLAUDE.md
    database_id = "1f0fbcfa-1853-80cf-a77b-d229376719d5"

    title = metadata.get("title", text[:50].strip())
    category = metadata.get("category", "")
    priority = metadata.get("priority", "Medium")

    properties = {
        "Task name": {"title": [{"text": {"content": title}}]},
        "Status": {"status": {"name": "Not started"}},
        "Priority": {"select": {"name": priority}},
        "Notes": {"rich_text": [{"text": {"content": text}}]},
    }
    if category:
        properties["Category"] = {"select": {"name": category}}

    resp = requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        json={"parent": {"database_id": database_id}, "properties": properties},
    )

    if resp.ok:
        page_url = resp.json().get("url", "")
        print(f"Created Notion task: {title}")
        if page_url:
            print(f"  URL: {page_url}")
    else:
        print(f"Notion API error ({resp.status_code}): {resp.text[:200]}")
        print("Falling back to clipboard.")
        _route_clipboard(text, metadata)


def _route_google_doc(text: str, metadata: dict) -> None:
    """Append text to a Google Doc.

    For now, copies to clipboard with instructions.
    Full Google Docs API integration requires OAuth flow.
    """
    # TODO: Integrate with Google Docs API via google-workspace MCP
    # For now, create a local markdown file as a staging area
    title = metadata.get("title", "voice-note")
    safe_title = "".join(c if c.isalnum() or c in "-_ " else "" for c in title)
    safe_title = safe_title.strip().replace(" ", "-").lower()

    drafts_dir = os.path.expanduser("~/Documents/voice-drafts")
    os.makedirs(drafts_dir, exist_ok=True)

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filepath = os.path.join(drafts_dir, f"{timestamp}-{safe_title}.md")

    with open(filepath, "w") as f:
        f.write(f"# {metadata.get('title', 'Voice Note')}\n\n")
        f.write(text)
        f.write("\n")

    print(f"Saved draft to: {filepath}")
    print("(Google Docs API integration coming in Phase 3)")


def _route_beads(text: str, metadata: dict) -> None:
    """Store as a bead via bd CLI."""
    title = metadata.get("title", text[:60].strip())

    try:
        subprocess.run(
            ["bd", "create", title, "--body", text],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Created bead: {title}")
    except FileNotFoundError:
        print("bd CLI not found. Falling back to clipboard.")
        _route_clipboard(text, metadata)
    except subprocess.CalledProcessError as e:
        print(f"bd error: {e.stderr}")
        print("Falling back to clipboard.")
        _route_clipboard(text, metadata)
