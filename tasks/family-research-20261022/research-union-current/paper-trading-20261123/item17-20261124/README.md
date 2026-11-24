# Item 17 of the paper platform checklist: where the agents' execution plan stands (2026-11-24)

Codex's item 17 (paper-trading-platform, branch `codex/strategy-trades-and-mbo-capture`, draft PR 5): a plan file
under `paper_platform/execution_plans/` holding the tape's contract, its Databento instrument ID, and a placement and
size choice for each rule from the agents. Greg's decision, as the checklist records it: "Paper orders can post a bid
or offer, lift an offer or hit a bid. Frankie and the agents choose placement and size for each strategy."

## In hand

- The instrument ID: 150611 in every record of all seven tape files (read from the files).
- The contract definition: NGX3, converted from the stored exchange definition record by NautilusTrader 1.231.0's
  own loader. `ngx3-nautilus-definitions.json` here holds the conversion of each stored definition file; they are the
  same apart from `ts_event` and `ts_init`. The record on Codex's branch
  (`paper_platform/execution_plans/NG_OCT2023_CONTRACT.md`) uses the Sunday start-up record of 2023-10-01.
- Two things read from the matcher's code that a manager's entry depends on (in that same record).
- The briefs for two decider agents, one for each rule family: `BRIEF_COMMON.md`, `BRIEF_CL.md`, `BRIEF_CX.md`.

## Family decisions and remaining work

Greg transferred #17 and both family decision agents to Codex. The resumed decision pass produced [CL01–CL15 answers](CL-answer.json) and [CX01–CX15 answers](CX-answer.json). Each answer records the agent's order choices and the source wording behind them. All 30 have decisions. The six CX managers also specify their parent entries and when to close. Both families chose one NGX3 contract per entry.

Codex builds the family-agent plan on draft PR #5 from the markets-data commit containing these answers. Frankie's separate launch is still on hold. A paper session needs Greg's explicit authorization.

## Start item 17 here

The two family agents used the briefs in this folder. Source paths in the answers are relative to the brief. The strategy files preserve the original line numbers.

| Family | Agent instructions | Author's files |
| --- | --- | --- |
| CL01–CL15 | [CL brief](BRIEF_CL.md) | [Claude's rules](claude-strategy/VERSIONS.md) · [Open questions](claude-strategy/OPEN_QUESTIONS.md) |
| CX01–CX15 | [CX brief](BRIEF_CX.md) | [Codex's rules](codex-strategy/VERSIONS.md) · [Open questions](codex-strategy/OPEN_QUESTIONS.md) |

Both agents use the [common brief](BRIEF_COMMON.md). The copies come from [Claude's source revision](https://github.com/DavisAI1974/markets-data/tree/46199c5f4af03fde341535a7aff6a0396300cc73/tasks/family-research-20261022/research-union-current/strategy-20261123-claude) and [Codex's source revision](https://github.com/DavisAI1974/markets-data/tree/ad10921479e49678dd228b0f6b144dca3e610a0d/tasks/family-research-20261022/research-union-current/strategy-20261123-codex). This folder also includes the [plan format](platform/README.md) and the [NGX3 contract definition](platform/NG_OCT2023_CONTRACT.md) for Databento instrument `150611`. Those two files were copied from [platform revision 2986b3c](https://github.com/DavisAI1974/paper-trading-platform/tree/2986b3ce3001bc1926df64a06588b4558a5b648e/paper_platform/execution_plans).

Collect `CL-answer.json` and `CX-answer.json` beside the briefs. Each participating rule needs its chosen contract quantity and its opening and closing instructions. CX05, CX06, CX11, CX12, CX13 and CX14 also need their parent entry rules and parent-close instructions. Frankie and the agents own these decisions. Frankie's launch awaits Greg's go.

Commit the versioned plan and decision attribution under [execution_plans on draft PR #5](https://github.com/DavisAI1974/paper-trading-platform/tree/codex/strategy-trades-and-mbo-capture/paper_platform/execution_plans). Leave undecided rules out of the plan and record their IDs under #17 in the [running checklist](https://github.com/DavisAI1974/paper-trading-platform/blob/codex/strategy-trades-and-mbo-capture/docs/platform/OWN_PLATFORM_WISHLIST_20261123.md). Preserve any plan used by a run. The [original 35-item list](https://github.com/DavisAI1974/markets-data/blob/111e46bc156ecf05bfa25814cea3b9c7040a5fc9/tasks/family-research-20261022/research-union-current/paper-trading-20261123/OWN_PLATFORM_WISHLIST_20261123.md) records the original request. Greg deferred checks, validation and tests. A paper session requires his explicit go.

## Codex's branch moved while this was written

Codex pushed five more commits (to `5216aa0`) before the record went up; they were merged, not rebased, and the
record is on the branch after them. His changes to `paper_execution.py` are about the run stop (a failed cancel, the
orders still working, the errors kept in the receipt). What `post`, `cross` and `cross_limit` do is unchanged, read
from the diff. The line numbers the briefs give for `paper_execution.py` have moved: read them again before a decider
is run.
