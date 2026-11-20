# .agents/

Operational context for AI agents working on this project.

## Structure

| Folder | Purpose |
|--------|---------|
| `skills/` | Reusable operational skills (how-tos for recurring tasks) |
| `memory/` | Notes and past decisions: why a choice was made |
| `instructions/` | Task- or milestone-specific instructions |
| `context/` | Project context: config, variables, catalog/schema mappings |
| `checklists/` | Deploy and QA checklists to run before declaring "done" |

## Conventions

- Markdown files, one topic per file, descriptive names
  (e.g. `memory/2026-11-19-loguru-choice.md`).
- Instructions in `AGENTS.md` remain the primary source: operational detail lives here.
- Update `memory/` on every significant architectural decision.
