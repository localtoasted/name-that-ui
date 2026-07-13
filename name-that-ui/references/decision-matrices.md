# UI pattern decision matrices

Use these matrices after searching the catalog. Behavior is decisive; visual styling is secondary.

## Floating and overlay surfaces

| Pattern | Trigger | Interactive content | Blocks background | Typical close |
|---|---|---:|---:|---|
| Tooltip | Hover and focus | No | No | Pointer/focus leaves; Escape |
| Hover card | Hover and focus | Usually preview-only | No | Pointer/focus leaves; Escape |
| Popover | Click/press | Yes | No | Explicit toggle, outside click, Escape |
| Dropdown menu | Click/press | Action items | No | Selection, outside click, Escape |
| Context menu | Right-click/long press | Action items | No | Selection, outside click, Escape |
| Modal dialog | Explicit action | Yes | Yes | Task completion, cancel, Escape when safe |
| Drawer / sheet | Explicit action | Yes | Often | Task completion, outside click if safe, Escape |
| Lightbox | Select media | Media navigation | Yes | Close, Escape, sometimes outside click |
| Toast | Automatic after event | At most a simple action | No | Timeout or dismiss |

Boundary rules:

- If it contains form controls, it is not a tooltip.
- If it is a list of commands with roving keyboard selection, prefer a menu.
- If it must be noticed or completed before continuing, use a dialog rather than a popover.
- If it previews linked content without requiring a click, consider a hover card.
- “Popup” describes appearance, not a precise component.

## Selection controls

| Need | Pattern | Rule |
|---|---|---|
| Independent yes/no option in a form | Checkbox | Checked state is part of a submitted set |
| Immediate system mode on/off | Switch | State takes effect immediately |
| One choice from a visible set | Radio group | All options remain visible |
| One compact choice from many | Select / pop-up button | Closed control displays current value |
| Searchable choice or free text | Combobox | Text input plus suggestion/listbox behavior |
| Switch views or modes | Tabs / toggle group | Use tabs for panels; toggle group for compact modes/tools |
| Primary action plus alternate actions | Combo/split button | Main segment acts; arrow opens alternatives |

Never use multiple independently toggleable buttons when the choices are mutually exclusive without implementing the selection semantics.

## Loading and progress

| Situation | Pattern |
|---|---|
| Duration/progress is known | Progress bar or determinate ring |
| Short wait, progress unknown | Spinner |
| Page/card structure is loading | Skeleton matching the eventual layout |
| Background action completed | Toast or inline status |

Avoid indefinite spinners when progress or staged status can be shown. Respect reduced-motion preferences.

## Navigation and disclosure

- **Tabs** switch peer panels inside the same context.
- **Accordion/disclosure** expands content inline without changing location.
- **Sidebar/source list** navigates durable sections or objects.
- **Breadcrumbs** expose hierarchy and provide ancestor navigation.
- **Command palette** searches actions or destinations; it is not a replacement for essential visible navigation.
- **Overflow menu / three dots** holds secondary actions, not primary or frequent ones.

## macOS vocabulary fork

| Visible thing | SwiftUI | AppKit |
|---|---|---|
| Menu bar extra / status item | `MenuBarExtra` | `NSStatusItem` |
| Popover | `.popover(...)` | `NSPopover` |
| Sidebar / navigation split | `NavigationSplitView` | `NSSplitViewController` |
| Toolbar item | `ToolbarItem` | `NSToolbarItem` |
| Search field | `.searchable(...)` | `NSSearchField` |
| Sheet | `.sheet(...)` | `NSWindow.beginSheet` |
| Save panel | `.fileExporter(...)` | `NSSavePanel` |
| Segmented control | `Picker` with segmented style | `NSSegmentedControl` |
| Settings window | `Settings` scene | preferences `NSWindowController` |

In a mixed project, identify the layer being changed. On Electron, use web primitives inside the window and Electron APIs for shell features such as `Tray`.

## Accessibility invariants

- Start with the native semantic element or established library primitive.
- Make every hover-disclosed affordance available from keyboard focus.
- Keep keyboard focus visible with `:focus-visible` or the native platform focus ring.
- Give icon-only controls an accessible name.
- Return focus to the invoking control when a temporary modal surface closes.
- Do not add ARIA roles that contradict native semantics.
- Test zoom, long text, reduced motion, high contrast, and keyboard-only use.
- Verify platform-specific keyboard behavior from the relevant primary specification rather than guessing.

