# Bead curtain

An interactive piece where every bead is one prompt, hung as a bead curtain in a lit
doorway. 2,297 prompts across 57 sessions, 10 Jun 2026 – 5 Oct 2026.

The labelled data holds 2,404 prompts across 78 sessions. Sessions of fewer than ten
prompts are not drawn: 21 of them, 107 prompts, 4.5% of the total. They hung as stubs of
one to nine beads and read as fraying rather than as sessions, and each still took a full
strand's width. `MIN_BEADS` in `index.html` is the threshold.

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
- Each strand hangs from the underside of the arch directly above it, not from a straight
  rod, so the top of the curtain is a dome and the outer strands start lower than the
  middle ones. Depths are measured from that per-strand start, so there is no single
  hanging line anywhere in the code.
- A cord stops at its last bead. Nothing trails below it.

## Encoding

One curtain, no modes. Every bead carries all five visible channels at once, so the
whole dataset is readable without switching anything. The channels stack because each
one owns a different property of the glass.

| Channel | Encoding |
|---|---|
| Phase | colour of the glass — blue UI, yellow Setup, scarlet Bugs, magenta UX |
| Clarity | polish — a tight bright specular (clean), softened (minor typos), dull and pitted (heavy typos) |
| Specificity | density — solid (specific) → thin and pale (vague) |
| Groundedness | an inclusion: plain, white fleck (image reference), gold band (comparison reference) |
| Bundling | facet lines cut across the body — smooth (single ask) → multi-faceted (many asks) |

**Decision fatigue** and **hour of day** both wanted colour, which phase already owns.
They are not drawn on the bead; they appear in the side panel with everything else.

## The doorway

The curtain hangs in a cusped stone doorway with daylight behind it. There is no wall or
floor drawn around it — the page shows through, so the doorway reads as one object on
paper rather than as a room. Everything that hangs is clipped to the opening, so a
swinging strand cannot stray outside it. There is no hinged door: the curtain *is* what
closes the opening.

The arch is a two-centred pointed arch — each half struck from a centre offset past the
middle, the two meeting in a point at the crown. The rise has to exceed the half-width or
the centres fall inside and it rounds off into a dome instead of coming to a point. Five
foils are cut into each half, bulging inward between sharp cusps.

Working outward from the opening: a dark timber frame lining it, then a pale stone lip,
then a band of carved rosettes, then a pilaster down each jamb. Each layer is a stroke
along the arch profile, offset further out than the last — strokes are centred on the
path, so a width of 2w reaches w either side, and `DOOR.stoneOff` is where the stonework
has to start to clear the timber.
The carving is deliberately small and low in contrast — at the opening zoom it should read
as texture, and only resolve into flowers when you zoom in. Relief is faked the way a
carver reads it, a shadow cast down-right and a highlight up-left, with the offsets floored
at about a pixel so it does not flatten out when zoomed away.

The arch has to be solved before the beads, because the strands hang from it: the arch
comes from the curtain's width, the strand tops from the arch, the bead depths from the
tops, and only then is the floor placed under the longest strand. Strands hang from the
*smooth* arch, not the cusped edge — following the scallops would give the top of the
curtain a saw-tooth that reads as a mistake.

The light matters to the encoding, not just the mood: the beads are backlit, which is what
the glass renderer was built for. Specificity is drawn as density, and a thin bead against
a bright opening is exactly what a vague prompt should look like.

## Interaction

The piece hangs on the left; a reading of one bead sits on the right.

- **Drag** across the strands — they sway and click softly, and the view pans with you.
- **Pinch** (or scroll wheel) to zoom. Zooming out stops with the whole doorway in frame,
  so it reads as a curtain hanging in an opening rather than a cropped field. Far out
  reads as a pattern; close up shows single beads lit from behind.
- **Hover** a bead and the side panel reads it straight away — specificity as the
  headline, then the analysis, then the context. A small label follows the pointer too.
- **Click** to pin a bead, so the panel holds it when the pointer moves off. Previous/Next
  walk the whole run in order.
- **Reset view** returns to the full curtain and clears the selection. **Pause motion**
  freezes the sway; panning, zooming and selection keep working.

Under 860px wide the panel stacks underneath and stays shut until you pick a bead, so it
does not eat half the piece while empty.

The analysis bars fill to where a label sits on its own scale, in the direction of the
thing named — Specificity full is *specific*, Bundling full is *many asks*. The value
printed is always the label. There is deliberately no 0–100 score: these are keyword
heuristics, and a number would imply precision they do not have.

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
