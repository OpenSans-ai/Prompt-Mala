# Prompt माला

An interactive piece where every flower is one prompt, hung as painted garlands in a
carved doorway. 2,297 prompts across 57 sessions, 10 Jun 2026 – 5 Oct 2026.

The labelled data holds 2,404 prompts across 78 sessions. Sessions of fewer than ten
prompts are not drawn: 21 of them, 107 prompts, 4.5% of the total. They hung as stubs of
one to nine flowers and read as fraying rather than as sessions, and each still took a
full garland's width. `MIN_BEADS` in `index.html` is the threshold.

The doorway is a painting, `public/door.png`. Everything hanging in it — every flower, leaf
and thread — is drawn procedurally into a canvas each frame.

The masthead title is a painting too, `public/logo.webp`. It stands beside the copy rather
than over it, and the band is deliberately short: a lede, one sentence saying what a flower
and a garland are, and the archive's counts on one quiet line. Everything else about the
piece is in the artwork or in the panel.

**`index.html` is no longer self-contained.** It needs `public/door.png`,
`public/logo.webp` and `public/indian-ghungroo-shaker-low.wav` beside it. Opened
on its own the curtain still draws, but against bare paper with no doorway; the console
says so. This is a change from how the piece used to work, and it is the cost of using a
painted door rather than a drawn one.

## Files

| Path | Publish? | What it is |
|---|---|---|
| `index.html` | yes | The piece. Needs `public/` alongside it. |
| `public/door.png` | yes | The painted doorway, 919×1711. 2.2MB. |
| `public/indian-ghungroo-shaker-low.wav` | yes | The ghungru. 163KB, 0.92s. Loaded on first interaction. |
| `public/logo.webp` | yes | The masthead lockup, 640×389 on transparency. 38KB. |
| `public/icon-32.png`, `-180`, `-512` | yes | Favicon, apple-touch icon, and the large one. The P on paper. |
| `public/og.png` | yes | The social card, 1200×630. |
| `public/logo-source.webp` | yes | The lockup as painted, on its cream ground, 1536×1024. Source for the four above. |
| `logo_assets.py` | — | Derives those four from the source. |
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

There is no key beside the piece. There used to be: a strip of eight swatches, four species
and four degrees of openness, that a reader had to hold in their head and carry back to the
curtain. It now lives in the panel as **This Flower**, and reads the one flower under the
pointer — which species it is and what that says, how far open the head is and what that
says — painted at the real diameter of its tier so the size on the page is the size being
explained. A key that can be specific does not have to be general, and the artwork takes
the width the strip was using. The swatch still goes through the curtain's own sprite maker,
so it cannot drift from what is on screen.

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
- **Hover** a flower and the side panel reads it straight away — a score and a verdict,
  what the flower itself is saying, then the three dimensions behind it, what the prompt
  did well and what it left out. A small label follows the pointer too.
- **Click** to pin a flower, so the panel holds it when the pointer moves off. Previous/Next
  walk the whole run in order.
- **Pause motion** freezes the sway; selection keeps working.

Small brass **ghungrus** are strung between the flowers. They are decoration and carry no
data, so they live in their own list rather than in `beads` — which is the whole reason hit
testing never picks one up, with no special case needed.

Brushing the garlands rings them, using a recording: `public/indian-ghungroo-shaker-low.wav`.
It is a single shake — it peaks around 50ms, is down to 6% by 160ms and silent after about
400ms — and that envelope is why it can be fired per contact without the tails piling into
mush. Playback rate is varied per contact, because otherwise every contact is the identical
recording and the ear picks that up immediately as a loop.

An earlier version synthesised the sound instead. The first attempt was a struck bell —
sine partials with a long tail — which is a chime, a different instrument. The second got
much closer with resonant filtered noise, dry and bright, but a real shell has a rattle in
it that is hard to fake. The recording replaced both.

`ringGhungru` takes its audio context as an argument rather than reaching for the global
one, so the whole playback path can be rendered into an `OfflineAudioContext` and measured
instead of guessed at. Across the drag strengths the piece actually produces (up to 0.12)
it renders at peaks of 0.10 to 0.40 with no clipping.

Under 860px wide the panel stacks underneath and stays shut until you pick a flower, so
it does not eat half the piece while empty. The piece itself keeps a floor of 190px and the
panel scrolls, so a short window can never squeeze the canvas to nothing. The one line of
instruction under the piece is shown at every width now rather than desktop only — with the
key gone from beside the doorway it is the only thing that says the garlands can be
touched.

The reading opens with a **Prompt Score** out of 10 — a weighted roll-up of the four
labels the garland already draws from (specificity, clarity, grounding, bundling), so the
number and the flower can never disagree. It is a roll-up of heuristics rather than a
measurement, and the panel says as much underneath it. The three dimensions below are the
ones the data actually carries, each with its label printed beside the bar rather than a
bare percentage. Actionability was cut: computed from the same four labels, it read as a
fourth opinion while being a restatement of the other three.

Intent and style are one section. Split, they were two labels and a rule around a single
thought — what the prompt was for, and how it was put — and the reader had to carry the
first across the gap to make sense of the second.

Sections are separated by a hairline and nothing else. Boxing each one would turn a reading
into a dashboard: six panels of chrome around six short pieces of text, in a piece that is
otherwise editorial. One rule, one label, then the words.

Two things the panel could show are absent rather than filled in. Nothing in the data
records what the author *wanted* out of a prompt, and no model response was ever captured,
so the piece cannot say whether the ask landed. Both would have been easy to invent.

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

### The logo

`public/logo-source.webp` is the lockup as painted, on a cream ground a shade darker than
the site's paper. Dropped into the masthead as it is, that ground reads as a box around
the title, so `logo_assets.py` divides it back out: the lockup is ink on paper, so how far
a pixel falls below the paper colour is how much ink is there, and that becomes the alpha
channel. The result is trimmed to the artwork and written out as `logo.webp`, the three
icons and the social card.

    python3 logo_assets.py

It is the one script here that is not stdlib-only: it wants Pillow and NumPy. Nothing
else in the repo does, and the assets are checked in, so there is no need to run it
unless the artwork changes.

Composited over the ground it came from, the transparent version reproduces the source
exactly. It is not meant for dark backgrounds — the pale flowers in the lockup are pale
*ink*, and they go dark if you put them on ink.

`og:image` is a relative path, which most scrapers resolve against the page. Strict ones
want it absolute; set the deployed URL in both HTML files if the social card matters.

## Caveats

Labels come from keyword and pattern heuristics over the prompt text, not a per-prompt
semantic read — 2,404 prompts was too many to judge individually. They are directionally
right but will misfire on sarcasm, heavy typos, and terse phrasing. Clarity in particular
measures typo density against a dictionary, so unusual proper nouns can read as typos.
