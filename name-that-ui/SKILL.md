---
name: name-that-ui
description: Identify, disambiguate, choose, and precisely specify user-interface patterns from screenshots, vague descriptions, product requirements, or existing code. Use for questions like "what is this UI thing called?", "is this a popover or tooltip?", "which component should I use?", translating plain English into web, ARIA, Electron, SwiftUI, or AppKit terminology, producing implementation-ready prompts, or debugging a UI pattern's behavior and accessibility.
---

# name-that-ui

Turn fuzzy visual language into the correct component name, behavior contract, and build-ready brief. Use the local catalog as the fast index and NameThat UI as the visual source of truth when live browsing is useful.

## Route the request

1. **Name it** — Identify a visible element from a screenshot or description.
2. **Choose it** — Select the right pattern for a product need.
3. **Translate it** — Map a generic name to the project's actual framework.
4. **Specify it** — Write an implementation brief or coding-agent prompt.
5. **Debug it** — Diagnose behavior, layering, focus, keyboard, or dismissal failures.

Use more than one route when needed. Do not stop at a label if the user clearly needs a build decision.

## Identify the pattern

1. Inspect the screenshot, prose, code, or product context.
2. Extract behavioral evidence before guessing:
   - trigger: click, hover, focus, right-click, drag, scroll, or automatic
   - placement: inline, anchored, viewport overlay, window-attached, or system chrome
   - content: label, actions, form controls, navigation, status, or rich preview
   - modality: whether the rest of the interface is blocked
   - persistence: what closes it and whether it survives selection
   - selection model: single, multiple, mutually exclusive, or none
3. Search the bundled catalog:

Resolve `<skill-dir>` to the directory containing this `SKILL.md`. In Claude Code, use `${CLAUDE_SKILL_DIR}`. In Codex, use the absolute path of the loaded skill directory, commonly `${CODEX_HOME:-$HOME/.codex}/skills/name-that-ui`.

```bash
python3 "<skill-dir>/scripts/ui_lookup.py" "plain-English description"
python3 "<skill-dir>/scripts/ui_lookup.py" "description" --platform web --json
```

4. Compare the top candidates using `references/decision-matrices.md` when the boundary is ambiguous.
5. If visual evidence is insufficient, state the top candidate and the one observation that would distinguish it. Do not invent certainty.

## Choose the right pattern

Start from behavior, not appearance. A rounded floating rectangle can be a tooltip, popover, menu, dialog, or hover card; styling does not decide the primitive.

Apply these checks:

- Use a **tooltip** only for a short, non-interactive label or hint on hover and keyboard focus.
- Use a **menu** for a keyboard-navigable action list that normally closes after selection.
- Use a **popover** for anchored rich or interactive content that does not block the rest of the page.
- Use a **dialog** for a focused task or decision that blocks background interaction.
- Use a **drawer/sheet** for a larger edge-attached task or contextual workspace.
- Use a **toast** for brief, non-blocking status; never make it the only place critical information or recovery actions exist.

Read `references/decision-matrices.md` for overlays, selection controls, loading feedback, navigation, and macOS-specific forks.

## Translate into the project

Inspect the existing stack before naming APIs. Preserve the project's current primitive and component library unless the user asks for a migration.

- Web: distinguish semantic HTML, ARIA patterns, and library components. Prefer native semantics before adding ARIA.
- Electron/Tauri: use web UI vocabulary inside the window; use the shell API for desktop chrome such as Electron `Tray`.
- SwiftUI: use declarative names such as `MenuBarExtra`, `NavigationSplitView`, `ToolbarItem`, and `.popover`.
- AppKit: use `NS` types such as `NSStatusItem`, `NSSplitViewController`, `NSToolbarItem`, and `NSPopover`.
- Mixed macOS app: name both the visible element and the implementation layer. If uncertain, give both SwiftUI and AppKit names and tell the coding agent to inspect before changing anything.

Never add a second implementation merely because the first uses a different vocabulary.

## Produce the answer

For a naming request, use this compact shape:

```markdown
**Name:** Popover
**Why:** It is click-triggered, anchored to a control, contains interactive content, and does not block the page.
**Not:** Tooltip — tooltips are non-interactive and appear on hover/focus.
**In this project:** Radix `Popover` / HTML `popover`.
```

For an implementation request, include:

1. canonical name and framework-specific primitive
2. trigger and anchoring
3. content and interaction model
4. open/close and dismissal rules
5. keyboard and focus behavior
6. responsive behavior
7. layering, collision, and scrolling behavior
8. states: default, hover, focus, active, disabled, loading, empty, and error as relevant
9. acceptance checks written as observable outcomes

Use `references/implementation-brief.md` as the template. Keep the user's own product language for labels; use technical vocabulary for the implementation contract.

## Debug the pattern

Check the primitive before the CSS. Common root causes:

- wrong primitive for the interaction model
- overlay clipped by an overflow ancestor or rendered in the wrong layer
- missing collision/flip/shift behavior near viewport edges
- outside-click firing before an inside interaction
- focus not moved, trapped, restored, or visibly indicated as required
- Escape, Tab, arrow-key, or typeahead behavior missing
- state duplicated between the trigger and surface
- mobile behavior copied from desktop without adapting hover or viewport constraints

Report the likely named subsystem, the evidence, and the smallest safe correction. Do not redesign unrelated UI.

## Use the source site

The bundled catalog is a concise index derived from [NameThat UI](https://namethatui.com/), the original visual UI dictionary created by [@argofowl](https://x.com/argofowl). This is an unofficial companion skill, not a frozen copy of every article and not an official affiliation. Browse the matching source page when the user supplies a screenshot, asks for a subtle distinction, needs a framework mapping not in local references, or requests current information. Prefer primary platform and library documentation for exact API or accessibility claims that may change.

Refresh the local index when requested:

```bash
python3 "<skill-dir>/scripts/update_catalog.py"
```
