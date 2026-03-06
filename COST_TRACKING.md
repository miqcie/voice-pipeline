# Engineering Cost Tracking

## AI-Assisted Build (Claude Opus 4.6 via Claude Code)

### Session 1: Initial Scaffold (March 6, 2026)

| Phase | Wall Clock | Claude Turns | Files Created |
|-------|-----------|-------------|---------------|
| Plan review + research (audio API docs) | ~8 min | 12 | 0 |
| Project scaffold (pyproject, gitignore, README, CLAUDE.md) | ~3 min | 5 | 5 |
| Core Python modules (process, route, main) | ~4 min | 4 | 5 |
| Shell script (voice-route.sh) | ~1 min | 1 | 1 |
| Git init + GitHub repo creation | ~4 min | 6 | 0 |
| **Total** | **~20 min** | **28** | **11 files** |

### Claude Code Cost Estimate
- Model: Claude Opus 4.6 ($5/1M input, $25/1M output)
- Estimated input tokens: ~80K (system prompt + skill docs + conversation)
- Estimated output tokens: ~15K (code generation + responses)
- **Estimated API cost: ~$0.78**

### Lines of Code Written
| File | Lines | Complexity |
|------|-------|------------|
| process.py | 108 | Medium — API integration, audio encoding, JSON parsing |
| route.py | 148 | Medium — 4 destination routers, 1Password/Notion API |
| main.py | 62 | Low — argparse CLI |
| voice-route.sh | 52 | Medium — sox recording with silence detection |
| prompts/router.md | 46 | N/A — prompt template |
| pyproject.toml | 14 | Low — config |
| README.md | 57 | Low — docs |
| CLAUDE.md | 24 | Low — project conventions |
| __init__.py + __main__.py | 4 | Trivial |
| .gitignore | 7 | Trivial |
| **Total** | **~522** | |

---

## Human-Only Estimate (100% manual)

### Assumptions
- Mid-senior Python developer familiar with Claude API
- Has built CLI tools before
- Needs to research: Claude audio input format, Notion API, beads CLI

| Phase | Estimated Time | Notes |
|-------|---------------|-------|
| Research Claude audio API docs | 30-45 min | Finding docs, understanding content block format, testing |
| Research Notion API for task creation | 20-30 min | Property schema, auth flow |
| Project setup (uv, pyproject, git) | 10-15 min | Routine but still takes time |
| process.py (API integration) | 45-60 min | Audio encoding, prompt engineering, JSON parsing edge cases |
| route.py (4 destinations) | 60-90 min | Notion API integration, 1Password lookup, beads CLI, error handling |
| main.py (CLI) | 15-20 min | Straightforward argparse |
| voice-route.sh (sox recording) | 20-30 min | sox flags for silence detection, signal handling |
| Router prompt (prompt engineering) | 30-45 min | Iterating on classification accuracy |
| README + docs | 15-20 min | |
| Testing + debugging | 45-60 min | API errors, audio format issues, Notion schema mismatches |
| Git + GitHub setup | 5-10 min | |
| **Total** | **5-7 hours** | |

### Human Cost Estimate
- Senior developer rate: $150-200/hr
- **Estimated human cost: $750 - $1,400**

---

## Comparison Summary

| Metric | AI-Assisted | Human-Only | Speedup |
|--------|------------|------------|---------|
| Wall clock time | ~20 min | 5-7 hours | ~15-20x |
| API/labor cost | ~$0.78 | $750-1,400 | ~960-1,800x |
| Files created | 11 | 11 | Same |
| Lines of code | ~522 | ~522 | Same |

### Caveats
- AI time doesn't include the **planning session** (separate conversation, ~30 min)
- Human estimate assumes starting from scratch with same requirements
- AI code still needs **human review** and the **routing prompt** (TODO(human))
- Human-coded version would likely have tests from the start
- Cost comparison is unfair to humans — AI doesn't need coffee breaks, but it does need sandbox permission approvals :)

---

## Running Cost Tracker

Update this section as work continues.

| Date | Session | AI Time | AI Cost | What was done |
|------|---------|---------|---------|---------------|
| 2026-03-06 | #1 | 20 min | ~$0.78 | Full scaffold, GitHub repo |
| 2026-03-06 | #2 | 10 min | ~$0.40 | Interview guide, eval framework, test harness |
| | | | | |
