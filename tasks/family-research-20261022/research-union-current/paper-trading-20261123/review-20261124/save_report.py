"""Save one finished subagent's report, word for word, into the markets-data review folder, and print its token figures."""
import json, sys, os
S = '/root/.claude/projects/-home-user/f6fc58bd-1d38-5c78-9832-91292fa09200/subagents/'
D = '/home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/review-20261124'
KINDS = ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens')
size = lambda u: sum(u.get(k) or 0 for k in KINDS)
run, agent, name, what = sys.argv[1:5]
best = kind = model = None
calls = {}
for line in open(S + f'agent-{agent}.jsonl'):
    try: d = json.loads(line)
    except ValueError: continue
    m = d.get('message')
    if not isinstance(m, dict): continue
    if m.get('id') and isinstance(m.get('usage'), dict):
        u = m['usage']; model = m.get('model')
        steps = [s for s in u.get('iterations') or [] if isinstance(s, dict)] or [u]
        own = [s for s in steps if s.get('type', 'message') == 'message'] or steps
        calls[m['id']] = (size(own[-1]), sum(size(s) for s in steps), sum(size(s) for s in steps if s.get('type') == 'advisor_message'))
    if m.get('role') != 'assistant': continue
    for b in m.get('content') or []:
        if isinstance(b, dict) and b.get('type') == 'tool_use' and 'andback' in (b.get('name') or ''):
            txt = max((v for v in (b.get('input') or {}).values() if isinstance(v, str)), key=len, default=None)
            if txt: best, kind = txt, 'handback'
        elif isinstance(b, dict) and b.get('type') == 'text' and kind != 'handback' and b.get('text', '').strip():
            best, kind = b['text'], 'text'
assert best, 'no report text'
head = (f"# Run {run}: {what}\n\nThe agent's own report, word for word, as it came back to the session "
        f"(session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. "
        f"What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.\n\n---\n\n")
open(os.path.join(D, f'run{run}-{name}.md'), 'w', encoding='utf8').write(head + best.rstrip('\n') + '\n')
v = list(calls.values())
print(json.dumps(dict(run=int(run), model=model, model_calls=len(v), last_call_tokens=v[-1][0] if v else 0,
                      all_calls_tokens=sum(t for _, t, _ in v), advisor_tokens=sum(a for _, _, a in v), report_chars=len(best), kind=kind)))
