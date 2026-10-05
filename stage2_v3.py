import re, json
from collections import Counter

with open('/tmp/full_labeled_v2.json') as f:
    records = json.load(f)

n = len(records)

# ---------------- 1. Refined Phase: UI / Setup / Bugs / UX (reduce catch-all) ----------------
BUGS_PAT = r'\b(fix|broken|doesn\'?t work|not working|issue|bug\b|crash|messed up|chaotic|wrong\b|error|glitch|missing|not reflecting|cannot see|can\'?t see|why is|why are|why isn\'?t|not showing|not intuitive|confusing)\b'
SETUP_PAT = r'\b(git pull|git push|git fetch|git commit|brew install|xcode-select|zprofile|zshrc|npm install|pod install|status ?line|/model|/clear|/compact|/background|/plugins|/reload-plugins|/remote-control|/mcp|api key|homebrew|android emmulator|android emulator|install\b|checkout|switch to|branch|push to (main|github)|^push\b|^pull\b|\bpush\b.{0,10}\bcommit\b|commit or discard|restart claude|run (dev|the) ?server|simulator\b|emulator\b|preview\b|revert\b|descope|artifact/|claude\.ai)\b'
UX_PAT = r'\b(figma|figjam|jira|atlassian|browse/[a-z]+-\d|wireframe|catalogues?|happy path|error flow|ux flow|flows?\b|journey|\bia\b|information architecture|screens? (designed|pending|needed)|onboarding|walkthroughs?|design links?|what should i build|descoped?|declined|configured setting)\b'
UI_PAT = r'\b(buttons?|borders?|radius|padding|gaps?|colou?rs?|shades?|icons?|align(ed)?|center(ed)?|shadows?|fonts?|spacing|screens?|tiles?|sections?|links?|bottom sheets?|action sheets?|input (box|field)s?|placeholders?|keyboards?|toasts?|drop shadow|bg\b|background|badges?|chips?|tags?|folders?|drawers?|blur|frost|grid|animations?|sizing|size\b|corners?|threads?|avatars?|profiles?|swipe|gesture|notifications?|filters?|search|calendar|attachments?|labels?|copy\b|wording|rename|call it|chevron|close\b|week view|prominent|heighted|height|queuing|sharing|contacts?|busy|separators?|lines?|shelf|shelves|fades?|dots?|tabs?|boxes?|circles?|visibility|unread|archive|left align|account screen|weekday|canvas|pages?)\b'

def classify_phase4_primary(text):
    low = text.lower()
    if re.search(BUGS_PAT, low):
        return 'Bugs'
    if re.search(SETUP_PAT, low):
        return 'Setup'
    if re.search(UX_PAT, low):
        return 'UX'
    if re.search(UI_PAT, low):
        return 'UI'
    return None

def classify_phase4(text):
    return classify_phase4_primary(text) or 'Other'

with open('/Users/Aeish/Prompt Bead Curtain/private/labeled_prompts_full.json') as f:
    full_records = json.load(f)  # has text

text_by_key = {(r['session_date'], r['order_in_session']): r['text'] for r in full_records}

for r in records:
    text = text_by_key[(r['session_date'], r['order_in_session'])]
    r['phase4_primary'] = classify_phase4_primary(text)

# fold leftover "Other" into closest fit: nearest same-session neighbor (prev, then next)
# that had a primary (keyword-based) match; final fallback = UI, the dominant activity.
by_session = {}
for idx, r in enumerate(records):
    by_session.setdefault(r['session_id'], []).append(idx)

for sid, idxs in by_session.items():
    for pos, idx in enumerate(idxs):
        r = records[idx]
        if r['phase4_primary'] is not None:
            r['phase4'] = r['phase4_primary']
            continue
        folded = None
        for back in range(pos - 1, -1, -1):
            cand = records[idxs[back]]['phase4_primary']
            if cand is not None:
                folded = cand
                break
        if folded is None:
            for fwd in range(pos + 1, len(idxs)):
                cand = records[idxs[fwd]]['phase4_primary']
                if cand is not None:
                    folded = cand
                    break
        r['phase4'] = folded or 'UI'

