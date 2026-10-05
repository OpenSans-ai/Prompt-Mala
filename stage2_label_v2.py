import re, json
from datetime import datetime

path = "/Users/Aeish/Downloads/Synacor-prompts.md"
with open(path, encoding="utf-8") as f:
    lines = f.readlines()

header_re = re.compile(r'^## (.+)$')
bullet_re = re.compile(r'^- \*\*(\d{2}:\d{2})\*\*\s?(.*)$')

sessions = []
cur_session = None
cur_prompt = None
for line in lines:
    line = line.rstrip('\n')
    h = header_re.match(line)
    if h:
        if cur_session:
            if cur_prompt:
                cur_session['prompts'].append(cur_prompt)
                cur_prompt = None
            sessions.append(cur_session)
        cur_session = {'date': h.group(1), 'prompts': []}
        continue
    b = bullet_re.match(line)
    if b:
        if cur_prompt:
            cur_session['prompts'].append(cur_prompt)
        cur_prompt = {'time': b.group(1), 'text': b.group(2)}
        continue
    if cur_prompt is not None:
        cur_prompt['text'] += '\n' + line
if cur_prompt:
    cur_session['prompts'].append(cur_prompt)
if cur_session:
    sessions.append(cur_session)

ack_vocab = {
    'yes','y','no','n','ok','okay','sure','fine','done','continue','go','go ahead',
    'stop','wait','thanks','thank you','great','perfect','nope','yeah','yep','yup',
    'good','alright','got it','noted','sounds good','fine then','k','kk','cool',
    'nice','correct','right','exactly','proceed','do it','go for it','same','agreed',
    'yes please','no thanks','not yet','not now','later','skip','next','fix it',
    'try again','retry','go back','keep that','keep going','looks good','lgtm'
}

def norm(text):
    t = text.strip().lower()
    t = re.sub(r'[!?.,]+$', '', t)
    t = re.sub(r'\s+', ' ', t)
    return t

def classify_bucket(text, wc):
    n = norm(text)
    is_slash = text.startswith('/') or text.startswith('!')
    has_block = '\n' in text and len(text.split('\n')) > 2
    is_pasted = wc > 60 or has_block or ('http' in text and wc > 20)
    is_tiny = (n in ack_vocab) or (wc <= 2 and not is_slash and not any(c.isdigit() for c in text) and len(text) < 20)
    if is_slash:
        return 'slash'
    if is_pasted:
        return 'pasted'
    if is_tiny:
        return 'tiny'
    return 'real'

for s in sessions:
    for p in s['prompts']:
        p['wordcount'] = len(p['text'].split())
        p['bucket'] = classify_bucket(p['text'], p['wordcount'])
        d = s['date'].split(' ', 1)[1]
        dt = datetime.strptime(d + ' ' + p['time'], '%d %b %Y %H:%M')
        p['dt'] = dt

filtered_sessions = []
for s in sessions:
    real_prompts = [p for p in s['prompts'] if p['bucket'] == 'real']
    if real_prompts:
        filtered_sessions.append({'date': s['date'], 'prompts': real_prompts})

total_real = sum(len(s['prompts']) for s in filtered_sessions)
print(f"Sessions kept: {len(filtered_sessions)}, total real prompts: {total_real}")

STOPWORDS = set("""a an the this that these those is are was were be been being to of in on
for with and or but if then so as at by from it its i you he she we they my our your their
his her do does did can could should would will shall not no yes please just also very really
have has had get gets got going go need want like make made look looks looking show
""".split())

def wordset(text):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return set(w for w in words if w not in STOPWORDS and len(w) > 2)

def jaccard(a, b):
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0

