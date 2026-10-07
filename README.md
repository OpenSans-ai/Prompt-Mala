# Garland curtain

An interactive piece where every flower is one prompt, hung as painted garlands in a
carved doorway. 2,297 prompts across 57 sessions, 10 Jun 2026 – 5 Oct 2026.

The labelled data holds 2,404 prompts across 78 sessions. Sessions of fewer than ten
prompts are not drawn: 21 of them, 107 prompts, 4.5% of the total. They hung as stubs of
one to nine flowers and read as fraying rather than as sessions, and each still took a
full garland's width. `MIN_BEADS` in `index.html` is the threshold.

Nothing here is a photograph or a texture file. Every flower, and the stone and timber
around them, is drawn procedurally into a canvas each frame.

## Files

| Path | Publish? | What it is |
|---|---|---|
| `index.html` | yes | The piece. Single self-contained file — open it directly, no server needed. |
| `public/data/beads.json` | yes | The labelled data as a separate artifact. Labels, numbers and timestamps only. |
| `private/labeled_prompts_full.json` | **no** | Same records **with the prompt text**. Working file, git-ignored. |

`index.html` has the data inlined so it works from `file://`, offline, and when
emailed as one attachment. That inlined copy is identical to `beads.json` — no prompt text.

## Fixed structure

- One flower = one prompt. One garland = one session, top to bottom in the order typed.
- Garlands run left to right in session order.
- A flower is round, so one number is both its width and its height. Word count reads as
  how open the head is:

  | Words | Form |
  |---|---|
  | ≤ 5 | bud |
  | 6–15 | half-open |
  | 16–40 | full bloom |
  | 41+ | double bloom |

  Size grows fast then levels off, so a 60-word prompt is a full head and a 3-word one a
  tight bud, without the longest prompt dwarfing everything around it.
- Form and size are **fixed structure** — they encode word count and nothing else.
- Vertical spacing is the real pause before that prompt: tight in fast streaks, visible
  bare thread where there was a gap.
- Each strand hangs from the underside of the arch directly above it, not from a straight
  rod, so the top of the curtain is a dome and the outer strands start lower than the
  middle ones. Depths are measured from that per-strand start, so there is no single
  hanging line anywhere in the code.
- A thread stops at its last flower. Nothing trails below it.

## Encoding

One curtain, no modes. Every flower carries all five visible channels at once, so the
whole dataset is readable without switching anything. The channels stack because each one
owns a different property of the painting.

| Channel | Encoding |
|---|---|
| Phase | which flower — cornflower UI, marigold Setup, vermilion Bugs, bougainvillea UX |
| Clarity | how wet the brush was — a clean prompt holds its edge, a typo-ridden one bleeds into the paper |
| Specificity | how much pigment — saturated (specific) → washed out (vague) |
| Groundedness | a mark beside the head: plain, a leaf (image reference), a gold bud (comparison reference) |
| Bundling | petal count — 5 (single ask), 8 (few asks), 12 (many asks) |

**Decision fatigue** and **hour of day** both wanted colour, which phase already owns.
They are not drawn on the flower; they appear in the side panel with everything else.

The key under the piece shows a painted swatch for every one of these, drawn with the same
renderer as the curtain itself, so it cannot drift from what is actually on screen.

## How a flower is painted

Nothing is outlined. Each head is laid down the way a brush would:

1. a loose wash of colour, with no edge at all
2. for each petal, a darker, slightly wider petal first — it only shows in the gaps
   between the petals on top, and it is what stops the head filling in and reading as one
   soft disc
3. the petal itself, every one a slightly different mix, because pigment never repeats
4. a dry darker touch at the throat, and stamens on anything properly open

Edges are feathered by drawing the same shape again at a widening scale and falling alpha
— that is the `soft` term, and clarity drives it. Over the whole frame goes a tooth of
paper grain, composited `soft-light`, which is what stops the gradients beneath reading as
vector art.

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

The arch has to be solved before the flowers, because the garlands hang from it: the arch
comes from the curtain's width, the garland tops from the arch, the flower depths from the
tops, and only then is the floor placed under the longest garland. Garlands hang from the
*smooth* arch, not the cusped edge — following the scallops would give the top of the
curtain a saw-tooth that reads as a mistake.

## Interaction

The piece hangs on the left; a reading of one flower sits on the right.

- **Drag** across the garlands — they sway and rustle softly, and the view pans with you.
- **Pinch** (or scroll wheel) to zoom. Zooming out stops with the whole doorway in frame,
  so it reads as a curtain hanging in an opening rather than a cropped field. Far out
  reads as a pattern; close up shows single painted heads.
- **Hover** a flower and the side panel reads it straight away — specificity as the
  headline, then the analysis, then the context. A small label follows the pointer too.
- **Click** to pin a flower, so the panel holds it when the pointer moves off. Previous/Next
  walk the whole run in order.
- **Reset view** returns to the full curtain and clears the selection. **Pause motion**
  freezes the sway; panning, zooming and selection keep working.

Under 860px wide the panel stacks underneath and stays shut until you pick a flower, so
it does not eat half the piece while empty. The piece itself keeps a floor of 190px and the
key scrolls, so a short window can never squeeze the canvas to nothing.

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
