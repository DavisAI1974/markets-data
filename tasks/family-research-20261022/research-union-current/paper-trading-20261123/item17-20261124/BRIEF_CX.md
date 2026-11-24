# Your rules: Codex's fifteen, CX01 to CX15

First read [common brief](BRIEF_COMMON.md) in full. It says what the job is, what each choice does in the matcher, the
rules you hold yourself to and the answer format. Then:

- The fifteen rule files: [rules/CX01.json](https://github.com/DavisAI1974/paper-trading-platform/blob/2986b3ce3001bc1926df64a06588b4558a5b648e/paper_platform/rules/CX01.json) to `CX15.json`. Nine are entry
  rules. Six are managers: CX05, CX11, CX13 (direction buy) and CX06, CX12, CX14 (direction sell).
- The author's strategy document, which the rule files were cut from. Quote from these two files (they have
  real lines): [codex-strategy/VERSIONS.md](codex-strategy/VERSIONS.md) (171 lines; its opening section "How to read and run v2" applies
  to all fifteen) and [codex-strategy/OPEN_QUESTIONS.md](codex-strategy/OPEN_QUESTIONS.md).
- How the platform runs them: [rulebook.py](https://github.com/DavisAI1974/paper-trading-platform/blob/2986b3ce3001bc1926df64a06588b4558a5b648e/paper_platform/rulebook.py) and `engine.py`.

For the six managers you also decide `entry_rules` and `on_parent_close`. The entry rules a manager could
follow are the 24 entry rules of the catalogue: Claude's CL01 to CL15 (side set at the trigger, so either side)
and Codex's CX01, CX03, CX07, CX10 (buy), CX02, CX04, CX08, CX09 (sell) and CX15 (either side). The matcher
passes a manager only the opens on the manager's own side. Whether a CX manager follows Claude's CL rules, the
CX rules only, or a shorter list is part of your decision; the checklist's item 2 says the 30 strategies run
"each on its own, never mixed", and points 11 to 15 of the common brief say what the code does. Say which words
you rest on.

Decide CX01 to CX15, each on its own. Write your answer to `CX-answer.json` beside this brief.
