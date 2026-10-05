# Bead curtain

An interactive piece where every bead is one prompt. 2,404 prompts across 78 sessions,
10 Jun 2026 – 5 Oct 2026.

## Files

| Path | Publish? | What it is |
|---|---|---|
| `index.html` | yes | The piece. Single self-contained file — open it directly, no server needed. |
| `public/data/beads.json` | yes | The labelled data as a separate artifact. Labels, numbers and timestamps only. |
| `private/labeled_prompts_full.json` | **no** | Same records **with the prompt text**. Working file, git-ignored. |

`index.html` has the bead data inlined so it works from `file://`, offline, and when
emailed as one attachment. That inlined copy is identical to `beads.json` — no prompt text.

## Fixed structure

- One bead = one prompt. One strand = one session, top to bottom in the order typed.
- Strands run left to right in session order.
- Every bead is the **same width**. Only length changes, and shape follows length tier:

  | Words | Shape |
  |---|---|
  | ≤ 5 | circle (seed bead) |
  | 6–15 | pill (short barrel) |
  | 16–40 | diamond (faceted) |
  | 41+ | tube (slender) |

  Length grows fast then levels off (capped at ~2.1× bead width), so a 1,100-word pasted
  prompt is a long bead that still fits the screen.

  The vertical scale is deliberately compressed. The floor is set by the seed bead: a
  ≤5-word prompt is a circle of exactly one bead width, so a 6-word prompt has to be
  longer than that or the encoding would invert. That floor, times the 98 prompts in the
  longest session, is what fixes the height of the whole piece.
- Shape and length are **fixed structure** — they encode word count and nothing else.
- Vertical spacing is the real pause before that prompt: tight in fast streaks, visible
  bare string where there was a gap.

## Encoding

One curtain, no modes. Every bead carries all five visible channels at once, so the
whole dataset is readable without switching anything. The channels stack because each
one owns a different property of the glass.

| Channel | Encoding |
|---|---|
| Phase | colour of the glass — sapphire UI, smoky quartz Setup, garnet Bugs, amethyst UX |
| Clarity | polish — a tight bright specular (clean), softened (minor typos), dull and pitted (heavy typos) |
| Specificity | density — solid (specific) → thin and pale (vague) |
| Groundedness | an inclusion: plain, white fleck (image reference), gold band (comparison reference) |
| Bundling | facet lines cut across the body — smooth (single ask) → multi-faceted (many asks) |

**Decision fatigue** and **hour of day** both wanted colour, which phase already owns.
They are not drawn on the bead; they appear in the tap sheet with everything else.

## Interaction

- **Drag** across the strands — they sway and click softly, and the view pans with you.
- **Pinch** (or scroll wheel) to zoom. Far out reads as a pattern; close up shows single beads.
  Zooming out stops once the curtain spans the full width — the curtain is taller than it
  is wide, so fitting the height too would strand it in a column with bare paper down both
  sides. At that point most of the piece is on screen; the tail of the few longest strands
  runs past the bottom, and you pan down for it.
- **Tap a bead** for its time and all of its labels.

## Privacy

This is client work. The piece never displays prompt text, file names or client names.
`beads.json` and the inlined copy carry only labels, numbers and timestamps. The
`feature` field used during labelling was dropped from both, since its values were nouns
lifted from the prompts. `private/` is git-ignored and must stay out of anything published.

## Rebuilding

`index.html` is assembled from `curtain_template.html` plus the inlined data. The
template is the whole piece with a single `/*__DATA__*/` line standing in for the
payload; `index.html` is that file with the marker replaced by three lines —
`const SESSIONS=…`, `const LEGEND=…`, `const ROWS=…`.

To regenerate after changing labels, re-run the Stage 2/3 scripts and swap the marker
for the new payload.

**Edit the template, not `index.html`.** They are the same file apart from those three
lines, so a change made only to `index.html` is silently discarded the next time the
data is re-injected.

## Caveats

Labels come from keyword and pattern heuristics over the prompt text, not a per-prompt
semantic read — 2,404 prompts was too many to judge individually. They are directionally
right but will misfire on sarcasm, heavy typos, and terse phrasing. Clarity in particular
measures typo density against a dictionary, so unusual proper nouns can read as typos.
