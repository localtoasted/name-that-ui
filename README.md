# name-that-ui

> **Credit:** Based on [NameThat UI](https://namethatui.com/), created by [@argofowl](https://x.com/argofowl).

An Agent Skill for Codex and Claude Code that turns fuzzy UI descriptions, screenshots, and product requirements into precise component names and implementation briefs.

It can:

- identify UI patterns from plain English
- distinguish adjacent patterns such as tooltip, popover, menu, and dialog
- recommend the right primitive for a product need
- translate terminology across web, Electron, SwiftUI, and AppKit
- produce accessibility-aware implementation and debugging briefs
- search a refreshable local catalog of NameThat UI entries

## Install for Codex

Copy the bundled skill into your personal Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R name-that-ui ~/.codex/skills/name-that-ui
```

Invoke it directly with `$name-that-ui`, or let Codex load it automatically when your request matches its description:

```text
Use $name-that-ui to identify this UI element and write an implementation brief.
```

## Install for Claude Code

Copy the same bundled skill into your personal Claude Code skills directory—no fork or rewritten `SKILL.md` is required:

```bash
mkdir -p ~/.claude/skills
cp -R name-that-ui ~/.claude/skills/name-that-ui
```

Invoke it directly with `/name-that-ui`, or let Claude Code load it automatically:

```text
/name-that-ui identify this UI element and write an implementation brief
```

Claude Code and Codex both read the standard `SKILL.md`, `references/`, and `scripts/` content. `agents/openai.yaml` provides optional Codex UI metadata and is safely ignored by Claude Code. Bundled script instructions resolve from the skill directory (`${CLAUDE_SKILL_DIR}` in Claude Code), so they work regardless of the project currently open.

## Automatic catalog updates

The repository checks [NameThat UI](https://namethatui.com/) for catalog changes at **9:23 AM Pacific time**:

- daily through Saturday, July 18, 2026
- every Monday beginning July 20, 2026
- any time the workflow is manually started from GitHub's Actions tab

If nothing changed, the workflow exits without creating a commit. If entries were added, removed, or renamed, it opens or updates a `Refresh UI catalog` pull request for review. It never merges or publishes catalog changes automatically.

The scheduled workflow uses a standard GitHub-hosted Ubuntu runner, which is free for this public repository.

## Original creator credit

This is an unofficial companion skill inspired by and derived from [NameThat UI](https://namethatui.com/), the original visual dictionary of UI created by [@argofowl](https://x.com/argofowl).

The original website, concept, taxonomy, visual demonstrations, and editorial content belong to their creator. This repository is not affiliated with or endorsed by NameThat UI. Please visit the original website—it is the canonical visual reference and the reason this skill exists.

The skill stores a compact searchable index of public entry names and aliases and links each result back to its original NameThat UI page. `scripts/update_catalog.py` refreshes that index from the website's public structured metadata.

## Repository layout

```text
name-that-ui/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
```

## Validation

The shared skill is validated with the official Codex skill validator, follows Claude Code's Agent Skills directory format, and has been forward-tested on fuzzy identification, component selection, implementation briefs, and SwiftUI/AppKit translation.

## License

The original code and skill instructions in this repository are available under the MIT License. NameThat UI source material remains the property of its original creator; see [NOTICE](NOTICE).
