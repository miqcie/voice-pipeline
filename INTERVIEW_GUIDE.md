# Voice Pipeline Interview Guide

Record yourself responding to each prompt below as a single voice memo. Speak naturally — use filler words, false starts, change your mind mid-sentence. The messier the better — that's what real voice notes sound like.

After recording, we'll use these as eval fixtures to tune the routing prompt.

---

## Section 1: Clear Signals (one destination each)

These should be easy wins. If the router can't get these right, the prompt needs major work.

### 1A — Clipboard (code/Claude Code)
> **Prompt:** You just thought of a refactor you want Claude Code to do. Say it out loud like you're dictating to your terminal.

### 1B — Notion (task)
> **Prompt:** You just got off a call with Melissa at Nereid. There's a follow-up action item due next week. Capture it.

### 1C — Google Doc (blog draft)
> **Prompt:** You had a shower thought about a blog post for Caldris — something about the gap between compliance buyers and AI builders. Riff on the idea.

### 1D — Beads (decision)
> **Prompt:** You just decided to use Claude Haiku instead of Opus for the voice pipeline routing. Explain why.

---

## Section 2: Ambiguous / Edge Cases

These test the router's judgment. There's no single "right" answer — your routing rules will define correctness.

### 2A — Task + Decision combo
> **Prompt:** You decided to change the Nereid project timeline AND need to tell Melissa about it. Capture both in one note.

### 2B — Vague / no clear destination
> **Prompt:** Just ramble about your day for 15-20 seconds. Nothing actionable, no clear destination.

### 2C — Content that could be blog OR bead
> **Prompt:** You noticed an interesting pattern across your CMMC clients — it could be a blog post or just something to remember. Talk it through without deciding.

### 2D — Multi-part with different destinations
> **Prompt:** In one breath: mention a code change you want, a task for someone, and a blog idea. Don't pause between them.

---

## Section 3: Natural Speech Patterns

These test cleanup quality — filler words, corrections, tangents.

### 3A — Heavy filler words
> **Prompt:** Describe a technical concept but use lots of "um", "uh", "like", "you know", "basically". Be your most unedited self.

### 3B — Self-correction mid-sentence
> **Prompt:** Start saying one thing, then correct yourself. "Actually no, wait — I meant..." Do this 2-3 times in one note.

### 3C — Trailing off / incomplete thought
> **Prompt:** Start a thought, trail off, then pick up a completely different thought. Don't clean it up.

---

## Section 4: Client / Domain-Specific

These test whether domain context improves routing.

### 4A — Client name mention
> **Prompt:** Mention "Eagle Ridge" and a compliance deliverable. Does the router know this should be a task?

### 4B — Technical jargon
> **Prompt:** Use CMMC/compliance jargon naturally — "SSP", "POA&M", "C3PAO", "SPRS score". See if the router still classifies correctly.

### 4C — Mixed personal and work
> **Prompt:** Start with something personal ("need to pick up groceries") then pivot to a work task. See what the router does with the personal part.

---

## How to Record

1. Open Voice Memos on your iPhone (or Mac)
2. For each prompt, just hit record and talk for 15-45 seconds
3. Export as .m4a files
4. Name them: `1a-clipboard.m4a`, `1b-notion.m4a`, etc.
5. Drop them in `tests/fixtures/audio/`

Or, if you prefer text first:
1. Dictate into Apple Notes or just type what you'd say
2. Save as `tests/fixtures/text/1a-clipboard.txt`, etc.

---

## After Recording

We'll build eval fixtures from your recordings:

```
tests/
  fixtures/
    audio/          ← your .m4a recordings
    text/           ← transcribed or typed versions
  expected/         ← expected routing results (JSON)
  test_routing.py   ← automated eval runner
```

Each fixture gets a matching expected output:
```json
{
  "id": "1a-clipboard",
  "input": "Hey Claude, refactor the auth middleware to use...",
  "expected_destination": "clipboard",
  "expected_metadata": {
    "priority": "Medium"
  },
  "notes": "Clear code task signal"
}
```

The eval runner scores: destination accuracy, cleanup quality, metadata extraction.
