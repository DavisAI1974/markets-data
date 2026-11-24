# Your rules: Claude's seventeen, CL01 to CL17

First read [common brief](BRIEF_COMMON.md) in full. It says what the job is, what each choice does in the matcher, the
rules you hold yourself to and the answer format. Then:

- The original fifteen rule files: [rules/CL01.json](https://github.com/DavisAI1974/paper-trading-platform/blob/2986b3ce3001bc1926df64a06588b4558a5b648e/paper_platform/rules/CL01.json) to `CL15.json`. Each is an
  entry rule; its side (buy or sell) is set at the trigger.
- The author's strategy document, which the rule files were cut from. Quote from these two files (they have
  real lines): [claude-strategy/VERSIONS.md](claude-strategy/VERSIONS.md) (748 lines; each rule has a section "## CLnn (v2). ...") and
  [claude-strategy/OPEN_QUESTIONS.md](claude-strategy/OPEN_QUESTIONS.md).
- How the platform runs Claude's rules: [claude_rules.py](https://github.com/DavisAI1974/paper-trading-platform/blob/2986b3ce3001bc1926df64a06588b4558a5b648e/paper_platform/claude_rules.py).

Decide CL01 through CL17, each on its own. For the two unsided-print rules, cite the [CL16 and CL17 source](claude-strategy/VERSIONS_WITH_CL16_CL17.md).
None of them is a manager, so no `entry_rules` or `on_parent_close`.

Write your answer to `CL-answer.json` beside this brief.