# ---- Role ----
TEACHER_PATTERNS = [
    r'\bwhat is\b', r"\bwhat's the\b", r'\bwhy\b', r'\bhow does\b', r'\bhow do\b',
    r'\bexplain\b', r'\bwhat are\b', r'\bdifference between\b', r"\btell me (what|how|why)\b",
    r'\bwhat all\b', r'\bhow come\b', r'\bunderstand\b', r'\bwhat widget\b',
]
MIRROR_PATTERNS = [
    r'\bi think\b', r'\bi feel\b', r"\bi'?m confused\b", r'\bi am confused\b', r'\bfeels\b',
    r'\blooks (messed up|weird|off|wrong|chaotic)\b', r'\bis this (even )?valid\b',
    r'\bdoes this make sense\b', r'\bwhat do you think\b', r'\bi wonder\b', r'\bright\?'
]
COMPANION_PATTERNS = [
    r'^\s*(hey|hi|hello)\b', r'\bjust (talking|chatting|curious)\b', r'\bhaha\b', r'\blol\b'
]
HANDS_VERBS = r'\b(add|remove|fix|make|create|build|change|move|align|increase|decrease|push|pull|run|install|set up|setup|implement|update|delete|show|load|switch|open|close|keep|drop|replace|use|follow|cover|include|generate|write|commit|discard|restart|reduce)\b'

def classify_role(text):
    low = text.lower()
    for pat in COMPANION_PATTERNS:
        if re.search(pat, low):
            return 'Companion'
    for pat in MIRROR_PATTERNS:
        if re.search(pat, low):
            return 'Mirror'
    for pat in TEACHER_PATTERNS:
        if re.search(pat, low):
            return 'Teacher'
    if re.search(HANDS_VERBS, low) or low.strip().startswith(('please', 'can you', 'could you')):
        return 'Hands'
    if low.rstrip().endswith('?'):
        return 'Teacher'
    return 'Hands'

def classify_politeness(text):
    low = text.lower()
    return bool(re.search(r'\b(please|thanks|thank you|sorry|appreciate)\b', low))

PROJECT_NOUNS = r'(app|project|code|screen|flow|feature|design|build|repo|branch|ui|component|button|file|work)'
def classify_ownership(text):
    low = text.lower()
    my_match = re.search(r'\b(my|our)\s+\w*\s*' + PROJECT_NOUNS, low)
    the_match = re.search(r'\bthe\s+\w*\s*' + PROJECT_NOUNS, low)
    my_pos = my_match.start() if my_match else None
    the_pos = the_match.start() if the_match else None
    if my_pos is not None and (the_pos is None or my_pos <= the_pos):
        return 'mine'
    if the_pos is not None:
        return 'the'
    return 'neither'

WONDER_PATTERNS = [
    r'\bmaybe\b', r'\bperhaps\b', r'\bi think\b', r'\bnot sure\b', r'\bwonder\b',
    r'\bwhat if\b', r'\bcould (we|it|this|you)\b', r'\bshould (we|i|it)\b',
    r'\bdo you think\b', r'\bis (it|this) (ok|okay|fine|right)\?', r'\bright\?'
]
def classify_certainty(text):
    low = text.lower()
    for pat in WONDER_PATTERNS:
        if re.search(pat, low):
            return 'wondering'
    if low.rstrip().endswith('?') and re.match(r'^\s*(is|are|can|could|should|would|do|does|did|what|why|how)\b', low):
        return 'wondering'
    return 'command'

META_PATTERNS = [
    r'\bwait\b', r'\bactually\b', r"\blet'?s (rethink|step back|reconsider)\b",
    r"\bthis isn'?t (right|working)\b", r'\breconsider\b', r'\bscrap that\b',
    r'\bstart over\b', r'\bdifferent approach\b',
    r'\bon second thought\b', r'\bi need to (think|clarify)\b',
    r"\bi'?m confused\b", r'\bi am confused\b'
]
def classify_metacognition(text):
    low = text.lower()
    return any(re.search(pat, low) for pat in META_PATTERNS)

