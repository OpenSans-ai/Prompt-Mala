# Garland curtain

An interactive piece where every flower is one prompt, hung as painted garlands in a
carved doorway. 2,297 prompts across 57 sessions, 10 Jun 2026 – 5 Oct 2026.

The labelled data holds 2,404 prompts across 78 sessions. Sessions of fewer than ten
prompts are not drawn: 21 of them, 107 prompts, 4.5% of the total. They hung as stubs of
one to nine flowers and read as fraying rather than as sessions, and each still took a
full garland's width. `MIN_BEADS` in `index.html` is the threshold.

The doorway is a painting, `public/door.png`. Everything hanging in it — every flower, leaf
and thread — is drawn procedurally into a canvas each frame.

**`index.html` is no longer self-contained.** It needs `public/door.png` beside it. Opened
on its own the curtain still draws, but against bare paper with no doorway; the console
says so. This is a change from how the piece used to work, and it is the cost of using a
painted door rather than a drawn one.

## Files

| Path | Publish? | What it is |
|---|---|---|
| `index.html` | yes | The piece. Needs `public/door.png` alongside it. |
| `public/door.png` | yes | The painted doorway, 919×1711. 2.2MB. |
| `public/data/beads.json` | yes | The labelled data as a separate artifact. Labels, numbers and timestamps only. |
| `private/labeled_prompts_full.json` | **no** | Same records **with the prompt text**. Working file, git-ignored. |

`index.html` has the data inlined, so the only thing it needs from outside is the door
image. That inlined copy is identical to `beads.json` — no prompt text.

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

The flowers are seen **from the side**, not looked down into. That is almost entirely a
matter of light: a head lit from its own centre reads as being viewed from above, so
instead the light comes down the top and the shadow gathers underneath, and a green calyx
peeks out at the base. There is no bright eye in the middle — that one detail was what made
every flower look like a specimen pinned flat.

Each head starts on a dark base disc. The gaps between the petals fall through to it, and
that shadow underneath is what gives a flower its depth. How much of the disc shows depends
on how densely the head covers it — a marigold buries it, four bracts would leave it
sitting there as a dark ball.

Then the head is built according to its species:

- **pompom** (marigold) — a ball of florets. Rings still run rim to middle so the packing
  stays dense, but nothing is lit by its distance from the centre: brightness comes from
  how high up the face a floret sits, which is what turns a flat rosette into a sphere.
  Every floret gets its own seat shadow, body and lit top edge. These are drawn **crisp** —
  a marigold reads as hundreds of distinct little petals catching light, and feathering the
  edges destroys exactly that.
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

The door is `public/door.png` drawn into the scene, not geometry. What the code holds is a
*measurement* of it: where the opening sits inside the image, and how the carved soffit runs
across the top. Those numbers are in `DOORIMG`.

They were read off the image rather than guessed. Tracing the dark interior against the
bright frame works down the left-hand jamb, which is lit; the right-hand jamb falls in
shadow and no brightness threshold separates it from the carving. The arch is symmetric, so
the lit half was traced and mirrored.

Everything else follows from that measurement. `PX` sets how many world units one image
pixel is worth, scaled off `CURTAIN_REACH` — the span of the outermost garland centres plus
the overhang of the widest head. It is deliberately not scaled off `worldW`, which carries a
margin at each end: that left the garlands seven per cent short of each jamb, and the arch
went on curving down past the last one with nothing under it, a visible wedge of empty
doorway at both shoulders.
The garland tops come from the soffit, so they hang from the painted arch — and `SOFFIT` is
*negative*. Each garland starts a little above the soffit, so the clip takes the top off its
first flower and you see the heads emerging from under the carving. Hung level with the
arch, or on a visible cord below it, they read as floating in the doorway rather than fixed
to it. The offset is kept small so even the smallest flower still shows two thirds of
itself. The thread is pale for the same reason: a brown thread on a brown doorway is
invisible, and without a visible thread the flowers look like they are hanging on nothing. The opening path
— down one jamb, across the bottom of the image, up the other, back over the arch — is the
clip, so nothing strays onto the carving.

A garland longer than the door is cut at the bottom of the image. That is accepted rather
than fought.

### How big a flower can be

The door is contained, never cropped, so its scale is fixed by the stage. That leaves
`KIND_D` as the only lever on how big a flower looks, and there is a hard limit behind it:
57 garlands have to fit across the opening. On a 1300×860 stage the door lands at 448px
wide, the opening at about 260px, and each garland gets 4.6px of it.

`KIND_D` is deliberately set wider than `STRAND_GAP` — the largest head is 2.1× the pitch —
so neighbouring garlands overlap and the curtain reads as a thick mass of flowers rather
than rows of dots. That is also how a real garland looks. Pushing it further keeps making
the flowers bigger, at the cost of being able to follow any single garland down.

The other lever is fewer garlands: raising `MIN_BEADS` drops more short sessions and gives
every remaining one more room.

## Interaction

The piece hangs on the left; a reading of one flower sits on the right.

- **Drag** across the garlands — they sway and rustle softly. Dragging moves the flowers,
  not the view.
- **There is no zoom and no pan.** The door holds still, the way a doorway does, and the
  whole of it stays in frame with a little air around it.
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
