// Loads beads.json and turns it into a hangable curtain: strands of beads with
// rest lengths, radii, colours and finishes already resolved.

import { CFG, PALETTE, FINISH } from './config.js';

const WC_MIN = 1, WC_MAX = 60;
const GAP_REF = 46020; // the longest pause in the data, in seconds

export async function loadBeads(url = 'data/beads.json') {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Could not load ${url} (${res.status})`);
  return res.json();
}

function radiusFor(wordCount) {
  const wc = Math.min(Math.max(wordCount ?? 1, WC_MIN), WC_MAX);
  const t = (Math.sqrt(wc) - Math.sqrt(WC_MIN)) / (Math.sqrt(WC_MAX) - Math.sqrt(WC_MIN));
  return CFG.beadRMin + (CFG.beadRMax - CFG.beadRMin) * t;
}

// A pause between prompts becomes exposed cord. Log scale, because the gaps
// span 60 seconds to 13 hours.
function slackFor(gapSeconds) {
  if (gapSeconds == null || gapSeconds <= 0) return 0;
  const t = Math.log1p(gapSeconds / 45) / Math.log1p(GAP_REF / 45);
  return CFG.gapMax * Math.min(t, 1);
}

function accentFor(row) {
  if (row.affect === 'frustrated') return 'ember';
  if (row.affect === 'pleased') return 'gold';
  return null;
}

// deciding -> a metal spacer threaded next to the bead.
function ringFor(row) {
  if (row.deciding === 'acceptance') return 'brass';
  if (row.deciding === 'rejection') return 'iron';
  return null;
}

export function buildScene(rows) {
  const bySession = new Map();
  for (const row of rows) {
    if (!bySession.has(row.session_id)) bySession.set(row.session_id, []);
    bySession.get(row.session_id).push(row);
  }

  // Strands run left to right in chronological order.
  const sessions = [...bySession.values()].map((list) => {
    list.sort((a, b) => a.order_in_session - b.order_in_session);
    return list;
  });
  sessions.sort((a, b) => new Date(a[0].timestamp) - new Date(b[0].timestamp));

  const strands = [];
  const beads = [];
  let worldH = 0;

  sessions.forEach((rowsIn, si) => {
    const anchorX = si * CFG.strandPitch;
    // A small out-of-plane offset per strand keeps the curtain from looking
    // like a flat grid: strands sit at slightly different depths.
    const depth = Math.sin(si * 2.399) * 0.5 + Math.sin(si * 0.731) * 0.5;

    const strand = {
      index: si,
      sessionId: rowsIn[0].session_id,
      date: rowsIn[0].session_date,
      length: rowsIn.length,
      night: rowsIn[0].day_night === 'night',
      anchorX,
      depth,                          // -1 .. 1
      scale: 1 + depth * 0.035,       // nearer strands read very slightly larger
      phase: (si % 7) * 0.897,        // wind phase, so the breeze travels sideways
      releaseAt: si * CFG.releaseStagger,
      beads: [],
      rest: [],                       // rest[i] = distance from particle i-1 to i
    };

    let y = CFG.rodY + CFG.headSlack;
    let prevR = 0;

    rowsIn.forEach((row, i) => {
      const r = radiusFor(row.word_count) * strand.scale;
      const slack = slackFor(row.flow_gap_seconds);
      const rest = i === 0 ? CFG.headSlack + r : prevR + r + CFG.gapTouch + slack;
      y = i === 0 ? CFG.rodY + rest : y + rest;

      const bead = {
        id: row.bead_id,
        row,
        strand,
        i,
        r,
        rest,
        slack,
        palette: PALETTE[row.phase4] ?? PALETTE.UI,
        phase4: row.phase4,
        finish: FINISH[row.clarity] ?? FINISH.clean,
        accent: accentFor(row),
        ring: ringFor(row),
        halo: row.metacognition === true,
        restY: y,
        // filled each frame by the physics + renderer
        x: anchorX, y: CFG.rodY, sx: 0, sy: 0, sr: 0, visible: false, dim: false,
      };

      strand.beads.push(bead);
      strand.rest.push(rest);
      beads.push(bead);
      prevR = r;
    });

    strand.restBottom = y + prevR + CFG.tailLength;
    worldH = Math.max(worldH, strand.restBottom);
    strands.push(strand);
  });

  const worldW = (strands.length - 1) * CFG.strandPitch;

  return { strands, beads, worldW, worldH, stats: summarise(rows, strands) };
}

function summarise(rows, strands) {
  const count = (key) => {
    const m = new Map();
    for (const r of rows) m.set(r[key], (m.get(r[key]) ?? 0) + 1);
    return m;
  };

  const dates = rows
    .map((r) => new Date(r.timestamp))
    .sort((a, b) => a - b);
  const fmt = (d) => d.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' });

  const longestPause = rows.reduce(
    (best, r) => ((r.flow_gap_seconds ?? -1) > (best.flow_gap_seconds ?? -1) ? r : best),
    rows[0],
  );
  const longestSession = strands.reduce((best, s) => (s.length > best.length ? s : best), strands[0]);

  return {
    prompts: rows.length,
    sessions: strands.length,
    from: fmt(dates[0]),
    to: fmt(dates[dates.length - 1]),
    phase4: count('phase4'),
    role: count('role'),
    clarity: count('clarity'),
    features: [...count('feature').entries()].sort((a, b) => b[1] - a[1]),
    frustrated: rows.filter((r) => r.affect === 'frustrated').length,
    pleased: rows.filter((r) => r.affect === 'pleased').length,
    rejections: rows.filter((r) => r.deciding === 'rejection').length,
    metacognition: rows.filter((r) => r.metacognition).length,
    night: rows.filter((r) => r.day_night === 'night').length,
    longestPause: longestPause.flow_gap_seconds,
    longestSession: { length: longestSession.length, date: longestSession.date },
    medianWords: median(rows.map((r) => r.word_count)),
  };
}

function median(xs) {
  const s = [...xs].sort((a, b) => a - b);
  const m = s.length >> 1;
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}
