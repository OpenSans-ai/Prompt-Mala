# Garland curtain

An interactive piece where every flower is one prompt, hung as painted garlands in a
carved doorway. 2,297 prompts across 57 sessions, 10 Jun 2026 – 5 Oct 2026.

The labelled data holds 2,404 prompts across 78 sessions. Sessions of fewer than ten
prompts are not drawn: 21 of them, 107 prompts, 4.5% of the total. They hung as stubs of
one to nine flowers and read as fraying rather than as sessions, and each still took a
full garland's width. `MIN_BEADS` in `index.html` is the threshold.

Nothing here is a photograph or a texture file. Every flower, and the carved timber around
them, is drawn procedurally into a canvas each frame.

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
- Vertical spacing is the real pause before that prompt: tight in fast streaks, visible
  bare thread where there was a gap.
- Each garland hangs from the underside of the arch directly above it, not from a straight
  rod, so the top of the curtain is a dome and the outer garlands start lower than the
  middle ones. Depths are measured from that per-garland start, so there is no single
  hanging line anywhere in the code.
- A thread stops at its last flower. Nothing trails below it.

## Encoding

**Two things are drawn, and only two.** Colour says which flower it is. How far open the
head is says how good the prompt was, as one rolled-up reading.

| Drawn | Encoding |
|---|---|
| Which flower | phase — **leaf** UI, **marigold** Setup, **rose** Bugs, **bougainvillea** UX |
| How open | overall quality — tight bud (rough), half-open (mixed), full bloom (solid), wide open (sharp) |

Four different species, not four tints of one, so they can be told apart by shape as well
as colour — which matters once the heads are small.

UI is the leaf. It is 63% of the data, and in a real garland the green is what there is
most of; marigolds are strung through it, not the other way round. Making the dominant
phase the quiet element is also what keeps the curtain from shouting — the colour lands on
the three phases you actually want to pick out.

Everything else is in the panel on the right and nowhere on the flower.

This is a deliberate retreat. Clarity, specificity, grounding and bundling each used to own
a visual property — edge bleed, pigment density, a leaf or gold bud, petal count. Five
things on every head meant that at any zoom where you could see the whole curtain it read
as noise, and at any zoom where you could read one flower you could not see the curtain.
Rolling them into one number costs nothing, because the four labels are still printed
individually a few centimetres to the right.

Openness is a weighted roll-up:

| Label | Weight | Direction |
|---|---|---|
| Specificity | 0.40 | specific is better — the strongest single signal of whether a prompt could be acted on alone |
| Clarity | 0.22 | clean is better |
| Grounding | 0.18 | anchored is better — pointing at an image or a comparison is evidence, not noise |
| Bundling | 0.20 | a single ask is better |

Those weights are a judgement, not a measurement. The tiers land at roughly 21 / 30 / 35 /
14 per cent, which is a spread rather than one bucket swallowing the set — worth
re-checking if the labels ever change.

**Decision fatigue**, **hour of day** and **word count** are not drawn at all. They are in
the panel.

The key under the piece shows a painted swatch for each of the eight things that are drawn,
rendered with the same code as the curtain, so it cannot drift from what is on screen. The
openness row is shown on the marigold — openness barely reads on a leaf.

## How a flower is painted

Each head starts on a dark base disc. The gaps between the petals fall through to it, and
that shadow underneath is what gives a flower its depth. How much of the disc shows depends
on how densely the head covers it — a marigold buries it, four bracts would leave it
sitting there as a dark ball.

Then the head is built according to its species:

- **pompom** (marigold) — rings of small florets packed from the rim inward, each ring a
  little smaller and lighter so the head domes toward the middle, then a tight knot of buds
  at the crown. Every floret gets its own seat shadow, body and lit top edge. These are
  drawn **crisp**: a marigold reads as hundreds of distinct little petals catching light,
  and feathering the edges destroys exactly that.
- **broad** (rose) — overlapping petals, outer rings first. All the shadows for a ring go
  down before any of the bodies; shadow-then-body per petal buries each body under the next
  petal's shadow and the head comes out black.
- **bract** (bougainvillea) — three broad papery bracts with a visible vein.
- **leaf** — one blade off true, with a midrib and side veins.

Over the whole frame goes a tooth of paper grain, composited `soft-light`, which is what
stops the gradients beneath reading as vector art.

Because only the phase varies per flower now, the sprite cache collapsed from about 1,200
entries to 43 — four flowers times four degrees of openness times the zoom steps.

## The doorway

The curtain hangs in a cusped doorway of dark carved timber, with daylight behind it. There is no wall or
floor drawn around it — the page shows through, so the doorway reads as one object on
paper rather than as a room. Everything that hangs is clipped to the opening, so a
swinging strand cannot stray outside it. There is no hinged door: the curtain *is* what
closes the opening.

The arch is a two-centred pointed arch — each half struck from a centre offset past the
middle, the two meeting in a point at the crown. The rise has to exceed the half-width or
the centres fall inside and it rounds off into a dome instead of coming to a point. Five
foils are cut into each half, bulging inward between sharp cusps.

Working outward from the opening: a timber bead lining it, then a moulded lip, then a band
of carved rosettes, then a post down each jamb, with a carved lintel across the head.
It is all one dark oiled wood, with the grain running the height of the jambs.

Each layer is a stroke along the arch profile, offset further out than the last — strokes
are centred on the path, so a width of 2w reaches w either side, and `DOOR.stoneOff` is
where the outer carving has to start to clear the bead.
The carving is deliberately small and low in contrast — at the opening zoom it should read
as texture, and only resolve into rosettes when you zoom in. Relief is faked the way a
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
- **Pinch** (or scroll wheel) to zoom. You land close enough that a single head reads as a
  painted flower rather than a dot; the long garlands run off the bottom of the frame.
  Zooming out stops with the whole doorway in view, where it reads as pattern instead.
  **Reset view** returns to the opening framing, not to the whole doorway.
- **Hover** a flower and the side panel reads it straight away — specificity as the
  headline, then the analysis, then the context. A small label follows the pointer too.
- **Click** to pin a flower, so the panel holds it when the pointer moves off. Previous/Next
  walk the whole run in order.
- **Pause motion** freezes the sway; panning, zooming and selection keep working.

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
