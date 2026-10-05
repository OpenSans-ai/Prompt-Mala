// Tunables and the data -> visual encoding tables.
// Every "magic number" in the app should live here so the look can be dialled
// in without hunting through the renderer.

export const CFG = {
  // --- layout, in world units (1 world unit ~ 1px at zoom 1) ---
  strandPitch: 26,      // horizontal distance between strands
  beadRMin: 3.6,        // radius of a 1-word prompt
  beadRMax: 9.8,        // radius of a 60-word prompt
  gapTouch: 1.4,        // cord visible between two beads that rest on each other
  gapMax: 30,           // extra cord added for the single longest pause
  rodY: 0,              // world y of the hanging rod
  headSlack: 9,         // cord between the rod and the first bead
  tailLength: 30,       // cord hanging below the last bead, before the knot

  // --- verlet physics ---
  gravity: 9200,
  damp: 0.988,
  iters: 3,             // constraint relaxation passes per substep
  substeps: 2,
  maxStep: 1 / 45,      // clamp dt so tab-switches don't explode the sim

  // --- air ---
  windBase: 430,        // ambient breeze acceleration
  windGust: 1450,       // peak of a passing gust
  gustEvery: [6, 15],   // seconds between gusts (random in range)
  gustLength: 2.6,

  // --- the hand pushing through the curtain ---
  pointerRadius: 88,
  pointerForce: 17000,
  dragRadius: 155,
  dragForce: 46000,

  // --- reveal animation: strands cascade down from the rod ---
  releaseStagger: 0.016, // seconds between each strand being released

  // --- light ---
  lightX: -0.34,        // key light direction, in bead radii
  lightY: -0.42,
};

// phase4 -> glass colour. Four jewel tones: topaz, sapphire, garnet, jade.
// tint = where the light enters, base = body, deep = the shadowed edge,
// caustic = the bright pool of light that passes through and lands inside.
export const PALETTE = {
  Setup: { tint: '#ffe0a0', base: '#cf8a2a', deep: '#5e3406', caustic: '#ffbe5c' },
  UI:    { tint: '#b9d0ff', base: '#3a68cc', deep: '#122a63', caustic: '#76a8ff' },
  Bugs:  { tint: '#ffb8ae', base: '#bf3f39', deep: '#5c1310', caustic: '#ff7b63' },
  UX:    { tint: '#a8ecc9', base: '#2a9670', deep: '#0b4330', caustic: '#5fe0a6' },
};

export const PHASE4_ORDER = ['Setup', 'UI', 'Bugs', 'UX'];

// clarity -> surface finish. A clean prompt is polished glass; a typo-ridden
// one is unpolished stone. The data decides how the light behaves.
export const FINISH = {
  clean:        { key: 'glass', spec: 0.30, specR: 0.26, caustic: 0.85, contrast: 1.00, grain: 0 },
  minor_typos:  { key: 'satin', spec: 0.17, specR: 0.46, caustic: 0.52, contrast: 0.88, grain: 0.05 },
  heavy_typos:  { key: 'stone', spec: 0.07, specR: 0.80, caustic: 0.20, contrast: 0.72, grain: 0.16 },
};

// Secondary accents, applied on top of the body. All of these are rare in the
// data, so they read as events rather than noise.
export const ACCENT = {
  ember: { affect: 'frustrated', colour: '#ff5a2a' }, // heat inside the bead
  gold:  { affect: 'pleased',    colour: '#ffd36b' }, // warm sparkle
};

export const LABELS = {
  phase4: 'Phase',
  role: 'Role',
  feature: 'Feature',
  clarity: 'Clarity',
  specificity: 'Specificity',
  groundedness: 'Grounding',
  bundling: 'Bundling',
  affect: 'Affect',
  certainty: 'Certainty',
  ownership: 'Ownership',
  anchoring: 'Anchoring',
  deciding: 'Deciding',
  decision_fatigue_position: 'Session position',
  day_night: 'Time of day',
};