for r in records:
    del r['phase4_primary']

c = Counter(r['phase4'] for r in records)
print("--- phase4 (UI/Setup/Bugs/UX, Other folded into closest fit) ---")
for k, v in c.most_common():
    print(f"  {k}: {v} ({v/n*100:.1f}%)")

# ---------------- 2. Prompt quality lenses ----------------
with open('/usr/share/dict/words') as f:
    DICT_WORDS = set(w.strip().lower() for w in f)

KNOWN_JARGON = {
    'ui','ux','ia','figma','figjam','jira','sso','2fa','app','css','api','json','html',
    'ios','android','xcode','mcp','github','git','npm','sdk','px','rgb','svg','bg','id',
    'url','pdf','jpg','png','otp','sms','url','vs','ok','iphone','ipad','jsx','tsx',
    'cta','faq','url','wifi','bluetooth','appstore'
}

def typo_ratio(text):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    words = [w.strip("'") for w in words if len(w) > 2]
    if not words:
        return 0.0
    bad = 0
    for w in words:
        if w in KNOWN_JARGON or w in DICT_WORDS:
            continue
        # strip trailing s for plurals quickly
        if w.endswith('s') and w[:-1] in DICT_WORDS:
            continue
        bad += 1
    return bad / len(words)

VAGUE_PATTERNS = [
    r'\bthis\b', r'\bthat\b', r'\bsomething\b', r'\bweird\b', r'\boff\b', r'\bkind of\b',
    r'\ba bit\b', r'\bsomehow\b', r'\bstuff\b', r'\bthing\b', r'\betc\b', r'\bwhatever\b',
    r'\bmessed up\b'
]
SPECIFIC_MARKERS = [
    r'\d', r'\bpx\b', r'"[^"]+"', r"'[^']+'", r'\bsame as\b', r'\blike the\b', r'\bsimilar to\b',
]
def classify_specificity(text):
    low = text.lower()
    specific_hits = sum(1 for p in SPECIFIC_MARKERS if re.search(p, low))
    vague_hits = sum(1 for p in VAGUE_PATTERNS if re.search(p, low))
    if specific_hits >= 1 and vague_hits == 0:
        return 'specific'
    if vague_hits >= 1 and specific_hits == 0:
        return 'vague'
    if specific_hits >= 1 and vague_hits >= 1:
        return 'mixed'
    return 'plain'

def classify_groundedness(text):
    has_visual = bool(re.search(r'\[(image|pasted text)', text.lower()))
    has_comparative = bool(re.search(r'\b(same as|like the|similar to|as we have|as (i|we) did)\b', text.lower()))
    if has_visual:
        return 'visual_reference'
    if has_comparative:
        return 'comparative_reference'
    return 'unanchored'

def classify_bundling(text):
    # count distinct asks: split on strong conjunctions / newlines / "also" / "and then"
    low = text.lower()
    parts = re.split(r'\balso\b|\band then\b|\.\s+|\n\s*\n|;', low)
    parts = [p.strip() for p in parts if len(p.strip()) > 3]
    if len(parts) <= 1:
        return 'single_ask'
    if len(parts) <= 3:
        return 'few_asks'
    return 'many_asks'

for r in records:
    text = text_by_key[(r['session_date'], r['order_in_session'])]
    tr = typo_ratio(text)
    r['typo_ratio'] = round(tr, 3)
    r['clarity'] = 'clean' if tr < 0.05 else ('minor_typos' if tr < 0.15 else 'heavy_typos')
    r['specificity'] = classify_specificity(text)
    r['groundedness'] = classify_groundedness(text)
    r['bundling'] = classify_bundling(text)

for lens in ['clarity', 'specificity', 'groundedness', 'bundling']:
    c = Counter(r[lens] for r in records)
    print(f"\n--- {lens} ---")
    for k, v in c.most_common():
        print(f"  {k}: {v} ({v/n*100:.1f}%)")

with open('/tmp/full_labeled_v3.json', 'w') as f:
    json.dump(records, f, indent=1)
print("\nSaved /tmp/full_labeled_v3.json")