# ---- Phase: independent keyword classification, NO carry-forward cascade ----
PHASE_DICTS = [
    ('setup_env', r'\b(git pull|git push|git fetch|git commit|brew install|xcode-select|zprofile|zshrc|npm install|pod install|status ?line|/model|/clear|/compact|/background|/plugins|/reload-plugins|/remote-control|api key|homebrew|android emmulator|android emulator|install.{0,15}(android|xcode|emulator|simulator app)|push to (main|github)|checkout|switch to.{0,15}branch|commit or discard)\b'),
    ('figma_ux_flow', r'\b(figma|figjam|jira|wireframe|catalogue?|happy path|error flow|ux flow|upside down flow)\b'),
    ('auth', r'\b(auth|login|signup|sign up|password|2fa|biometric|sso|authenticat)\b'),
    ('bug_fix', r'\b(fix|broken|doesn\'?t work|not working|issue|bug\b|crash|messed up|chaotic|wrong\b)\b'),
    ('preview_test', r'\b(load the preview|run (dev|the) ?server|run simulator|open simulator)\b'),
    ('content_copy', r'\b(copy|wording|label text|string says|rename|call it)\b'),
    ('ui_visual_design', r'\b(button|border|radius|padding|gap|colou?r|shade|icon|align|center|shadow|font|spacing|screen|bottom sheet|input (box|field)|placeholder|keyboard|toast|drop shadow|bg\b|background|badge|chip|tag|folder|drawer|blur|frost|grid|walkthrough|onboarding|animation|size|corner|thread|avatar|profile|swipe|gesture|notification|filter|search|calendar|attachment)\b'),
]
def classify_phase(text):
    low = text.lower()
    for name, pat in PHASE_DICTS:
        if re.search(pat, low):
            return name
    return 'general_task'

FRUSTRATED_PATTERNS = [
    r'\bstill (not|cannot|can\'?t)\b', r'\bnot working\b', r'\bwrong\b', r'\bmessed up\b',
    r'\bchaotic\b', r'\bconfus(ed|ing)\b', r'\bugh\b',
    r'\bwhy is\b', r'\bagain\?', r"\bi odnt want\b", r'\bdont want\b',
    r'\bnot looking good\b', r'\bmissing\b'
]
PLEASED_PATTERNS = [
    r'\bperfect\b', r'\bgreat\b', r'\blove (it|this)\b', r'\bnice\b', r'\bexactly\b',
    r'\bbeautiful\b', r'\bgood job\b', r'\blooks good\b', r'\bthanks\b', r'\byes go ahead\b'
]
def classify_affect(text):
    low = text.lower()
    frustrated = any(re.search(p, low) for p in FRUSTRATED_PATTERNS)
    pleased = any(re.search(p, low) for p in PLEASED_PATTERNS)
    if frustrated and not pleased:
        return 'frustrated'
    if pleased and not frustrated:
        return 'pleased'
    return 'neutral'

REJECTION_PATTERNS = [
    r'^\s*no+\b', r'\bnot this\b', r'\btry again\b', r'\bgo back\b', r'\bundo\b',
    r'\brevert\b', r'\bscrap\b', r"\bthat'?s not right\b", r'\bwrong\b', r'\bnooo+\b',
    r'\bremove (that|this)\b', r'\bstill (not|wrong)\b', r'\bdont want\b', r"\bi odnt want\b"
]
ACCEPTANCE_PATTERNS = [
    r'\bperfect\b', r'\bkeep (that|this|it)\b', r'\bgreat\b', r'\bexactly\b',
    r'\blooks good\b', r'\blgtm\b', r'\bgood job\b', r'\bnice\b', r'\byes go ahead\b',
    r'\blove (it|this)\b', r'\bthat\'?s it\b'
]
def classify_deciding(text):
    low = text.lower()
    rej = any(re.search(p, low) for p in REJECTION_PATTERNS)
    acc = any(re.search(p, low) for p in ACCEPTANCE_PATTERNS)
    if rej and not acc:
        return 'rejection'
    if acc and not rej:
        return 'acceptance'
    return 'neither'

