# Warm Future Design System

Warm Future combines warm neutral surfaces with a small set of optimistic
accents. Interfaces should remain practical, calm, and easy to scan.

## Palette

| Token | Color | Use |
| --- | --- | --- |
| Background | `#FFF9F4` | Main application background |
| Text | `#2F2A28` | Primary text and headings |
| Primary Pink | `#E56B8A` | Primary actions and active emphasis |
| Accent Turquoise | `#63D5D0` | Rules, active states, and fresh accents |
| Soft Yellow | `#F7D97A` | Reference and informational states |
| Mint Green | `#8ADDBA` | Ready, published, and shipped states |
| Lavender | `#B8A7E8` | Drafting and review states |
| Warm Gray | `#D8CCC3` | Paused, backlog, archived, and borders |
| Soft Coral | `#F2A6A0` | Blocked, overdue, and warning states |

Badge fills use pale companion tints, with the base palette colors retained on
their borders. This keeps status labels distinct without making tables noisy.

## Status Colors

| Status | Color |
| --- | --- |
| Active | Accent Turquoise |
| Doing / In Progress | Primary Pink |
| Ready / Ready to Publish | Mint Green |
| Done / Published / Shipped | Mint Green |
| Drafting / Needs Review / Needs Visual | Lavender |
| Paused / Backlog / Archived | Warm Gray |
| Overdue / Blocked | Soft Coral |
| Reference | Soft Yellow |

## Typography and Surfaces

Inter is preferred, with system sans-serif fonts as fallbacks. Cards use warm
off-white surfaces, subtle borders, restrained shadows, and a maximum corner
radius of 8px. Color should clarify state and hierarchy rather than decorate.

## Sidebar

The sidebar supplements the primary tabs with a compact overview of the app's
sections, storage connection, and workflow. Section markers may use the broader
palette, but navigation remains informational until dedicated page navigation
is introduced. Sidebar metadata uses the same warm surfaces, soft borders, and
restrained 8px corner radius as the main dashboard.

## Iconography

Use small emoji icons to improve scanning in section headers, tabs, and compact
sidebar labels. Icons should support a clear label rather than replace it. Keep
them out of dense tables and repeated controls, and use the platform emoji font
stack so Inter remains the primary interface typeface.

## Weekly Pulse

The Weekly Pulse is a compact overview band below the dashboard command center.
It reuses status calculations from the main dashboard and presents them as six
small, responsive cells. Use casual supporting copy and palette-colored edge
accents without introducing a strict daily workflow.

## Lost Nomad Branding

Lost Nomad is the personal and public brand carried by the dashboard. Its themes
include Florida and the Sunbelt, YIMBY growth and urbanism, optimistic futurism,
demographics and fertility, American liberal patriotism, global curiosity,
tropical vitalism, and data-backed public writing. It should feel research-led
and future-oriented rather than like generic travel content.

Lost Nomad sits inside the Warm Future visual system rather than replacing it.
The main title uses a short turquoise horizon line, a small pink sun, and a
restrained yellow continuation segment. The tiny gap and continuation suggest a
route or forward motion without reading as a loading bar. Compact sidebar and
main-title treatments use the same flex-aligned horizon, sun, and continuation
geometry, with the sidebar and dashboard overview versions scaled down. These
motifs suggest navigation, maps, growth, and data. Keep them near major brand
titles only. Do not add large logos, heavy imagery, or decorative motion.

## Tables and Metadata

Dataframes and editors use only wrapper-level spacing, warm borders, and modest
font sizing so native Streamlit sorting, scrolling, editing, and toolbars remain
usable. Avoid CSS that changes grid canvas dimensions or clips toolbar controls.

The sidebar shows the render-time refresh timestamp after Google Sheets data has
loaded successfully. A quiet footer closes the app with Lost Nomad, Warm Future,
Streamlit, and Google Sheets attribution without competing with dashboard content.

## Dashboard Polish

- Weekly Pulse values are the strongest element in each compact metric cell;
  labels and supporting notes remain small and quiet.
- Read-only project tables use pale status and stage chips for classification;
  they are not progress bars. Editable tables keep native Streamlit controls.
- Project Detail includes a four-segment qualitative progress bar labeled Plan,
  Build, Review, and Ready. Existing Status and Stage values determine the
  filled segments, with the farther-along mapping used. The bar intentionally
  has no numeric percentage and should not be treated as a precise estimate.
- Major section headers rotate through restrained palette-colored accent rails
  to improve scanning without changing card structure.
- The sidebar separates Lost Nomad branding, navigation, system metadata, and
  workflow into clear groups.
- A faint, evenly spaced turquoise dot grid may sit behind the app as a subtle
  map-and-data texture. It must remain low contrast and never reduce readability.
- Relevant sections may include one compact mini-stat line to summarize the
  counts users need before scanning a table. Avoid duplicating full metric cards.
- High-priority values in read-only task tables use a pale pink treatment and a
  narrow left rail. Editable tables retain native priority controls.
- The sidebar status legend uses small color dots rather than full explanatory
  cards. An About card may close the dashboard with concise product context.
- Active projects may appear as a responsive card grid near the top of Overview;
  each card stays compact and emphasizes its next action.
- Recently Updated uses a short, date-sorted table rather than a timeline. The
  publishing pipeline uses five ordered status segments with counts and no
  editing controls.
- The Lost Nomad North Star line belongs in the sidebar brand card and should
  remain quieter than the app title.
