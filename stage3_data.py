import json
from datetime import datetime

with open('/tmp/full_labeled_v3.json') as f:
    records = json.load(f)

PHASE = ['UI', 'Setup', 'Bugs', 'UX']
CLARITY = ['clean', 'minor_typos', 'heavy_typos']
SPEC = ['specific', 'plain', 'mixed', 'vague']
GROUND = ['unanchored', 'visual_reference', 'comparative_reference']
BUNDLE = ['single_ask', 'few_asks', 'many_asks']
HOUR = ['morning', 'afternoon', 'evening', 'late_night']

def hour_bucket(h):
    if 6 <= h < 12: return 0
    if 12 <= h < 17: return 1
    if 17 <= h < 22: return 2
    return 3

# ---- lean public JSON (separate artifact, labels/numbers/timestamps only) ----
public = []
for i, r in enumerate(records):
    dt = datetime.fromisoformat(r['timestamp'])
    public.append({
        'bead_id': i,
        'session_id': r['session_id'],
        'session_date': r['session_date'],
        'order_in_session': r['order_in_session'],
        'session_length': r['session_length'],
        'timestamp': r['timestamp'],
        'word_count': r['word_count'],
        'phase': r['phase4'],
        'decision_fatigue_position': r['decision_fatigue_position'],
        'clarity': r['clarity'],
        'specificity': r['specificity'],
        'groundedness': r['groundedness'],
        'bundling': r['bundling'],
        'hour_of_day': HOUR[hour_bucket(dt.hour)],
        'flow_gap_seconds': r['flow_gap_seconds'],
    })

with open('/Users/Aeish/Prompt Bead Curtain/public/data/beads.json', 'w') as f:
    json.dump(public, f, indent=1)

# ---- compact inline payload for the single-file HTML ----
sessions = {}
for r in records:
    sessions.setdefault(r['session_id'], r['session_date'])
SESSIONS = [sessions[k] for k in sorted(sessions)]

rows = []
for r in records:
    dt = datetime.fromisoformat(r['timestamp'])
    gap = r['flow_gap_seconds']
    rows.append([
        r['session_id'],
        r['order_in_session'],
        r['session_length'],
        r['timestamp'][5:16],
        r['word_count'],
        PHASE.index(r['phase4']),
        CLARITY.index(r['clarity']),
        SPEC.index(r['specificity']),
        GROUND.index(r['groundedness']),
        BUNDLE.index(r['bundling']),
        hour_bucket(dt.hour),
        -1 if gap is None else gap,
    ])

legend = {
    'phase': PHASE,
    'clarity': ['clean', 'minor typos', 'heavy typos'],
    'specificity': SPEC,
    'groundedness': ['unanchored', 'image ref', 'comparison ref'],
    'bundling': ['single ask', 'few asks', 'many asks'],
    'hour': ['morning', 'afternoon', 'evening', 'late night'],
    'fatigue': ['early', 'middle', 'late'],
}

out = []
out.append('const SESSIONS=' + json.dumps(SESSIONS, separators=(',', ':')) + ';')
out.append('const LEGEND=' + json.dumps(legend, separators=(',', ':')) + ';')
out.append('const ROWS=' + json.dumps(rows, separators=(',', ':')) + ';')

with open('/tmp/data_inline.js', 'w') as f:
    f.write('\n'.join(out))

import os
print('public beads.json records:', len(public))
print('inline payload KB:', round(os.path.getsize('/tmp/data_inline.js')/1024, 1))
print('sessions:', len(SESSIONS))