# ---- Feature extraction for anchoring (finer than phase) ----
FEATURE_NOUNS = [
    'bottom sheet', 'input box', 'input field', 'keyboard', 'toast', 'border', 'shadow',
    'radius', 'padding', 'gap', 'colour', 'color', 'icon', 'chip', 'tag', 'folder', 'drawer',
    'thread', 'badge', 'filter', 'search', 'animation', 'notification', 'sync', 'login',
    'signup', 'token', 'biometric', '2fa', 'sso', 'preview', 'simulator', 'figma', 'figjam',
    'jira', 'button', 'screen', 'flow', 'blur', 'frost', 'grid', 'font', 'placeholder',
    'walkthrough', 'onboarding', 'calendar', 'attachment', 'label', 'swipe', 'gesture',
    'avatar', 'profile', 'branch', 'git', 'emulator'
]
def extract_feature(text, phase):
    low = text.lower()
    for noun in FEATURE_NOUNS:
        if noun in low:
            return noun
    return 'misc:' + phase

records = []
session_idx_counter = 0
for s in filtered_sessions:
    session_id = session_idx_counter
    session_idx_counter += 1
    n = len(s['prompts'])
    prev_dt = None
    rejection_streak = 0
    for i, p in enumerate(s['prompts']):
        text = p['text']
        wc = p['wordcount']
        dt = p['dt']

        frac = i / max(n - 1, 1)
        position = 'early' if frac < 1/3 else ('middle' if frac < 2/3 else 'late')

        gap_seconds = None if prev_dt is None else int((dt - prev_dt).total_seconds())
        prev_dt = dt

        hour = dt.hour
        daynight = 'day' if 6 <= hour < 19 else 'night'

        role = classify_role(text)
        polite = classify_politeness(text)
        ownership = classify_ownership(text)
        certainty = classify_certainty(text)
        meta = classify_metacognition(text)
        phase = classify_phase(text)
        feature = extract_feature(text, phase)
        affect = classify_affect(text)
        deciding = classify_deciding(text)

        if deciding == 'rejection':
            rejection_streak += 1
            rej_before_accept = None
        elif deciding == 'acceptance':
            rej_before_accept = rejection_streak
            rejection_streak = 0
        else:
            rej_before_accept = None

        rec = {
            'session_id': session_id,
            'session_date': s['date'],
            'order_in_session': i,
            'session_length': n,
            'timestamp': dt.isoformat(),
            'word_count': wc,
            'text': text,
            'role': role,
            'politeness': polite,
            'ownership': ownership,
            'certainty': certainty,
            'metacognition': meta,
            'phase': phase,
            'feature': feature,
            'deciding': deciding,
            'rejections_before_acceptance': rej_before_accept,
            'decision_fatigue_position': position,
            'affect': affect,
            'flow_gap_seconds': gap_seconds,
            'day_night': daynight,
        }
        records.append(rec)

# ---- Anchoring: per FEATURE (finer grain), similarity to first chronological occurrence ----
feature_first_wordset = {}
for rec in records:
    feat = rec['feature']
    ws = wordset(rec['text'])
    if feat not in feature_first_wordset:
        feature_first_wordset[feat] = ws
        rec['anchoring'] = 'close'
    else:
        sim = jaccard(ws, feature_first_wordset[feat])
        if sim >= 0.15:
            rec['anchoring'] = 'close'
        elif sim >= 0.05:
            rec['anchoring'] = 'moved'
        else:
            rec['anchoring'] = 'far'

with open('/tmp/full_labeled_v2.json', 'w') as f:
    json.dump(records, f, indent=1, default=str)

print(f"Total labeled records: {len(records)}")
print("Saved to /tmp/full_labeled_v2.json")

n_feat = len(set(r['feature'] for r in records))
print(f"Distinct features for anchoring: {n_feat}")
